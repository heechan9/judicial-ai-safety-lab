"""Build expert-review case templates from normalized cases and scenario mappings."""
def build_expert_case_template(case,mappings):
    if not getattr(case,"case_id",None): raise ValueError("case id required")
    if not isinstance(mappings,list) or not mappings: raise ValueError("mappings required")
    return {
      "case_id":case.case_id,
      "source_refs":[case.source_id],
      "public_metadata":{
        "title":case.title,
        "case_number":case.case_number,
        "decision_date":case.decision_date,
        "court":case.court,
        "source_url":case.source_url,
      },
      "evidence_status":{
        "source_mode":case.source_mode,
        "api_raw_verified":case.api_raw_verified,
        "detail_verified":case.detail_verified,
      },
      "verification_tasks":[
        {"mapping_id":x["mapping_id"],"scenario_type":x["scenario_type"],
         "rationale":x["rationale"],"priority":x["priority"]}
        for x in mappings
      ],
      "system_output":None,
      "review_reason":"JAISL 평가 실행 전 템플릿",
      "expert_rating_status":"NOT_STARTED",
      "boundary":"전문가는 판결·형량 선택이 아니라 근거추적·상태·불확실성·사람검토 적절성을 평가",
    }
