#!/usr/bin/env python3
"""Extract Hytale recipes from a locally obtained game Assets.zip; no invented data."""
import argparse, json, zipfile
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
        recipes=[]; errors=[]; scanned=0
        for info in z.infolist():
            p=info.filename.replace("\\","/")
            if not p.endswith(".json") or "/Server/Item/" not in "/"+p or info.file_size>3000000:continue
            if "/Recipes/" not in "/"+p and "/Items/" not in "/"+p:continue
            scanned+=1
            try: obj=json.loads(z.read(info))
            except (ValueError,UnicodeError,RuntimeError) as e:
                errors.append({"file":p,"reason":"invalid_json"});continue
            if not isinstance(obj,dict):continue
            candidates=[]
            if "/Recipes/" in "/"+p:candidates.append((obj,None))
            if isinstance(obj.get("Recipe"),dict):candidates.append((obj["Recipe"],Path(p).stem))
            for r,implicit in candidates:
                ins=materials(r.get("Input"))
                outs=materials(r.get("Output")) or materials(r.get("PrimaryOutput"))
                if not outs and implicit:
                    qty=r.get("OutputQuantity",1)
                    outs=materials({"ItemId":implicit,"Quantity":qty})
                if not ins or not outs:
                    errors.append({"file":p,"reason":"unresolved_input_or_output"});continue
                recipes.append({"id":Path(p).stem,"inputs":ins,"outputs":outs,"bench_requirements":r.get("BenchRequirement",[]),"source_file":p})
    return {"schema_version":2,"source":"Hytale Assets.zip","json_files_scanned":scanned,"recipe_count":len(recipes),"rejected_count":len(errors),"rejected_examples":errors[:100],"recipes":recipes}

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("assets_zip",type=Path)
    ap.add_argument("--output",type=Path,default=Path("data/hytale-recipes.json"))
    a=ap.parse_args()
    data=extract(a.assets_zip)
    if not data["recipe_count"]:raise SystemExit("No recipes extracted. Check the Assets.zip file.")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Recipes:",data["recipe_count"],"Rejected:",data["rejected_count"],"Saved:",a.output)
