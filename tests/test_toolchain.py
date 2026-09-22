import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import run_ee_probe
import setup_ee_compiler
from compiler_evidence import evidence
from test_bootstrap import elf


class ToolchainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def archive(self, name='bin/ee-gcc'):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w:xz') as archive:
            info = tarfile.TarInfo(name)
            info.size = 4
            info.mode = 0o755
            archive.addfile(info, io.BytesIO(b'tool'))
        return stream.getvalue()

    def install(self, data, expected=None):
        config = self.root / 'config.json'
        config.write_text(json.dumps(dict(url='https://example.invalid/compiler',
                                         version='test', archive_size=len(data),
                                         sha256=expected or hashlib.sha256(data).hexdigest())))
        argv = ['setup', '--config', str(config), '--destination', str(self.root / 'installed')]
        with patch.object(sys, 'argv', argv), patch('urllib.request.urlopen', return_value=io.BytesIO(data)):
            setup_ee_compiler.main()

    def test_pinned_install_and_no_overwrite(self):
        data = self.archive()
        self.install(data)
        self.assertEqual((self.root / 'installed/bin/ee-gcc').read_bytes(), b'tool')
        with self.assertRaises(ValueError):
            self.install(data)

    def test_archive_hash_mismatch(self):
        with self.assertRaises(ValueError):
            self.install(self.archive(), '0' * 64)
        self.assertFalse((self.root / 'installed').exists())

    def test_archive_path_escape(self):
        with self.assertRaises(tarfile.FilterError):
            self.install(self.archive('../escape'))
        self.assertFalse((self.root / 'escape').exists())

    def test_compile_stages_unchanged_source_and_flags(self):
        compiler = self.root / 'compiler'
        (compiler / 'bin').mkdir(parents=True)
        (compiler / 'bin/ee-gcc').write_bytes(b'tool')
        source = self.root / 'sources'
        source.mkdir()
        (source / 'probe.cpp').write_text('int example;\n')
        config = self.root / 'config.json'
        config.write_text(json.dumps(dict(version='test', probe_flags=['-O2'])))
        output = self.root / 'probe.o'

        def compile_fake(command, cwd, check):
            self.assertEqual(Path(command[0]).read_bytes(), b'tool')
            self.assertNotEqual(Path(command[0]), compiler / 'bin/ee-gcc')
            self.assertEqual(command[1:], ['-O2', '-c', 'probe.cpp', '-o', 'probe.o'])
            self.assertNotEqual(cwd, source)
            self.assertEqual((cwd / 'probe.cpp').read_text(), 'int example;\n')
            self.assertTrue(check)
            (cwd / 'probe.o').write_bytes(b'object')

        argv = ['probe', '--compiler', str(compiler), '--sources', str(source),
                '--config', str(config), '--output', str(output)]
        with patch.object(sys, 'argv', argv), patch('subprocess.run', side_effect=compile_fake):
            run_ee_probe.main()
        self.assertEqual(output.read_bytes(), b'object')

    def test_compiler_banner_context_and_offsets(self):
        data = bytes(elf()) + b'\0\nLibrary Build:example\n\0Append: GCC2096 SCE3020\n\0'
        result = evidence(data)
        self.assertEqual(result['banners'][0]['preceding_string'], '\nLibrary Build:example\n')
        self.assertEqual(result['banners'][0]['offset'], data.index(b'Append:'))
        self.assertEqual(evidence(elf())['banners'], [])


if __name__ == '__main__':
    unittest.main()
