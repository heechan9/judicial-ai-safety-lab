import json
from pathlib import Path
import pytest
from judicial_ai_safety_lab.cohort_freeze import freeze_full_cohort,verify_frozen_cohort
from judicial_ai_safety_lab.case_catalog import build_case_catalog
from judicial_ai_safety_lab.enrichment_queue import build_enrichment_queue
from judicial_ai_safety_lab.cohort_cli import main as cohort_main

def _discovery():
    p=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    return json.loads(p.read_text(encoding="utf-8"))

def test_full_cohort_freeze_locks_all_30_before_outcomes():
    d=_discovery()
    c=freeze_full_cohort(d,cohort_id="pilot-v1-all30",
        rule="include all 30 official public discovery cases before JAISL outcome review",
        cutoff="2026-09-29T00:00:00+09:00")
    assert c["member_count"]==30
    assert c["membership_locked"]
    assert c["outcome_reviewed_before_freeze"] is False
    assert verify_frozen_cohort(c,d)["valid"]

def test_frozen_cohort_detects_membership_tamper():
    d=_discovery()
    c=freeze_full_cohort(d,cohort_id="x",rule="all",cutoff="2026-09-29T00:00:00+09:00")
    c["source_ids"]=c["source_ids"][:-1]
    with pytest.raises(ValueError): verify_frozen_cohort(c,d)

def test_enrichment_queue_is_all_30_for_discovery_catalog():
    catalog=build_case_catalog(_discovery())
    q=build_enrichment_queue(catalog)
    assert q["pending_count"]==30
    assert all(x["next_action"]=="FETCH_OFFICIAL_DETAIL" for x in q["items"])
    assert [x["case_id"] for x in q["items"]]==sorted(x["case_id"] for x in q["items"])

def test_enrichment_queue_shrinks_after_evidence_flags():
    catalog=build_case_catalog(_discovery())
    catalog["cases"][0]["api_raw_verified"]=True
    catalog["cases"][0]["normalized_detail_verified"]=True
    q=build_enrichment_queue(catalog)
    assert q["pending_count"]==29

def test_cohort_cli(tmp_path):
    source=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    out=tmp_path/"cohort.json"
    cohort_main(["--discovery",str(source),"--cohort-id","pilot-v1-all30",
                 "--rule","all 30 before outcome review","--cutoff","2026-09-29T00:00:00+09:00",
                 "--output",str(out)])
    c=json.loads(out.read_text(encoding="utf-8"))
    assert c["member_count"]==30 and c["membership_locked"]

def test_enrichment_cli(tmp_path):
    from judicial_ai_safety_lab.catalog_cli import main as catalog_main
    from judicial_ai_safety_lab.enrichment_cli import main as enrichment_main
    source=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    catalog=tmp_path/"catalog.json"
    catalog_main(["--discovery",str(source),"--output",str(catalog)])
    out=tmp_path/"queue.json"
    enrichment_main(["--catalog",str(catalog),"--output",str(out)])
    q=json.loads(out.read_text(encoding="utf-8"))
    assert q["pending_count"]==30
