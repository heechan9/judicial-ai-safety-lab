import json
import pytest
from judicial_ai_safety_lab.validation_gate import external_validation_gate
from judicial_ai_safety_lab.expert_packet_cli import main as packet_main
from judicial_ai_safety_lab.validation_cli import main as validation_main
from judicial_ai_safety_lab.precedent_fetch import search_precedents,fetch_precedent_detail

def test_validation_gate_does_not_skip_missing_stages():
    x=external_validation_gate(internal_ci=True)
    assert x["current_state"]=="INTERNAL_VERIFIED"
    assert "real_data_manifest" in x["missing"]

def test_validation_gate_reaches_external_pilot_only_with_all_evidence():
    x=external_validation_gate(
      internal_ci=True,
      real_data_manifest={"valid":True},
      pilot_selection={"selected_count":30,"selection_hash":"a"*64},
      expert_summary={"reviewer_count":2,"case_count":30},
      audit_state={"has_completed_code_audit":True},
      claim_audit={"public_review_required":False},
    )
    assert x["current_state"]=="EXTERNALLY_VALIDATED_PILOT"
    assert x["missing"]==[]

def test_precedent_fetch_uses_injected_fetcher_without_exposing_credential():
    seen=[]
    def fake(url):
        seen.append(url)
        return {"ok":True}
    x=search_precedents("손해배상",oc="secret-demo",fetcher=fake,display=5,page=1)
    assert x["response"]=={"ok":True}
    assert "secret-demo" in seen[0]
    assert "secret-demo" not in json.dumps(x,ensure_ascii=False)
    y=fetch_precedent_detail("228541",oc="secret-demo",fetcher=fake)
    assert y=={"ok":True}

def test_expert_packet_cli(tmp_path):
    cases=tmp_path/"cases.json"
    cases.write_text(json.dumps([{
      "case_id":"CASE-1","source_refs":["PREC-1"],
      "system_output":"사람 검토 필요","review_reason":"근거 변경"
    }],ensure_ascii=False),encoding="utf-8")
    out=tmp_path/"packet.json"
    packet_main(["--cases",str(cases),"--target-commit","a"*40,"--output",str(out)])
    packet=json.loads(out.read_text(encoding="utf-8"))
    assert packet["cases"][0]["review_case_id"]=="E001"
    assert packet["target_commit"]=="a"*40

def test_validation_cli(tmp_path):
    manifest=tmp_path/"manifest.json"
    manifest.write_text(json.dumps({"valid":True}),encoding="utf-8")
    pilot=tmp_path/"pilot.json"
    pilot.write_text(json.dumps({"selected_count":30,"selection_hash":"a"*64}),encoding="utf-8")
    expert=tmp_path/"expert.json"
    expert.write_text(json.dumps({"reviewer_count":2,"case_count":30}),encoding="utf-8")
    audit=tmp_path/"audit.json"
    audit.write_text(json.dumps({"has_completed_code_audit":True}),encoding="utf-8")
    claim=tmp_path/"claim.json"
    claim.write_text(json.dumps({"public_review_required":False}),encoding="utf-8")
    out=tmp_path/"state.json"
    validation_main([
      "--internal-ci","--real-data-manifest",str(manifest),"--pilot-selection",str(pilot),
      "--expert-summary",str(expert),"--audit-state",str(audit),"--claim-audit",str(claim),
      "--output",str(out)
    ])
    result=json.loads(out.read_text(encoding="utf-8"))
    assert result["current_state"]=="EXTERNALLY_VALIDATED_PILOT"

def test_raw_precedent_collection_never_persists_credential():
    from judicial_ai_safety_lab.precedent_collect import collect_raw_precedents,verify_raw_collection
    seen=[]
    def fake(url):
        seen.append(url)
        return {"PrecSearch":{"totalCnt":"1","prec":[{"판례정보일련번호":"1"}]}}
    result=collect_raw_precedents("손해배상",oc="top-secret",fetcher=fake,display=1,page=1)
    assert verify_raw_collection(result)["valid"]
    dumped=json.dumps(result,ensure_ascii=False)
    assert "top-secret" not in dumped
    assert result["credential_stored"] is False
    assert "target=prec" in seen[0]

def test_raw_precedent_collection_detects_tamper():
    from judicial_ai_safety_lab.precedent_collect import collect_raw_precedents,verify_raw_collection
    result=collect_raw_precedents("x",oc="secret",fetcher=lambda url:{"a":1})
    result["raw_response"]["a"]=2
    with pytest.raises(ValueError):
        verify_raw_collection(result)
