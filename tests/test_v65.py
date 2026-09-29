import copy
import json
import pytest
from judicial_ai_safety_lab.assessment_contract import build_assessment_contract,validate_assessment_contract
from judicial_ai_safety_lab.review_session import (
    ReviewActionContract,create_session,freeze_session,add_review_action,
    record_human_review,package_session)
from judicial_ai_safety_lab.package_verify import verify_review_package

def sample_report():
    return {
      "decision":"HUMAN_REVIEW_REQUIRED",
      "verification_planning":{
        "research_fixture_only":True,
        "frozen_baseline":{"status":"FROZEN","baseline_hash":"a"*64},
        "finding_registry":{"open_ids":["F1"]},
        "review_session":{
          "session_id":"S1",
          "state":"REVIEW_PENDING",
          "actions":[{"action_id":"A1","action_type":"VERIFY_SOURCE","target_ref":"LAW-1","rationale":"원본 확인"}],
          "human_disposition":None,
        },
      },
    }

def test_assessment_contract_requires_review_pending_and_no_fake_human_disposition():
    c=build_assessment_contract(sample_report())
    assert validate_assessment_contract(c)["valid"]
    bad=sample_report()
    bad["verification_planning"]["review_session"]["human_disposition"]="자동 입력"
    with pytest.raises(ValueError): build_assessment_contract(bad)

def test_assessment_contract_rejects_duplicate_finding_ids():
    c=build_assessment_contract(sample_report())
    c["finding_ids"]=["F1","F1"]
    with pytest.raises(ValueError): validate_assessment_contract(c)

def test_review_package_verifier_detects_payload_tamper():
    s=create_session(session_id="S1",baseline_hash="a"*64,open_findings=("F1",))
    freeze_session(s)
    add_review_action(s,ReviewActionContract("A1","VERIFY_SOURCE","LAW-1","원본 확인"))
    record_human_review(s,disposition="검토 완료",resolved_findings=("F1",))
    p=package_session(s)
    assert verify_review_package(p)["valid"]
    tampered=copy.deepcopy(p)
    tampered["payload"]["human_disposition"]="변조"
    with pytest.raises(ValueError): verify_review_package(tampered)

def test_review_package_verifier_detects_package_event_tamper():
    s=create_session(session_id="S2",baseline_hash="b"*64,open_findings=("F1",))
    freeze_session(s)
    add_review_action(s,ReviewActionContract("A1","CHECK_CONFLICT","X","상충 확인"))
    record_human_review(s,disposition="검토",resolved_findings=())
    p=package_session(s)
    broken=copy.deepcopy(p)
    broken["package_event"]["prev_hash"]="0"*64
    with pytest.raises(ValueError): verify_review_package(broken)
