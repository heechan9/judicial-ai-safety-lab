"""Requirement-level defect/retest log with immutable revision references."""
from dataclasses import dataclass, field, asdict
from datetime import datetime
import re

SHA_RE=re.compile(r"^[0-9a-f]{40}$")
ALLOWED={"open":{"fixed":"fixed"},"fixed":{"pass":"closed","fail":"open"},"closed":{"reopen":"open"}}

@dataclass
class QualityRecord:
    record_id:str
    requirement:str
    expected:str
    observed:str
    revision:str
    status:str="open"
    history:list[dict]=field(default_factory=list)

def _stamp(value:str)->str:
    datetime.fromisoformat(value.replace("Z","+00:00"))
    return value

def _revision(value:str)->str:
    if not SHA_RE.fullmatch(value or ""): raise ValueError("revision must be a full lowercase git SHA")
    return value

def create_record(*,record_id,requirement,expected,observed,revision,at):
    if not all(isinstance(v,str) and v.strip() for v in (record_id,requirement,expected,observed)):
        raise ValueError("quality record fields must be non-empty strings")
    rev=_revision(revision); stamp=_stamp(at)
    return QualityRecord(record_id,requirement,expected,observed,rev,history=[
      {"action":"registered","at":stamp,"revision":rev,"note":"human/automated source must be recorded separately"}
    ])

def transition(record:QualityRecord,*,action,note,revision,at):
    target=ALLOWED.get(record.status,{}).get(action)
    if not target: raise ValueError("invalid quality-log transition")
    if len(record.history)>=50: raise ValueError("quality-log history limit reached")
    if not isinstance(note,str) or not note.strip(): raise ValueError("transition note is required")
    record.status=target
    record.revision=_revision(revision)
    record.history.append({"action":action,"at":_stamp(at),"revision":record.revision,"note":note.strip()})
    return record

def record_dict(record): return asdict(record)
