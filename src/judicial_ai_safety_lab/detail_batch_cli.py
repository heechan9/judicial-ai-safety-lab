"""Collect official detail for every case in a catalog/enrichment queue."""
import argparse,json
from pathlib import Path
from .detail_batch_collect import collect_detail_batch

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--queue",required=True,type=Path)
    p.add_argument("--output-dir",required=True,type=Path)
    p.add_argument("--report",required=True,type=Path)
    p.add_argument("--stop-on-error",action="store_true")
    args=p.parse_args(argv)
    queue=json.loads(args.queue.read_text(encoding="utf-8"))
    items=queue.get("items") if isinstance(queue,dict) else None
    if not isinstance(items,list): raise ValueError("queue must contain items")
    result=collect_detail_batch(items,output_dir=args.output_dir,stop_on_error=args.stop_on_error)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    with args.report.open("x",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({k:result[k] for k in ("requested","collected","failed","skipped_existing","complete")},
                     ensure_ascii=False))

if __name__=="__main__":
    main()
