"""Summarize JAISL expert-evaluation ratings from JSON."""
import argparse,json
from pathlib import Path
from .expert_eval import ExpertRating,summarize_ratings,pairwise_exact_agreement

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ratings",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    raw=json.loads(args.ratings.read_text(encoding="utf-8"))
    if not isinstance(raw,list): raise ValueError("ratings file must be a JSON list")
    ratings=[ExpertRating(**x) for x in raw]
    result={"summary":summarize_ratings(ratings),"pairwise_exact_agreement":pairwise_exact_agreement(ratings)}
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f: f.write(text)
    print(text)

if __name__=="__main__":
    main()
