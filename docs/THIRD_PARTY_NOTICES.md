# Third-party notices

`tools/_vendor/sfd_muxer/container.py` includes the pure-Python container
implementation from `sfd-muxer` 0.1.1 by soyjxck, distributed with an MIT
license. Its upstream project credits the CRI SofDec muxer by nebulas-star as
the reference implementation. The vendored license is in
[`third_party/licenses/sfd-muxer-MIT.txt`](../third_party/licenses/sfd-muxer-MIT.txt).

The MARPS2 adapter in `tools/sofdec.py` adds the corpus-specific safeguards:
MPEG-2 profile checks, original CRI metadata-sector preservation, and video
packet boundaries that keep picture headers intact and leave room for valid
padding packets. Upstream's generic mux mode is not used directly for game
assets.
