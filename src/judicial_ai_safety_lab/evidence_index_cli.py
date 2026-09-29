"""Build an evidence index from a batch reconciliation result."""
import argparse,json
from pathlib import Path
from .evidence_index import build_evidence_index

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--batch",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    batch=json.loads(args.batch.read_text(encoding="utf-8"))
    result=build_evidence_index(batch)
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f:
            f.write(text)
    print(text)

if __name__=="__main__":
    main()
