"""Completely invented data in an export contract; no real game records."""
def export_fixture():
 licence='https://hysphere.app/about#data-license';stamp='2026-01-01T00:00:00Z'
 items=[{'id':'test:'+k,'name':'Synthetic '+k,'category':'synthetic'} for k in ['raw','part','gear','dust']]
 recipes=[{'id':'test:make-part','kind':'craft','sourceItemId':'test:part','inputs':[{'itemId':'test:raw','quantity':3}],'outputs':[{'itemId':'test:part','quantity':2}],'benches':[{'id':'test:bench','type':'Crafting','categories':[],'tier':1}],'timeSeconds':1,'knowledgeRequired':False},{'id':'test:make-gear','kind':'craft','sourceItemId':'test:gear','inputs':[{'itemId':'test:part','quantity':2}],'outputs':[{'itemId':'test:gear','quantity':1},{'itemId':'test:dust','quantity':1}],'benches':[],'timeSeconds':2,'knowledgeRequired':False}]
 manifest={'contract':'sphere-data/v1','revision':stamp,'extractedAt':stamp,'game':{'version':'ORIGINAL-SYNTHETIC-TEST-NOT-HYTALE'},'license':{'url':licence},'datasets':[{'id':'items','recordCount':len(items)},{'id':'recipes','recordCount':len(recipes)}]}
 def wrap(key,rows):return {'contract':'sphere-data/v1','extractedAt':stamp,'gameVersion':manifest['game']['version'],'count':len(rows),key:rows}
 return manifest,wrap('items',items),wrap('recipes',recipes)
