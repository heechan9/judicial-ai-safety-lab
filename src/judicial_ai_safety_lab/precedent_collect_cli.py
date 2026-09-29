"""Collect an official precedent-search response without persisting LAW_OC."""
import argparse,json
from pathlib import Path
from .precedent_collect import collect_raw_precedents,verify_raw_collection

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query",required=True)
    p.add_argument("--display",type=int,default=20)
    p.add_argument("--page",type=int,default=1)
    p.add_argument("--org")
    p.add_argument("--curt")
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    result=collect_raw_precedents(args.query,display=args.display,page=args.page,org=args.org,curt=args.curt)
    verify_raw_collection(result)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"valid":True,"raw_response_hash":result["raw_response_hash"],"credential_stored":False},ensure_ascii=False))

if __name__=="__main__":
    main()
