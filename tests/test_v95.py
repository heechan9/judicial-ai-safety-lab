import json
from pathlib import Path
import pytest
from judicial_ai_safety_lab.precedent_normalization import (
    normalize_discovery_case,enrich_with_verified_detail,case_dict)
from judicial_ai_safety_lab.scenario_mapping import build_default_mappings,validate_mapping_set
from judicial_ai_safety_lab.expert_case_template import build_expert_case_template
from judicial_ai_safety_lab.case_template_cli import main as template_main

def _first_discovery():
    path=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    doc=json.loads(path.read_text(encoding="utf-8"))
    return sorted(doc["cases"],key=lambda x:(x["domain"],x["decision_date"],x["source_id"]))[0]

def test_discovery_case_normalization_keeps_unverified_detail_empty():
    case=normalize_discovery_case(_first_discovery(),case_id="JAISL-D001")
    assert case.source_mode=="PUBLIC_WEB_DISCOVERY_ONLY"
    assert not case.api_raw_verified and not case.detail_verified
    assert case.holding_summary is None and case.issue_summary is None

def test_verified_detail_enrichment_requires_matching_identity():
    case=normalize_discovery_case(_first_discovery(),case_id="JAISL-D001")
    detail={"판례정보일련번호":case.prec_seq,"판결요지":"요지","판시사항":"쟁점",
            "참조조문":"민법 제1조, 민법 제2조","참조판례":"대법원 2020다1"}
    enriched=enrich_with_verified_detail(case,detail)
    assert enriched.api_raw_verified and enriched.detail_verified
    assert enriched.holding_summary=="요지"
    assert enriched.related_articles==("민법 제1조","민법 제2조")
    bad=dict(detail,판례정보일련번호="999")
    with pytest.raises(ValueError): enrich_with_verified_detail(case,bad)

def test_default_mapping_flags_missing_detail_without_legal_outcome():
    case=normalize_discovery_case(_first_discovery(),case_id="JAISL-D001")
    mappings=build_default_mappings(case)
    result=validate_mapping_set(mappings)
    assert result["valid"]
    kinds={x["scenario_type"] for x in mappings}
    assert "SOURCE_TRACEABILITY" in kinds
    assert "MISSING_INFORMATION" in kinds
    assert all("JUDGMENT" not in x["scenario_type"] for x in mappings)

def test_expert_template_remains_not_started():
    case=normalize_discovery_case(_first_discovery(),case_id="JAISL-D001")
    mappings=build_default_mappings(case)
    t=build_expert_case_template(case,mappings)
    assert t["system_output"] is None
    assert t["expert_rating_status"]=="NOT_STARTED"
    assert "판결" in t["boundary"]

def test_case_template_cli_builds_all_30(tmp_path):
    source=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    out=tmp_path/"bundle.json"
    template_main(["--discovery",str(source),"--output",str(out)])
    bundle=json.loads(out.read_text(encoding="utf-8"))
    assert bundle["case_count"]==30
    assert len(bundle["expert_templates"])==30
    assert bundle["mapping_count"]>=90
    assert all(not x["api_raw_verified"] for x in bundle["cases"])
