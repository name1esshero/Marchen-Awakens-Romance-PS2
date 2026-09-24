"""Characterize the boot ELF's `__tf*` (compiler-synthesized RTTI) linkonce
sections: their byte-size classes, the construct-on-first-use shape they all
share, and the base-class relationship each single-inheritance-shaped
function's own machine code reveals by calling another `__tf*` function.

This is disassembly evidence, not a claim about vtable layout or full
inheritance: it decodes exactly the `jal` (function-call) instructions each
`__tf*` function's own bytes contain, using the standard MIPS `jal` encoding
(opcode 6, 26-bit word-aligned target, top 4 bits taken from the delay slot's
own address), and records only calls whose target address falls inside
another `__tf*` section. Read-only; never mutates the reference input and
never writes to `preserved/boot/` or `config/camera_sections.txt`.
"""
import argparse
import json
import struct
from collections import Counter, defaultdict
from pathlib import Path

from bootstrap import elf_sections
from linkonce_inventory import classify

PREFIX = ".gnu.linkonce.t."
TF_MARKER = "__tf"


def jal_targets(code, base_address):
    """Every `jal` target address encoded in `code`, keyed by call-site address."""
    targets = {}
    for offset in range(0, len(code) - 3, 4):
        word = struct.unpack_from("<I", code, offset)[0]
        if word >> 26 == 0x03:
            call_site = base_address + offset
            field = word & 0x03FFFFFF
            targets[call_site] = ((call_site + 4) & 0xF0000000) | (field << 2)
    return targets


def typeinfo_sections(data):
    sections = elf_sections(data)["sections"]
    result = []
    for s in sections:
        if not s["name"].startswith(PREFIX) or s["size"] == 0:
            continue
        mangled = s["name"][len(PREFIX):]
        if not mangled.startswith(TF_MARKER):
            continue
        kind, cls, _ = classify(mangled)
        # `__tf<len><Name>` classifies cleanly; `__tft<...>` (a template
        # instantiation's type-info, e.g. `__tft12CStringStack1i_256_`) does
        # not match the plain-class shape and is kept under its raw mangled
        # suffix rather than silently dropped or misattributed.
        display_name = cls if kind == "typeinfo" else mangled[len(TF_MARKER):]
        result.append(dict(name=s["name"], address=s["address"], offset=s["offset"],
                            size=s["size"], class_name=display_name))
    result.sort(key=lambda s: s["address"])
    return result


def analyze(data):
    tf_sections = typeinfo_sections(data)
    addr_to_section = {s["address"]: s for s in tf_sections}
    by_addr_range = sorted(tf_sections, key=lambda s: s["address"])

    def owning_section(addr):
        # Sections are non-overlapping and sorted by address; a linear scan
        # is fine at this scale (under 500 entries) and keeps this file free
        # of a second, easy-to-get-wrong interval-search implementation.
        for s in by_addr_range:
            if s["address"] <= addr < s["address"] + s["size"]:
                return s
        return None

    edges = []
    roots = []
    helper_calls = defaultdict(list)
    for s in tf_sections:
        code = data[s["offset"]:s["offset"] + s["size"]]
        calls = jal_targets(code, s["address"])
        bases = []
        for target in calls.values():
            owner = owning_section(target)
            if owner is not None and owner["address"] != s["address"]:
                bases.append(owner)
            elif owner is None:
                helper_calls[s["size"]].append(target)
        if bases:
            for base in bases:
                edges.append(dict(class_name=s["class_name"], base_class=base["class_name"],
                                   size=s["size"]))
        else:
            roots.append(dict(class_name=s["class_name"], size=s["size"]))

    size_histogram = Counter(s["size"] for s in tf_sections)
    helper_by_size = {size: sorted(set(hex(a) for a in addrs))
                       for size, addrs in sorted(helper_calls.items())}
    fanout = Counter(e["base_class"] for e in edges)

    return dict(
        section_count=len(tf_sections),
        size_histogram=dict(sorted(size_histogram.items())),
        root_count=len(roots),
        edge_count=len(edges),
        helper_call_targets_by_size=helper_by_size,
        roots=sorted(roots, key=lambda r: r["class_name"]),
        edges=sorted(edges, key=lambda e: e["class_name"]),
        base_class_fanout=fanout.most_common(),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf", type=Path)
    args = parser.parse_args()
    report = analyze(args.elf.read_bytes())
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
