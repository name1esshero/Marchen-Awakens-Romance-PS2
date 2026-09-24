"""Build English title-logo textures from an editable transparent wordmark."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import graphics_compose
import rtx3


def _validate_paths(base_path, output_path):
    if base_path.name.endswith('_jp.tga') or output_path.name.endswith('_jp.tga'):
        raise ValueError('Japanese baseline paths are read-only; use the _eng sibling')


def _gray(rgba):
    result = bytearray(rgba)
    for offset in range(0, len(result), 4):
        red, green, blue = result[offset:offset + 3]
        light = (299 * red + 587 * green + 114 * blue + 500) // 1000
        result[offset:offset + 3] = bytes((light, light, light))
    return bytes(result)


def _composite_rgba(base, overlay):
    if len(base) != len(overlay):
        raise ValueError('art layer dimensions differ from the base canvas')
    result = bytearray(base)
    for offset in range(0, len(result), 4):
        red, green, blue, alpha = overlay[offset:offset + 4]
        if alpha == 0:
            continue
        base_red, base_green, base_blue, base_alpha = result[offset:offset + 4]
        source_a = alpha / 255.0
        base_a = base_alpha / 255.0
        output_a = source_a + base_a * (1.0 - source_a)
        if not output_a:
            result[offset:offset + 4] = bytes(4)
            continue
        result[offset:offset + 4] = bytes((
            graphics_compose._round_channel(
                (red * source_a + base_red * base_a * (1.0 - source_a)) / output_a),
            graphics_compose._round_channel(
                (green * source_a + base_green * base_a * (1.0 - source_a)) / output_a),
            graphics_compose._round_channel(
                (blue * source_a + base_blue * base_a * (1.0 - source_a)) / output_a),
            graphics_compose._round_positive(output_a * 255),
        ))
    return bytes(result)


def build(base_tga, logo_png, clear_regions, placements):
    """Return a full-canvas transparent art layer and localized TGA.

    Each placement is ``(x, y, width, height, treatment)`` where treatment is
    ``color`` or ``gray``. Each clear region is ``(x, y, width, height)``.
    Callers provide the existing English sibling as the base; Japanese source
    baselines are never localization inputs.
    """
    base_width, base_height, base_rgba = rtx3.read_tga(base_tga)
    logo_width, logo_height, logo_rgba = graphics_compose.decode_png(logo_png)
    if len(placements) == 0 or len(clear_regions) == 0:
        raise ValueError('at least one placement and clear region are required')
    layer = bytearray(base_width * base_height * 4)

    def rect(values, label):
        x, y, width, height = values
        if (x < 0 or y < 0 or width <= 0 or height <= 0
                or x + width > base_width or y + height > base_height):
            raise ValueError(f'{label} is outside the source TGA canvas')
        return x, y, width, height

    for placement in placements:
        x, y, width, height, treatment = placement
        rect((x, y, width, height), 'placement')
        if treatment not in ('color', 'gray'):
            raise ValueError(f'unsupported logo treatment: {treatment}')
        source = _gray(logo_rgba) if treatment == 'gray' else logo_rgba
        _, _, fitted, _ = graphics_compose.fit_overlay(
            logo_width, logo_height, source, width, height, 'contain')
        for row in range(height):
            source_offset = row * width * 4
            target_offset = ((y + row) * base_width + x) * 4
            layer[target_offset:target_offset + width * 4] = (
                fitted[source_offset:source_offset + width * 4])

    cleared = bytearray(base_rgba)
    normalized_clears = [rect(region, 'clear region') for region in clear_regions]
    for x, y, width, height in normalized_clears:
        for row in range(y, y + height):
            offset = (row * base_width + x) * 4
            cleared[offset:offset + width * 4] = bytes(width * 4)

    layer_png = rtx3.write_png(base_width, base_height, layer)
    output_rgba = _composite_rgba(cleared, layer)
    output_tga = rtx3.write_tga(base_width, base_height, output_rgba)
    report = dict(canvas=[base_width, base_height], fit='contain per placement')
    report.update(
        clear_regions=[list(region) for region in normalized_clears],
        placements=[list(placement) for placement in placements],
        output_sha256=hashlib.sha256(output_tga).hexdigest(),
        layer_sha256=hashlib.sha256(layer_png).hexdigest(),
    )
    return layer_png, output_tga, report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True, type=Path,
                        help='existing English TGA sibling; Japanese baseline remains read-only')
    parser.add_argument('--logo', required=True, type=Path,
                        help='transparent RGBA master wordmark PNG')
    parser.add_argument('--layer', required=True, type=Path,
                        help='full-canvas editable logo layer PNG')
    parser.add_argument('--output', required=True, type=Path,
                        help='localized English TGA sibling')
    parser.add_argument('--clear-region', nargs=4, type=int, action='append',
                        required=True, metavar=('X', 'Y', 'W', 'H'))
    parser.add_argument('--placement', nargs=5, action='append', required=True,
                        metavar=('X', 'Y', 'W', 'H', 'COLOR_OR_GRAY'))
    parser.add_argument('--replace', action='store_true',
                        help='replace existing layer/output files')
    args = parser.parse_args(argv)
    try:
        _validate_paths(args.base, args.output)
        if not args.replace and (args.layer.exists() or args.output.exists()):
            raise ValueError('output exists; pass --replace to overwrite')
        logo = args.logo.read_bytes()
        base = args.base.read_bytes()
        clears = [tuple(region) for region in args.clear_region]
        placements = [(*map(int, item[:4]), item[4].lower())
                      for item in args.placement]
        layer, output, report = build(base, logo, clears, placements)
        width, height, _ = rtx3.read_tga(output)
        if rtx3.tga_dimensions(output) != (width, height):
            raise ValueError('output dimensions differ from the input canvas')
        args.layer.parent.mkdir(parents=True, exist_ok=True)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.layer.write_bytes(layer)
        args.output.write_bytes(output)
        report.update(canvas=[width, height], layer=str(args.layer),
                      output=str(args.output))
        print(json.dumps(report, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
