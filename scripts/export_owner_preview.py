#!/usr/bin/env python3
"""Safe interactive owner preview using the existing app/engine plus original art gallery. No deploy."""
import argparse,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def export(output):
 s=importlib.util.spec_from_file_location('beta_export',ROOT/'scripts/export_beta.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);out=m.export(output);html=out.read_text();script=(ROOT/'web/beta/visual-gallery.js').read_text().replace('</script','<\\/script');html=html.replace('</body>','<script>window.CRAFT_BUILD.ownerReview=true;'+script+'</script></body>');out.write_text(html);return out
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'.private/stage19/hytale-craft-owner-preview.html');a=p.parse_args();print(export(a.output))
