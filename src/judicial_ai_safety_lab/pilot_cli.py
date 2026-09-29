"""Freeze a pre-registered pilot selection from candidate JSON."""
import argparse,json
from pathlib import Path
from .pilot_selection import PilotCandidate,select_pilot

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--candidates",required=True,type=Path)
    p.add_argument("--targets",required=True,type=Path,help="JSON object: stratum -> count")
    p.add_argument("--selection-note",required=True)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)
    rows=json.loads(args.candidates.read_text(encoding="utf-8"))
    targets=json.loads(args.targets.read_text(encoding="utf-8"))
    selected=select_pilot([PilotCandidate(**x) for x in rows],targets=targets,selection_note=args.selection_note)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(selected,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"selected_count":selected["selected_count"],"selection_hash":selected["selection_hash"]},ensure_ascii=False))

if __name__=="__main__":
    main()
