import copy
import pytest
from judicial_ai_safety_lab.audit_chain import append_event,validate_chain
from judicial_ai_safety_lab.review_session import (
    ReviewActionContract,create_session,freeze_session,add_review_action,
    record_human_review,package_session)

def test_audit_chain_detects_tampering():
    chain=[]
    append_event(chain,"A",data={"x":1},at="2026-09-29T01:00:00+00:00")
    append_event(chain,"B",data={"y":2},at="2026-09-29T01:01:00+00:00")
    assert validate_chain(chain)["valid"]
    broken=copy.deepcopy(chain)
    broken[0]["data"]["x"]=999
    with pytest.raises(ValueError): validate_chain(broken)

def test_audit_chain_detects_reordering():
    chain=[]
    append_event(chain,"A",at="2026-09-29T01:00:00+00:00")
    append_event(chain,"B",at="2026-09-29T01:01:00+00:00")
    with pytest.raises(ValueError): validate_chain([chain[1],chain[0]])

def test_review_package_contains_valid_chain_head():
    s=create_session(session_id="S6",baseline_hash="a"*64,open_findings=("F1",))
    freeze_session(s)
    add_review_action(s,ReviewActionContract("A1","VERIFY_SOURCE","LAW-1","원본 확인"))
    record_human_review(s,disposition="검토 완료",resolved_findings=("F1",))
    p=package_session(s)
    assert p["audit_chain"]["valid"]
    assert p["payload"]["audit_chain_head"]==p["payload"]["audit_log"][-1]["event_hash"]
    assert p["package_event"]["prev_hash"]==p["payload"]["audit_chain_head"]

def test_audit_chain_naive_timestamp_rejected():
    chain=[]
    with pytest.raises(ValueError):
        append_event(chain,"A",at="2026-09-29T01:00:00")
