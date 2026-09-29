"""Preflight a frozen cohort for real-data JAISL execution and expert review.

This gate does not run legal analysis. It checks whether the evidence needed to
run the pre-registered cohort exists and whether any identity conflicts remain.
"""
def pilot_preflight(*,cohort,batch_reconciliation,evidence_index):
    if not isinstance(cohort,dict) or cohort.get("schema")!="jaisl.cohort-freeze.v1":
        raise ValueError("valid frozen cohort required")
    if not cohort.get("membership_locked") or cohort.get("outcome_reviewed_before_freeze") is not False:
        raise ValueError("cohort must be locked before outcome review")
    if not isinstance(batch_reconciliation,dict) or batch_reconciliation.get("schema")!="jaisl.batch-reconcile.v1":
        raise ValueError("valid batch reconciliation required")
    if not isinstance(evidence_index,dict) or evidence_index.get("schema")!="jaisl.evidence-index.v1":
        raise ValueError("valid evidence index required")

    expected=set(cohort.get("source_ids",[]))
    actual=set(evidence_index.get("index",{}))
    missing_sources=sorted(expected-actual)
    extra_sources=sorted(actual-expected)
    statuses={sid:evidence_index["index"][sid]["status"] for sid in sorted(actual & expected)}
    pending=sorted(sid for sid,status in statuses.items() if status=="DETAIL_PENDING")
    review=sorted(sid for sid,status in statuses.items() if status=="IDENTITY_REVIEW_REQUIRED")
    verified=sorted(sid for sid,status in statuses.items() if status=="VERIFIED_DETAIL_READY")
    unknown=sorted(sid for sid,status in statuses.items()
                   if status not in {"DETAIL_PENDING","IDENTITY_REVIEW_REQUIRED","VERIFIED_DETAIL_READY"})

    ready=(not missing_sources and not extra_sources and not pending and not review and not unknown
           and len(verified)==len(expected))
    blockers=[]
    if missing_sources: blockers.append("MISSING_EVIDENCE_INDEX_SOURCES")
    if extra_sources: blockers.append("EXTRA_EVIDENCE_INDEX_SOURCES")
    if pending: blockers.append("DETAIL_PENDING")
    if review: blockers.append("IDENTITY_REVIEW_REQUIRED")
    if unknown: blockers.append("UNKNOWN_EVIDENCE_STATUS")
    if len(verified)!=len(expected): blockers.append("COHORT_NOT_FULLY_VERIFIED")
    return {
      "schema":"jaisl.pilot-preflight.v1",
      "ready_for_real_data_run":ready,
      "ready_for_expert_packet":False,
      "cohort_member_count":len(expected),
      "verified_count":len(verified),
      "pending_count":len(pending),
      "identity_review_count":len(review),
      "missing_sources":missing_sources,
      "extra_sources":extra_sources,
      "blockers":list(dict.fromkeys(blockers)),
      "note":"Expert packet readiness remains false until JAISL outputs are produced and frozen after this evidence preflight.",
    }
