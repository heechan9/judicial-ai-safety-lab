"""Check whether expert ratings cover the full frozen case set."""
import argparse,json
from pathlib import Path
from .expert_eval import ExpertRating
from .expert_review_gate import expert_review_gate

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ratings",required=True,type=Path)
    p.add_argument("--packet",required=True,type=Path)
    p.add_argument("--min-reviewers",type=int,default=2)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)

    rows=json.loads(args.ratings.read_text(encoding="utf-8"))
    packet=json.loads(args.packet.read_text(encoding="utf-8"))
    if packet.get("schema")!="jaisl.expert-packet.v1":
        raise ValueError("expert packet required")
    expected=[x["case_id"] for x in packet["cases"]]
    ratings=[ExpertRating(**x) for x in rows]
    result=expert_review_gate(ratings,expected_case_ids=expected,min_reviewers=args.min_reviewers)
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f: f.write(text)
    print(text)

if __name__=="__main__":
    main()
