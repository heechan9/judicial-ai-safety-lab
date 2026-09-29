"""Register traceable external audit results."""
import argparse,json
from pathlib import Path
from .external_audit_registry import ExternalAudit,external_validation_state

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audits",required=True,type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    rows=json.loads(args.audits.read_text(encoding="utf-8"))
    if not isinstance(rows,list): raise ValueError("audits must be a JSON list")
    result=external_validation_state([ExternalAudit(**x) for x in rows])
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f: f.write(text)
    print(text)

if __name__=="__main__":
    main()
