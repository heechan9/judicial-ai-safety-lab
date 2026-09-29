import json
from pathlib import Path
import pytest
from judicial_ai_safety_lab.expert_eval import ExpertRating
from judicial_ai_safety_lab.expert_review_gate import expert_review_gate
from judicial_ai_safety_lab.expert_rating_template import build_rating_templates
from judicial_ai_safety_lab.expert_review_gate_cli import main as gate_main
from judicial_ai_safety_lab.expert_rating_template_cli import main as template_main

def _packet():
    return {
      "schema":"jaisl.expert-packet.v1",
      "packet_version":"real-pilot-v1",
      "target_commit":"a"*40,
      "packet_hash":"b"*64,
      "cases":[
        {"review_case_id":"E001","case_id":"JAISL-D001","source_refs":["S1"],"system_output":"x","review_reason":"r"},
        {"review_case_id":"E002","case_id":"JAISL-D002","source_refs":["S2"],"system_output":"x","review_reason":"r"},
      ],
      "instructions":{"evaluate":"x","do_not_evaluate":"y"},
    }

def _rating(rid,cid,critical=False):
    return ExpertRating(rid,cid,5,5,4,5,4,critical_error=critical,comment="check" if critical else "")

def test_expert_gate_requires_two_reviews_per_case():
    ratings=[_rating("R1","JAISL-D001"),_rating("R1","JAISL-D002"),
             _rating("R2","JAISL-D001")]
    x=expert_review_gate(ratings,expected_case_ids=["JAISL-D001","JAISL-D002"])
    assert not x["coverage_complete"]
    assert x["missing_reviews_by_case"]=={"JAISL-D002":1}
    assert "INCOMPLETE_CASE_COVERAGE" in x["blockers"]

def test_expert_gate_complete_without_critical_errors():
    ratings=[_rating(r,c) for r in ("R1","R2") for c in ("JAISL-D001","JAISL-D002")]
    x=expert_review_gate(ratings,expected_case_ids=["JAISL-D001","JAISL-D002"])
    assert x["coverage_complete"] and x["ready_to_summarize"]
    assert x["ratings_count"]==4 and x["blockers"]==[]

def test_expert_gate_critical_error_requires_adjudication():
    ratings=[_rating(r,c,critical=(r=="R2" and c=="JAISL-D002"))
             for r in ("R1","R2") for c in ("JAISL-D001","JAISL-D002")]
    x=expert_review_gate(ratings,expected_case_ids=["JAISL-D001","JAISL-D002"])
    assert x["coverage_complete"] and not x["ready_to_summarize"]
    assert "CRITICAL_ERRORS_REQUIRE_ADJUDICATION" in x["blockers"]

def test_expert_gate_rejects_duplicate_reviewer_case():
    with pytest.raises(ValueError):
        expert_review_gate([_rating("R1","JAISL-D001"),_rating("R1","JAISL-D001")],
                           expected_case_ids=["JAISL-D001"])

def test_rating_template_has_null_scores_and_two_reviewers():
    t=build_rating_templates(_packet(),["R1","R2"])
    assert t["packet_hash"]=="b"*64
    assert t["templates"]["R1"][0]["source_traceability"] is None
    assert len(t["templates"]["R2"])==2

def test_rating_template_and_gate_clis(tmp_path):
    packet=tmp_path/"packet.json"; reviewers=tmp_path/"reviewers.json"
    packet.write_text(json.dumps(_packet(),ensure_ascii=False),encoding="utf-8")
    reviewers.write_text(json.dumps(["R1","R2"]),encoding="utf-8")
    template=tmp_path/"template.json"
    template_main(["--packet",str(packet),"--reviewers",str(reviewers),"--output",str(template)])
    t=json.loads(template.read_text(encoding="utf-8"))
    assert len(t["templates"])==2

    ratings=[]
    for r in ("R1","R2"):
        for c in ("JAISL-D001","JAISL-D002"):
            ratings.append({
              "reviewer_id":r,"case_id":c,"source_traceability":5,"status_correctness":5,
              "uncertainty_appropriateness":4,"human_review_appropriateness":5,
              "explanation_clarity":4,"critical_error":False,"comment":""
            })
    rp=tmp_path/"ratings.json"; rp.write_text(json.dumps(ratings),encoding="utf-8")
    out=tmp_path/"gate.json"
    gate_main(["--ratings",str(rp),"--packet",str(packet),"--output",str(out)])
    g=json.loads(out.read_text(encoding="utf-8"))
    assert g["ready_to_summarize"]
