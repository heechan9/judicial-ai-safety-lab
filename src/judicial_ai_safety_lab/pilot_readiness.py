"""Compute per-case readiness without upgrading evidence by inference."""

def evaluate_case_readiness(catalog, evidence_by_source=None, frozen_selection_ids=()):
    if not isinstance(catalog,dict) or not isinstance(catalog.get("cases"),list):
        raise ValueError("invalid catalog")
    evidence_by_source=evidence_by_source or {}
    frozen=set(frozen_selection_ids)
    rows=[]
    for row in catalog["cases"]:
        source_id=row["source_id"]
        evidence=evidence_by_source.get(source_id,{})
        raw=bool(evidence.get("api_raw_verified"))
        normalized=bool(evidence.get("normalized_detail_verified"))
        selected=source_id in frozen
        pilot_eligible=raw and normalized and selected
        rows.append({
          "case_id":row["case_id"],
          "source_id":source_id,
          "api_raw_verified":raw,
          "normalized_detail_verified":normalized,
          "selected_in_frozen_pilot":selected,
          "pilot_eligible":pilot_eligible,
          "missing":[name for name,ok in (
             ("api_raw_verified",raw),
             ("normalized_detail_verified",normalized),
             ("selected_in_frozen_pilot",selected),
          ) if not ok],
        })
    return {
      "schema":"jaisl.pilot-readiness.v1",
      "case_count":len(rows),
      "pilot_eligible_count":sum(x["pilot_eligible"] for x in rows),
      "cases":rows,
      "note":"Readiness is evidence-gated; discovery alone never makes a case pilot-eligible.",
    }
