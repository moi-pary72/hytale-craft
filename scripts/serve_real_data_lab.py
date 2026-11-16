#!/usr/bin/env python3
"""Loopback-only, no indexing/cache, research-data-only local viewer. No tunnels."""
import argparse,json
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
try:import import_catalog as base
except ModuleNotFoundError:from scripts import import_catalog as base

def make_server(directory,port=0,root=base.ROOT):
 directory=base.private_path(directory,Path(root));config=directory/'lab-config.js'
 if not config.is_file() or any(p.is_symlink() for p in directory.rglob('*')):raise ValueError('Expected self-contained private research build without symlinks')
 class Handler(SimpleHTTPRequestHandler):
  def log_message(self,*args):pass
  def list_directory(self,path):self.send_error(403,'Directory listing disabled')
  def local_request(self):
   host=self.headers.get('Host','').split(':')[0]
   origin=self.headers.get('Origin')
   if host not in ('127.0.0.1','localhost') or origin is not None and origin not in (f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'):
    self.send_error(403,'Local research access only');return False
   return True
  def do_HEAD(self):
   if self.local_request():super().do_HEAD()
  def do_GET(self):
   if not self.local_request():return
   if self.path.split('?')[0]=='/research-data.json' and 'gzip' in self.headers.get('Accept-Encoding',''):
    raw=(directory/'research-data.json.gz').read_bytes();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Encoding','gzip');self.send_header('Vary','Accept-Encoding');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
   else:super().do_GET()

  def end_headers(self):
   self.send_header('Cache-Control','no-store');self.send_header('X-Robots-Tag','noindex, nofollow');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer');super().end_headers()
 return ThreadingHTTPServer(('127.0.0.1',port),partial(Handler,directory=str(directory)))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);p.add_argument('--port',type=int,default=8765);a=p.parse_args();s=make_server(a.directory,a.port);print(f'PRIVATE LOOPBACK ONLY: http://127.0.0.1:{s.server_port}/',flush=True)
 try:s.serve_forever()
 except KeyboardInterrupt:pass
 finally:s.server_close()
