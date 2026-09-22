"""Census the boot ELF's named `.gnu.linkonce.t.*` sections by best-effort
GNU-v2/cfront mangled-name shape. Read-only; never mutates the reference input.

This is a naming-shape heuristic, not a demangler and not a semantic recovery
tool. It classifies a section name into a coarse kind (member function,
constructor, destructor, type-info thunk, or unparsed) and, where the shape
exposes one, a class name and the leftover (unparsed) encoded suffix. It does
not validate that the extracted class name is correct C++, does not decode
parameter/return types, and never inspects instruction bytes.
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

from bootstrap import elf_sections

PREFIX = ".gnu.linkonce.t."

# `Method__C<len><Class><encoded-params>` (const member) or without the `C`.
_MEMBER = re.compile(r"^(?P<func>[A-Za-z_][A-Za-z0-9_]*)__(?P<const>C)?"
                     r"(?P<len>[1-9][0-9]*)(?P<tail>.*)$", re.DOTALL)
# `__tf<len><Class>`: compiler-synthesized type-info accessor for a class.
_TYPEINFO = re.compile(r"^__tf(?P<len>[1-9][0-9]*)(?P<tail>.*)$", re.DOTALL)
# `__<len><Class><encoded-params>`: constructor (function name == class name).
_CTOR = re.compile(r"^__(?P<len>[1-9][0-9]*)(?P<tail>.*)$", re.DOTALL)
# `_$_<len><Class>`: destructor.
_DTOR = re.compile(r"^_\$_(?P<len>[1-9][0-9]*)(?P<tail>.*)$", re.DOTALL)


def classify(mangled):
    """Return (kind, class_name_or_None, extra_dict) for one linkonce name."""
    m = _MEMBER.match(mangled)
    if m and len(m.group("tail")) >= int(m.group("len")):
        length = int(m.group("len"))
        tail = m.group("tail")
        cls, rest = tail[:length], tail[length:]
        if cls[:1].isalpha() or cls[:1] == "_":
            kind = "const_member" if m.group("const") else "member"
            return kind, cls, {"method": m.group("func"), "raw_params": rest}

    m = _TYPEINFO.match(mangled)
    if m and len(m.group("tail")) >= int(m.group("len")):
        length = int(m.group("len"))
        cls = m.group("tail")[:length]
        if cls[:1].isalpha() or cls[:1] == "_":
            return "typeinfo", cls, {}

    m = _DTOR.match(mangled)
    if m and len(m.group("tail")) >= int(m.group("len")):
        length = int(m.group("len"))
        cls = m.group("tail")[:length]
        if cls[:1].isalpha() or cls[:1] == "_":
            return "destructor", cls, {}

    m = _CTOR.match(mangled)
    if m and len(m.group("tail")) >= int(m.group("len")):
        length = int(m.group("len"))
        tail = m.group("tail")
        cls, rest = tail[:length], tail[length:]
        if cls[:1].isalpha() or cls[:1] == "_":
            return "constructor", cls, {"raw_params": rest}

    return "unparsed", None, {}


def inventory(data):
    sections = elf_sections(data)["sections"]
    linkonce = [s for s in sections if s["name"].startswith(PREFIX) and s["size"] > 0]
    linkonce.sort(key=lambda s: s["address"])
    entries = []
    for s in linkonce:
        mangled = s["name"][len(PREFIX):]
        kind, cls, extra = classify(mangled)
        entry = dict(name=s["name"], address=s["address"], offset=s["offset"],
                     size=s["size"], sha256=s["sha256"], kind=kind, class_name=cls)
        entry.update(extra)
        entries.append(entry)

    by_class = Counter(e["class_name"] for e in entries if e["class_name"])
    by_kind = Counter(e["kind"] for e in entries)
    size_histogram = Counter(e["size"] for e in entries)
    return dict(
        section_count=len(entries),
        total_bytes=sum(e["size"] for e in entries),
        address_range=[linkonce[0]["address"], linkonce[-1]["address"] + linkonce[-1]["size"]]
        if linkonce else None,
        by_kind=dict(sorted(by_kind.items())),
        classes_observed=len(by_class),
        top_classes_by_section_count=by_class.most_common(20),
        size_histogram=dict(sorted(size_histogram.items())),
        sections=entries,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf", type=Path)
    args = parser.parse_args()
    report = inventory(args.elf.read_bytes())
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
