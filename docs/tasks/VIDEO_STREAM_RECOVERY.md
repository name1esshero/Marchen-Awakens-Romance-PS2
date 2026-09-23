# SofDec movie editing and reinsertion — 2026-09-23

## Finding

The 13 direct members of `MOVIE.AFS;1` total 685,111,296 source bytes. They use
2,048-byte CRI SofDec sectors with MPEG-2 Main video on stream `0xe0`, CRI ADX
audio on `0xc0`, and two private `0xbf` metadata packets in the four-sector
opening. The 640×448 video profile is progressive 4:2:0 at 30000/1001 fps.
`tools/sofdec.py` validates this observed profile, the sector/PES extents, CRI
signatures and source audio before allowing a replacement.

The source exports contain 615,212,537 MPEG-2 video elementary-stream bytes,
59,642,694 ADX audio bytes, and 10,256,065 SofDec/container/packetization bytes.
Only the MPEG-2 video bytes count as semantically editable in the census. Audio
is preserved but has no override representation yet; private metadata and
container bytes remain format data, not editable media.

## Round-trip evidence

The baseline remux preserves both `0xbf` metadata payloads (including the
`CRITAGS` sector), and its extracted MPEG-2 video and ADX elementary streams
match their exported Japanese sources exactly. Full decode comparisons across
all 13 streams matched every video frame hash and every decoded PCM audio byte.
The comparisons covered 33,107 frames total; this is a no-op remux check, not a
game runtime test.

The generic upstream `sfd-muxer` packetizer needed corpus-specific changes:
keep MPEG picture headers intact at sector boundaries, permit shortened
non-final packets, and leave enough space for a valid padding PES packet. The
adapter regenerates the first two system sectors and pack headers while
retaining the original metadata payloads in opening sectors two and three.
Rebuilt PS streams pass the local strict packet parser and recover exact source
elementary streams. The MIT-licensed upstream implementation and attribution
are recorded in [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md); the
game-specific adapter is in `tools/sofdec.py`.

An edited MPEG-2 test clip also decoded all of its frames after remux while the
original ADX stream and CRI metadata remained intact. A synthetic YFS/AFS test
verifies that an expanded video override moves the member and updates both
archive tables; Japanese source sidecars remain unchanged. A temporary
5,705,777,152-byte relocated mod ISO with that test clip built successfully,
reparsed, and yielded the exact edited video stream plus its original ADX stream
from `MOVIE.AFS`. The smoke-test image was discarded. No edited movie has been
inspected in an emulator.

## Editable workspace

Run `make movies-export` to populate the root `movies/` directory. It contains
flat immutable `*_jp.m2v` and `*_jp.sfa` source files plus `index.json` with
source, stream and profile hashes. Do not edit the Japanese files. Place a
profile-compatible edited MPEG-2 elementary stream beside its source as
`*_eng.m2v`; `make movies-audit` checks the immutable sources, the override hash,
and the game's sequence profile. `make build-mod-disc` remuxes each English
video with the original ADX and CRI metadata, applies the relocated member, and
writes `mar_eng.iso` in the workspace root. No audio replacement is supported.

The current profile check requires 640×448, aspect code 2, MPEG-2 Main/Main,
progressive sequence, 4:2:0 chroma, and the observed 30000/1001 frame-rate code.
An edited file that changes these fields is rejected before ISO construction.

## Reproduction and limits

Run `python3 -m unittest tests.test_mpeg_ps tests.test_sofdec_movies -v` for
synthetic structure, metadata-preservation, incompatible-profile rejection,
audio-preserving remux, and archive relocation checks. `make movies-audit`
revalidates exported baselines and English overrides. `make asset-census`
refreshes the byte-weighted report using only audited MPEG-2 video source spans
in B.

The MPEG-2 stream can be edited and reinserted through the full ISO builder;
ADX editing, in-game playback, and translated frame layout remain open.
