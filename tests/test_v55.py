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

def test_cli_stops_at_review_pending_without_fake_human_decision(tmp_path,monkeypatch):
    import json
    from judicial_ai_safety_lab import cli
    data=tmp_path/"data"; data.mkdir()
    (data/"legal_sources.sample.json").write_text(json.dumps([
      {"source_id":"S1","institution":"moleg","source_type":"statute","title":"합성 법령","version":"1",
       "status":"effective","checksum":"demo"}],ensure_ascii=False),encoding="utf-8")
    (data/"scenarios.json").write_text(json.dumps([
      {"scenario_id":"J1","category":"normal","baseline_pass":True,"ai_pass":True},
      {"scenario_id":"J2","category":"prompt_injection","baseline_pass":True,"ai_pass":False,
       "attacked":True,"severity":4}
    ]),encoding="utf-8")
    monkeypatch.setattr(cli,"ROOT",tmp_path)
    monkeypatch.setattr(cli,"render",lambda report,path: None)
    monkeypatch.setattr(cli,"save_session",lambda *args,**kwargs: None)
    cli.main()
    report=json.loads((tmp_path/"results/assessment.json").read_text(encoding="utf-8"))
    vp=report["verification_planning"]
    assert vp["review_policy"]["allowed"]
    assert vp["review_session"]["state"]=="REVIEW_PENDING"
    assert vp["review_session"]["human_disposition"] is None
    assert vp["finding_registry"]["count"]>=1

def test_review_cli_packages_only_after_explicit_human_disposition(tmp_path):
    import json
    from judicial_ai_safety_lab.review_cli import review_assessment, main as review_main
    report={
      "decision":"HUMAN_REVIEW_REQUIRED",
      "verification_planning":{
        "research_fixture_only":True,
        "frozen_baseline":{"status":"FROZEN","baseline_hash":"a"*64},
        "finding_registry":{"open_ids":["F1","F2"]},
        "review_session":{
          "session_id":"S1","state":"REVIEW_PENDING","human_disposition":None,
          "actions":[
            {"action_id":"A1","action_type":"VERIFY_SOURCE","target_ref":"LAW-1","rationale":"원본 확인"}
          ]
        }
      }
    }
    from judicial_ai_safety_lab.assessment_contract import build_assessment_contract
    report["assessment_contract"]=build_assessment_contract(report)
    packaged=review_assessment(report,disposition="F1 확인 완료",resolved_findings=["F1"])
    assert packaged["state"]=="PACKAGED"
    assert packaged["payload"]["open_findings"]==["F2"]
    assert packaged["payload"]["human_disposition"]=="F1 확인 완료"

    assessment=tmp_path/"assessment.json"
    assessment.write_text(json.dumps(report,ensure_ascii=False),encoding="utf-8")
    output=tmp_path/"reviewed.json"
    review_main(["--assessment",str(assessment),"--disposition","검토 완료","--resolve","F1","--output",str(output)])
    saved=json.loads(output.read_text(encoding="utf-8"))
    assert saved["state"]=="PACKAGED"
    with pytest.raises(FileExistsError):
        review_main(["--assessment",str(assessment),"--disposition","재실행","--output",str(output)])

def test_review_cli_rejects_unknown_finding_resolution():
    from judicial_ai_safety_lab.review_cli import review_assessment
    report={"decision":"HUMAN_REVIEW_REQUIRED","verification_planning":{
      "research_fixture_only":True,
      "frozen_baseline":{"status":"FROZEN","baseline_hash":"a"*64},
      "finding_registry":{"open_ids":["F1"]},
      "review_session":{"session_id":"S1","state":"REVIEW_PENDING","human_disposition":None,"actions":[
        {"action_id":"A1","action_type":"CHECK_CONFLICT","target_ref":"X","rationale":"확인"}]}}}
    from judicial_ai_safety_lab.assessment_contract import build_assessment_contract
    report["assessment_contract"]=build_assessment_contract(report)
    with pytest.raises(ValueError):
        review_assessment(report,disposition="검토",resolved_findings=["NOPE"])

def test_packaged_payload_is_immutable_snapshot_of_prepackage_audit_log():
    from judicial_ai_safety_lab.review_session import create_session,freeze_session,add_review_action,record_human_review,package_session,ReviewActionContract
    s=create_session(session_id="S2",baseline_hash="b"*64,open_findings=("F1",))
    freeze_session(s)
    add_review_action(s,ReviewActionContract("A1","VERIFY_SOURCE","LAW-1","원본 확인"))
    record_human_review(s,disposition="검토 완료",resolved_findings=("F1",))
    p=package_session(s)
    assert p["payload"]["audit_log"][-1]["event"]=="HUMAN_REVIEW_RECORDED"
    assert p["package_event"]["event"]=="SESSION_PACKAGED"
    assert all(x["event"]!="SESSION_PACKAGED" for x in p["payload"]["audit_log"])

def test_review_session_requires_real_sha256_baseline():
    from judicial_ai_safety_lab.review_session import create_session
    with pytest.raises(ValueError):
        create_session(session_id="S3",baseline_hash="g"*64)
