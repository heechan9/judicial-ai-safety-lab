"""Build a frozen 30-case JAISL real-data assessment after preflight."""
import argparse,json
from pathlib import Path
from .batch_reconcile import load_detail_envelopes
from .real_case_assessment import build_real_case_assessment

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--discovery",required=True,type=Path)
    p.add_argument("--detail-dir",required=True,type=Path)
    p.add_argument("--preflight",required=True,type=Path)
    p.add_argument("--target-commit",required=True)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    discovery=json.loads(args.discovery.read_text(encoding="utf-8"))
    preflight=json.loads(args.preflight.read_text(encoding="utf-8"))
    envelopes=load_detail_envelopes(args.detail_dir)
    result=build_real_case_assessment(discovery,envelopes,preflight,target_commit=args.target_commit)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"case_count":result["case_count"],"verified_count":result["verified_count"],
                      "frozen":result["frozen"],"expert_packet_ready":result["expert_packet_ready"],
                      "assessment_hash":result["assessment_hash"]},ensure_ascii=False))

if __name__=="__main__":
    main()
