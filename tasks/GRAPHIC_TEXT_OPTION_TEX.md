# Option-menu texture text audit (DQ-20)

Read-only visual review of the six `user_interface` textures mapped to
`disc!/_DATA.YFS;1!/data/menu/option_tex.b`. The sibling `icon` entry is not in
this scope; it was reviewed under DQ-10. Every Japanese baseline was compared
against `graphics/index.json` and the mapped TXC source in the extracted bundle.

| Japanese TGA | Size | TGA SHA-256 | Source TXC SHA-256 | Visual finding |
|---|---:|---|---|---|
| `00039_01544_0000_ctrl_jp.tga` | 256×256 | `4064da47397c59fcc98c0f98d4853d77d1cd3ffcf33872461a3820a2e05e9a0b` | `a5688ba47692fe634a4b8e65f31b0785bbe9bda25800250e72ab93e2c1f3afa0` | Controller outline and button symbols; no readable Japanese wording. |
| `00039_01544_0001_gmst_jp.tga` | 256×256 | `0c98601563fe72fde368a297b2a326ca0522cad0bab930c3f97c0668e222749e` | `6780805b9398ec783018f7b8dc212db5eba0999e0d2f0bddaf757757811e31c7` | Chessboard and pieces; no visible wording. |
| `00039_01544_0003_optn_jp.tga` | 256×64 | `d634021fe2cfac159b65d369681f6695d2ef0bf606d98ebacbb0be2f9e96bddf` | `cb13f68f38b65e902ab82d0afeca09242e115cecbf07bbec7b3322fde88cc392` | Clear Japanese wordmark `オプション` (“OPTIONS”); visible alpha bounds are x=1–188, y=13–58 (188×46 pixels). |
| `00039_01544_0004_sdst_jp.tga` | 256×256 | `3002742c25f2ee974d140ac71d7f4d454336e5c6531d1599a2ed518804e23c96` | `d148478ca367d75ace4b58b3ead3dc0a478341c1a0501c46d982137edef4ea3c` | Rendered object/lens-like menu illustration; no visible wording. |
| `00039_01544_0005_svld_jp.tga` | 256×256 | `086f6e9fc516583b7f8c4f72e0f9b3a6c4bbdeed5c1808ba11bd3264ddf630f2` | `8a1a623f741669fa4ddf480eddad531c242c9ab03a6225f871a1109bfd890cb8` | Dark, empty panel/window artwork; no readable wording. |
| `00039_01544_0006_window_jp.tga` | 128×128 | `a53fe384bbf276adaed7da83c8504a9e6968a90e3e54bd6214d89c9229e29087` | `6d9c309e9c1d7be73264010b3bee22f841b311d185dc76e9835994203da51560` | Window/control marks and a tiny low-contrast glyph-like strip near the bottom; no wording is confidently readable, so leave it unresolved. |

All six files are type-2, 32-bit, top-origin TGAs (`descriptor=0x28`); their
declared dimensions and exact payload extents parse successfully. The full TGA
and source-TXC hashes above match the index. The Japanese wordmark is the only
confirmed readable language-bearing surface in this six-image scope; the tiny
marks in `window` remain a candidate, not a transcription. The `icon` row is
excluded because DQ-10 already reviewed it.

No source image or English override was edited during this audit. Flat texture
inspection does not establish UVs, renderer behavior, screen placement, or
runtime visibility. See [`LOCALIZATION_METHODOLOGY.md`](../docs/LOCALIZATION_METHODOLOGY.md),
[`graphics/index.json`](../graphics/index.json), and the
[source bundle](../extracted/assets/00039.asset/01544.resources/).
