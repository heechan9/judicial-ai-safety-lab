"""Batch reconcile a discovery pool against a directory of detail envelopes."""
import argparse,json
from pathlib import Path
from .batch_reconcile import load_detail_envelopes,reconcile_discovery_batch

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--discovery",required=True,type=Path)
    p.add_argument("--detail-dir",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    discovery=json.loads(args.discovery.read_text(encoding="utf-8"))
    envelopes=load_detail_envelopes(args.detail_dir)
    result=reconcile_discovery_batch(discovery,detail_envelopes=envelopes)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps(result["summary"],ensure_ascii=False))

if __name__=="__main__":
    main()
