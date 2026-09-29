"""Build a blinded expert packet from a frozen real-data assessment."""
import argparse,json
from pathlib import Path
from .expert_packet import build_expert_packet

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--assessment",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    assessment=json.loads(args.assessment.read_text(encoding="utf-8"))
    if assessment.get("schema")!="jaisl.real-assessment.v1" or assessment.get("frozen") is not True:
        raise ValueError("frozen real assessment required")
    if assessment.get("expert_packet_ready") is not True:
        raise ValueError("assessment is not ready for expert packet")
    packet=build_expert_packet(
        assessment["expert_cases"],
        target_commit=assessment["target_commit"],
        packet_version="real-pilot-v1",
    )
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(packet,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"case_count":len(packet["cases"]),"packet_hash":packet["packet_hash"]},ensure_ascii=False))

if __name__=="__main__":
    main()
