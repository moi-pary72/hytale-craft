#!/usr/bin/env python3
"""Extract Hytale recipes from a locally obtained game Assets.zip; no invented data."""
import argparse, json, zipfile, hashlib, os, shutil
from datetime import datetime, timezone
from pathlib import Path

def material(v):
    if not isinstance(v, dict): return None
    kinds=[k for k in ("ItemId","ResourceTypeId","ItemTag") if isinstance(v.get(k),str) and v[k]]
    q=v.get("Quantity",1)
    if len(kinds)!=1 or type(q)!=int or not 0<q<10000000:return None
    return {"kind":kinds[0],"id":v[kinds[0]],"quantity":q}

def materials(v):
    if isinstance(v,dict):v=[v]
    if not isinstance(v,list) or not v:return None
    a=[material(x) for x in v]
    return a if all(a) else None

def extract(source):
    with zipfile.ZipFile(source) as z:
        recipes=[]; errors=[]; scanned=0; items=[]; seen=set()
        for info in z.infolist():
            p=info.filename.replace("\\","/")
            if not p.endswith(".json") or "/Server/Item/" not in "/"+p or info.file_size>3000000:continue
            if "/Recipes/" not in "/"+p and "/Items/" not in "/"+p:continue
            scanned+=1
            try: obj=json.loads(z.read(info))
            except (ValueError,UnicodeError,RuntimeError) as e:
                errors.append({"file":p,"reason":"invalid_json"});continue
            if not isinstance(obj,dict):continue
            if "/Items/" in "/"+p:
                item_id=Path(p).stem
                if item_id in seen:raise ValueError("Duplicate item ID: "+item_id)
                seen.add(item_id)
                items.append({"id":item_id,"translation_key":obj.get("TranslationProperties",{}).get("Name"),"names":{"en":None,"ru":None},"source_file":p})
            if obj.get("Parent"):
                errors.append({"file":p,"reason":"inheritance_requires_resolution"});continue
            candidates=[]
            if "/Recipes/" in "/"+p:candidates.append((obj,None))
            if isinstance(obj.get("Recipe"),dict):candidates.append((obj["Recipe"],Path(p).stem))
            for r,implicit in candidates:
                ins=materials(r.get("Input"))
                outs=materials(r.get("Output")) or materials(r.get("PrimaryOutput"))
                if not outs and implicit and "Output" not in r and "PrimaryOutput" not in r:
                    qty=r.get("OutputQuantity",1)
                    outs=materials({"ItemId":implicit,"Quantity":qty})
                if r.get("Parent") or not ins or not outs:
                    errors.append({"file":p,"reason":"unresolved_input_or_output"});continue
                recipes.append({"id":p,"inputs":ins,"outputs":outs,"bench_requirements":r.get("BenchRequirement",[]),"source_file":p})
    known={i["id"] for i in items}
    for r in recipes:
        r["unresolved_item_ids"] = sorted({m["id"] for m in r["inputs"]+r["outputs"] if m["kind"]=="ItemId" and m["id"] not in known})
        r["calculation_supported"] = not r["unresolved_item_ids"] and len(r["outputs"])==1 and all(m["kind"]=="ItemId" for m in r["inputs"]+r["outputs"])
    with open(source,"rb") as archive_file:
        digest=hashlib.file_digest(archive_file,"sha256").hexdigest()
    return {"schema_version":2,"items":items,"item_count":len(items),"archive_sha256":digest,"source":"Hytale Assets.zip","json_files_scanned":scanned,"recipe_count":len(recipes),"rejected_count":len(errors),"rejected_examples":errors[:100],"recipes":recipes}

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("assets_zip",type=Path)
    ap.add_argument("--output",type=Path,default=Path("data/hytale-recipes.json"))
    ap.add_argument("--game-version",required=True)
    ap.add_argument("--report",type=Path,default=Path("docs/reports/assets-import.json"))
    a=ap.parse_args()
    data=extract(a.assets_zip)
    data["game_version"]=a.game_version
    data["imported_at"]=datetime.now(timezone.utc).isoformat()
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    if any(r["unresolved_item_ids"] for r in data["recipes"]):raise SystemExit("Unresolved item IDs; working file preserved; see report")
    if data["rejected_count"]:raise SystemExit("Import rejected: unresolved/invalid assets; production file preserved. Inspect extract() report.")
    if not data["recipe_count"]:raise SystemExit("No recipes extracted. Check the Assets.zip file.")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    if a.output.exists():shutil.copy2(a.output,a.output.with_suffix(".previous.json"))
    tmp=a.output.with_suffix(".tmp")
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    os.replace(tmp,a.output)
    print("Recipes:",data["recipe_count"],"Rejected:",data["rejected_count"],"Saved:",a.output)
