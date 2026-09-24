"""Freeze evidence to what was available at a decision cutoff.

Prevents hindsight leakage in replay/second-look evaluation. Later material can
be shown as a subsequent change, but cannot silently enter the frozen snapshot.
"""
from datetime import datetime

def _dt(value):
    d=datetime.fromisoformat(value.replace("Z","+00:00"))
    if d.utcoffset() is None: raise ValueError("timestamp must include timezone")
    return d

def freeze_evidence(records,*,cutoff):
    boundary=_dt(cutoff); admitted=[]; excluded=[]
    for row in records:
        if not isinstance(row,dict) or "source_id" not in row or "observed_at" not in row:
            raise ValueError("evidence rows require source_id and observed_at")
        target=admitted if _dt(row["observed_at"])<=boundary else excluded
        target.append(row)
    return {
      "cutoff":cutoff,
      "admitted":admitted,
      "excluded_future":excluded,
      "hindsight_leakage_blocked":bool(excluded),
    }
