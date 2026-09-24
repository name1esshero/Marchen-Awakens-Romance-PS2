# Training-title English texture

## Scope and source

This task translates only the confirmed `トレーニング` (“Training”) title in
`graphics/user_interface/00039_01593_0010_trng_jp.tga` to the exact English
word `TRAINING`. The Japanese baseline remains the immutable comparison source;
no other training-menu texture was changed.

Source TGA: 256×64, type 2, 32-bit, descriptor `0x28`, 65,554 bytes,
SHA-256 `2323318d0dc1ea71fc6713af798e6b5682abb9c1d505a439903d5f840e35b8f8`.
The source alpha scan confirms visible title bounds inclusive `(1,12)–(224,57)`,
or half-open `[1,225) × [12,58)`. The indexed RTX3 source hash is
`6a8f80ad278924cdce9d4780c29bc773038ede804e13d6a1f458186ced3f3bb0`.

## Generated layer

The built-in image-generation tool created one transparent lettering layer. The
first candidate (`b93774b44c5bc5cef10dc583328b32b7e20639c30baf378a6f9e53e862618618`)
was not used: its alpha-bounds ratio was 3.256:1 and it left the wordmark too
narrow when kept proportional. The selected second output is tracked at
[`00039_01593_0010_trng_eng_layer.png`](../graphics/user_interface/00039_01593_0010_trng_eng_layer.png);
its source-generation path was
`~/.codex/generated_images/01a0d064-effe-7f93-88db-6e0d8454b41e/exec-36d1b281-31e6-4aee-8f79-ea65f52535e5.png`.

Selected layer: 2172×724 PNG, SHA-256
`1e49150306afb0acae23de3c4c07dba548ad755c58015fa5ba09a838bfcb1a86`;
alpha bounds at threshold 1 are `[45,2135) × [77,684)`, giving a 3.443:1
visible ratio. It was inspected at native game-texture scale and at 4× nearest
neighbor. The exact text is visibly `TRAINING`; the artwork uses the requested
yellow/chartreuse-to-orange-red-to-magenta/purple shading and dark beveled
outline/extrusion.

Final prompt (built-in tool, style references only; no source canvas edit):

```text
Use case: logo-brand
Asset type: a freestanding game-menu title wordmark layer
Input image 1: Japanese source is only the reference for the original beveled game-title style and color placement. Input image 2: prior English candidate is only a reference for the desired dark bevel/extrusion and gradient. Do not include or reproduce Japanese characters.
Primary request: create exactly one transparent English lettering layer spelling TRAINING.
Style/medium: match the references' bold angular game-logo treatment: pale yellow/chartreuse highlights at the top, muted orange-red across the middle, magenta-purple shading toward the bottom, and a dark charcoal beveled outline with a short dark extrusion. Preserve strong clean strokes and small-size legibility.
Composition/framing: make the complete wordmark a shallow, very wide horizontal form with the visible lettering about 4.9 times wider than its cap-height, designed to fit a 224×46-pixel destination without cropping. Use normal-width uppercase letters with low cap height, compact spacing, and no tall narrow/condensed proportions. Keep generous transparent space above/below if needed. Center the wordmark, keep all eight letters fully inside the image.
Text (verbatim): "TRAINING" — uppercase, exactly T-R-A-I-N-I-N-G in that order.
Constraints: genuinely transparent background with clean alpha around the lettering; no source-canvas layout or background.
Avoid: Japanese text, extra words, symbols, background, checkerboard, glow, watermark, clipped or tall letters, or a second line.
```

## Deterministic composition and verification

The final sibling is
[`00039_01593_0010_trng_eng.tga`](../graphics/user_interface/00039_01593_0010_trng_eng.tga),
SHA-256 `52fa9103b580e2c3988c273b48515808460b53394bce050ec3209662e76c6e14`.
It keeps the source 256×64 canvas and TGA type/depth/descriptor/extent. The
tracked result was composed with:

```sh
python3 tools/graphics_compose.py \
  --base graphics/user_interface/00039_01593_0010_trng_jp.tga \
  --overlay graphics/user_interface/00039_01593_0010_trng_eng_layer.png \
  --output graphics/user_interface/00039_01593_0010_trng_eng.tga \
  --region 1 12 224 46 --clear-region 1 12 224 46 --fit contain
```

Parameters: destination and clear rectangle `(x=1, y=12, width=224, height=46)`,
`contain`, alpha threshold 1. Aspect-preserving fit uses a centered 158×46
wordmark, leaving horizontal space inside the measured source region rather than
cropping or distorting the generated letters. Final visible alpha bounds are
`[34,192) × [12,58)`.

Verification: a second composition with the same base, tracked layer and
parameters produced byte-identical output SHA-256
`52fa9103b580e2c3988c273b48515808460b53394bce050ec3209662e76c6e14`. A
pixel-by-pixel comparison found 10,304 changed pixels, all inside the declared
clear rectangle, and zero changed pixels outside it. The Japanese baseline
still hashes to its source value above.

## Limits

This confirms deterministic TGA artwork composition only. Source-palette RTX3
import, ISO reinsertion and emulator checks are owned by the lead and were not
run here. No UV mapping, runtime placement, or in-game readability is claimed.
