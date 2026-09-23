"""Decode and reinsert verified RTX3 raster modes as editable TGA."""
import argparse
import binascii
import json
from pathlib import Path
import struct
import sys
import zlib

MAGIC = b'RTX3'
HEADER_SIZE = 0x40
PSMT8 = 19
PSMT4 = 20
PSMT8H = 27
PSMT4HL = 36
PSMT4HH = 44
PSMCT32 = 0


def parse(raw):
    if len(raw) < HEADER_SIZE or raw[:4] != MAGIC:
        raise ValueError('not an RTX3 texture')
    if struct.unpack_from('<I', raw, 4)[0] != len(raw) - 8:
        raise ValueError('RTX3 declared file size mismatch')
    tex0 = struct.unpack_from('<Q', raw, 8)[0]
    psm = (tex0 >> 20) & 0x3F
    tw, th = (tex0 >> 26) & 0xF, (tex0 >> 30) & 0xF
    width, height = struct.unpack_from('<HH', raw, 0x20)
    pixel_size = struct.unpack_from('<I', raw, 0x24)[0]
    if not width or not height or width != 1 << tw or height != 1 << th:
        raise ValueError('RTX3 dimensions disagree with GS TEX0')
    bpp_by_psm = {PSMCT32: 32, PSMT8: 8, PSMT4: 4,
                  PSMT8H: 8, PSMT4HL: 4, PSMT4HH: 4}
    if psm not in bpp_by_psm:
        raise ValueError(f'unsupported RTX3 pixel storage mode {psm}')
    bpp = bpp_by_psm[psm]
    expected_pixel_size = width * height * bpp // 8
    if pixel_size != expected_pixel_size:
        raise ValueError('RTX3 pixel byte count disagrees with dimensions/PSM')
    palette_entries = {PSMT8: 256, PSMT8H: 256,
                       PSMT4: 16, PSMT4HL: 16, PSMT4HH: 16}.get(psm, 0)
    palette_size = palette_entries * 4
    if len(raw) != HEADER_SIZE + palette_size + pixel_size:
        raise ValueError('RTX3 length does not match header, palette and pixel extents')
    return dict(tex0=tex0, psm=psm, width=width, height=height, bpp=bpp,
                pixel_size=pixel_size, palette_offset=HEADER_SIZE + pixel_size,
                palette_size=palette_size,
                pixels_offset=HEADER_SIZE)


def _unswizzle8(data, width, height):
    if len(data) != width * height or width % 16:
        raise ValueError('PSMT8 dimensions/data are not supported by this swizzler')
    out = bytearray(len(data))
    for y in range(height):
        for x in range(width):
            block = (y & ~0xF) * width + (x & ~0xF) * 2
            swap = (((y + 2) >> 2) & 1) * 4
            row = (((y & ~3) >> 1) + (y & 1)) & 7
            column = row * width * 2 + ((x + swap) & 7) * 4
            lane = ((y >> 1) & 1) + ((x >> 2) & 2)
            out[y * width + x] = data[block + column + lane]
    return out


def _swizzle8(data, width, height):
    if len(data) != width * height or width % 16:
        raise ValueError('PSMT8 dimensions/data are not supported by this swizzler')
    out = bytearray(len(data))
    for y in range(height):
        for x in range(width):
            block = (y & ~0xF) * width + (x & ~0xF) * 2
            swap = (((y + 2) >> 2) & 1) * 4
            row = (((y & ~3) >> 1) + (y & 1)) & 7
            column = row * width * 2 + ((x + swap) & 7) * 4
            lane = ((y >> 1) & 1) + ((x >> 2) & 2)
            out[block + column + lane] = data[y * width + x]
    return out


def _unswizzle4(data, width, height):
    if len(data) != width * height // 2 or width % 32 or height % 4:
        raise ValueError('PSMT4 dimensions/data are not supported by this swizzler')
    out = bytearray(len(data))
    for y in range(height):
        for x in range(width):
            page_x, page_y = x & ~0x7F, y & ~0x7F
            pages_h = (width + 127) // 128
            pages_v = (height + 127) // 128
            page_num = (page_y // 128) * pages_h + page_x // 128
            page_y32 = (page_num // pages_v) * 32
            page_x32 = (page_num % pages_v) * 64
            page = page_y32 * height * 2 + page_x32 * 4
            local_x, local_y = x & 0x7F, y & 0x7F
            block = ((local_x & ~0x1F) >> 1) * height + (local_y & ~0xF) * 2
            swap = (((y + 2) >> 2) & 1) * 4
            row = (((y & ~3) >> 1) + (y & 1)) & 7
            column = row * height * 2 + ((x + swap) & 7) * 4
            lane = (x >> 3) & 3
            nibble = ((data[page + block + column + lane] >> 4) & 0xF
                      if (y >> 1) & 1 else data[page + block + column + lane] & 0xF)
            index = y * width + x
            if index & 1:
                out[index >> 1] = (out[index >> 1] & 0x0F) | (nibble << 4)
            else:
                out[index >> 1] = (out[index >> 1] & 0xF0) | nibble
    return out


def _swizzle4(data, width, height):
    if len(data) != width * height // 2 or width % 32 or height % 4:
        raise ValueError('PSMT4 dimensions/data are not supported by this swizzler')
    out = bytearray(len(data))
    for y in range(height):
        for x in range(width):
            page_x, page_y = x & ~0x7F, y & ~0x7F
            pages_h = (width + 127) // 128
            pages_v = (height + 127) // 128
            page_num = (page_y // 128) * pages_h + page_x // 128
            page_y32 = (page_num // pages_v) * 32
            page_x32 = (page_num % pages_v) * 64
            page = page_y32 * height * 2 + page_x32 * 4
            local_x, local_y = x & 0x7F, y & 0x7F
            block = ((local_x & ~0x1F) >> 1) * height + (local_y & ~0xF) * 2
            swap = (((y + 2) >> 2) & 1) * 4
            row = (((y & ~3) >> 1) + (y & 1)) & 7
            column = row * height * 2 + ((x + swap) & 7) * 4
            lane = (x >> 3) & 3
            offset = page + block + column + lane
            index = y * width + x
            nibble = ((data[index >> 1] >> 4) & 0xF if index & 1
                      else data[index >> 1] & 0xF)
            if (y >> 1) & 1:
                out[offset] = (out[offset] & 0x0F) | (nibble << 4)
            else:
                out[offset] = (out[offset] & 0xF0) | nibble
    return out


def _unswizzle32(data, width, height):
    if len(data) != width * height * 4 or width % 64 or height % 32:
        raise ValueError('PSMCT32 dimensions/data are not supported by this swizzler')
    blocks = (0, 1, 4, 5, 16, 17, 20, 21,
              2, 3, 6, 7, 18, 19, 22, 23,
              8, 9, 12, 13, 24, 25, 28, 29,
              10, 11, 14, 15, 26, 27, 30, 31)
    columns = (0, 1, 4, 5, 8, 9, 12, 13,
               2, 3, 6, 7, 10, 11, 14, 15)
    out = bytearray(len(data))
    pages_w = width // 64
    for y in range(height):
        for x in range(width):
            page_x, page_y = x // 64, y // 32
            page = page_x + page_y * pages_w
            px, py = x - page_x * 64, y - page_y * 32
            block_x, block_y = px // 8, py // 8
            block = blocks[block_x + block_y * 8]
            bx, by = px - block_x * 8, py - block_y * 8
            column = by // 2
            word = columns[bx + (by - column * 2) * 8]
            source = (page * 2048 + block * 64 + column * 16 + word) * 4
            dest = (y * width + x) * 4
            out[dest:dest + 4] = data[source:source + 4]
    return out


def _swizzle32(data, width, height):
    if len(data) != width * height * 4 or width % 64 or height % 32:
        raise ValueError('PSMCT32 dimensions/data are not supported by this swizzler')
    blocks = (0, 1, 4, 5, 16, 17, 20, 21,
              2, 3, 6, 7, 18, 19, 22, 23,
              8, 9, 12, 13, 24, 25, 28, 29,
              10, 11, 14, 15, 26, 27, 30, 31)
    columns = (0, 1, 4, 5, 8, 9, 12, 13,
               2, 3, 6, 7, 10, 11, 14, 15)
    out = bytearray(len(data))
    pages_w = width // 64
    for y in range(height):
        for x in range(width):
            page_x, page_y = x // 64, y // 32
            page = page_x + page_y * pages_w
            px, py = x - page_x * 64, y - page_y * 32
            block_x, block_y = px // 8, py // 8
            block = blocks[block_x + block_y * 8]
            bx, by = px - block_x * 8, py - block_y * 8
            column = by // 2
            word = columns[bx + (by - column * 2) * 8]
            dest = (page * 2048 + block * 64 + column * 16 + word) * 4
            source = (y * width + x) * 4
            out[dest:dest + 4] = data[source:source + 4]
    return out


def _clut_index(index, psm):
    if psm in (PSMT8, PSMT8H):
        return ((index & 0xE7) + ((index & 0x08) << 1) + ((index & 0x10) >> 1))
    # The 16-entry CSM1 palette order is left unchanged pending evidence of a
    # different layout in this game.
    return index


def _expand_gs_alpha(color):
    """Expand the GS 0..128 alpha range to an 8-bit raster alpha channel."""
    return color[:3] + (min(255, color[3] * 2),)


def decode_legacy_rgba(raw):
    """Decode with the earlier GS swizzle/CLUT mapping hypothesis."""
    info = parse(raw)
    width, height, psm = info['width'], info['height'], info['psm']
    if psm in (PSMT8H, PSMT4HL, PSMT4HH):
        raise ValueError(f'RTX3 PSM {psm} high-bit storage order is unresolved; refusing a guessed decode')
    pixels_raw = raw[info['pixels_offset']:info['pixels_offset'] + info['pixel_size']]
    if psm == PSMCT32:
        out = _unswizzle32(pixels_raw, width, height)
        for i in range(3, len(out), 4):
            out[i] = min(255, out[i] * 2)
        return width, height, bytes(out)
    palette_raw = raw[info['palette_offset']:info['palette_offset'] + info['palette_size']]
    palette = [None] * (info['palette_size'] // 4)
    for i in range(len(palette)):
        j = _clut_index(i, psm)
        r, g, b, a = palette_raw[i * 4:i * 4 + 4]
        palette[j] = _expand_gs_alpha((r, g, b, a))
    if psm in (PSMT8, PSMT8H):
        indices = _unswizzle8(pixels_raw, width, height)
    else:
        indices = _unswizzle4(pixels_raw, width, height)
    out = bytearray(width * height * 4)
    if psm in (PSMT8, PSMT8H):
        for i, index in enumerate(indices):
            out[i * 4:i * 4 + 4] = bytes(palette[index])
    else:
        for i in range(width * height):
            index = (indices[i >> 1] >> (4 if i & 1 else 0)) & 0xF
            out[i * 4:i * 4 + 4] = bytes(palette[index])
    return width, height, bytes(out)


def decode_stored_order_rgba(raw):
    """Decode indexed pixels linearly with the palette entries as stored.

    This diagnostic deliberately skips PSM swizzling, the GS CLUT index
    permutation, and alpha expansion. The default PSMT8 path applies the
    CLUT permutation and expands GS alpha while leaving pixels in stored order.
    """
    info = parse(raw)
    width, height, psm = info['width'], info['height'], info['psm']
    pixels = raw[info['pixels_offset']:info['pixels_offset'] + info['pixel_size']]
    if psm == PSMCT32:
        return width, height, pixels
    if psm not in (PSMT4, PSMT8):
        raise ValueError(f'RTX3 PSM {psm} has no supported stored-order preview')
    palette_raw = raw[info['palette_offset']:info['palette_offset'] + info['palette_size']]
    palette = [tuple(palette_raw[i:i + 4]) for i in range(0, len(palette_raw), 4)]
    out = bytearray(width * height * 4)
    for i in range(width * height):
        if psm == PSMT8:
            index = pixels[i]
        else:
            index = (pixels[i >> 1] >> (4 if i & 1 else 0)) & 0xF
        color = palette[index]
        out[i * 4:i * 4 + 4] = color
    return width, height, bytes(out)


def decode_linear_mapped_rgba(raw):
    """Decode indexed pixels linearly and apply the observed CLUT permutation."""
    info = parse(raw)
    width, height, psm = info['width'], info['height'], info['psm']
    if psm not in (PSMT4, PSMT8):
        raise ValueError(f'RTX3 PSM {psm} has no supported linear indexed decode')
    pixels = raw[info['pixels_offset']:info['pixels_offset'] + info['pixel_size']]
    palette_raw = raw[info['palette_offset']:info['palette_offset'] + info['palette_size']]
    palette = [None] * (info['palette_size'] // 4)
    for i in range(len(palette)):
        color = tuple(palette_raw[i * 4:i * 4 + 4])
        palette[_clut_index(i, psm)] = _expand_gs_alpha(color)
    out = bytearray(width * height * 4)
    for i in range(width * height):
        index = (pixels[i] if psm == PSMT8 else
                 (pixels[i >> 1] >> (4 if i & 1 else 0)) & 0xF)
        out[i * 4:i * 4 + 4] = bytes(palette[index])
    return width, height, bytes(out)


def decode_rgba(raw):
    """Decode supported modes using the current best-supported layout."""
    info = parse(raw)
    if info['psm'] in (PSMT4, PSMT8):
        return decode_linear_mapped_rgba(raw)
    return decode_legacy_rgba(raw)


def _encode_indexed_tga(original, tga, map_clut):
    info = parse(original)
    width, height, rgba = read_tga(tga)
    if (width, height) != (info['width'], info['height']):
        raise ValueError('replacement TGA dimensions must match RTX3')
    if info['psm'] not in (PSMT4, PSMT8):
        raise ValueError('stored-order import supports indexed PSMT4/PSMT8 only')
    decoder = decode_linear_mapped_rgba if map_clut else decode_stored_order_rgba
    old_width, old_height, old_rgba = decoder(original)
    if (width, height, rgba) == (old_width, old_height, old_rgba):
        return original

    palette_raw = original[info['palette_offset']:info['palette_offset'] + info['palette_size']]
    stored_palette = [tuple(palette_raw[i:i + 4])
                      for i in range(0, len(palette_raw), 4)]
    if map_clut:
        palette = [None] * len(stored_palette)
        for i, color in enumerate(stored_palette):
            palette[_clut_index(i, info['psm'])] = _expand_gs_alpha(color)
    else:
        palette = stored_palette
    pixels_raw = original[info['pixels_offset']:info['pixels_offset'] + info['pixel_size']]
    if info['psm'] == PSMT8:
        original_indices = pixels_raw
    else:
        original_indices = bytes(
            (pixels_raw[i >> 1] >> (4 if i & 1 else 0)) & 0xF
            for i in range(width * height))
    cache = {}
    indices = bytearray(width * height)
    for i in range(width * height):
        color = tuple(rgba[i * 4:i * 4 + 4])
        if bytes(color) == old_rgba[i * 4:i * 4 + 4]:
            indices[i] = original_indices[i]
            continue
        index = cache.get(color)
        if index is None:
            index = min(range(len(palette)), key=lambda j: sum(
                (color[k] - palette[j][k]) ** 2 for k in range(4)))
            cache[color] = index
        indices[i] = index

    if info['psm'] == PSMT8:
        packed = indices
    else:
        packed = bytearray(info['pixel_size'])
        for i, index in enumerate(indices):
            if i & 1:
                packed[i >> 1] |= index << 4
            else:
                packed[i >> 1] = index
    return original[:HEADER_SIZE] + bytes(packed) + palette_raw


def encode_stored_order_tga(original, tga):
    """Reinsert an indexed TGA using pixel and CLUT entries exactly as stored."""
    return _encode_indexed_tga(original, tga, map_clut=False)


def encode_linear_mapped_tga(original, tga):
    """Reinsert linear indexed pixels with the CLUT permutation applied."""
    return _encode_indexed_tga(original, tga, map_clut=True)


def read_tga(raw):
    if len(raw) < 18:
        raise ValueError('truncated TGA header')
    id_length, color_map_type, image_type = raw[:3]
    if color_map_type != 0 or image_type != 2:
        raise ValueError('only uncompressed true-color TGA is supported')
    width, height, depth, descriptor = struct.unpack_from('<HHBB', raw, 12)
    if not width or not height or depth not in (24, 32):
        raise ValueError('unsupported TGA dimensions or pixel depth')
    channels = depth // 8
    start = 18 + id_length
    if len(raw) != start + width * height * channels:
        raise ValueError('TGA pixel extent does not match dimensions')
    rgba = bytearray(width * height * 4)
    for file_y in range(height):
        y = file_y if descriptor & 0x20 else height - 1 - file_y
        for file_x in range(width):
            x = width - 1 - file_x if descriptor & 0x10 else file_x
            src = start + (file_y * width + file_x) * channels
            dst = (y * width + x) * 4
            blue, green, red = raw[src:src + 3]
            alpha = raw[src + 3] if channels == 4 else 255
            rgba[dst:dst + 4] = bytes((red, green, blue, alpha))
    return width, height, bytes(rgba)


def encode_legacy_tga(original, tga):
    info = parse(original)
    width, height, rgba = read_tga(tga)
    if (width, height) != (info['width'], info['height']):
        raise ValueError('replacement TGA dimensions must match RTX3')
    old_width, old_height, old_rgba = decode_legacy_rgba(original)
    if (width, height, rgba) == (old_width, old_height, old_rgba):
        return original

    if info['psm'] == PSMCT32:
        pixels = bytearray(rgba)
        for i in range(3, len(pixels), 4):
            pixels[i] = (pixels[i] + 1) // 2
        body = _swizzle32(pixels, width, height)
        return original[:HEADER_SIZE] + body

    palette_raw = original[info['palette_offset']:info['palette_offset'] + info['palette_size']]
    palette = [None] * (info['palette_size'] // 4)
    for i in range(len(palette)):
        j = _clut_index(i, info['psm'])
        r, g, b, a = palette_raw[i * 4:i * 4 + 4]
        palette[j] = (r, g, b, min(255, a * 2))
    cache = {}
    indices = bytearray(width * height)
    for i in range(width * height):
        color = tuple(rgba[i * 4:i * 4 + 4])
        index = cache.get(color)
        if index is None:
            target_alpha = (color[3] + 1) // 2
            target = (color[0], color[1], color[2], target_alpha * 2)
            index = min(range(len(palette)), key=lambda j: sum(
                (target[k] - palette[j][k]) ** 2 for k in range(4)))
            cache[color] = index
        indices[i] = index

    if info['bpp'] == 8:
        packed = _swizzle8(indices, width, height)
    else:
        nibbles = bytearray(info['pixel_size'])
        for i, index in enumerate(indices):
            if i & 1:
                nibbles[i >> 1] |= index << 4
            else:
                nibbles[i >> 1] = index
        packed = _swizzle4(nibbles, width, height)
    return original[:HEADER_SIZE] + packed + palette_raw


def encode_tga(original, tga):
    """Use the current best-supported encoding for the texture's PSM."""
    info = parse(original)
    if info['psm'] in (PSMT4, PSMT8):
        return encode_linear_mapped_tga(original, tga)
    return encode_legacy_tga(original, tga)


def write_tga(width, height, rgba):
    if len(rgba) != width * height * 4 or width > 0xFFFF or height > 0xFFFF:
        raise ValueError('invalid RGBA dimensions')
    header = struct.pack('<BBBHHBHHHHBB', 0, 0, 2, 0, 0, 0, 0, 0,
                         width, height, 32, 0x28)
    bgra = bytearray(len(rgba))
    for i in range(0, len(rgba), 4):
        bgra[i:i + 4] = bytes((rgba[i + 2], rgba[i + 1], rgba[i], rgba[i + 3]))
    return header + bgra


def write_png(width, height, rgba):
    if len(rgba) != width * height * 4:
        raise ValueError('invalid RGBA dimensions')
    def chunk(kind, data):
        body = kind + data
        return struct.pack('>I', len(data)) + body + struct.pack('>I', binascii.crc32(body) & 0xFFFFFFFF)
    scanlines = b''.join(b'\0' + rgba[y * width * 4:(y + 1) * width * 4]
                         for y in range(height))
    header = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header)
            + chunk(b'IDAT', zlib.compress(scanlines, 9)) + chunk(b'IEND', b''))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('info', 'export', 'import'):
        command = sub.add_parser(name)
        command.add_argument('source', type=Path)
        if name in ('export', 'import'):
            command.add_argument('output', type=Path)
        if name == 'export':
            command.add_argument('--format', choices=('tga', 'png'), default='tga')
        if name in ('export', 'import'):
            mapping = command.add_mutually_exclusive_group()
            mapping.add_argument('--stored-order', action='store_true',
                                 help='use linear pixels and stored CLUT order (skip CLUT permutation)')
            mapping.add_argument('--legacy-mapping', action='store_true',
                                 help='use the previous GS swizzle/CLUT transform for comparison')
        if name == 'import':
            command.add_argument('replacement', type=Path)
    args = parser.parse_args()
    try:
        raw = args.source.read_bytes()
        info = parse(raw)
        if args.command == 'info':
            print(json.dumps(info, indent=2))
        elif args.command == 'export':
            decoder = (decode_legacy_rgba if args.legacy_mapping else
                       decode_stored_order_rgba if args.stored_order else decode_rgba)
            width, height, rgba = decoder(raw)
            data = write_tga(width, height, rgba) if args.format == 'tga' else write_png(width, height, rgba)
            if args.output.exists():
                raise ValueError('output already exists')
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(data)
        else:
            if args.output.exists():
                raise ValueError('output already exists')
            args.output.parent.mkdir(parents=True, exist_ok=True)
            encoder = (encode_legacy_tga if args.legacy_mapping else
                       encode_stored_order_tga if args.stored_order else encode_tga)
            args.output.write_bytes(encoder(raw, args.replacement.read_bytes()))
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
