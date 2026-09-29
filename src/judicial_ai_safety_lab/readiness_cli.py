"""Compute pilot readiness for a case catalog."""
import argparse,json
from pathlib import Path
from .case_catalog import validate_case_catalog
from .pilot_readiness import evaluate_case_readiness

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog",required=True,type=Path)
    p.add_argument("--evidence",type=Path)
    p.add_argument("--selection",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    catalog=json.loads(args.catalog.read_text(encoding="utf-8"))
    validate_case_catalog(catalog)
    evidence=json.loads(args.evidence.read_text(encoding="utf-8")) if args.evidence else {}
    selected=[]
    if args.selection:
        s=json.loads(args.selection.read_text(encoding="utf-8"))
        selected=[x["source_id"] for x in s.get("selected",[])]
    result=evaluate_case_readiness(catalog,evidence_by_source=evidence,frozen_selection_ids=selected)
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f: f.write(text)
    print(text)

if __name__=="__main__":
    main()
