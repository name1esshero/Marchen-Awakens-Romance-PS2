"""Build in a temporary tree containing only the declared source inputs.

No ISO, extracted references, existing objects, compiler cache or reports are
copied. The parent process compares the resulting ELF hash to config/boot.sha256.
This checks the current bootstrap target, not a full-disc source-only build.
"""
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parents[1]
    expected = (root / 'config/boot.sha256').read_text().split()[0]
    with tempfile.TemporaryDirectory(prefix='marps2-source-only-') as name:
        target = Path(name)
        for directory in ('preserved/boot', 'asm'):
            shutil.copytree(root / directory, target / directory)
        (target / 'tools').mkdir()
        for path in ('Makefile', 'graphics_rules.mk',
                     'tools/bootstrap.py', 'tools/reconstruct_elf.py'):
            shutil.copy2(root / path, target / path)
        subprocess.run(['make', '--no-print-directory', 'build-boot'], cwd=target, check=True)
        actual = hashlib.sha256((target / 'build/SLPM_661.56').read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'source-only rebuild mismatch: {actual}')
    print('PASS: isolated source-only boot rebuild matches the pinned reference hash')


if __name__ == '__main__':
    main()
