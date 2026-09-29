"""Compute JAISL external-validation state from committed evidence summaries."""
import argparse,json
from pathlib import Path
from .validation_gate import external_validation_gate

def _load(path):
    if path is None: return None
    return json.loads(Path(path).read_text(encoding="utf-8"))

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--internal-ci",action="store_true")
    p.add_argument("--real-data-manifest",type=Path)
    p.add_argument("--pilot-selection",type=Path)
    p.add_argument("--expert-summary",type=Path)
    p.add_argument("--audit-state",type=Path)
    p.add_argument("--claim-audit",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args(argv)
    result=external_validation_gate(
      internal_ci=args.internal_ci,
      real_data_manifest=_load(args.real_data_manifest),
      pilot_selection=_load(args.pilot_selection),
      expert_summary=_load(args.expert_summary),
      audit_state=_load(args.audit_state),
      claim_audit=_load(args.claim_audit),
    )
    text=json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open("x",encoding="utf-8") as f: f.write(text)
    print(text)

if __name__=="__main__":
    main()
