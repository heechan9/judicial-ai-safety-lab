"""Evaluate whether critical expert-review cases have explicit adjudication."""
import argparse,json
from pathlib import Path
from .expert_adjudication import AdjudicationRecord,adjudication_gate

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--critical-cases",required=True,type=Path,help="JSON list of case IDs")
    p.add_argument("--records",required=True,type=Path,help="JSON list of adjudication records")
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    critical=json.loads(args.critical_cases.read_text(encoding="utf-8"))
    rows=json.loads(args.records.read_text(encoding="utf-8"))
    result=adjudication_gate(critical,[AdjudicationRecord(**x) for x in rows])
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f: f.write(text)
    print(text)

if __name__=="__main__":
    main()
