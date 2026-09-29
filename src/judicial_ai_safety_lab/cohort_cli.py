"""Freeze the full public discovery cohort before model outcome review."""
import argparse,json
from pathlib import Path
from .cohort_freeze import freeze_full_cohort,verify_frozen_cohort

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--discovery",required=True,type=Path)
    p.add_argument("--cohort-id",required=True)
    p.add_argument("--rule",required=True)
    p.add_argument("--cutoff",required=True)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    discovery=json.loads(args.discovery.read_text(encoding="utf-8"))
    cohort=freeze_full_cohort(discovery,cohort_id=args.cohort_id,rule=args.rule,cutoff=args.cutoff)
    verify_frozen_cohort(cohort,discovery)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(cohort,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"valid":True,"member_count":cohort["member_count"],"cohort_hash":cohort["cohort_hash"]},ensure_ascii=False))

if __name__=="__main__":
    main()
