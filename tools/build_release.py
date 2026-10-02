"""Build an explicit, scripts-free release ZIP with fixed entry metadata."""
import argparse
import json
import os
import stat
import tempfile
import zipfile
from pathlib import Path

from validate import ROOT, RELEASE_FILES, validate_tree, validate_archive, sha, require


def build(output, root=ROOT):
    root = Path(root).resolve()
    report = validate_tree(root)
    output = Path(output).absolute()
    require(output.resolve().is_relative_to(root / 'dist'), 'output_must_be_inside_dist')
    for path in [output, *output.parents]:
        if path == root:
            break
        require(not path.is_symlink() and not (path.exists() and getattr(path.lstat(), 'st_file_attributes', 0) & 0x400), 'output_reparse')
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f'practical-work-kit-{report["version"]}.zip'
    # Fresh exclusive temp files prevent a pre-existing hardlink/symlink from being written through.
    fd, temp_name = tempfile.mkstemp(prefix='.release-', suffix='.zip', dir=output)
    os.close(fd)
    temp_archive = Path(temp_name)
    checksum_temp = None
    try:
        with zipfile.ZipFile(temp_archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for rel in sorted(RELEASE_FILES):
                info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(info, (root / rel).read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        result = validate_archive(temp_archive, root)
        digest = sha(temp_archive.read_bytes())
        fd, checksum_name = tempfile.mkstemp(prefix='.checksums-', suffix='.txt', dir=output)
        checksum_temp = Path(checksum_name)
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(f'{digest}  {archive.name}\n')
        os.replace(temp_archive, archive)
        os.replace(checksum_temp, output / 'SHA256SUMS.txt')
    finally:
        temp_archive.unlink(missing_ok=True)
        if checksum_temp is not None:
            checksum_temp.unlink(missing_ok=True)
    # Deterministic bytes within the same Python/zlib environment, not a cross-version promise.
    return {**result, 'archive': archive.name, 'bytes': archive.stat().st_size}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    if not args.output.is_absolute():
        args.output = ROOT / args.output
    print(json.dumps(build(args.output)))
