"""Build a stable discovery case catalog."""
import argparse,json
from pathlib import Path
from .case_catalog import build_case_catalog,validate_case_catalog

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--discovery",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    discovery=json.loads(args.discovery.read_text(encoding="utf-8"))
    catalog=build_case_catalog(discovery)
    validate_case_catalog(catalog)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(catalog,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"valid":True,"case_count":catalog["case_count"],"catalog_hash":catalog["catalog_hash"]},ensure_ascii=False))

if __name__=="__main__":
    main()
