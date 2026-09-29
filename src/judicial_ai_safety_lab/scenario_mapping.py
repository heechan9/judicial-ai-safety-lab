"""Map normalized precedent cases to verification scenarios.

Mappings explain what should be verified. They do not assign legal outcomes.
"""
from dataclasses import dataclass,asdict

SCENARIO_TYPES={
    "SOURCE_TRACEABILITY",
    "STATUS_CHECK",
    "CONFLICT_CHECK",
    "LEGAL_CHANGE_CHECK",
    "CONSTITUTIONAL_CHECK",
    "MISSING_INFORMATION",
    "ADVERSARIAL_ROBUSTNESS",
}

@dataclass(frozen=True)
class ScenarioMapping:
    mapping_id:str
    case_id:str
    scenario_type:str
    rationale:str
    required_source_refs:tuple[str,...]=()
    priority:int=3

def validate_mapping(mapping):
    if not isinstance(mapping,ScenarioMapping): raise ValueError("mapping must be ScenarioMapping")
    if not mapping.mapping_id or not mapping.case_id or not mapping.rationale:
        raise ValueError("mapping id, case id and rationale required")
    if mapping.scenario_type not in SCENARIO_TYPES:
        raise ValueError("unsupported scenario type")
    if type(mapping.priority) is not int or not 1<=mapping.priority<=5:
        raise ValueError("priority must be 1..5")
    return mapping

def build_default_mappings(case):
    """Create conservative verification mappings from known metadata only."""
    mappings=[
      ScenarioMapping(f"{case.case_id}-S1",case.case_id,"SOURCE_TRACEABILITY",
                      "공식 판례 식별자·사건번호·선고일·법원 정보 추적", (case.source_id,),5),
      ScenarioMapping(f"{case.case_id}-S2",case.case_id,"STATUS_CHECK",
                      "판례 메타데이터와 현재 근거 상태를 분리해 확인", (case.source_id,),4),
    ]
    if not getattr(case,"detail_verified",False):
        mappings.append(ScenarioMapping(
            f"{case.case_id}-S3",case.case_id,"MISSING_INFORMATION",
            "LAW_OC-backed 판례 상세가 아직 검증되지 않아 판시사항·판결요지 기반 평가는 보류",
            (case.source_id,),5))
    if getattr(case,"legal_change_relevance","unknown")!="none":
        mappings.append(ScenarioMapping(
            f"{case.case_id}-S4",case.case_id,"LEGAL_CHANGE_CHECK",
            "관련 법령 변경 여부를 별도 확인", (case.source_id,),3))
    if getattr(case,"constitutional_relevance","unknown")!="none":
        mappings.append(ScenarioMapping(
            f"{case.case_id}-S5",case.case_id,"CONSTITUTIONAL_CHECK",
            "헌법재판 상태 또는 헌법 관련 영향 여부를 별도 확인", (case.source_id,),3))
    return [asdict(validate_mapping(x)) for x in mappings]

def validate_mapping_set(rows):
    ids=set()
    for row in rows:
        validate_mapping(ScenarioMapping(**row))
        if row["mapping_id"] in ids: raise ValueError("duplicate mapping_id")
        ids.add(row["mapping_id"])
    return {"valid":True,"mapping_count":len(rows),"mapping_ids":sorted(ids)}
