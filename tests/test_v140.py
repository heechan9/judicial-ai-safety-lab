import json
from pathlib import Path
import pytest
from judicial_ai_safety_lab.expert_eval import ExpertRating
from judicial_ai_safety_lab.expert_reliability import quadratic_weighted_kappa
from judicial_ai_safety_lab.expert_adjudication import AdjudicationRecord,adjudication_gate
from judicial_ai_safety_lab.expert_reliability_cli import main as reliability_main
from judicial_ai_safety_lab.expert_adjudication_cli import main as adjudication_main

def _ratings():
    return [
      ExpertRating("R1","C1",5,5,4,5,4,False,""),
      ExpertRating("R2","C1",5,4,4,5,4,False,""),
      ExpertRating("R1","C2",4,4,3,4,5,False,""),
      ExpertRating("R2","C2",4,4,4,4,5,False,""),
    ]

def test_quadratic_weighted_kappa_two_reviewers():
    result=quadratic_weighted_kappa(_ratings())
    assert result["schema"]=="jaisl.expert-reliability.v1"
    assert result["eligible_cases"]==2
    assert set(result["dimensions"])=={
      "source_traceability","status_correctness","uncertainty_appropriateness",
      "human_review_appropriateness","explanation_clarity"
    }
    assert result["dimensions"]["source_traceability"]["comparisons"]==2

def test_kappa_requires_exactly_two_reviewers():
    with pytest.raises(ValueError):
        quadratic_weighted_kappa(_ratings()+[
          ExpertRating("R3","C1",5,5,5,5,5,False,"")
        ])

def test_adjudication_gate_preserves_unresolved_critical_error():
    records=[AdjudicationRecord(
      "C1","R3","2026-09-29T16:00:00+09:00",
      "CRITICAL_ERROR_CONFIRMED","추가 확인 필요",("R1:C1","R2:C1")
    )]
    result=adjudication_gate(["C1"],records)
    assert not result["ready_after_adjudication"]
    assert result["unresolved_case_ids"]==["C1"]

def test_adjudication_gate_can_clear_after_explicit_record():
    records=[AdjudicationRecord(
      "C1","R3","2026-09-29T16:00:00+09:00",
      "CRITICAL_ERROR_CLEARED","공식 근거 재확인 후 critical error 아님",("R1:C1","R2:C1")
    )]
    result=adjudication_gate(["C1"],records)
    assert result["ready_after_adjudication"]
    assert result["missing_case_ids"]==[]

def test_reliability_and_adjudication_clis(tmp_path):
    ratings=tmp_path/"ratings.json"
    ratings.write_text(json.dumps([r.__dict__ for r in _ratings()],ensure_ascii=False),encoding="utf-8")
    rout=tmp_path/"reliability.json"
    reliability_main(["--ratings",str(ratings),"--output",str(rout)])
    assert json.loads(rout.read_text(encoding="utf-8"))["eligible_cases"]==2

    critical=tmp_path/"critical.json"; critical.write_text(json.dumps(["C1"]),encoding="utf-8")
    records=tmp_path/"records.json"
    records.write_text(json.dumps([{
      "case_id":"C1","adjudicator_id":"R3","decided_at":"2026-09-29T16:00:00+09:00",
      "disposition":"CRITICAL_ERROR_CLEARED","rationale":"재검토 완료",
      "source_rating_ids":["R1:C1","R2:C1"]
    }],ensure_ascii=False),encoding="utf-8")
    aout=tmp_path/"adjudication.json"
    adjudication_main(["--critical-cases",str(critical),"--records",str(records),"--output",str(aout)])
    assert json.loads(aout.read_text(encoding="utf-8"))["ready_after_adjudication"]
