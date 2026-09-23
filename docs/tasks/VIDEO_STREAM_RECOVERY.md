# Movie stream structure census — 2026-09-23

## Finding

The 13 direct resources in `MOVIE.AFS;1` total 685,111,296 bytes. All parse
under the observed 2,048-byte sectorized MPEG-1 program-stream envelope and
reassemble byte-for-byte from the indexed source extents. The parser validates
334,514 sector-aligned 12-byte pack headers, 364,158 length-delimited packets,
the program-end code at the start of each final sector, and 26,572 terminal
`0xff` bytes. Every byte of every stream belongs to one validated segment.

Packet stream IDs in the corpus are `0xbb` (26), `0xbe` (29,644), `0xbf` (26),
`0xc0` (29,592), and `0xe0` (304,870). These counts establish packet boundaries
and container structure. They do not establish the meanings of packet payloads,
timestamps, or codec headers.

## Media probe

A temporary FFmpeg 7.0.2 static binary supplied by `imageio-ffmpeg` decoded one
video frame and one audio sample from each stream. The probe reported 640×448,
29.97 fps MPEG-2 Main video and 48 kHz stereo ADX audio for all 13 files. This
was a decode smoke test, not a full corruption scan, a re-encode, or a game
runtime test. The temporary binary is not a repository dependency.

## Editing/rebuild boundary

`tools/mpeg_ps.py` validates and preserves the observed container envelope. Its
writer is an exact no-op reassembler; it does not expose decoded frames, subtitle
tracks, audio samples, or a remux/relocation writer. The census therefore counts
these bytes as structurally classified, but does not include them in semantic
editability B.

The bundled FFmpeg generic MPEG, VCD, and VOB muxers refused the source ADX
audio as an unsupported audio codec during a subtitle-remux experiment. A
separate community PSS muxing utility inspected during research expects BD
private-stream audio packets, whereas this corpus exposes audio packets under
stream ID `0xc0`; it is not evidence of a compatible mux path. No replacement
movie has been produced. Keep the movie bytes in the editable/rebuild work queue
until the codec and game-specific remux contract are independently established.

## Reproduction and limits

Run `python3 -m unittest tests.test_mpeg_ps -v` for synthetic complete-stream,
exact reassembly, zero-length packet, bad marker, bad trailer, and cross-sector
extent checks. Run `python3 tools/asset_recovery_census.py` against the prepared
workspace to audit the full 13-file corpus and regenerate the byte-weighted
report.

The parser deliberately accepts only the observed MPEG-1 12-byte pack-header
variant, one pack per data sector, nonzero length-bounded packets contained in a
single sector, and the observed final-sector trailer. It does not validate
MPEG-2 picture/audio syntax, editability, a modified stream, or playback.
