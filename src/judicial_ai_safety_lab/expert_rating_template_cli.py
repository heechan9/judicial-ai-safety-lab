"""Generate empty reviewer rating templates from a frozen expert packet."""
import argparse,json
from pathlib import Path
from .expert_rating_template import build_rating_templates

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--packet",required=True,type=Path)
    p.add_argument("--reviewers",required=True,type=Path,help="JSON list of stable reviewer IDs")
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    packet=json.loads(args.packet.read_text(encoding="utf-8"))
    reviewers=json.loads(args.reviewers.read_text(encoding="utf-8"))
    result=build_rating_templates(packet,reviewers)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"reviewer_count":len(result["reviewer_ids"]),
                      "case_count":len(next(iter(result["templates"].values())))},ensure_ascii=False))

if __name__=="__main__":
    main()
