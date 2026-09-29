"""Collect one official precedent detail without persisting LAW_OC."""
import argparse,json
from pathlib import Path
from .precedent_detail_collect import collect_precedent_detail,verify_detail_envelope

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--prec-seq",required=True)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    envelope=collect_precedent_detail(args.prec_seq)
    verify_detail_envelope(envelope)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(envelope,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"valid":True,"prec_seq":envelope["prec_seq"],"raw_response_hash":envelope["raw_response_hash"],"credential_stored":False},ensure_ascii=False))

if __name__=="__main__":
    main()
