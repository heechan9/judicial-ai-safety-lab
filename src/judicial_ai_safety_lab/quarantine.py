"""Quarantine invalid evidence instead of silently dropping it."""
from dataclasses import dataclass, field, asdict

ALLOWED={"quarantined":{"fix":"fixed"},"fixed":{"retest_pass":"closed","retest_fail":"quarantined"},"closed":{"reopen":"quarantined"}}

@dataclass
class QuarantineRecord:
    evidence_id:str
    reason:str
    status:str="quarantined"
    history:list[dict]=field(default_factory=list)

def quarantine(evidence_id,reason):
    if not isinstance(evidence_id,str) or not evidence_id.strip(): raise ValueError("evidence id required")
    if not isinstance(reason,str) or not reason.strip(): raise ValueError("quarantine reason required")
    return QuarantineRecord(evidence_id.strip(),reason.strip(),history=[{"action":"quarantined","reason":reason.strip()}])

def transition(record,action,note):
    target=ALLOWED.get(record.status,{}).get(action)
    if not target: raise ValueError("invalid quarantine transition")
    if not isinstance(note,str) or not note.strip(): raise ValueError("transition note required")
    record.status=target
    record.history.append({"action":action,"note":note.strip()})
    return record

def as_record(record): return asdict(record)
