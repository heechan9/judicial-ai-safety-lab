"""Validate an official public precedent discovery candidate pool."""
import argparse,json
from pathlib import Path
from .public_discovery import validate_public_discovery

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",required=True,type=Path)
    args=p.parse_args(argv)
    doc=json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(validate_public_discovery(doc),ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
