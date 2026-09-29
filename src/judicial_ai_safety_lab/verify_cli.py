"""Verify a packaged JAISL human-review record."""
import argparse
import json
from pathlib import Path
from .package_verify import verify_review_package

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--package",required=True,type=Path)
    args=p.parse_args(argv)
    value=json.loads(args.package.read_text(encoding="utf-8"))
    result=verify_review_package(value)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
