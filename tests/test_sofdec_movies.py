import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from tools import assets, movies, mpeg_ps, sofdec
from tools._vendor.sfd_muxer import container as sfd


def elementary_video(frame_payload=b"frame-0"):
    sequence = bytes.fromhex(
        "000001b3 2801c024 0c3be302 10404040 "
        "000001b5 148a000100"
    )
    picture = b"\x00\x00\x01\x00\x00\x08\x00\x00\x00\x00"
    return sequence + picture + frame_payload


def adx_stream():
    data = bytearray(0x130 + 64)
    data[:2] = b"\x80\x00"
    data[6] = 18
    data[7] = 2
    data[8:12] = (48000).to_bytes(4, "big")
    data[0x11A:0x120] = b"(c)CRI"
    data[0x130:] = b"\x22" * 64
    return bytes(data)


def synthetic_movie(video=None):
    video = elementary_video() if video is None else video
    audio = adx_stream()
    base = sfd.SFD.mux(video, audio)
    opening = base._opening_blocks()
    prefix = bytearray(opening[:3 * sfd.SECTOR])
    payload = b"CRITAGS\0synthetic\0"
    private = (b"\x00\x00\x01\xbf" + len(payload).to_bytes(2, "big") + payload)
    padding_total = sfd.SECTOR - 12 - len(private)
    tag_sector = (
        sfd._pack_head(sfd._scr_for_block(3, base.mux_rate), base.mux_rate) +
        private + sfd._padding_stream(padding_total - 6)
    )
    prefix.extend(tag_sector)
    raw = sofdec._GameSFD(video, audio, bytes(prefix)).to_bytes()
    mpeg_ps.parse(raw)
    return raw, video, audio


def afs_with_movie(movie):
    offset = 2048
    data = bytearray(offset)
    data[:4] = b"AFS\0"
    struct.pack_into("<I", data, 4, 1)
    struct.pack_into("<2I", data, 8, offset, len(movie))
    data.extend(movie)
    return bytes(data)


def yfs_with_movie_archive(archive):
    offset = 2048
    data = bytearray(offset)
    data[:4] = b"YFS\0"
    struct.pack_into("<2H", data, 4, 1, 1)
    struct.pack_into("<2H", data, 68, 1, 0)
    entry = 72
    data[entry:entry + 11] = b"MOVIE.AFS;1"
    struct.pack_into("<3I", data, entry + 24, len(archive), offset, 0)
    data.extend(archive)
    return bytes(data)


class SofdecMovieTests(unittest.TestCase):
    def test_extract_and_rebuild_preserve_audio_cri_tags_and_sector_contract(self):
        original, video, audio = synthetic_movie()
        streams = sofdec.extract(original)
        rebuilt = sofdec.rebuild(original, streams["video"])
        parsed = mpeg_ps.parse(rebuilt)
        recovered = sfd.SFD.from_bytes(rebuilt)

        self.assertEqual(streams["video"], video)
        self.assertEqual(streams["audio"], audio)
        self.assertEqual(recovered.extract_video(), video)
        self.assertEqual(recovered.extract_audio(), audio)
        self.assertEqual(parsed["packet_counts_by_stream_id"]["0xbf"], 2)
        self.assertEqual(parsed["structural_bytes"], len(rebuilt))
        for sector in (2, 3):
            start = sector * sofdec.SECTOR_SIZE + 12
            end = (sector + 1) * sofdec.SECTOR_SIZE
            self.assertEqual(rebuilt[start:end], original[start:end])

    def test_rejects_an_edited_video_with_incompatible_dimensions_or_rate(self):
        original, video, _audio = synthetic_movie()
        changed_profile = bytearray(video)
        changed_profile[7] = (changed_profile[7] & 0xF0) | 5
        with self.assertRaisesRegex(ValueError, "unsupported game movie video profile"):
            sofdec.rebuild(original, bytes(changed_profile))

    def test_rejects_changed_cri_tags(self):
        original, _video, _audio = synthetic_movie()
        changed = bytearray(original)
        changed[3 * sofdec.SECTOR_SIZE + 12 + 6] ^= 1
        with self.assertRaisesRegex(ValueError, "CRITAGS signature"):
            sofdec.extract(bytes(changed))

    def test_english_movie_override_relocates_through_parent_archive(self):
        original, video, audio = synthetic_movie()
        edited_video = video + (
            b"\x00\x00\x01\x00\x00\x08\x00\x00\x00\x00edited-frame" * 1000
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_archive = root / "movie.yfs"
            source_archive.write_bytes(yfs_with_movie_archive(afs_with_movie(original)))
            workspace = root / "workspace"
            with source_archive.open("rb") as stream:
                census = {"containers": {}, "leaves": 0, "extensions": {}, "unparsed": []}
                assets.export_node(
                    stream, 0, source_archive.stat().st_size, workspace,
                    *assets.archive(stream, 0, source_archive.stat().st_size), census,
                )
            source_sidecar = workspace / "00000.asset/00000.bin"
            catalog = [{
                "name": "disc!/MOVIE.AFS;1!/00000.bin",
                "size": len(original),
                "source": "00000.asset/00000.bin",
                "sha256": hashlib.sha256(original).hexdigest(),
                "zero": False,
            }]
            (workspace / "catalog.json").write_text(
                json.dumps(catalog), encoding="utf-8",
            )
            movie_root = root / "movies"
            movies.export(workspace, movie_root)
            english_path = movie_root / "00000_eng.m2v"
            english_path.write_bytes(edited_video)
            audit = movies.audit(workspace, movie_root)
            self.assertEqual(audit["english_override_count"], 1)

            rebuilt_archive = root / "rebuilt.afs"
            assets.build(workspace, rebuilt_archive, relocate=True,
                         movie_overrides=movie_root)
            rows = assets.archive(io.BytesIO(rebuilt_archive.read_bytes()), 0,
                                  rebuilt_archive.stat().st_size)[2]
            movie_entry = rows[0]
            self.assertGreater(movie_entry["size"], len(original))
            with rebuilt_archive.open("rb") as stream:
                stream.seek(movie_entry["offset"])
                rebuilt_movie = stream.read(movie_entry["size"])
            streams = sfd.SFD.from_bytes(rebuilt_movie)
            self.assertEqual(streams.extract_video(), edited_video)
            self.assertEqual(streams.extract_audio(), audio)
            self.assertEqual(source_sidecar.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
