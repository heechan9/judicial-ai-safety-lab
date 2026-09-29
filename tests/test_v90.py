import json
from pathlib import Path
import pytest
from judicial_ai_safety_lab.case_catalog import build_case_catalog,validate_case_catalog
from judicial_ai_safety_lab.pilot_readiness import evaluate_case_readiness
from judicial_ai_safety_lab.catalog_cli import main as catalog_main
from judicial_ai_safety_lab.readiness_cli import main as readiness_main

def _discovery():
    path=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))

def test_case_catalog_from_committed_discovery_pool():
    catalog=build_case_catalog(_discovery())
    result=validate_case_catalog(catalog)
    assert result["valid"] and result["case_count"]==30
    assert catalog["cases"][0]["case_id"]=="JAISL-D001"
    assert all(not row["pilot_eligible"] for row in catalog["cases"])
    assert all(row["evidence_status"]=="PUBLIC_WEB_DISCOVERY_ONLY" for row in catalog["cases"])

def test_pilot_readiness_stays_zero_without_api_and_frozen_selection():
    catalog=build_case_catalog(_discovery())
    x=evaluate_case_readiness(catalog)
    assert x["case_count"]==30
    assert x["pilot_eligible_count"]==0
    assert all("api_raw_verified" in row["missing"] for row in x["cases"])

def test_pilot_readiness_requires_all_three_gates():
    catalog=build_case_catalog(_discovery())
    source=catalog["cases"][0]["source_id"]
    x=evaluate_case_readiness(
        catalog,
        evidence_by_source={source:{"api_raw_verified":True,"normalized_detail_verified":True}},
        frozen_selection_ids=[source],
    )
    assert x["pilot_eligible_count"]==1
    row=next(r for r in x["cases"] if r["source_id"]==source)
    assert row["pilot_eligible"] and row["missing"]==[]

def test_catalog_and_readiness_cli(tmp_path):
    discovery=tmp_path/"discovery.json"
    discovery.write_text(json.dumps(_discovery(),ensure_ascii=False),encoding="utf-8")
    catalog_path=tmp_path/"catalog.json"
    catalog_main(["--discovery",str(discovery),"--output",str(catalog_path)])
    catalog=json.loads(catalog_path.read_text(encoding="utf-8"))
    assert catalog["case_count"]==30

    out=tmp_path/"readiness.json"
    readiness_main(["--catalog",str(catalog_path),"--output",str(out)])
    state=json.loads(out.read_text(encoding="utf-8"))
    assert state["pilot_eligible_count"]==0

def test_catalog_rejects_premature_verification_claim():
    catalog=build_case_catalog(_discovery())
    catalog["cases"][0]["pilot_eligible"]=True
    import hashlib
    payload=json.dumps(catalog["cases"],ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    catalog["catalog_hash"]=hashlib.sha256(payload).hexdigest()
    with pytest.raises(ValueError):
        validate_case_catalog(catalog)
