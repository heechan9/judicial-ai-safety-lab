"""Create/verify a frozen real-data manifest from normalized official records."""
import argparse,json
from pathlib import Path
from .real_data_protocol import build_real_data_manifest,verify_real_data_manifest

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--records",required=True,type=Path)
    p.add_argument("--source-name",required=True)
    p.add_argument("--source-url",required=True)
    p.add_argument("--cutoff",required=True)
    p.add_argument("--selection-rule",required=True)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    records=json.loads(args.records.read_text(encoding="utf-8"))
    manifest=build_real_data_manifest(records,source_name=args.source_name,source_url=args.source_url,
        cutoff=args.cutoff,selection_rule=args.selection_rule)
    verify_real_data_manifest(records,manifest)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(manifest,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"valid":True,"record_count":manifest["record_count"],"records_hash":manifest["records_hash"]},ensure_ascii=False))

if __name__=="__main__":
    main()
