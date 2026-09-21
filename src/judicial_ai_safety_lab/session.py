import json,hashlib
from pathlib import Path
def canonical_hash(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def save_session(path,report,sources,scenarios):
    x={"schema":"jaisl.session.v1","report_hash":canonical_hash(report),"source_hash":canonical_hash(sources),"scenario_hash":canonical_hash(scenarios)}
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding="utf-8")
