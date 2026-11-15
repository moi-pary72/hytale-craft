"""Original synthetic browser fixture served by test interception, never by site build."""
import hashlib,json
from pathlib import Path
DATA=json.loads((Path(__file__).parent/'fixtures/legacy-game-synthetic.json').read_text())
RAW=(json.dumps(DATA,sort_keys=True,indent=2)+'\n').encode()
CATALOG={'schema_version':1,'items':DATA['items'],'recipes':[],'recipe_ids':[],'source_generated_at':'2026-01-01'}
def install(page):
    def respond(route,value):route.fulfill(status=200,content_type='application/json',body=json.dumps(value))
    page.route('**/data/catalog.json',lambda route:respond(route,CATALOG))
    page.route('**/data/recipes/manifest.json',lambda route:respond(route,{'schema_version':1,'path':'fixture.json','sha256':hashlib.sha256(RAW).hexdigest()}))
    page.route('**/data/recipes/fixture.json',lambda route:route.fulfill(status=200,content_type='application/json',body=RAW))
