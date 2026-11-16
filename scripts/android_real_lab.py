#!/usr/bin/env python3
"""Personal, loopback-only Android lab. Never uploads data or starts a tunnel."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import urllib.request
import zipfile

try:
    from verify_real_data_lab import verify, ROOT, base
    from serve_real_data_lab import make_server
except ModuleNotFoundError:
    from scripts.verify_real_data_lab import verify, ROOT, base
    from scripts.serve_real_data_lab import make_server

SPEC = ROOT / 'docs/stage18/RESTORE_MANIFEST.json'
PRIVATE = ROOT / '.private/android'
NAMES = {'manifest.json', 'items.json', 'recipes.json'}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def checked(raw, name, spec):
    if len(raw) > base.MAX_BYTES or digest(raw) != spec['files'][name]['sha256']:
        raise ValueError('Pinned export changed or is invalid: ' + name + '. Existing data preserved.')
    base.strict_json(raw)
    return raw


def download(destination, spec):
    """Only documented exports; all verified before any file is installed."""
    if destination.exists():
        raise ValueError('Refusing to replace an existing source directory')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as tmp:
        stage = Path(tmp) / 'source'
        stage.mkdir(mode=0o700)
        for name in sorted(NAMES):
            url = spec['files'][name]['url']
            if url != 'https://hysphere.app/data/v1/' + name:
                raise ValueError('Unexpected export URL')
            request = urllib.request.Request(url, headers={'User-Agent': 'HytaleCraft-PersonalResearch/1.0'})
            with urllib.request.urlopen(request, timeout=60) as response:
                if response.geturl() != url:
                    raise ValueError('Export redirect requires review')
                raw = response.read(base.MAX_BYTES + 1)
            path = stage / name
            path.write_bytes(checked(raw, name, spec))
            path.chmod(0o600)
        stage.rename(destination)


def backup(source, archive, spec):
    """Actual data backup, local only; read back each member before promotion."""
    payload = {name: checked((source / name).read_bytes(), name, spec) for name in NAMES}
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        read_backup(archive, spec)
        return
    temporary = archive.with_suffix('.tmp')
    try:
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as z:
            for name, raw in sorted(payload.items()):
                z.writestr(name, raw)
        temporary.chmod(0o600)
        read_backup(temporary, spec)
        temporary.replace(archive)
    finally:
        temporary.unlink(missing_ok=True)


def read_backup(archive, spec):
    with zipfile.ZipFile(archive) as z:
        if set(z.namelist()) != NAMES or len(z.infolist()) != 3:
            raise ValueError('Unexpected backup members')
        if any(i.file_size > base.MAX_BYTES for i in z.infolist()):
            raise ValueError('Oversized backup')
        return {name: checked(z.read(name), name, spec) for name in NAMES}


def restore(archive, destination, spec):
    payload = read_backup(archive, spec)
    if destination.exists():
        raise ValueError('Restore requires an empty destination; existing files preserved')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as tmp:
        stage = Path(tmp) / 'source'
        stage.mkdir(mode=0o700)
        for name, raw in payload.items():
            p = stage / name
            p.write_bytes(raw)
            p.chmod(0o600)
        stage.rename(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download-open-export', action='store_true', help='Personal noncommercial research only; accepts documented source conditions')
    parser.add_argument('--restore', type=Path, help='Restore a local private data ZIP, never a public URL')
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    os.umask(0o077)
    spec = base.strict_json(SPEC.read_bytes())
    source = PRIVATE / 'source'
    archive = PRIVATE / 'backup/hysphere-pinned-private.zip'
    PRIVATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not source.exists():
        if args.restore:
            restore(args.restore, source, spec)
        elif archive.exists():
            restore(archive, source, spec)
        elif args.download_open_export:
            print('Downloading documented exports directly to this device for personal research.', flush=True)
            download(source, spec)
        else:
            parser.error('No local data. Use --download-open-export only for permitted personal noncommercial research.')
    verify(source)
    backup(source, archive, spec)
    # Fresh code-specific build: never reuse stale UI or overwrite an old research build.
    output = Path(tempfile.mkdtemp(prefix='build-', dir=PRIVATE))
    output.rmdir()
    try:
        report = verify(source, output=output)
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise
    (PRIVATE / 'last-verification.json').write_text(json.dumps({**report, 'local_data_backup': str(archive), 'backup_sha256': digest(archive.read_bytes())}, indent=2))
    print('Verified: 3219 items; 638 structural methods; 1471 quarantined records. Two self-input methods remain blocked.')
    print('Local private DATA backup:', archive)
    print('Quarantine and original records remain in the private source/build; no cloud upload.')
    if args.prepare_only:
        print('Build:', output)
        return
    server = make_server(output, 8765)
    print('Open Chrome ON THIS DEVICE: http://127.0.0.1:8765/\nKeep Termux running. Ctrl+C stops access. Same address preserves browser state.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
