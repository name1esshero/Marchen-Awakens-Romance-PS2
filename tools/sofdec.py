"""Extract and rebuild this game's sectorized CRI SofDec movie variant."""

from collections import defaultdict
import hashlib
import io

try:
    from ._vendor.sfd_muxer import container as _sfd
    from ._vendor.sfd_muxer.container import SFD
    from . import mpeg_ps
except ImportError:  # Support direct execution of sibling tools.
    from _vendor.sfd_muxer import container as _sfd
    from _vendor.sfd_muxer.container import SFD
    import mpeg_ps

SECTOR_SIZE = 2048
SOURCE_PREFIX_SECTORS = 4
SOURCE_PREFIX_BYTES = SECTOR_SIZE * SOURCE_PREFIX_SECTORS
MAX_VIDEO_PACKET_PAYLOAD = 0x7DB
PICTURE_START = b"\x00\x00\x01\x00"


def video_profile(video: bytes) -> dict:
    """Read the bounded sequence header and MPEG-2 sequence extension."""
    if len(video) < 9 or video[:4] != b"\x00\x00\x01\xb3":
        raise ValueError("video elementary stream lacks an MPEG sequence header")
    width = (video[4] << 4) | (video[5] >> 4)
    height = ((video[5] & 0x0F) << 8) | video[6]
    aspect_ratio_code = video[7] >> 4
    frame_rate_code = video[7] & 0x0F
    extension_offset = video.find(b"\x00\x00\x01\xb5", 8)
    if extension_offset < 0 or extension_offset + 9 > len(video):
        raise ValueError("video elementary stream lacks a complete MPEG-2 sequence extension")
    bits = int.from_bytes(video[extension_offset + 4:extension_offset + 8], "big")
    extension_id = bits >> 28
    if extension_id != 1:
        raise ValueError("first MPEG extension is not a sequence extension")
    rate_extension = video[extension_offset + 8]
    return {
        "codec": "MPEG-2 video",
        "width": width,
        "height": height,
        "aspect_ratio_code": aspect_ratio_code,
        "frame_rate_code": frame_rate_code,
        "frame_rate": "30000/1001" if frame_rate_code == 4 else None,
        "profile_and_level": (bits >> 20) & 0xFF,
        "progressive_sequence": (bits >> 19) & 1,
        "chroma_format": (bits >> 17) & 0x03,
        "horizontal_size_extension": (bits >> 15) & 0x03,
        "vertical_size_extension": (bits >> 13) & 0x03,
        "low_delay": rate_extension >> 7,
        "frame_rate_extension_n": (rate_extension >> 5) & 0x03,
        "frame_rate_extension_d": rate_extension & 0x1F,
    }


def _validate_video_profile(video: bytes) -> dict:
    profile = video_profile(video)
    expected = (640, 448, 2, 4, 0x48, 1, 1, 0, 0, 0, 0, 0)
    observed = (
        profile["width"], profile["height"], profile["aspect_ratio_code"],
        profile["frame_rate_code"], profile["profile_and_level"],
        profile["progressive_sequence"], profile["chroma_format"],
        profile["horizontal_size_extension"], profile["vertical_size_extension"],
        profile["low_delay"], profile["frame_rate_extension_n"],
        profile["frame_rate_extension_d"],
    )
    if observed != expected:
        raise ValueError(f"unsupported game movie video profile: {observed!r}")
    return profile


_COMPATIBLE_VIDEO_FIELDS = (
    "width", "height", "aspect_ratio_code", "frame_rate_code",
    "profile_and_level", "progressive_sequence", "chroma_format",
    "horizontal_size_extension", "vertical_size_extension", "low_delay",
    "frame_rate_extension_n", "frame_rate_extension_d",
)


def _validate_source(raw: bytes) -> dict:
    parsed = mpeg_ps.parse(raw)
    counts = parsed["packet_counts_by_stream_id"]
    if not counts.get("0xc0") or not counts.get("0xe0"):
        raise ValueError("movie lacks the observed ADX audio or MPEG video stream")
    if counts.get("0xbf") != 2:
        raise ValueError("movie does not contain the two observed CRI metadata packets")
    allowed = {"0xbb", "0xbe", "0xbf", "0xc0", "0xe0"}
    if set(counts) - allowed:
        raise ValueError("movie contains an unsupported program-stream ID")

    packet_ids_by_sector = defaultdict(list)
    private_packets = []
    for offset, size, kind, stream_id in parsed["segments"]:
        if kind != "packet":
            continue
        packet_ids_by_sector[offset // SECTOR_SIZE].append(stream_id)
        if stream_id == 0xBF:
            private_packets.append((offset, size, raw[offset + 6:offset + size]))
    expected_packets = {
        0: [0xBB, 0xBE],
        1: [0xBB, 0xBE],
        2: [0xBF],
        3: [0xBF, 0xBE],
    }
    if any(packet_ids_by_sector.get(sector) != ids
           for sector, ids in expected_packets.items()):
        raise ValueError("movie opening sectors do not match the observed SofDec profile")
    if b"SofdecStream" not in private_packets[0][2]:
        raise ValueError("first CRI metadata packet lacks its SofdecStream signature")
    if not private_packets[1][2].startswith(b"CRITAGS\0"):
        raise ValueError("second CRI metadata packet lacks the observed CRITAGS signature")

    streams = SFD.from_bytes(raw)
    video = streams.extract_video()
    audio = streams.extract_audio()
    profile = _validate_video_profile(video)
    if audio[0x11A:0x120] != b"(c)CRI":
        raise ValueError("ADX stream lacks the CRI signature")
    return {
        "parsed": parsed,
        "video": video,
        "audio": audio,
        "video_profile": profile,
        "video_sha256": hashlib.sha256(video).hexdigest(),
        "audio_sha256": hashlib.sha256(audio).hexdigest(),
        "metadata_prefix": raw[:SOURCE_PREFIX_BYTES],
    }


def extract(raw: bytes) -> dict:
    """Return editable MPEG-2 video and preserved CRI ADX source streams."""
    result = _validate_source(raw)
    return {
        "video": result["video"],
        "audio": result["audio"],
        "video_profile": result["video_profile"],
        "video_sha256": result["video_sha256"],
        "audio_sha256": result["audio_sha256"],
        "source_sha256": result["parsed"]["sha256"],
    }


class _GameSFD(SFD):
    """Use the upstream timestamp scheduler with this corpus's sector rules."""

    def __init__(self, video: bytes, audio: bytes, metadata_prefix: bytes):
        super().__init__(video, audio)
        if len(metadata_prefix) != SOURCE_PREFIX_BYTES:
            raise ValueError("movie metadata prefix must contain four sectors")
        self.metadata_prefix = metadata_prefix

    def _emit_video(self, fh, stream, scr_block, stream_id=_sfd.VIDEO_STREAM_ID):
        end = min(stream.pos + MAX_VIDEO_PACKET_PAYLOAD, len(stream.data))
        if end < len(stream.data):
            start = stream.data.find(
                PICTURE_START,
                max(stream.pos, end - 5),
                min(len(stream.data), end + len(PICTURE_START) - 1),
            )
            if start >= 0 and start < end:
                end = start
        if end <= stream.pos:
            raise ValueError(f"cannot place complete picture header at {stream.pos:#x}")

        chunk = stream.data[stream.pos:end]
        stream.pos = end
        first = chunk.find(PICTURE_START)
        if first < 0:
            fh.write(self._video_packet(
                scr_block=scr_block, payload=chunk, pts=0, dts=0,
                dts_type=4, stream_id=stream_id,
            ))
        else:
            if first + 6 > len(chunk):
                raise ValueError(f"incomplete MPEG picture header at {first:#x}")
            picture_type, temporal_reference = _sfd._parse_picture(chunk, first)
            pts = int((stream.pic_basic + temporal_reference) * stream.dts_basic)
            dts = int(stream.dts_forecast)
            dts_type = 3 if picture_type == 3 else 1
            fh.write(self._video_packet(
                scr_block=scr_block, payload=chunk, pts=pts, dts=dts,
                dts_type=dts_type, stream_id=stream_id,
            ))
            current = first
            while current >= 0:
                if current + 6 > len(chunk):
                    raise ValueError(f"incomplete MPEG picture header at {current:#x}")
                _, temporal_reference = _sfd._parse_picture(chunk, current)
                stream.pic_current += 1
                if temporal_reference > stream.pic_biggest:
                    stream.pic_biggest = temporal_reference
                if temporal_reference == 0:
                    stream.pic_basic += stream.pic_biggest + 1
                    stream.pic_current = stream.pic_basic
                stream.dts_forecast = stream.dts_basic * stream.pic_current
                current = chunk.find(PICTURE_START, current + 1)
        if stream.pos >= len(stream.data):
            stream.finished = True

    def _write_to(self, fh):
        opening = self._opening_blocks()
        fh.write(opening[:2 * SECTOR_SIZE])
        for block in (2, 3):
            sector = self.metadata_prefix[block * SECTOR_SIZE:(block + 1) * SECTOR_SIZE]
            pack = _sfd._pack_head(
                _sfd._scr_for_block(block, self.mux_rate), self.mux_rate,
            )
            fh.write(pack)
            fh.write(sector[len(_sfd.PACK_START) + 8:])
        self._main_loop(fh, 4)
        fh.write(self._closing_block())


def rebuild(raw: bytes, edited_video: bytes) -> bytes:
    """Re-multiplex an edited MPEG-2 stream with its original audio and CRI tags."""
    source = _validate_source(raw)
    edited_profile = _validate_video_profile(edited_video)
    baseline_profile = source["video_profile"]
    if any(edited_profile[field] != baseline_profile[field]
           for field in _COMPATIBLE_VIDEO_FIELDS):
        raise ValueError("edited video profile differs from the game's MPEG-2 profile")

    muxer = _GameSFD(edited_video, source["audio"], source["metadata_prefix"])
    output = io.BytesIO()
    muxer._write_to(output)
    rebuilt = output.getvalue()
    parsed = mpeg_ps.parse(rebuilt)
    if parsed["packet_counts_by_stream_id"].get("0xbf") != 2:
        raise ValueError("rebuilt movie lost a CRI metadata packet")
    for block in (2, 3):
        start = block * SECTOR_SIZE + 12
        end = (block + 1) * SECTOR_SIZE
        if rebuilt[start:end] != raw[start:end]:
            raise ValueError("rebuilt movie changed the preserved CRI metadata sectors")
    result = SFD.from_bytes(rebuilt)
    if result.extract_video() != edited_video:
        raise ValueError("rebuilt movie video stream differs from the edited source")
    if result.extract_audio() != source["audio"]:
        raise ValueError("rebuilt movie audio stream differs from the original")
    return rebuilt
