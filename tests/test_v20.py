from judicial_ai_safety_lab.ccourt_connector import capability_manifest
from judicial_ai_safety_lab.moleg_change_connector import law_change_history_url,article_change_history_url,intelligent_search_url
from judicial_ai_safety_lab.legal_change import legal_change_guard,regression_targets

def test_ccourt_capabilities():
    c=capability_manifest()
    assert c["mode"]=="public_open_data"
    assert "korean_precedent_detail" in c["capabilities"]

def test_moleg_change_urls():
    assert "target=lsHstInf" in law_change_history_url("20260921",oc="demo")
    assert "target=lsJoHstInf" in article_change_history_url("001971","000500",oc="demo")
    assert "target=aiSearch" in intelligent_search_url("불복기간",oc="demo")

def test_constitutional_guard():
    x=legal_change_guard(source_status="effective",constitutional_result="헌법불합치")
    assert x["human_review"] and "CONSTITUTIONAL_IMPACT" in x["flags"]

def test_regression_targeting():
    m={"J1":["LAW-A"],"J2":["LAW-B","LAW-C"],"J3":["LAW-A","LAW-C"]}
    assert regression_targets(["LAW-C"],m)==["J2","J3"]
