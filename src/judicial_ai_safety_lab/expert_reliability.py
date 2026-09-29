"""Ordinal inter-rater reliability for JAISL expert review."""
from collections import defaultdict
from .expert_eval import DIMENSIONS,ExpertRating,validate_rating

def _quadratic_weight(a,b):
    return ((a-b)/4.0)**2

def quadratic_weighted_kappa(ratings):
    """Compute per-dimension quadratic weighted Cohen kappa for exactly two reviewers.

    Original ratings are not altered. This is a descriptive research metric,
    not proof of legal correctness.
    """
    ratings=list(ratings)
    for r in ratings:
        if not isinstance(r,ExpertRating):
            raise ValueError("ratings must contain ExpertRating objects")
        validate_rating(r)
    reviewers=sorted(set(r.reviewer_id for r in ratings))
    if len(reviewers)!=2:
        raise ValueError("exactly two reviewers required")
    by_case=defaultdict(dict)
    for r in ratings:
        if r.reviewer_id in by_case[r.case_id]:
            raise ValueError("duplicate reviewer/case rating")
        by_case[r.case_id][r.reviewer_id]=r
    shared=[v for v in by_case.values() if len(v)==2]
    if not shared:
        return {"schema":"jaisl.expert-reliability.v1","eligible_cases":0,"dimensions":{}}

    out={}
    for dim in DIMENSIONS:
        pairs=[(getattr(v[reviewers[0]],dim),getattr(v[reviewers[1]],dim)) for v in shared]
        n=len(pairs)
        observed=sum(_quadratic_weight(a,b) for a,b in pairs)/n
        pa={k:sum(a==k for a,_ in pairs)/n for k in range(1,6)}
        pb={k:sum(b==k for _,b in pairs)/n for k in range(1,6)}
        expected=sum(pa[a]*pb[b]*_quadratic_weight(a,b) for a in range(1,6) for b in range(1,6))
        if expected==0:
            kappa=1.0 if observed==0 else None
        else:
            kappa=1.0-observed/expected
        out[dim]={"kappa":None if kappa is None else round(kappa,4),"comparisons":n}
    return {
      "schema":"jaisl.expert-reliability.v1",
      "reviewers":reviewers,
      "eligible_cases":len(shared),
      "dimensions":out,
      "note":"Quadratic weighted Cohen kappa for ordinal 1-5 ratings; descriptive pilot reliability only.",
    }
