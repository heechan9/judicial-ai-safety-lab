"""Build deterministic LAW_OC enrichment queue from a case catalog."""
import argparse,json
from pathlib import Path
from .case_catalog import validate_case_catalog
from .enrichment_queue import build_enrichment_queue

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--catalog",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    catalog=json.loads(args.catalog.read_text(encoding="utf-8"))
    validate_case_catalog(catalog)
    result=build_enrichment_queue(catalog)
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f: f.write(text)
    print(text)

if __name__=="__main__":
    main()
