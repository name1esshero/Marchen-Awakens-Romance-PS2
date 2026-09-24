"""Deterministically fit a generated PNG text layer onto a recovered TGA canvas."""
import argparse
import binascii
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

import rtx3


PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
MAX_PIXELS = 100_000_000


def decode_png(raw):
    """Decode non-interlaced, 8-bit grayscale/RGB/RGBA PNG to RGBA bytes."""
    if not raw.startswith(PNG_SIGNATURE):
        raise ValueError('generated overlay is not a PNG')
    pos = len(PNG_SIGNATURE)
    header = None
    compressed = bytearray()
    ended = False
    while pos < len(raw):
        if len(raw) - pos < 12:
            raise ValueError('truncated PNG chunk')
        length = struct.unpack_from('>I', raw, pos)[0]
        kind = raw[pos + 4:pos + 8]
        pos += 8
        if length > len(raw) - pos - 4:
            raise ValueError('PNG chunk exceeds file extent')
        data = raw[pos:pos + length]
        expected_crc = struct.unpack_from('>I', raw, pos + length)[0]
        actual_crc = binascii.crc32(kind + data) & 0xffffffff
        if actual_crc != expected_crc:
            raise ValueError(f'bad PNG {kind.decode("ascii", "replace")} checksum')
        pos += length + 4
        if kind == b'IHDR':
            if header is not None or length != 13:
                raise ValueError('invalid PNG IHDR')
            header = struct.unpack('>IIBBBBB', data)
        elif kind == b'IDAT':
            if header is None:
                raise ValueError('PNG IDAT precedes IHDR')
            compressed.extend(data)
        elif kind == b'IEND':
            if length != 0:
                raise ValueError('invalid PNG IEND')
            ended = True
            break
        elif kind[0] & 0x20 == 0 and kind != b'PLTE':
            raise ValueError(f'unsupported critical PNG chunk {kind!r}')
    if not ended or pos != len(raw) or header is None:
        raise ValueError('incomplete PNG')

    width, height, depth, color_type, compression, filtering, interlace = header
    channels_by_type = {0: 1, 2: 3, 4: 2, 6: 4}
    if not width or not height or width * height > MAX_PIXELS:
        raise ValueError('unsupported PNG dimensions')
    if (depth != 8 or color_type not in channels_by_type or compression != 0
            or filtering != 0 or interlace != 0):
        raise ValueError('PNG must be 8-bit non-interlaced grayscale, RGB, or RGBA')

    channels = channels_by_type[color_type]
    stride = width * channels
    expected_size = height * (stride + 1)
    try:
        scanlines = zlib.decompress(compressed)
    except zlib.error as exc:
        raise ValueError('invalid PNG compressed image data') from exc
    if len(scanlines) != expected_size:
        raise ValueError('PNG decompressed size does not match its dimensions')

    decoded = bytearray(height * stride)
    cursor = 0
    for y in range(height):
        filter_type = scanlines[cursor]
        cursor += 1
        source = scanlines[cursor:cursor + stride]
        cursor += stride
        prior = decoded[(y - 1) * stride:y * stride] if y else bytes(stride)
        row = bytearray(stride)
        if filter_type > 4:
            raise ValueError(f'unsupported PNG row filter {filter_type}')
        for x, value in enumerate(source):
            left = row[x - channels] if x >= channels else 0
            above = prior[x]
            upper_left = prior[x - channels] if x >= channels else 0
            if filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = above
            elif filter_type == 3:
                predictor = (left + above) // 2
            elif filter_type == 4:
                p = left + above - upper_left
                pa, pb, pc = abs(p - left), abs(p - above), abs(p - upper_left)
                predictor = left if pa <= pb and pa <= pc else (
                    above if pb <= pc else upper_left)
            else:
                predictor = 0
            row[x] = (value + predictor) & 0xff
        decoded[y * stride:(y + 1) * stride] = row

    rgba = bytearray(width * height * 4)
    if color_type == 6:
        return width, height, bytes(decoded)
    for pixel in range(width * height):
        src = pixel * channels
        dst = pixel * 4
        if color_type == 0:
            gray = decoded[src]
            rgba[dst:dst + 4] = bytes((gray, gray, gray, 255))
        elif color_type == 2:
            rgba[dst:dst + 4] = decoded[src:src + 3] + b'\xff'
        else:  # grayscale + alpha
            gray, alpha = decoded[src:src + 2]
            rgba[dst:dst + 4] = bytes((gray, gray, gray, alpha))
    return width, height, bytes(rgba)


def alpha_bounds(width, height, rgba, threshold=1):
    if len(rgba) != width * height * 4:
        raise ValueError('overlay RGBA size does not match its dimensions')
    if not 1 <= threshold <= 255:
        raise ValueError('alpha threshold must be between 1 and 255')
    min_x, min_y, max_x, max_y = width, height, -1, -1
    for y in range(height):
        for x in range(width):
            if rgba[(y * width + x) * 4 + 3] >= threshold:
                min_x, min_y = min(min_x, x), min(min_y, y)
                max_x, max_y = max(max_x, x), max(max_y, y)
    if max_x < min_x:
        raise ValueError('generated overlay has no visible pixels')
    return min_x, min_y, max_x + 1, max_y + 1


def _crop(width, height, rgba, bounds):
    x0, y0, x1, y1 = bounds
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height):
        raise ValueError('crop bounds are outside the image')
    out = bytearray((x1 - x0) * (y1 - y0) * 4)
    out_width = x1 - x0
    for y in range(y0, y1):
        src = (y * width + x0) * 4
        dst = (y - y0) * out_width * 4
        out[dst:dst + out_width * 4] = rgba[src:src + out_width * 4]
    return out_width, y1 - y0, bytes(out)


def _round_positive(value):
    return max(1, int(value + 0.5))


def _resize_area(width, height, rgba, out_width, out_height):
    """Area-resample RGBA with premultiplied-alpha accumulation."""
    out = bytearray(out_width * out_height * 4)
    x_scale, y_scale = width / out_width, height / out_height
    for dy in range(out_height):
        y0, y1 = dy * y_scale, (dy + 1) * y_scale
        for dx in range(out_width):
            x0, x1 = dx * x_scale, (dx + 1) * x_scale
            area = (x1 - x0) * (y1 - y0)
            alpha_sum = red_sum = green_sum = blue_sum = 0.0
            for sy in range(int(y0), min(height, int(y1 + 0.999999))):
                wy = max(0.0, min(y1, sy + 1) - max(y0, sy))
                for sx in range(int(x0), min(width, int(x1 + 0.999999))):
                    wx = max(0.0, min(x1, sx + 1) - max(x0, sx))
                    weight = wx * wy
                    offset = (sy * width + sx) * 4
                    r, g, b, a = rgba[offset:offset + 4]
                    alpha = a / 255.0
                    alpha_sum += weight * alpha
                    red_sum += weight * r * alpha
                    green_sum += weight * g * alpha
                    blue_sum += weight * b * alpha
            offset = (dy * out_width + dx) * 4
            alpha = alpha_sum / area
            if alpha_sum:
                out[offset:offset + 4] = bytes((
                    _round_positive(red_sum / alpha_sum),
                    _round_positive(green_sum / alpha_sum),
                    _round_positive(blue_sum / alpha_sum),
                    _round_positive(alpha * 255),
                ))
    return bytes(out)


def _resize_bilinear(width, height, rgba, out_width, out_height):
    out = bytearray(out_width * out_height * 4)
    for dy in range(out_height):
        fy = max(0.0, min(height - 1, (dy + 0.5) * height / out_height - 0.5))
        y0, y1 = int(fy), min(height - 1, int(fy) + 1)
        wy = fy - y0
        for dx in range(out_width):
            fx = max(0.0, min(width - 1, (dx + 0.5) * width / out_width - 0.5))
            x0, x1 = int(fx), min(width - 1, int(fx) + 1)
            wx = fx - x0
            weights = ((x0, y0, (1 - wx) * (1 - wy)),
                       (x1, y0, wx * (1 - wy)),
                       (x0, y1, (1 - wx) * wy),
                       (x1, y1, wx * wy))
            alpha_sum = red_sum = green_sum = blue_sum = 0.0
            for sx, sy, weight in weights:
                offset = (sy * width + sx) * 4
                r, g, b, a = rgba[offset:offset + 4]
                alpha = a / 255.0
                alpha_sum += weight * alpha
                red_sum += weight * r * alpha
                green_sum += weight * g * alpha
                blue_sum += weight * b * alpha
            offset = (dy * out_width + dx) * 4
            if alpha_sum:
                out[offset:offset + 4] = bytes((
                    _round_positive(red_sum / alpha_sum),
                    _round_positive(green_sum / alpha_sum),
                    _round_positive(blue_sum / alpha_sum),
                    _round_positive(alpha_sum * 255),
                ))
    return bytes(out)


def fit_overlay(width, height, rgba, box_width, box_height, fit='contain',
                alpha_threshold=1):
    """Alpha-crop and deterministically scale an overlay into a fixed box."""
    if not 1 <= alpha_threshold <= 255:
        raise ValueError('alpha threshold must be between 1 and 255')
    cleaned = bytearray(rgba)
    for offset in range(3, len(cleaned), 4):
        if cleaned[offset] < alpha_threshold:
            cleaned[offset] = 0
    bounds = alpha_bounds(width, height, cleaned, alpha_threshold)
    cropped_width, cropped_height, cropped = _crop(width, height, cleaned, bounds)
    if fit not in ('contain', 'cover'):
        raise ValueError('fit must be contain or cover')
    scale = (min(box_width / cropped_width, box_height / cropped_height)
             if fit == 'contain' else
             max(box_width / cropped_width, box_height / cropped_height))
    resized_width = _round_positive(cropped_width * scale)
    resized_height = _round_positive(cropped_height * scale)
    if resized_width * resized_height > MAX_PIXELS:
        raise ValueError('normalized overlay dimensions are too large')
    if resized_width <= cropped_width and resized_height <= cropped_height:
        resized = _resize_area(cropped_width, cropped_height, cropped,
                               resized_width, resized_height)
    else:
        resized = _resize_bilinear(cropped_width, cropped_height, cropped,
                                   resized_width, resized_height)
    if fit == 'contain':
        out_width, out_height = min(box_width, resized_width), min(box_height, resized_height)
        x0 = (resized_width - out_width) // 2
        y0 = (resized_height - out_height) // 2
        resized_width, resized_height, resized = _crop(
            resized_width, resized_height, resized,
            (x0, y0, x0 + out_width, y0 + out_height))
        canvas = bytearray(box_width * box_height * 4)
        x_offset, y_offset = (box_width - out_width) // 2, (box_height - out_height) // 2
        for y in range(out_height):
            src = y * out_width * 4
            dst = ((y + y_offset) * box_width + x_offset) * 4
            canvas[dst:dst + out_width * 4] = resized[src:src + out_width * 4]
        return box_width, box_height, bytes(canvas), bounds
    # Cover fills the requested box, then takes a centered crop of the scaled layer.
    x0 = (resized_width - box_width) // 2
    y0 = (resized_height - box_height) // 2
    out_width, out_height, result = _crop(
        resized_width, resized_height, resized,
        (x0, y0, x0 + box_width, y0 + box_height))
    return out_width, out_height, result, bounds


def _rect(value, width, height, label):
    x, y, rect_width, rect_height = value
    if (x < 0 or y < 0 or rect_width <= 0 or rect_height <= 0
            or x + rect_width > width or y + rect_height > height):
        raise ValueError(f'{label} is outside the base TGA canvas')
    return x, y, rect_width, rect_height


def compose(base_tga, overlay_png, region=None, clear_region=None, fit='contain',
            alpha_threshold=1):
    """Composite a transparent PNG layer onto an unchanged TGA canvas."""
    base_width, base_height, base_rgba = rtx3.read_tga(base_tga)
    overlay_width, overlay_height, overlay_rgba = decode_png(overlay_png)
    if region is None:
        region = (0, 0, base_width, base_height)
    x, y, width, height = _rect(region, base_width, base_height, 'destination region')
    if clear_region is not None:
        cx, cy, clear_width, clear_height = _rect(
            clear_region, base_width, base_height, 'clear region')
        canvas = bytearray(base_rgba)
        for row in range(cy, cy + clear_height):
            start = (row * base_width + cx) * 4
            canvas[start:start + clear_width * 4] = bytes(clear_width * 4)
    else:
        canvas = bytearray(base_rgba)
    _, _, fitted, source_bounds = fit_overlay(
        overlay_width, overlay_height, overlay_rgba, width, height, fit,
        alpha_threshold)
    for oy in range(height):
        for ox in range(width):
            src = (oy * width + ox) * 4
            alpha = fitted[src + 3]
            if not alpha:
                continue
            dst = ((y + oy) * base_width + x + ox) * 4
            br, bg, bb, ba = canvas[dst:dst + 4]
            sr, sg, sb = fitted[src:src + 3]
            a = alpha / 255.0
            base_a = ba / 255.0
            out_a = a + base_a * (1.0 - a)
            if out_a:
                canvas[dst:dst + 4] = bytes((
                    _round_positive((sr * a + br * base_a * (1.0 - a)) / out_a),
                    _round_positive((sg * a + bg * base_a * (1.0 - a)) / out_a),
                    _round_positive((sb * a + bb * base_a * (1.0 - a)) / out_a),
                    _round_positive(out_a * 255),
                ))
    return (base_width, base_height, rtx3.write_tga(base_width, base_height, canvas),
            dict(overlay_width=overlay_width, overlay_height=overlay_height,
                 overlay_alpha_bounds=source_bounds, region=[x, y, width, height],
                 clear_region=list(clear_region) if clear_region else None, fit=fit,
                 alpha_threshold=alpha_threshold))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True, type=Path, help='original exported TGA canvas')
    parser.add_argument('--overlay', required=True, type=Path,
                        help='generated transparent PNG text/art layer')
    parser.add_argument('--output', required=True, type=Path, help='new full-canvas TGA')
    parser.add_argument('--region', nargs=4, type=int, metavar=('X', 'Y', 'W', 'H'),
                        help='destination box; defaults to the entire source canvas')
    parser.add_argument('--clear-region', nargs=4, type=int, metavar=('X', 'Y', 'W', 'H'),
                        help='optional source area to clear before compositing')
    parser.add_argument('--fit', choices=('contain', 'cover'), default='contain',
                        help='preserve the overlay aspect ratio (default: contain)')
    parser.add_argument('--alpha-threshold', type=int, default=1,
                        help='discard overlay alpha below this value (1-255; default: 1)')
    parser.add_argument('--replace', action='store_true',
                        help='replace an existing output TGA')
    args = parser.parse_args()
    try:
        if args.output.exists() and not args.replace:
            raise ValueError('output already exists; pass --replace to overwrite it')
        base = args.base.read_bytes()
        overlay = args.overlay.read_bytes()
        width, height, result, report = compose(
            base, overlay, args.region, args.clear_region, args.fit,
            args.alpha_threshold)
        if rtx3.tga_dimensions(result) != (width, height):
            raise ValueError('composed TGA dimensions do not match the source canvas')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(result)
        report.update(canvas=[width, height], output_sha256=hashlib.sha256(result).hexdigest(),
                      output=str(args.output))
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except (OSError, ValueError, struct.error, zlib.error) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
