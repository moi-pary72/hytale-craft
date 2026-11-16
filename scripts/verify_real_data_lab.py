#!/usr/bin/env python3
"""Verify locally authorized exports and optionally reproduce the pinned research bundle. Offline only."""
import argparse,hashlib,json
from pathlib import Path
try:from build_real_data_lab import build,ROOT,base
except ModuleNotFoundError:from scripts.build_real_data_lab import build,ROOT,base

def verify(input_dir,manifest=None,output=None):
 manifest=manifest or ROOT/'docs/stage18/RESTORE_MANIFEST.json';spec=base.strict_json(Path(manifest).read_bytes());inp=base.private_path(input_dir,ROOT);checks={}
 if set(spec['files'])!={'manifest.json','items.json','recipes.json'}:raise ValueError('Unexpected restore inputs')
 for name,meta in spec['files'].items():
  p=inp/name
  if p.is_symlink() or p.stat().st_size>base.MAX_BYTES:raise ValueError('Unsafe restore input')
  actual=hashlib.sha256(p.read_bytes()).hexdigest()
  if actual!=meta['sha256']:raise ValueError('Restore source checksum mismatch: '+name)
  checks[name]=actual
 report={'raw_integrity':True,'source_revision':spec['source_revision'],'exact_game_build':None,'raw_sha256':checks,'private_only':True,'permanent_data_backup':False}
 if output is not None:
  result=build(inp,output,True,normalized_on=spec['normalization_date'])
  if result['dataset_sha256']!=spec['normalized_data_sha256']:raise ValueError('Reproduced dataset differs; investigate without replacing preserved snapshots')
  if result['metrics']!=spec['metrics']:raise ValueError('Reproduced metrics differ')
  report.update(rebuilt=True,dataset_sha256=result['dataset_sha256'],metrics=result['metrics'])
 return report
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--manifest',type=Path);p.add_argument('--rebuild',type=Path);a=p.parse_args();print(json.dumps(verify(a.input,a.manifest,a.rebuild),indent=2))
