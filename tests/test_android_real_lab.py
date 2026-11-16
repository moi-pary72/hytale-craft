"""Synthetic inputs only. No network or game data in CI."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts.android_real_lab import backup, restore, read_backup, download, NAMES

class AndroidRestore(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.spec = {'files': {}}
        for name in NAMES:
            raw = json.dumps({'synthetic': name}).encode()
            (self.source / name).write_bytes(raw)
            self.spec['files'][name] = {'sha256': hashlib.sha256(raw).hexdigest(), 'url': 'https://hysphere.app/data/v1/' + name}

    def test_backup_restore_offline_and_existing_bytes_preserved(self):
        archive = self.root / 'backup.zip'
        backup(self.source, archive, self.spec)
        recovered = self.root / 'restored'
        restore(archive, recovered, self.spec)
        for name in NAMES:
            self.assertEqual((recovered / name).read_bytes(), (self.source / name).read_bytes())
        with self.assertRaises(ValueError):
            restore(archive, self.source, self.spec)
        (self.source / 'items.json').write_text('{}')
        with self.assertRaises(ValueError):
            backup(self.source, archive, self.spec)
        self.assertEqual(len(read_backup(archive, self.spec)), 3)

    def test_failed_download_never_installs_partial_source(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def geturl(self): return 'https://hysphere.app/data/v1/items.json'
            def read(self, size): return b'{}'
        destination = self.root / 'downloaded'
        with patch('urllib.request.urlopen', return_value=Response()):
            with self.assertRaises(ValueError):
                download(destination, self.spec)
        self.assertFalse(destination.exists())

if __name__ == '__main__':
    unittest.main()
