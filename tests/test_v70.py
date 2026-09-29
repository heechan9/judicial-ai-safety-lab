import pytest
from judicial_ai_safety_lab.precedent_connector import precedent_search_url,precedent_detail_url,normalize_precedent
from judicial_ai_safety_lab.real_data_protocol import build_real_data_manifest,verify_real_data_manifest
from judicial_ai_safety_lab.expert_eval import ExpertRating,summarize_ratings,pairwise_exact_agreement

def test_precedent_urls_require_credential_and_pin_target(monkeypatch):
    monkeypatch.delenv("LAW_OC",raising=False)
    with pytest.raises(ValueError): precedent_search_url("손해배상",oc=None)
    u=precedent_search_url("손해배상",oc="demo",display=10,page=2,org="400201")
    assert "target=prec" in u and "type=JSON" in u and "display=10" in u and "page=2" in u
    d=precedent_detail_url("228541",oc="demo")
    assert "target=prec" in d and "ID=228541" in d

def test_normalize_official_precedent_shape():
    r=normalize_precedent({"판례정보일련번호":228541,"사건명":"합성 사건명","사건번호":"2026다123",
                           "선고일자":20260901,"법원명":"대법원"})
    assert r.source_id=="PREC-228541"
    assert r.institution=="court"
    assert r.canonical_ref=="대법원 2026다123"

def test_real_data_manifest_freezes_identity_order_and_hash():
    records=[{"source_id":"PREC-1","title":"A"},{"source_id":"PREC-2","title":"B"}]
    m=build_real_data_manifest(records,source_name="국가법령정보 공동활용",
        source_url="https://www.law.go.kr/DRF/",cutoff="2026-09-29T00:00:00+09:00",
        selection_rule="published precedents selected before evaluation")
    assert verify_real_data_manifest(records,m)["valid"]
    with pytest.raises(ValueError): verify_real_data_manifest(list(reversed(records)),m)

def test_real_data_manifest_rejects_duplicate_ids():
    rows=[{"source_id":"X"},{"source_id":"X"}]
    with pytest.raises(ValueError):
        build_real_data_manifest(rows,source_name="x",source_url="https://example.com",
            cutoff="2026-09-29T00:00:00+09:00",selection_rule="fixed")

def test_expert_eval_summary_and_agreement():
    ratings=[
      ExpertRating("R1","C1",5,4,4,5,4,False,""),
      ExpertRating("R2","C1",5,4,3,5,4,False,""),
      ExpertRating("R1","C2",4,4,4,4,4,True,"근거 상태 확인 필요"),
      ExpertRating("R2","C2",4,4,4,4,4,False,""),
    ]
    s=summarize_ratings(ratings)
    assert s["reviewer_count"]==2 and s["case_count"]==2 and s["critical_error_count"]==1
    a=pairwise_exact_agreement(ratings)
    assert a["eligible_cases"]==2 and 0<=a["agreement"]<=1

def test_expert_eval_rejects_out_of_range_rating():
    bad=ExpertRating("R1","C1",6,4,4,4,4)
    with pytest.raises(ValueError): summarize_ratings([bad])

def test_real_data_cli_and_expert_cli(tmp_path):
    import json
    from judicial_ai_safety_lab.real_data_cli import main as real_main
    from judicial_ai_safety_lab.expert_cli import main as expert_main

    records=tmp_path/"records.json"
    records.write_text(json.dumps([
      {"source_id":"PREC-1","title":"A"},
      {"source_id":"PREC-2","title":"B"}
    ],ensure_ascii=False),encoding="utf-8")
    manifest=tmp_path/"manifest.json"
    real_main([
      "--records",str(records),
      "--source-name","국가법령정보 공동활용",
      "--source-url","https://www.law.go.kr/DRF/",
      "--cutoff","2026-09-29T00:00:00+09:00",
      "--selection-rule","pre-registered",
      "--output",str(manifest)
    ])
    saved=json.loads(manifest.read_text(encoding="utf-8"))
    assert saved["record_count"]==2

    ratings=tmp_path/"ratings.json"
    ratings.write_text(json.dumps([
      {"reviewer_id":"R1","case_id":"C1","source_traceability":5,"status_correctness":5,
       "uncertainty_appropriateness":4,"human_review_appropriateness":5,"explanation_clarity":4,
       "critical_error":False,"comment":""},
      {"reviewer_id":"R2","case_id":"C1","source_traceability":5,"status_correctness":4,
       "uncertainty_appropriateness":4,"human_review_appropriateness":5,"explanation_clarity":4,
       "critical_error":False,"comment":""}
    ],ensure_ascii=False),encoding="utf-8")
    out=tmp_path/"expert-summary.json"
    expert_main(["--ratings",str(ratings),"--output",str(out)])
    result=json.loads(out.read_text(encoding="utf-8"))
    assert result["summary"]["reviewer_count"]==2
    assert result["pairwise_exact_agreement"]["eligible_cases"]==1
