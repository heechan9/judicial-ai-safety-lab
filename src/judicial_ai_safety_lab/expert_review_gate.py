"""Fail-closed completion gate for independent expert ratings.

The gate checks coverage and independence metadata only. It does not decide
whether the system is legally correct or judicially certified.
"""
from collections import Counter,defaultdict
from .expert_eval import ExpertRating,validate_rating,DIMENSIONS

def expert_review_gate(ratings,*,expected_case_ids,min_reviewers=2):
    ratings=list(ratings)
    expected=list(expected_case_ids)
    if not expected or len(expected)!=len(set(expected)):
        raise ValueError("expected_case_ids must be unique and non-empty")
    if type(min_reviewers) is not int or min_reviewers<2:
        raise ValueError("min_reviewers must be at least 2")

    seen=set()
    by_case=defaultdict(set)
    by_reviewer=defaultdict(set)
    critical=[]
    for r in ratings:
        if not isinstance(r,ExpertRating):
            raise ValueError("ratings must contain ExpertRating objects")
        validate_rating(r)
        key=(r.reviewer_id,r.case_id)
        if key in seen:
            raise ValueError(f"duplicate reviewer/case rating: {r.reviewer_id}/{r.case_id}")
        seen.add(key)
        if r.case_id not in expected:
            raise ValueError(f"unexpected case_id: {r.case_id}")
        by_case[r.case_id].add(r.reviewer_id)
        by_reviewer[r.reviewer_id].add(r.case_id)
        if r.critical_error:
            critical.append({"reviewer_id":r.reviewer_id,"case_id":r.case_id,"comment":r.comment})

    reviewers=sorted(by_reviewer)
    missing_by_case={
      cid: min_reviewers-len(by_case.get(cid,set()))
      for cid in expected if len(by_case.get(cid,set()))<min_reviewers
    }
    missing_by_reviewer={
      rid: sorted(set(expected)-cases)
      for rid,cases in by_reviewer.items() if set(expected)-cases
    }

    complete=(len(reviewers)>=min_reviewers and not missing_by_case)
    blockers=[]
    if len(reviewers)<min_reviewers: blockers.append("INSUFFICIENT_INDEPENDENT_REVIEWERS")
    if missing_by_case: blockers.append("INCOMPLETE_CASE_COVERAGE")
    if critical: blockers.append("CRITICAL_ERRORS_REQUIRE_ADJUDICATION")

    return {
      "schema":"jaisl.expert-review-gate.v1",
      "expected_case_count":len(expected),
      "reviewer_count":len(reviewers),
      "ratings_count":len(ratings),
      "minimum_reviewers_per_case":min_reviewers,
      "coverage_complete":complete,
      "critical_error_count":len(critical),
      "critical_errors":critical,
      "missing_reviews_by_case":missing_by_case,
      "missing_cases_by_reviewer":missing_by_reviewer,
      "ready_to_summarize":complete and not critical,
      "blockers":blockers,
      "note":"Completion gate for research expert review only; not judicial certification.",
    }
