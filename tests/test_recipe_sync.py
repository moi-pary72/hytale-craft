"""Synthetic contract fixtures; no invented data goes into the published catalog."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from scripts.sync_recipes import normalize, write_snapshot, LICENSE

class RecipeSyncTests(unittest.TestCase):
    def source(self):
        manifest={'contract':'sphere-data/v1','license':{'url':LICENSE},'game':{'version':'fixture'},'extractedAt':'2026-01-01','revision':'fixture','datasets':[{'id':'items','recordCount':2},{'id':'recipes','recordCount':1}]}
        common={'contract':'sphere-data/v1','extractedAt':'2026-01-01','gameVersion':'fixture'}
        items={**common,'count':2,'items':[{'id':'A'},{'id':'R'}]}
        recipes={**common,'count':1,'recipes':[{'id':'test','kind':'craft','inputs':[{'itemId':'R','quantity':2}],'outputs':[{'itemId':'A','quantity':1}],'benches':[]}]}
        return manifest,items,recipes
    def test_no_missing_ingredient_fallback(self):
        m,i,r=self.source();r['recipes'][0]['inputs'][0].pop('itemId')
        with self.assertRaises(ValueError):normalize(m,i,r,{})
    def test_revision_license_and_counts(self):
        for field in ('date','license','count'):
            m,i,r=self.source()
            if field=='date':r['extractedAt']='different'
            elif field=='license':m['license']['url']='unknown'
            else:r['count']=2
            with self.assertRaises(ValueError):normalize(m,i,r,{})
    def test_snapshot_determinism_and_backup(self):
        d=normalize(*self.source(),{})
        with tempfile.TemporaryDirectory() as p:
            self.assertTrue(write_snapshot(d,Path(p)))
            self.assertFalse(write_snapshot(d,Path(p)))
            d['source']['revision']='fixture2'
            self.assertTrue(write_snapshot(d,Path(p)))
            self.assertTrue(list(Path(p).glob('*.previous.json')))
    def test_no_active_community_snapshot(self):
        root=Path('data/recipes');m=json.loads((root/'manifest.json').read_text())
        self.assertIsNone(m['path']);self.assertIsNone(m['sha256']);self.assertIsNone(m['active'])
        self.assertFalse((root/'hysphere-2026-08-12.json').exists())
    def test_network_collection_disabled(self):
        from scripts.sync_recipes import fetch
        from scripts.sync_catalog import fetch as fetch_catalog
        from unittest.mock import patch
        with patch('subprocess.run') as network:
            for fn in (fetch,fetch_catalog):
                with self.assertRaises(PermissionError):fn('anything')
            network.assert_not_called()
