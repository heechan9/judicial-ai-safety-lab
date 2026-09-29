"""Expert evaluation contract for JAISL outputs.

Designed for evaluating source/evidence handling, uncertainty, review routing,
and explanation quality — not for asking the system to choose case outcomes.
"""
from dataclasses import dataclass,asdict
from statistics import mean,median

DIMENSIONS=(
 "source_traceability",
 "status_correctness",
 "uncertainty_appropriateness",
 "human_review_appropriateness",
 "explanation_clarity",
)

@dataclass(frozen=True)
class ExpertRating:
    reviewer_id:str
    case_id:str
    source_traceability:int
    status_correctness:int
    uncertainty_appropriateness:int
    human_review_appropriateness:int
    explanation_clarity:int
    critical_error:bool=False
    comment:str=""

def validate_rating(r):
    if not isinstance(r,ExpertRating): raise ValueError("rating must be ExpertRating")
    if not r.reviewer_id or not r.case_id: raise ValueError("reviewer_id and case_id are required")
    for d in DIMENSIONS:
        v=getattr(r,d)
        if type(v) is not int or not 1<=v<=5: raise ValueError(f"{d} must be 1..5")
    return r

def summarize_ratings(ratings):
    ratings=list(ratings)
    if not ratings: raise ValueError("ratings required")
    for r in ratings: validate_rating(r)
    reviewers=sorted(set(r.reviewer_id for r in ratings))
    cases=sorted(set(r.case_id for r in ratings))
    per_dimension={}
    for d in DIMENSIONS:
        vals=[getattr(r,d) for r in ratings]
        per_dimension[d]={"mean":round(mean(vals),3),"median":median(vals),"n":len(vals)}
    critical=[asdict(r) for r in ratings if r.critical_error]
    return {
      "reviewer_count":len(reviewers),
      "case_count":len(cases),
      "ratings_count":len(ratings),
      "dimensions":per_dimension,
      "critical_error_count":len(critical),
      "critical_errors":critical,
      "note":"Descriptive expert-evaluation summary; not an official judicial certification.",
    }

def pairwise_exact_agreement(ratings):
    """Exact 1–5 agreement for cases rated by exactly two reviewers."""
    ratings=list(ratings)
    grouped={}
    for r in ratings:
        validate_rating(r)
        grouped.setdefault(r.case_id,[]).append(r)
    eligible=[v for v in grouped.values() if len(v)==2]
    if not eligible: return {"eligible_cases":0,"agreement":None}
    matches=0; total=0
    for pair in eligible:
        for d in DIMENSIONS:
            matches += getattr(pair[0],d)==getattr(pair[1],d)
            total += 1
    return {"eligible_cases":len(eligible),"agreement":round(matches/total,4),"comparisons":total}
