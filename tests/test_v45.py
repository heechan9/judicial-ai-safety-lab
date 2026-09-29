import pytest
from judicial_ai_safety_lab.review_planner import ReviewCandidate, belief_state, plan_reviews
from judicial_ai_safety_lab.comparison_guard import compare_records, collect_comparisons
from judicial_ai_safety_lab.verification_level import verification_level
from judicial_ai_safety_lab.baseline_guard import freeze_baseline, verify_baseline
from judicial_ai_safety_lab.environment_fingerprint import build_environment_fingerprint, compare_environment
from judicial_ai_safety_lab.privacy_release import privacy_release_guard

def test_belief_state_normalizes_and_never_claims_legal_correctness():
    x=belief_state(supported=2,uncertain=1,conflicting=1)
    assert abs(sum(x["belief"].values())-1)<1e-5
    assert x["review_required"]
    assert "not a probability" in x["note"]

def test_review_planner_ranks_verification_not_outcome():
    x=plan_reviews([
      ReviewCandidate("check-ccourt","헌재 상태 확인",information_gain=0.9,urgency=0.8,cost=0.2),
      ReviewCandidate("check-extra","추가 자료 확인",information_gain=0.4,urgency=0.2,cost=0.1)])
    assert x["selected_next"]=="check-ccourt"
    assert "not what legal decision" in x["note"]

def test_review_planner_rejects_duplicate_ids():
    with pytest.raises(ValueError):
        plan_reviews([ReviewCandidate("x","a",1),ReviewCandidate("x","b",2)])

def test_comparison_guard_aborts_identity_mismatch():
    with pytest.raises(ValueError):
        compare_records({"source_id":"A","scenario_id":"J1","result":"x"},
                        {"source_id":"B","scenario_id":"J1","result":"y"},
                        comparable_fields=("result",))

def test_comparison_guard_collects_valid_differences():
    x=collect_comparisons([
      ({"source_id":"A","scenario_id":"J1","result":"x"},
       {"source_id":"A","scenario_id":"J1","result":"y"}),
      ({"source_id":"A","scenario_id":"J2","result":"z"},
       {"source_id":"A","scenario_id":"J2","result":"z"})],
      comparable_fields=("result",))
    assert x["status"]=="FAIL"
    assert x["comparisons"][0]["status"]=="DIFFERENT"

def test_verification_level_separates_missing_original():
    x=verification_level(original_available=False,artifact_consistent=True)
    assert x["level"]=="UNVERIFIABLE_MISSING_ORIGINAL"

def test_verification_level_verified_requires_original_and_recompute():
    assert verification_level(original_available=True,independently_recomputed=True)["level"]=="VERIFIED"

def test_frozen_baseline_detects_posthoc_change():
    c={"source_snapshot":"S1","scenario_manifest":"M1","model_version":"V1",
       "prompt_hash":"P1","evaluation_contract":"E1"}
    frozen=freeze_baseline(c)
    changed=dict(c,source_snapshot="S2")
    assert verify_baseline(frozen,c)["matches"]
    assert verify_baseline(frozen,changed)["status"]=="BASELINE_CHANGED"

def test_environment_match_does_not_prove_historical_identity():
    a=build_environment_fingerprint(dependencies={"x":"1"},environment={"MODE":"test"},source_commit="a"*40)
    b=build_environment_fingerprint(dependencies={"x":"1"},environment={"MODE":"test"},source_commit="a"*40)
    x=compare_environment(a,b)
    assert x["metadata_match"] and not x["historical_environment_proven"]

def test_privacy_release_keeps_unverified_residual_scopes():
    x=privacy_release_guard(public_files_clean=True,public_ui_clean=True)
    assert x["current_public_clean"]
    assert set(x["residual_scope_unverified"])=={"git_history","prior_branches","external_caches"}
    assert x["requires_review"]
