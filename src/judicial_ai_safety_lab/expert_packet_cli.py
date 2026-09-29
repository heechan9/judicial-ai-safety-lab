"""Build a blinded expert-review packet from frozen case-output JSON."""
import argparse,json
from pathlib import Path
from .expert_packet import build_expert_packet

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cases",required=True,type=Path)
    p.add_argument("--target-commit",required=True)
    p.add_argument("--packet-version",default="v1")
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    rows=json.loads(args.cases.read_text(encoding="utf-8"))
    packet=build_expert_packet(rows,target_commit=args.target_commit,packet_version=args.packet_version)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(packet,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"case_count":len(packet["cases"]),"packet_hash":packet["packet_hash"]},ensure_ascii=False))

if __name__=="__main__":
    main()
