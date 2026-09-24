# `GameOver_tex.b` texture audit

## Scope and method

This read-only audit covers all four `graphics/index.json` entries whose
`asset_path` is exactly `disc!/_DATA.YFS;1!/data/menu/GameOver_tex.b`. All four
corresponding `_jp.tga` baselines were visually reviewed individually. The two
`bg_*` images were inspected both as ordinary RGBA composites and as separate
grayscale alpha-plane views; the alpha views make the text-shaped transparent
areas legible when RGB alone is black. Previews used the exported TGA pixel
rows in their top-origin order, with no unswizzling or UV remapping.

The dimensions, TGA headers/extents, disk TGA hashes and indexed image hashes
were checked for every row. All four are uncompressed type-2, 32-bit true-color
TGAs with no image ID, origin `(0,0)`, top-origin descriptor `0x28`, and exact
`18 + width × height × 4` extents. The index's `source_sha256` values below
identify the source TXC members; those TXC payload files are not present in this
worktree, so their hashes are reported from the index and were not independently
recomputed here. TGA hashes were computed from the checked-in files and match
`image_sha256` in the index.

Bounds are inclusive source-pixel coordinates with origin at the upper-left.
For `bg_00` and `bg_01`, the letterform bounds use the low-alpha core (`alpha <
128`); softer surrounding shading extends beyond that core. For `gmover`, the
letter face bounds use pixels with all RGB channels greater than 128; its dark
bevel/shadow extends outside that face region. For `flear`, the nonzero-alpha
bounds include every pixel with alpha >0; its bright-core bounds use pixels
with alpha >32 and all RGB channels ≥160.

## Inventory and findings

| Indexed source member / category | Japanese baseline; dimensions; TGA extent | Source TXC SHA-256 (index) | Exported TGA SHA-256 | Visual finding; text bounds |
| --- | --- | --- | --- | --- |
| `0000_bg_00.txc.bin` / `backgrounds` | `00039_00988_0000_bg_00_jp.tga`; 512×512; 1,048,594 B | `99fb2d03e2e534d1718405b07813fa5428a806296b56d7d2fdd8ecb82d569228` | `b5f44d200170a09f276da0f331962e76fb24da7247af53226b04f4989ff26d9b` | RGB is all zero; 16 alpha levels form a low-alpha English `GAME OVER` silhouette with a broad soft horizontal band. Core bounds at alpha <128: `(60,219)`–`(451,291)`. No Japanese text observed. |
| `0001_bg_01.txc.bin` / `backgrounds` | `00039_00988_0001_bg_01_jp.tga`; 512×512; 1,048,594 B | `76d9cf38e592db1b0fe01544eb925f174528eb8e2a9ec3720c25217f73684172` | `3ccf712ebc41f28498a5618f4adce392e3747fcc11061df3382945b0ed509745` | RGB is all zero; 16 alpha levels form a crisper low-alpha English `GAME OVER` silhouette. Core bounds at alpha <128: `(64,221)`–`(451,289)`. No Japanese text observed. |
| `0002_flear.txc.bin` / `effects` | `00039_00988_0002_flear_jp.tga`; 256×256; 262,162 B | `b960776ec869c3fc688d69acf503febbcdaaa4244cef0c90070190c665fca66f` | `eb309ed460f2963bf4ac6210d252a3727a10dd3de9e9b19483e94bcd61f88cdc` | Pale radial flare/glow with 129 alpha levels; nonzero-alpha bounds `(22,22)`–`(234,234)` and bright-core bounds `(31,31)`–`(225,225)`. No text or text-like strokes observed. |
| `0003_gmover.txc.bin` / `user_interface` | `00039_00988_0003_gmover_jp.tga`; 512×128; 262,162 B | `e1fa277e7bf492460b490c572deaec61a2c81c3bc93414b193b2263cb96ede33` | `a2aa90ce4c7ef3bcb38f8e3dfbf93bcbf4293c72226873201139fc9835db0962` | Fully opaque, direct English `GAME OVER` wordmark with gray/black bevel and shadow. Bright letter-face bounds at RGB >128: `(64,27)`–`(450,98)`; colored/shadow pixels extend to `(61,26)`–`(451,99)`. No Japanese text observed. |

All four extracted TGA hashes are distinct. Their extents total 2,621,512 bytes.
The English phrase is visible in three textures: `bg_00`, `bg_01`, and
`gmover`. It is English lettering, not a Japanese string requiring
transcription. `flear` is visual-effect artwork without wording.

## Result and limits

The alpha-plane review matters for the two `bg_*` assets: an RGB-only preview is
uniformly black because every source RGB sample is zero, while a normal RGBA
composite reveals the low-alpha silhouette as `GAME OVER`. Viewing
the alpha plane separately confirms that the text-bearing shape is encoded in
alpha rather than RGB. The independently visible `gmover` asset confirms the
same English wording in an opaque lettering texture.

This establishes only the pixels and metadata of the indexed TGA exports. It
does not establish how the alpha masks are blended, which texture is displayed,
or any UVs, draw order, composition, animation, or runtime behavior. No Japanese
baseline was changed, no English override was authored, and no container/ISO
build or emulator test was performed.
