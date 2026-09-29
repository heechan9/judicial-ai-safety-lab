"""Pre-register and freeze a small real-data pilot sample.

This module selects by explicit strata and stable source order before model
outcomes are inspected. It does not infer legal labels.
"""
from dataclasses import dataclass,asdict
import hashlib,json

@dataclass(frozen=True)
class PilotCandidate:
    source_id:str
    stratum:str
    title:str
    metadata:dict

def _hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def select_pilot(candidates,*,targets,selection_note):
    candidates=list(candidates)
    if not isinstance(targets,dict) or not targets:
        raise ValueError("targets must be a non-empty mapping")
    if any(type(v) is not int or v<1 for v in targets.values()):
        raise ValueError("target counts must be positive integers")
    if not isinstance(selection_note,str) or not selection_note.strip():
        raise ValueError("selection note required")

    seen=set(); grouped={k:[] for k in targets}
    for c in candidates:
        if not isinstance(c,PilotCandidate): raise ValueError("invalid pilot candidate")
        if not c.source_id or c.source_id in seen: raise ValueError("source ids must be unique and non-empty")
        seen.add(c.source_id)
        if c.stratum in grouped:
            grouped[c.stratum].append(c)

    selected=[]
    shortages={}
    for stratum,count in targets.items():
        rows=sorted(grouped[stratum],key=lambda x:x.source_id)
        if len(rows)<count:
            shortages[stratum]={"required":count,"available":len(rows)}
            continue
        selected.extend(rows[:count])
    if shortages:
        raise ValueError(f"insufficient candidates: {shortages}")

    payload=[asdict(x) for x in selected]
    return {
      "schema":"jaisl.pilot-selection.v1",
      "targets":dict(targets),
      "selection_note":selection_note.strip(),
      "selected_count":len(payload),
      "selected":payload,
      "selection_hash":_hash(payload),
      "limitations":[
        "pilot selection is not a representative population sample",
        "strata are research categories, not legal outcome classes",
        "selection must be frozen before reviewing model outcomes",
      ],
    }
