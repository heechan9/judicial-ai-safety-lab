"""Register completed external audits only when traceable evidence exists."""
from dataclasses import dataclass,asdict
from datetime import datetime
import re

SHA40=re.compile(r"^[0-9a-f]{40}$")

@dataclass(frozen=True)
class ExternalAudit:
    audit_id:str
    reviewer:str
    reviewer_type:str
    target_commit:str
    reviewed_at:str
    scope:str
    evidence_ref:str
    status:str

def register_external_audit(audit):
    if not isinstance(audit,ExternalAudit): raise ValueError("invalid audit")
    if audit.status not in {"COMPLETED","PARTIAL","FAILED"}: raise ValueError("invalid audit status")
    if not SHA40.fullmatch(audit.target_commit or ""): raise ValueError("target commit must be full lowercase SHA")
    dt=datetime.fromisoformat(audit.reviewed_at.replace("Z","+00:00"))
    if dt.utcoffset() is None: raise ValueError("reviewed_at must include timezone")
    for field in ("audit_id","reviewer","reviewer_type","scope","evidence_ref"):
        if not isinstance(getattr(audit,field),str) or not getattr(audit,field).strip():
            raise ValueError(f"{field} required")
    return asdict(audit)

def external_validation_state(audits):
    audits=list(audits)
    records=[register_external_audit(a) for a in audits]
    completed=[x for x in records if x["status"]=="COMPLETED"]
    return {
      "audit_count":len(records),
      "completed_count":len(completed),
      "has_completed_code_audit":any("code" in x["scope"].lower() and x["status"]=="COMPLETED" for x in records),
      "has_completed_ui_audit":any("ui" in x["scope"].lower() and x["status"]=="COMPLETED" for x in records),
      "records":records,
    }
