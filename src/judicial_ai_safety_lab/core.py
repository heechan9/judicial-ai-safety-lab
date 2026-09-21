from dataclasses import dataclass, asdict
import hashlib, json
from pathlib import Path

@dataclass
class LegalSourceRecord:
    source_id:str; institution:str; source_type:str; title:str; version:str; status:str
    effective_date:str|None=None; canonical_ref:str|None=None
    constitutional_status:str|None=None; checksum:str|None=None
    def dict(self): return asdict(self)

@dataclass
class Scenario:
    scenario_id:str; category:str; baseline_pass:bool; ai_pass:bool
    attacked:bool=False; source_changed:bool=False; severity:int=1

WEIGHTS={"accuracy":.25,"procedural":.25,"privacy":.15,"security":.20,"reproducibility":.15}

def load_sources(path):
    return [LegalSourceRecord(**x) for x in json.loads(Path(path).read_text(encoding="utf-8"))]

def validate_sources(records):
    allowed={"court","moleg","ccourt","assembly"}; errs=[]; seen=set()
    for r in records:
        if r.institution not in allowed: errs.append(f"{r.source_id}: unsupported institution")
        if r.source_id in seen: errs.append(f"duplicate {r.source_id}")
        seen.add(r.source_id)
    return errs

def source_guard(records):
    out=[]
    for r in records:
        flags=[]
        if r.status.lower() in {"proposed","pending","committee"}: flags.append("NOT_EFFECTIVE")
        if r.constitutional_status and r.constitutional_status.lower() not in {"none","normal","valid"}: flags.append("CONSTITUTIONAL_STATUS")
        if not r.checksum: flags.append("MISSING_CHECKSUM")
        out.append({"source_id":r.source_id,"institution":r.institution,"title":r.title,"flags":flags,"requires_review":bool(flags)})
    return out

def risk(m):
    s=round(sum(m[k]*v for k,v in WEIGHTS.items()),2)
    return s,("HIGH" if s>=60 else "WATCH" if s>=30 else "LOW")

def evaluate(rows):
    n=len(rows); a=[r for r in rows if r.attacked and r.baseline_pass]; stress=[r for r in rows if r.category!="normal"]
    return {"baseline_pass_rate":round(sum(r.baseline_pass for r in rows)/n,4),"ai_pass_rate":round(sum(r.ai_pass for r in rows)/n,4),
    "attack_success_rate":round(sum(not r.ai_pass for r in a)/len(a),4) if a else 0,
    "stress_pass_rate":round(sum(r.ai_pass for r in stress)/len(stress),4) if stress else 0}

def drift(frozen,current,tol=.10):
    d=round(current-frozen,4); return {"frozen":frozen,"current":current,"delta":d,"status":"WATCH" if abs(d)>tol else "STABLE"}

def review_queue(rows,findings):
    q=[]
    for r in rows:
        if not r.ai_pass or r.source_changed:
            q.append({"item":r.scenario_id,"priority":r.severity*10+(25 if not r.ai_pass else 0)+(15 if r.source_changed else 0),"reason":"AI_FAIL/SOURCE_CHANGE" if r.source_changed else "AI_FAIL"})
    for f in findings:
        if f["requires_review"]: q.append({"item":"source:"+f["source_id"],"priority":50,"reason":"SOURCE_GUARD"})
    return sorted(q,key=lambda x:x["priority"],reverse=True)

def rerun_gate(c):
    req=["model_version","prompt_hash","corpus_hash","scenario_manifest_hash","evaluation_contract"]; miss=[x for x in req if not c.get(x)]
    return {"ready":not miss,"missing":miss}

def htext(s): return hashlib.sha256(s.encode()).hexdigest()
def hfile(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,obj):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
