# `lib_movie_sum.b` UI texture audit

## Scope and method

This read-only audit covers all 23 `graphics/index.json` rows with
`asset_path` exactly `disc!/_DATA.YFS;1!/data/menu/lib_movie_sum.b` and
`category` equal to `user_interface`. All 23 corresponding `_jp.tga` files were
opened and visually inspected individually, with nearest-neighbor enlargement
for pixel review. Previews used the exported TGA pixel rows in their declared
top-origin orientation; no unswizzling, UV remapping, or baseline edits were
performed.

Every row is indexed as 64×64 and its full-file SHA-256 below matches
`graphics/index.json`. Each file is exactly 16,402 bytes and has an uncompressed
true-color TGA header: image type 2, 32 bits per pixel, no image ID, origin
(0,0), and descriptor `0x28` (top origin, 8 alpha bits). Thus each extent is
exactly `18 + 64 × 64 × 4 = 16,402` bytes. The alpha channel is present in the
format but every alpha sample in every file is 255. The 23 files have 23
distinct hashes and total 377,246 bytes.

## Inventory and findings

“Text bounds” are inclusive source-pixel bounds. No readable Japanese, Latin,
or other text was found in any of the 23 textures, so every row has no text
bounds. The varied small scene details were not promoted to text candidates
without visible letterforms.

| Japanese baseline | Dimensions; TGA extent | SHA-256 | Visual finding; visible text/bounds |
| --- | ---: | --- | --- |
| `00039_01523_0000_ms_s001_jp.tga` | 64×64; 16,402 B | `8139f3ea31221f0b70c83eee55232c0633517fbb27278122c0f40500dd06efe6` | Dark, ornate tower/arch-like artwork with a bright lower strip; no text; bounds: none. |
| `00039_01523_0001_ms_s002_jp.tga` | 64×64; 16,402 B | `bfa1b2b3931cde9f40cc1c9072694b3d6fd31aa302196036bbaf9647b802b818` | Blue-sky and brown structure scene; small details do not resolve as writing; bounds: none. |
| `00039_01523_0002_ms_s003_jp.tga` | 64×64; 16,402 B | `d3c5923ae9c60fdee3637531a097aff22285c39a309e03d55b4876e12439dd5c` | Low-contrast purple panel with inset rectangular shading; no text-like marks; bounds: none. |
| `00039_01523_0003_ms_s004_jp.tga` | 64×64; 16,402 B | `afeb602cbb12b392db82c23a7690a9b19cdc3a0a0b46c9a51a95b0d6a56a5f1a` | Low-contrast purple panel with a broad inset gradient; no text-like marks; bounds: none. |
| `00039_01523_0004_ms_s005_jp.tga` | 64×64; 16,402 B | `220c88d8e2504a82053c5a70b032497d739bfa05a1201f6e40ffcb130cb17f23` | Pale angular vertical artwork against blue/gray; no text; bounds: none. |
| `00039_01523_0005_ms_s006_jp.tga` | 64×64; 16,402 B | `71d2b364a84e8fb17676818671c5522a53123e60dc738eecc8adf06b5297441d` | Dark human-like silhouette in a pale inset panel; no text; bounds: none. |
| `00039_01523_0006_ms_s007_jp.tga` | 64×64; 16,402 B | `6d9565651857b524aefaf01c372bd933588df0296880c46ec2268ddbacda60ca` | Close-up portrait-like artwork on a dark background; no text; bounds: none. |
| `00039_01523_0007_ms_s008_jp.tga` | 64×64; 16,402 B | `5a418d9ececa978832539a1d50d677abe2956107c9c1652a5447b0b3e7815786` | Prominent green musical-note emblem with yellow arcs over a bright blue multicolor scene; no text; bounds: none. |
| `00039_01523_0008_ms_s009_jp.tga` | 64×64; 16,402 B | `f0dacf6199b5788d9185c7e389483fa7eb160d1137772b144463de7054c76ae3` | Same musical-note motif over a pale/blue multicolor scene; no text; bounds: none. |
| `00039_01523_0009_ms_s010_jp.tga` | 64×64; 16,402 B | `5e3d228b22240e087ea347ffa5098698945a3854ea7e8fb255b1a7a69a7fa5e6` | Musical-note motif over a brown, yellow, and black scene; no text; bounds: none. |
| `00039_01523_0010_ms_s011_jp.tga` | 64×64; 16,402 B | `af1afef055a0167bfb6e48df25775733ce1372e1c67d590cab42383adfc04e95` | Musical-note motif over a cream/red field with block-like details; no text; bounds: none. |
| `00039_01523_0011_ms_s012_jp.tga` | 64×64; 16,402 B | `cf73e81dd263c42130e3ff77de4d605cc63aa186c6f0969f3f4179d73e3b8e46` | Musical-note motif over a dark, shelf-like interior pattern; no text; bounds: none. |
| `00039_01523_0012_ms_s013_jp.tga` | 64×64; 16,402 B | `a503b36f3a0d921a7396526c67fd4b7759e679c3d6b0b50f5aad5d059ac36a49` | Musical-note motif over a pink/magenta illustrated field; no text; bounds: none. |
| `00039_01523_0013_ms_s014_jp.tga` | 64×64; 16,402 B | `08ecbb2aec88e1dd3a16a5519d82d785f7f3aacf6ee50f4e92f31f06461da860` | Musical-note motif over a purple, blue, and gray scene; no text; bounds: none. |
| `00039_01523_0014_ms_s015_jp.tga` | 64×64; 16,402 B | `2065e50c3d9793ba354b288f7283533b6ad724340aa2c92660633f26b05909b1` | Musical-note motif over a dark blue field; no text; bounds: none. |
| `00039_01523_0015_ms_s016_jp.tga` | 64×64; 16,402 B | `aa9b76ebfd4e0c9ce974ca75757af658ab73886afd457a03805dbf7d775bc702` | Musical-note motif over a charcoal/purple field with orange detail; no text; bounds: none. |
| `00039_01523_0016_ms_s017_jp.tga` | 64×64; 16,402 B | `7b3a125c2d9bc0522864ae537d7b1a71d5b847880e4b84b10ee8f5753fe1a554` | Musical-note motif over a blue, dark, and brown scene; no text; bounds: none. |
| `00039_01523_0017_ms_s018_jp.tga` | 64×64; 16,402 B | `86d850114d83e71cbbb17b33ef3039890fdf878f78ef6a21f9ed5df68428c340` | Musical-note motif over a dark-blue field with pale horizontal bands; no text; bounds: none. |
| `00039_01523_0018_ms_s019_jp.tga` | 64×64; 16,402 B | `49059b193df4d4b87cf2b80433b42efb3bd7d5c3f602efbb0ca475979f5ae8f6` | Musical-note motif over a dark green/brown scene; no text; bounds: none. |
| `00039_01523_0019_ms_s020_jp.tga` | 64×64; 16,402 B | `a1fb28717ce17228db58c418fd81fc8a1efc2502665331630b07217509b03212` | Musical-note motif over a purple/black scene; no text; bounds: none. |
| `00039_01523_0020_ms_s021_jp.tga` | 64×64; 16,402 B | `795cd7286ccff93875cfb27d1b9ed0661b0271b305374ead69c04ac301c828da` | Musical-note motif over a gray/brown structure scene; no text; bounds: none. |
| `00039_01523_0021_ms_s022_jp.tga` | 64×64; 16,402 B | `0fea54de2186c5a742839d9e574fbc46820753d8007fba75ed14d988f582bc2a` | Musical-note motif over dark ornamental architecture with a bright lower strip; no text; bounds: none. |
| `00039_01523_0022_ms_s023_jp.tga` | 64×64; 16,402 B | `6a5815c0e1e9b0e4f887d48accf7c3805f31e5a2e15baae77c44e565dcbf5c3c` | Musical-note motif over a charcoal portrait-like scene; no text; bounds: none. |

## Result and limits

This bundle slice yielded no translation-bearing surface in the exported
texture pixels. The most consistent recognizable mark is the green musical
note with yellow arcs in rows `0007`–`0022`; it is a graphic emblem, not
Japanese lettering. Rows `0002` and `0003` are low-contrast panels, but visual
review found only broad shading and no unresolved character-like strokes.

The audit establishes only the contents and byte integrity of these exported
TGAs. It does not establish UV rectangles, draw order, composition, animation,
runtime visibility, or the role of the bundle resources. No English variants,
container rebuild, ISO build, or emulator test was performed; all Japanese
baselines remain unchanged.
