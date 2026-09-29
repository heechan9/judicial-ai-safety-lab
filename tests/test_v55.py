import pytest
from judicial_ai_safety_lab.review_session import (
    ReviewActionContract,create_session,freeze_session,add_review_action,
    record_human_review,package_session,validate_action)
from judicial_ai_safety_lab.review_policy import guard_review_plan
from judicial_ai_safety_lab.finding_registry import Finding,register_findings

def test_review_action_contract_allows_only_verification_actions():
    ok=ReviewActionContract("A1","VERIFY_SOURCE","LAW-1","근거 원본 확인")
    assert validate_action(ok).action_type=="VERIFY_SOURCE"
    bad=ReviewActionContract("A2","RECOMMEND_JUDGMENT","CASE-1","판결 선택")
    with pytest.raises(ValueError): validate_action(bad)

def test_review_session_end_to_end_requires_human_step():
    s=create_session(session_id="S1",baseline_hash="a"*64,open_findings=("F1","F2"))
    freeze_session(s)
    add_review_action(s,ReviewActionContract("A1","VERIFY_SOURCE","LAW-1","변경 근거 확인"))
    with pytest.raises(ValueError): package_session(s)
    record_human_review(s,disposition="추가 확인 후 연구용 결과 유지",resolved_findings=("F1",))
    p=package_session(s)
    assert p["state"]=="PACKAGED"
    assert p["payload"]["open_findings"]==["F2"]
    assert "not a legal judgment" in p["note"]

def test_review_session_rejects_unknown_resolved_finding():
    s=create_session(session_id="S1",baseline_hash="a"*64,open_findings=("F1",))
    freeze_session(s)
    add_review_action(s,ReviewActionContract("A1","CHECK_CONFLICT","S1","상충 확인"))
    with pytest.raises(ValueError):
        record_human_review(s,disposition="검토",resolved_findings=("NOPE",))

def test_review_policy_blocks_legal_outcome_action_types():
    x=guard_review_plan([{"action_type":"VERIFY_SOURCE"},{"action_type":"RECOMMEND_SENTENCE"}])
    assert not x["allowed"]
    assert x["blocked_action_types"]==["RECOMMEND_SENTENCE"]

def test_finding_registry_preserves_identity_and_scope():
    x=register_findings([
      Finding("F1","SOURCE_CHANGED","LAW-1",4,"법적 근거 변경"),
      Finding("F2","TECHNICAL_FAILURE","J4",5,"공격 시험 실패")])
    assert x["count"]==2 and x["open_ids"]==["F1","F2"]

def test_finding_registry_rejects_unknown_kind():
    with pytest.raises(ValueError):
        register_findings([Finding("F1","LEGAL_OUTCOME","CASE",5,"bad")])
