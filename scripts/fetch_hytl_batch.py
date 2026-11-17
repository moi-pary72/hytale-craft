#!/usr/bin/env python3
"""Fetch one authorized metadata page to private staging; never exposes credentials or publishes."""
import argparse,hashlib,json,os,urllib.request,urllib.error
from datetime import datetime,timezone
from pathlib import Path
try:import import_catalog as base
except ModuleNotFoundError:from scripts import import_catalog as base
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):raise ValueError('Redirect requires review; credentials not forwarded')
def fetch(dataset,offset,output):
 if dataset not in ('items','recipes') or not 0<=offset<=10000:raise ValueError('Only documented metadata pagination supported')
 output=base.private_path(output,base.ROOT)
 if output.exists():raise ValueError('Choose a new private snapshot path')
 key=os.environ.get('HYTL_API_KEY')
 if not key:raise ValueError('HYTL_API_KEY is not configured. No request made. Configure a free authorized metadata key outside code/browser.')
 url=f'https://hytl.dev/api/v1/{dataset}?limit=100&offset={offset}'
 request=urllib.request.Request(url,headers={'Authorization':'Bearer '+key,'Accept':'application/json'})
 try:
  with urllib.request.build_opener(NoRedirect).open(request,timeout=30) as response:raw=response.read(base.MAX_BYTES+1)
 except urllib.error.HTTPError as e:
  raise ValueError('Metadata request stopped: HTTP '+str(e.code)+'; respect provider access/rate limits. No fallback or automatic retry.') from None
 if len(raw)>base.MAX_BYTES:raise ValueError('Metadata page too large')
 base.strict_json(raw);output.parent.mkdir(parents=True,exist_ok=True);base.atomic(output,raw);output.chmod(0o600);receipt={'source':url,'fetched_at':datetime.now(timezone.utc).isoformat(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'dataset':dataset,'rights':'access-key-is-not-publication-or-game-asset-permission','schema':'raw-provider-response-needs-reviewed-adapter','publication':'blocked'};base.atomic(output.with_suffix('.receipt.json'),base.encoded(receipt));return receipt
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--dataset',choices=('items','recipes'),required=True);p.add_argument('--offset',type=int,default=0);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 try:r=fetch(a.dataset,a.offset,a.output);print(json.dumps(r))
 except (ValueError,urllib.error.URLError):raise SystemExit('Metadata acquisition stopped; verify configured authorization, provider contract and private output. No secret or response body logged.')
