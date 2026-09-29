import json
import pytest
from judicial_ai_safety_lab.claim_audit import ClaimEvidence,audit_claims
from judicial_ai_safety_lab.quarantine import quarantine,transition
from judicial_ai_safety_lab.evidence_package import build_manifest,write_manifest
from judicial_ai_safety_lab.review_simulator import ReviewAction,simulate_review_path

def test_claim_audit_requires_refs_for_supported_claims():
    with pytest.raises(ValueError):
        audit_claims([ClaimEvidence("C1","x",verification_level="VERIFIED")])

def test_claim_audit_flags_public_unverified_claim():
    x=audit_claims([ClaimEvidence("C1","public claim",("doc:a",),"CONSISTENT_WITH_ARTIFACT",True),
                    ClaimEvidence("C2","missing original",(),"UNVERIFIABLE_MISSING_ORIGINAL",True)])
    assert x["pass_count"]==1 and x["review_count"]==1
    assert x["public_review_required"]

def test_quarantine_fix_retest_cycle():
    q=quarantine("E1","identity mismatch")
    transition(q,"fix","relinked source")
    transition(q,"retest_pass","identity verified")
    assert q.status=="closed"
    transition(q,"reopen","new mismatch")
    assert q.status=="quarantined"

def test_evidence_package_manifest(tmp_path):
    (tmp_path/"a.txt").write_text("hello",encoding="utf-8")
    (tmp_path/"b.json").write_text('{"x":1}',encoding="utf-8")
    m=build_manifest(tmp_path,["a.txt","b.json"],run_id="R1",status="COMPLETE",metadata={"commit":"a"*40})
    assert set(m["artifacts"])=={"a.txt","b.json"}
    assert m["limitations"][0]=="hash integrity is not authenticity"
    out=tmp_path/"manifest.json"; write_manifest(out,m)
    assert json.loads(out.read_text(encoding="utf-8"))["run_id"]=="R1"

def test_evidence_package_rejects_escape(tmp_path):
    other=tmp_path.parent/"outside.txt"; other.write_text("x",encoding="utf-8")
    with pytest.raises(ValueError): build_manifest(tmp_path,["../outside.txt"],run_id="R",status="X")

def test_review_simulator_prefers_fewer_open_findings_then_cost():
    actions=[
      ReviewAction("A",resolves=("u1",),cost=1),
      ReviewAction("B",resolves=("u2",),cost=1),
      ReviewAction("C",resolves=("u1","u2"),cost=3)]
    x=simulate_review_path(("u1","u2"),actions,max_depth=2)
    assert x["best_path"]["open"]==()
    assert x["best_path"]["cost"]==2
    assert x["best_path"]["path"] in (["A","B"],["B","A"])
    assert "not a legal-outcome" in x["note"]

def test_review_simulator_cannot_hide_new_uncertainty():
    x=simulate_review_path(("u1",),[ReviewAction("A",resolves=("u1",),introduces=("u2",),cost=1)],max_depth=1)
    assert x["best_path"]["open"]==("u2",)

def test_cli_integrates_v50_verification_planning(tmp_path,monkeypatch,capsys):
    import json
    from judicial_ai_safety_lab import cli
    data=tmp_path/"data"; data.mkdir()
    (data/"legal_sources.sample.json").write_text(json.dumps([
      {"source_id":"S1","institution":"moleg","source_type":"statute","title":"합성 법령","version":"1",
       "status":"effective","checksum":"demo"}],ensure_ascii=False),encoding="utf-8")
    (data/"scenarios.json").write_text(json.dumps([
      {"scenario_id":"J1","category":"normal","baseline_pass":True,"ai_pass":True},
      {"scenario_id":"J2","category":"source_change","baseline_pass":True,"ai_pass":False,"source_changed":True}
    ]),encoding="utf-8")
    monkeypatch.setattr(cli,"ROOT",tmp_path)
    monkeypatch.setattr(cli,"render",lambda report,path: None)
    monkeypatch.setattr(cli,"save_session",lambda *args,**kwargs: None)
    cli.main()
    report=json.loads((tmp_path/"results/assessment.json").read_text(encoding="utf-8"))
    vp=report["verification_planning"]
    assert vp["research_fixture_only"]
    assert vp["frozen_baseline"]["status"]=="FROZEN"
    assert vp["next_review_plan"]["selected_next"]=="review-source-change"
    assert vp["claim_audit"]["public_review_required"]

def test_evidence_package_rejects_symlink_and_overwrite(tmp_path):
    target=tmp_path/"real.txt"; target.write_text("x",encoding="utf-8")
    link=tmp_path/"link.txt"
    try:
        link.symlink_to(target)
    except OSError:
        pytest.skip("symlink unsupported")
    with pytest.raises(ValueError):
        build_manifest(tmp_path,["link.txt"],run_id="R",status="COMPLETE")
    m=build_manifest(tmp_path,["real.txt"],run_id="R",status="COMPLETE")
    out=tmp_path/"manifest.json"
    write_manifest(out,m)
    with pytest.raises(FileExistsError):
        write_manifest(out,m)
