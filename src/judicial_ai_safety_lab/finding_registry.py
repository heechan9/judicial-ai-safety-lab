"""Normalize unresolved verification findings and preserve their identity."""
from dataclasses import dataclass,asdict

KINDS={
 "SOURCE_UNSUPPORTED","SOURCE_CONFLICT","SOURCE_CHANGED","SOURCE_UNCERTAIN",
 "TECHNICAL_FAILURE","CONSTITUTIONAL_IMPACT","PRIVACY_DATA_REVIEW",
 "MISSING_ORIGINAL","BASELINE_CHANGED","INTEGRITY_FAILURE",
}

@dataclass(frozen=True)
class Finding:
    finding_id:str
    kind:str
    target_ref:str
    severity:int
    detail:str

def register_findings(findings):
    out=[]; seen=set()
    for f in findings:
        if not isinstance(f,Finding): raise ValueError("findings must be Finding objects")
        if not f.finding_id or f.finding_id in seen: raise ValueError("finding ids must be unique and non-empty")
        if f.kind not in KINDS: raise ValueError("unsupported finding kind")
        if type(f.severity) is not int or not 1<=f.severity<=5: raise ValueError("severity must be 1..5")
        if not f.target_ref or not f.detail: raise ValueError("finding target/detail required")
        seen.add(f.finding_id); out.append(asdict(f))
    return {"findings":out,"count":len(out),"open_ids":[x["finding_id"] for x in out]}
