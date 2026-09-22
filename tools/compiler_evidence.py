"""Report literal compiler banners and their preceding strings from an ELF.

Reports observations only, without treating library strings as whole-game
compiler provenance. Output goes to stdout; input is read-only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

from bootstrap import elf_sections


def evidence(data):
    metadata = elf_sections(data)
    findings = []
    for match in re.finditer(rb'Append: GCC[0-9]+ SCE[0-9]+\n\x00', data):
        start = match.start()
        end = start - 1
        if end < 0 or data[end] != 0:
            raise ValueError('banner is not preceded by a terminated string')
        previous = data.rfind(b'\0', 0, end) + 1
        containing = [s for s in metadata['sections'] if s['type'] != 8
                      and s['offset'] <= start < s['offset'] + s['size']]
        findings.append(dict(offset=start, banner=match.group()[:-1].decode('ascii'),
                             preceding_string=data[previous:end].decode('ascii'),
                             sections=[s['name'] for s in containing]))
    return dict(sha256=hashlib.sha256(data).hexdigest(), banners=findings,
                interpretation='Literal library build labels; not proof of the game compiler identity')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf', type=Path)
    args = parser.parse_args()
    print(json.dumps(evidence(args.elf.read_bytes()), indent=2))
