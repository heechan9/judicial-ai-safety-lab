"""Preserve reviewer disagreement and record explicit adjudication without overwriting ratings."""
from dataclasses import dataclass,asdict
from datetime import datetime

@dataclass(frozen=True)
class AdjudicationRecord:
    case_id:str
    adjudicator_id:str
    decided_at:str
    disposition:str
    rationale:str
    source_rating_ids:tuple[str,...]

ALLOWED={"NO_CHANGE","CRITICAL_ERROR_CONFIRMED","CRITICAL_ERROR_CLEARED","MORE_REVIEW_REQUIRED"}

def validate_adjudication(record):
    if not isinstance(record,AdjudicationRecord):
        raise ValueError("record must be AdjudicationRecord")
    if not record.case_id or not record.adjudicator_id or not record.rationale:
        raise ValueError("case_id, adjudicator_id and rationale required")
    if record.disposition not in ALLOWED:
        raise ValueError("invalid disposition")
    dt=datetime.fromisoformat(record.decided_at.replace("Z","+00:00"))
    if dt.utcoffset() is None:
        raise ValueError("decided_at must include timezone")
    if len(record.source_rating_ids)<2 or len(record.source_rating_ids)!=len(set(record.source_rating_ids)):
        raise ValueError("at least two unique source_rating_ids required")
    return asdict(record)

def adjudication_gate(critical_case_ids,records):
    critical=sorted(set(critical_case_ids))
    validated=[validate_adjudication(r) for r in records]
    by_case={r["case_id"]:r for r in validated}
    missing=[cid for cid in critical if cid not in by_case]
    unresolved=[
      cid for cid in critical
      if cid in by_case and by_case[cid]["disposition"] in {"CRITICAL_ERROR_CONFIRMED","MORE_REVIEW_REQUIRED"}
    ]
    ready=not missing and not unresolved
    return {
      "schema":"jaisl.expert-adjudication-gate.v1",
      "critical_case_count":len(critical),
      "adjudication_count":len(validated),
      "missing_case_ids":missing,
      "unresolved_case_ids":unresolved,
      "ready_after_adjudication":ready,
      "records":validated,
      "note":"Adjudication is additive and never overwrites original expert ratings.",
    }
