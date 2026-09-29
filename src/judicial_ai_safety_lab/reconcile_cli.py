"""Reconcile one discovery case with one credential-backed detail envelope."""
import argparse,json
from pathlib import Path
from .evidence_reconcile import reconcile_case

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--discovery-row",required=True,type=Path)
    p.add_argument("--case-id",required=True)
    p.add_argument("--detail-envelope",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    row=json.loads(args.discovery_row.read_text(encoding="utf-8"))
    env=json.loads(args.detail_envelope.read_text(encoding="utf-8"))
    result=reconcile_case(row,case_id=args.case_id,detail_envelope=env)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"status":result["status"],"case_id":result["case_id"],"source_id":result["source_id"]},ensure_ascii=False))

if __name__=="__main__":
    main()
