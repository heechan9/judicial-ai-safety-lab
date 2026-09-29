"""v4.5 belief-state and review planning helpers.

Inspired by partial-observation planning patterns, but deliberately limited to
verification planning. This module never recommends a legal outcome.
"""
from dataclasses import dataclass

BELIEF_KEYS=("supported","uncertain","conflicting","changed","unsupported")

@dataclass(frozen=True)
class ReviewCandidate:
    action_id:str
    description:str
    information_gain:float
    urgency:float=0.0
    cost:float=0.0

def belief_state(*, supported=0.0, uncertain=0.0, conflicting=0.0, changed=0.0, unsupported=0.0):
    values={"supported":supported,"uncertain":uncertain,"conflicting":conflicting,
            "changed":changed,"unsupported":unsupported}
    if any(type(v) not in (int,float) or v<0 for v in values.values()):
        raise ValueError("belief weights must be non-negative numbers")
    total=sum(values.values())
    if total<=0: raise ValueError("belief weights must contain positive mass")
    normalized={k:round(v/total,6) for k,v in values.items()}
    return {"belief":normalized,
            "review_required":normalized["supported"]<1.0,
            "note":"Verification-state belief only; not a probability of legal correctness."}

def score_candidate(candidate:ReviewCandidate):
    vals=(candidate.information_gain,candidate.urgency,candidate.cost)
    if any(type(v) not in (int,float) for v in vals): raise ValueError("candidate values must be numeric")
    if candidate.information_gain<0 or candidate.urgency<0 or candidate.cost<0:
        raise ValueError("candidate values must be non-negative")
    return round(candidate.information_gain*2 + candidate.urgency - candidate.cost,6)

def plan_reviews(candidates):
    candidates=list(candidates)
    seen=set()
    for c in candidates:
        if not isinstance(c,ReviewCandidate): raise ValueError("invalid review candidate")
        if not c.action_id or c.action_id in seen: raise ValueError("review action ids must be unique and non-empty")
        seen.add(c.action_id)
    ranked=sorted(
        ({"action_id":c.action_id,"description":c.description,"score":score_candidate(c),
          "information_gain":c.information_gain,"urgency":c.urgency,"cost":c.cost} for c in candidates),
        key=lambda x:(-x["score"],x["action_id"]))
    return {"ranked_actions":ranked,
            "selected_next":ranked[0]["action_id"] if ranked else None,
            "note":"Ranks what to verify next, not what legal decision to make."}
