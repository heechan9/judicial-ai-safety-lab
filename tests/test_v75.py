import pytest
from judicial_ai_safety_lab.pilot_selection import PilotCandidate,select_pilot
from judicial_ai_safety_lab.expert_packet import build_expert_packet
from judicial_ai_safety_lab.external_audit_registry import ExternalAudit,register_external_audit,external_validation_state

def test_pilot_selection_freezes_strata_and_order():
    rows=[
      PilotCandidate("P3","stable","C",{}),
      PilotCandidate("P1","stable","A",{}),
      PilotCandidate("P2","conflict","B",{}),
      PilotCandidate("P4","conflict","D",{}),
    ]
    x=select_pilot(rows,targets={"stable":1,"conflict":1},selection_note="pre-registered")
    assert [r["source_id"] for r in x["selected"]]==["P1","P2"]
    assert len(x["selection_hash"])==64

def test_pilot_selection_rejects_shortage():
    with pytest.raises(ValueError):
        select_pilot([PilotCandidate("P1","stable","A",{})],
                     targets={"stable":2},selection_note="fixed")

def test_expert_packet_blinds_review_ids_and_limits_scope():
    x=build_expert_packet([
      {"case_id":"CASE-1","source_refs":["PREC-1"],"system_output":"사람 검토 필요","review_reason":"source change"}
    ],target_commit="a"*40)
    assert x["cases"][0]["review_case_id"]=="E001"
    assert "judgment" in x["instructions"]["do_not_evaluate"]

def test_external_audit_registry_requires_traceable_completed_result():
    a=ExternalAudit("A1","Claude","AI reviewer","a"*40,"2026-09-29T12:00:00+09:00",
                    "UI/UX audit","docs/audits/result.md","COMPLETED")
    r=register_external_audit(a)
    assert r["status"]=="COMPLETED"
    s=external_validation_state([a])
    assert s["has_completed_ui_audit"]
    assert not s["has_completed_code_audit"]

def test_external_audit_rejects_fake_commit_or_naive_time():
    with pytest.raises(ValueError):
        register_external_audit(ExternalAudit("A","Jules","AI","short","2026-09-29T12:00:00",
                                              "code audit","x","COMPLETED"))
