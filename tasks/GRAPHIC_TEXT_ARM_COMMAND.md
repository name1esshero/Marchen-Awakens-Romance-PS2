# `EQUIP ARM` command texture

## Source and translation

The recovered 256×64 PSMT8 baseline
[`00039_00921_0004_arrm_jp.tga`](../graphics/weapons/00039_00921_0004_arrm_jp.tga)
has SHA-256
`9c4a5b76daee0895ed4f17c05ff339aac9daf21f2b9ef67146558d53b626d8d6` and
contains `ARMを装着する`, translated here as **EQUIP ARM**. The matching source
TXC in `arm_get_tex.b` is 17,472 bytes, SHA-256
`de9283c764fb097e677aad8600b6a24c602767eea07ab11868414dcea5817ba5`.
The Japanese baseline remains unchanged.

## Reproducible artwork path

The transparent model-generated lettering input is stored beside the texture as
[`00039_00921_0004_arrm_eng_layer.png`](../graphics/weapons/00039_00921_0004_arrm_eng_layer.png),
2079×756 pixels, SHA-256
`5685e2e698ddb774473f9f4cf2ff9eaeb0a905e8659eb49f9a4b4a0150b1d888`. The
prompt requested only flat, bright-white `EQUIP ARM` lettering on transparency;
the model output is an input layer, not the finished game texture.

An earlier beveled/shaded lettering draft was rejected: uniform fit occupied
only about 135 pixels of the 236-pixel width and faint alpha fringes remained.
The revised flat, wide lettering plus a 128/255 alpha threshold fills the band
more clearly. No rejected draft was imported.

`tools/graphics_compose.py` removes pixels below alpha 128, crops to the
remaining alpha bounds, deterministically fits the layer into source bounds
`[10,246)×[12,53)`, clears the Japanese text and edge pixels in
`[8,248)×[10,54)`, then composites onto the untouched 256×64 source canvas.
The command is reproducible through the repository rule:

```sh
make graphics-compose \
  GRAPHICS_COMPOSE_BASE=graphics/weapons/00039_00921_0004_arrm_jp.tga \
  GRAPHICS_COMPOSE_OVERLAY=graphics/weapons/00039_00921_0004_arrm_eng_layer.png \
  GRAPHICS_COMPOSE_OUTPUT=graphics/weapons/00039_00921_0004_arrm_eng.tga \
  GRAPHICS_COMPOSE_REGION='10 12 236 41' \
  GRAPHICS_COMPOSE_CLEAR_REGION='8 10 240 44' \
  GRAPHICS_COMPOSE_ALPHA_THRESHOLD=128 \
  GRAPHICS_COMPOSE_REPLACE=1
```

The output [`00039_00921_0004_arrm_eng.tga`](../graphics/weapons/00039_00921_0004_arrm_eng.tga)
is 65,554 bytes, 256×64, SHA-256
`2dff20901f160c119aefbf0db65699b87d963ca93e9af8a824fc5e29e73d4a03`. Pixel
comparison confirms that every pixel outside the clear rectangle is identical
to the Japanese baseline. The source PSMT8 palette importer emits the original
17,472-byte TXC size; staged override SHA-256 is
`0ab7047f48e2fbcbe48deaff45fc6702e05962feec84e7fb4f151b11bf516a2c`.
Static native-size review found the phrase legible. Emulator, UV placement, and
runtime composition remain unverified.

## Verification

- `python3 -m unittest tests.test_graphics_compose -v`: four tests pass for PNG
  filters/CRC, alpha-threshold crop, bounded clearing/composition, and exact
  canvas dimensions.
- `rtx3.encode_tga` maps the English TGA to the source PSMT8 TXC without changing
  payload size; decode preview is 256×64.
- `tools/graphics.py build` lists the asset among fourteen English TXC
  overrides. `make verify-graphics-image` reparses its 17,472-byte TXC from the
  rebuilt ISO with SHA-256
  `0ab7047f48e2fbcbe48deaff45fc6702e05962feec84e7fb4f151b11bf516a2c`; all
  fourteen overrides total 1,400,064 exact TXC bytes. The authenticated full-disc
  comparison is recorded in
  `reports/mar_eng_compare_14_graphics_database.json`. Runtime, UV placement,
  and emulator acceptance remain unverified.
