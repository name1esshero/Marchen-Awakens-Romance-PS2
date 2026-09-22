"""Stage the historical i386 compiler and probe on a native temporary filesystem.

The legacy tools fail to stat large-inode files on this workspace's Windows
mount. Staging changes host paths only, not source content or compiler flags.
No inputs are modified; output is written only after successful compilation.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', type=Path, default=Path('.tools/ee-gcc2.96'))
    parser.add_argument('--sources', type=Path, default=Path('candidates/ee_camera'))
    parser.add_argument('--config', type=Path, default=Path('config/ee_compiler.json'))
    parser.add_argument('--output', type=Path, default=Path('build/ee_camera.o'))
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    with tempfile.TemporaryDirectory(prefix='marps2-ee-probe-') as name:
        temporary = Path(name)
        shutil.copytree(args.compiler, temporary / 'compiler')
        shutil.copytree(args.sources, temporary / 'source')
        compiler = temporary / 'compiler/bin/ee-gcc'
        subprocess.run([str(compiler), *config['probe_flags'], '-c', 'probe.cpp', '-o', 'probe.o'],
                       cwd=temporary / 'source', check=True)
        data = (temporary / 'source/probe.o').read_bytes()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(f"Compiled EE candidate with {config['version']} {config['probe_flags']}; native temporary staging")


if __name__ == '__main__':
    main()
