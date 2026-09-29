"""Check whether the frozen 30-case cohort has complete verified detail evidence."""
import argparse,json
from pathlib import Path
from .pilot_preflight import pilot_preflight

def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cohort",required=True,type=Path)
    p.add_argument("--batch",required=True,type=Path)
    p.add_argument("--evidence-index",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    result=pilot_preflight(cohort=_load(args.cohort),
                           batch_reconciliation=_load(args.batch),
                           evidence_index=_load(args.evidence_index))
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f: f.write(text)
    print(text)

if __name__=="__main__":
    main()
