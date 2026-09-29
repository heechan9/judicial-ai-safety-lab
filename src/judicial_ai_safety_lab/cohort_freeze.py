"""Freeze the entire discovered precedent cohort before outcome review.

For the first pilot, freezing all 30 discovered cases avoids post-hoc case
selection. Verification tags may be added later, but membership cannot change
without creating a new cohort version.
"""
import hashlib,json

def _hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def freeze_full_cohort(discovery,*,cohort_id,rule,cutoff):
    cases=discovery.get("cases") if isinstance(discovery,dict) else None
    if not isinstance(cases,list) or not cases:
        raise ValueError("discovery cases required")
    if discovery.get("discovery_only") is not True:
        raise ValueError("source must be a discovery document")
    if not isinstance(cohort_id,str) or not cohort_id.strip():
        raise ValueError("cohort_id required")
    if not isinstance(rule,str) or not rule.strip():
        raise ValueError("cohort rule required")
    ids=[x.get("source_id") for x in cases]
    if any(not isinstance(x,str) or not x for x in ids) or len(ids)!=len(set(ids)):
        raise ValueError("source ids must be unique and non-empty")
    ordered=sorted(ids)
    payload={
      "cohort_id":cohort_id.strip(),
      "source_discovery_schema":discovery.get("schema"),
      "membership_rule":rule.strip(),
      "cutoff":cutoff,
      "member_count":len(ordered),
      "source_ids":ordered,
    }
    return {
      "schema":"jaisl.cohort-freeze.v1",
      **payload,
      "cohort_hash":_hash(payload),
      "membership_locked":True,
      "outcome_reviewed_before_freeze":False,
      "limitations":[
        "cohort freeze fixes membership, not legal labels",
        "later exclusions require a new version and explicit reason",
        "API/detail verification remains separate from cohort membership",
      ],
    }

def verify_frozen_cohort(cohort,discovery):
    if cohort.get("schema")!="jaisl.cohort-freeze.v1":
        raise ValueError("unsupported cohort schema")
    expected=freeze_full_cohort(
        discovery,
        cohort_id=cohort["cohort_id"],
        rule=cohort["membership_rule"],
        cutoff=cohort["cutoff"],
    )
    for key in ("member_count","source_ids","cohort_hash","membership_locked","outcome_reviewed_before_freeze"):
        if cohort.get(key)!=expected.get(key):
            raise ValueError(f"cohort mismatch: {key}")
    return {"valid":True,"member_count":cohort["member_count"],"cohort_hash":cohort["cohort_hash"]}
