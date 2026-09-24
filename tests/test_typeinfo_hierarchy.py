import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from typeinfo_hierarchy import analyze, jal_targets


def elf(sections):
    """Minimal ELF32 with one PROGBITS section per (name, code, address) triple.

    A section's load address is independent of its file offset, exactly as
    in the real linked boot ELF, so callers pick addresses to suit their
    `jal` targets without worrying about layout.
    """
    header_size = 52
    section_header_size = 40
    section_count = 1 + len(sections) + 1  # null + real sections + shstrtab
    data_offset = (header_size + section_count * section_header_size + 7) & ~7

    names = bytearray(b'\0')
    name_offsets = []
    for name, _, _ in sections:
        name_offsets.append(len(names))
        names += name.encode() + b'\0'
    shstrtab_name_offset = len(names)
    names += b'.shstrtab\0'

    file_offsets = []
    body = bytearray()
    for _, code, _ in sections:
        file_offsets.append(data_offset + len(body))
        body += code
    names_offset = data_offset + len(body)

    data = bytearray(names_offset + len(names))
    data[:7] = b'\x7fELF\x01\x01\x01'
    struct.pack_into('<HHIIIIIHHHHHH', data, 16,
                      1, 8, 1, 0, 0, header_size, 0, header_size,
                      0, 0, section_header_size, section_count, section_count - 1)
    data[data_offset:data_offset + len(body)] = body
    data[names_offset:names_offset + len(names)] = names

    for i, (_, code, address) in enumerate(sections):
        header_offset = header_size + (i + 1) * section_header_size
        struct.pack_into('<10I', data, header_offset,
                          name_offsets[i], 1, 6, address, file_offsets[i],
                          len(code), 0, 0, 4, 0)
    shstrtab_index = section_count - 1
    struct.pack_into('<10I', data, header_size + shstrtab_index * section_header_size,
                      shstrtab_name_offset, 3, 0, 0, names_offset, len(names), 0, 0, 1, 0)
    return bytes(data)


def jal(call_site_address, target_address):
    field = (target_address >> 2) & 0x03FFFFFF
    return struct.pack('<I', (0x03 << 26) | field)


NOP = b'\x00\x00\x00\x00'


class TypeinfoHierarchyTests(unittest.TestCase):
    def test_jal_target_matches_known_boot_elf_bytes(self):
        # `.gnu.linkonce.t.__tf7CCamera` at 0x33af6c calls
        # `.gnu.linkonce.t.__tf9C3dObject` at 0x33b744 in the real boot ELF;
        # this is the exact encoded word, used as a real-world regression
        # anchor independent of the synthetic ELF builder below.
        code = bytes.fromhex('d1ed0c0c')
        targets = jal_targets(code, 0x33af6c)
        self.assertEqual(targets, {0x33af6c: 0x33b744})

    def test_root_class_has_no_base_when_call_targets_a_non_tf_helper(self):
        parent_addr = 0x1000
        helper_addr = 0x9000
        parent_code = NOP + jal(parent_addr + 4, helper_addr) + NOP
        data = elf([('.gnu.linkonce.t.__tf6Parent', parent_code, parent_addr)])
        report = analyze(data)
        self.assertEqual(report['root_count'], 1)
        self.assertEqual(report['edge_count'], 0)
        self.assertEqual(report['roots'][0]['class_name'], 'Parent')

    def test_single_base_edge_from_a_call_into_another_tf_section(self):
        parent_addr = 0x1000
        parent_code = NOP * 4
        child_addr = 0x2000
        helper_addr = 0x9000
        child_code = jal(child_addr, parent_addr) + jal(child_addr + 4, helper_addr)
        data = elf([('.gnu.linkonce.t.__tf6Parent', parent_code, parent_addr),
                    ('.gnu.linkonce.t.__tf5Child', child_code, child_addr)])
        report = analyze(data)
        self.assertEqual(report['root_count'], 1)
        self.assertEqual(report['edge_count'], 1)
        self.assertEqual(report['edges'][0], {'class_name': 'Child', 'base_class': 'Parent', 'size': 8})

    def test_template_instantiation_typeinfo_keeps_raw_suffix_not_none(self):
        parent_addr = 0x1000
        parent_code = NOP * 4
        template_addr = 0x2000
        template_code = jal(template_addr, parent_addr)
        data = elf([('.gnu.linkonce.t.__tf6Parent', parent_code, parent_addr),
                    ('.gnu.linkonce.t.__tft8Templ1i_4_', template_code, template_addr)])
        report = analyze(data)
        self.assertEqual(report['edge_count'], 1)
        edge = report['edges'][0]
        self.assertEqual(edge['base_class'], 'Parent')
        self.assertEqual(edge['class_name'], 't8Templ1i_4_')


if __name__ == '__main__':
    unittest.main()
