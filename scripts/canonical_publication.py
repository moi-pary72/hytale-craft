"""Reviewed original-data publication gate, independent of candidate rights claims."""
import hashlib,importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def approved_learning(root=ROOT):
    root=Path(root);approval_path=root/'data/educational-publication-approval.json';source=root/'data/educational-canonical-v2.json'
    if approval_path.is_symlink() or source.is_symlink():raise ValueError('Canonical public input symlink')
    approval=json.loads(approval_path.read_text());raw=source.read_bytes()
    if approval.get('path')!='data/educational-canonical-v2.json' or approval.get('kind')!='original-synthetic' or approval.get('game_data') is not False or hashlib.sha256(raw).hexdigest()!=approval.get('sha256'):raise ValueError('No reviewed canonical publication approval or checksum mismatch')
    data=json.loads(raw)
    sys.path.insert(0,str(ROOT/'scripts'))
    try:
        spec=importlib.util.spec_from_file_location('canonical_review',ROOT/'scripts/import_catalog_v2.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);errors,_,_=module.validate(data)
    finally:sys.path.pop(0)
    if errors:raise ValueError('Canonical technical validation failed')
    if data['snapshot']['channel']!='test' or data['snapshot']['source_revision']!=approval.get('source_revision') or [s['id'] for s in data['sources']]!=approval.get('source_ids'):raise ValueError('Canonical provenance does not match reviewed original source')
    if any(r['status']!='tutorial' for section in ('items','groups','stations','recipes') for r in data[section]):raise ValueError('Only original tutorial records approved')
    if any(s['license'].get(k)!='allowed' for s in data['sources'] for k in ('commercial_use','redistribution','automated_access','game_ip_use')):raise ValueError('Source declarations disagree with trusted approval')
    return data,approval,raw
