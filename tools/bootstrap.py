"""Read-only ISO research; explicit extraction into a separate output directory.

Supports single-volume, contiguous ISO9660 files and ELF32 little-endian.
Rejects extended attributes, interleaving, multi-extents and directory cycles.
This is not a disc rebuilder or a general-purpose filesystem implementation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

SECTOR = 2048


def read_at(stream, offset, size):
    if offset < 0 or size < 0:
        raise ValueError("negative extent")
    stream.seek(offset)
    data = stream.read(size)
    if len(data) != size:
        raise ValueError("truncated extent")
    return data


def dual(data, offset, width):
    a = int.from_bytes(data[offset:offset + width], "little")
    b = int.from_bytes(data[offset + width:offset + 2 * width], "big")
    if a != b:
        raise ValueError("inconsistent dual-endian field")
    return a


def record(data):
    if len(data) < 34 or data[0] != len(data) or 33 + data[32] > len(data):
        raise ValueError("invalid directory record")
    if data[1] or data[26] or data[27] or data[25] & 0x80:
        raise ValueError("unsupported extended/interleaved/multi-extent record")
    if dual(data, 28, 2) != 1:
        raise ValueError("unsupported volume sequence")
    return dual(data, 2, 4), dual(data, 10, 4), data[25], data[33:33 + data[32]]


def inventory(stream, image_size):
    pvd = None
    for sector in range(16, min(image_size // SECTOR, 256)):
        data = read_at(stream, sector * SECTOR, SECTOR)
        if data[1:7] != b"CD001\x01":
            raise ValueError("invalid ISO volume descriptor")
        if data[0] == 1:
            pvd = data
        if data[0] == 255:
            break
    else:
        raise ValueError("missing volume descriptor terminator")
    if pvd is None or dual(pvd, 128, 2) != SECTOR:
        raise ValueError("missing PVD or unsupported block size")
    volume_size = dual(pvd, 80, 4) * SECTOR
    if volume_size > image_size:
        raise ValueError("volume exceeds image")
    if dual(pvd, 120, 2) != 1 or dual(pvd, 124, 2) != 1:
        raise ValueError("unsupported multi-volume image")
    entries, seen, paths = [], set(), set()

    def walk(lba, size, parent):
        if lba in seen:
            raise ValueError("directory cycle or alias")
        seen.add(lba)
        if lba * SECTOR + size > volume_size:
            raise ValueError("directory outside volume")
        data = read_at(stream, lba * SECTOR, size)
        pos = 0
        while pos < size:
            length = data[pos]
            if not length:
                pos = (pos // SECTOR + 1) * SECTOR
                continue
            if pos % SECTOR + length > SECTOR:
                raise ValueError("record crosses sector")
            block, count, flags, name = record(data[pos:pos + length])
            pos += length
            if name in (b"\0", b"\1"):
                continue
            name = name.decode("ascii")
            if name in (".", "..") or any(c in name for c in "/\\:"):
                raise ValueError("unsafe ISO name")
            path = parent + name
            if path in paths or block * SECTOR + count > volume_size:
                raise ValueError("duplicate path or extent outside volume")
            paths.add(path)
            item = dict(path=path, lba=block, size=count, directory=bool(flags & 2))
            entries.append(item)
            if flags & 2:
                walk(block, count, path + "/")
            else:
                item["prefix_hex"] = read_at(stream, block * SECTOR, min(count, 16)).hex()

    root = record(pvd[156:156 + pvd[156]])
    walk(root[0], root[1], "")
    return dict(system_id=pvd[8:40].decode("ascii").strip(),
                volume_id=pvd[40:72].decode("ascii").strip(),
                volume_bytes=volume_size, image_bytes=image_size, entries=entries)


def elf_sections(data):
    if len(data) < 52 or data[:7] != b"\x7fELF\x01\x01\x01":
        raise ValueError("expected ELF32 little-endian")
    h = struct.unpack_from("<HHIIIIIHHHHHH", data, 16)
    if h[10] != 40 or h[11] == 0 or h[12] >= h[11]:
        raise ValueError("unsupported ELF section table")
    if h[5] + h[11] * 40 > len(data):
        raise ValueError("truncated ELF section table")
    sections = [struct.unpack_from("<10I", data, h[5] + i * 40) for i in range(h[11])]
    for s in sections:
        if s[1] != 8 and s[4] + s[5] > len(data):
            raise ValueError("ELF section outside file")
    strings = sections[h[12]]
    names = data[strings[4]:strings[4] + strings[5]]
    result = []
    for i, s in enumerate(sections):
        end = names.find(b"\0", s[0])
        if s[0] >= len(names) or end < 0:
            raise ValueError("invalid section name")
        item = dict(index=i, name=names[s[0]:end].decode("ascii"), type=s[1],
                    flags=s[2], address=s[3], offset=s[4], size=s[5], alignment=s[8])
        if s[1] != 8:
            item["sha256"] = hashlib.sha256(data[s[4]:s[4] + s[5]]).hexdigest()
        result.append(item)
    return dict(machine=h[1], entry=h[3], flags=h[6], sections=result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--reports", type=Path, default=Path("reports"))
    parser.add_argument("--extract", type=Path, help="explicitly extract files <=16 MiB")
    args = parser.parse_args()
    with args.image.open("rb") as stream:
        manifest = inventory(stream, args.image.stat().st_size)
        stream.seek(0)
        manifest["sha256"] = hashlib.file_digest(stream, "sha256").hexdigest()
        args.reports.mkdir(parents=True, exist_ok=True)
        for item in manifest["entries"]:
            if item["directory"] or item["size"] > 16 * 1024 * 1024:
                continue
            data = read_at(stream, item["lba"] * SECTOR, item["size"])
            item["sha256"] = hashlib.sha256(data).hexdigest()
            if args.extract:
                output = args.extract / item["path"]
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(data)
            if data.startswith(b"\x7fELF"):
                report = elf_sections(data)
                report["iso_path"] = item["path"]
                report["sha256"] = item["sha256"]
                filename = item["path"].replace("/", "_") + ".elf.json"
                (args.reports / filename).write_text(json.dumps(report, indent=2) + "\n")
        (args.reports / "disc.json").write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"SHA256 {manifest['sha256']}; {len(manifest['entries'])} entries")


if __name__ == "__main__":
    main()
