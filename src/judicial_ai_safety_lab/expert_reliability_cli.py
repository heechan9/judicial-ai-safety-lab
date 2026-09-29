"""Compute ordinal inter-rater reliability from expert ratings JSON."""
import argparse,json
from pathlib import Path
from .expert_eval import ExpertRating
from .expert_reliability import quadratic_weighted_kappa

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ratings",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    rows=json.loads(args.ratings.read_text(encoding="utf-8"))
    ratings=[ExpertRating(**x) for x in rows]
    result=quadratic_weighted_kappa(ratings)
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f: f.write(text)
    print(text)

if __name__=="__main__":
    main()
