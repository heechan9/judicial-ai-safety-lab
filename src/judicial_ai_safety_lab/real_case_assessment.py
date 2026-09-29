"""Build the first frozen JAISL real-data assessment after evidence preflight.

This layer assesses evidence traceability / verification routing only.
It does not predict judgments, sentences, verdicts, or legal correctness.
"""
import hashlib,json
from .public_discovery import validate_public_discovery
from .batch_reconcile import reconcile_discovery_batch
from .evidence_index import build_evidence_index
from .precedent_normalization import NormalizedPrecedentCase
from .scenario_mapping import build_default_mappings

def _hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def _case_from_dict(d):
    x=dict(d)
    x["related_articles"]=tuple(x.get("related_articles") or ())
    x["cited_precedents"]=tuple(x.get("cited_precedents") or ())
    return NormalizedPrecedentCase(**x)

def build_real_case_assessment(discovery,detail_envelopes,preflight,*,target_commit):
    validate_public_discovery(discovery)
    if not isinstance(preflight,dict) or preflight.get("schema")!="jaisl.pilot-preflight.v1":
        raise ValueError("valid pilot preflight required")
    if preflight.get("ready_for_real_data_run") is not True:
        raise ValueError("pilot preflight is not ready")
    if not isinstance(target_commit,str) or len(target_commit)!=40 or any(c not in "0123456789abcdef" for c in target_commit):
        raise ValueError("target_commit must be a full lowercase Git SHA")

    batch=reconcile_discovery_batch(discovery,detail_envelopes=detail_envelopes)
    index=build_evidence_index(batch)
    if batch["summary"]!={"total":30,"verified_detail_ready":30,"identity_review_required":0,"detail_pending":0}:
        raise ValueError("all 30 cases must be VERIFIED_DETAIL_READY")

    by_prec={str(k):v for k,v in detail_envelopes.items()}
    by_source={row["source_id"]:row for row in discovery["cases"]}
    ordered=sorted(discovery["cases"],key=lambda x:(x["domain"],x["decision_date"],x["source_id"]))
    cases=[]; expert_cases=[]
    for i,row in enumerate(ordered,1):
        case_id=f"JAISL-D{i:03d}"
        one=reconcile_discovery_batch(
            {"schema":discovery["schema"],"source_site":discovery["source_site"],
             "discovery_method":discovery["discovery_method"],"discovered_at":discovery["discovered_at"],
             "discovery_only":True,"pilot_selection_frozen":False,"note":discovery["note"],"cases":[row]},
            detail_envelopes={row["prec_seq"]:by_prec[row["prec_seq"]]}
        )
        status=one["cases"][0]["status"]
        if status!="VERIFIED_DETAIL_READY":
            raise ValueError(f"{case_id} is not verified")

        # Reconcile again through the shared single-case function to preserve normalized detail.
        from .evidence_reconcile import reconcile_case
        rec=reconcile_case(row,case_id=case_id,detail_envelope=by_prec[row["prec_seq"]])
        normalized=rec["normalized_case"]
        obj=_case_from_dict(normalized)
        mappings=build_default_mappings(obj)
        verification_summary=(
            "공식 판례 상세 응답과 사건 식별정보가 일치하고 원응답 해시와 정규화 해시가 고정되었다. "
            "이 상태는 근거 추적성 검증이며 판결의 법적 옳고 그름을 자동 판정하지 않는다."
        )
        case_result={
          "case_id":case_id,
          "source_id":row["source_id"],
          "prec_seq":row["prec_seq"],
          "domain":row["domain"],
          "verification_status":"VERIFIED_DETAIL_READY",
          "raw_response_hash":rec["raw_response_hash"],
          "normalized_hash":rec["normalized_hash"],
          "title_equivalence":rec.get("title_equivalence"),
          "normalized_case":normalized,
          "verification_tasks":mappings,
          "system_output":verification_summary,
          "human_review_required":any(m["scenario_type"] in {"LEGAL_CHANGE_CHECK","CONSTITUTIONAL_CHECK"} for m in mappings),
        }
        cases.append(case_result)
        expert_cases.append({
          "case_id":case_id,
          "source_refs":[row["source_id"]],
          "system_output":verification_summary,
          "review_reason":"공식 근거 추적·상태·불확실성·사람검토 적절성 평가",
        })

    frozen_payload={
      "target_commit":target_commit,
      "case_count":len(cases),
      "case_ids":[x["case_id"] for x in cases],
      "raw_hashes":[x["raw_response_hash"] for x in cases],
      "normalized_hashes":[x["normalized_hash"] for x in cases],
    }
    return {
      "schema":"jaisl.real-assessment.v1",
      "target_commit":target_commit,
      "case_count":len(cases),
      "verified_count":sum(x["verification_status"]=="VERIFIED_DETAIL_READY" for x in cases),
      "cases":cases,
      "expert_cases":expert_cases,
      "assessment_hash":_hash(frozen_payload),
      "frozen":True,
      "expert_packet_ready":True,
      "limitations":[
        "assessment verifies evidence provenance and routing, not legal correctness",
        "expert review is not yet completed",
        "real-data pilot does not constitute judicial certification",
      ],
    }
