import json
import pytest
from judicial_ai_safety_lab.precedent_detail_collect import collect_precedent_detail,verify_detail_envelope
from judicial_ai_safety_lab.evidence_reconcile import extract_detail_object,reconcile_case

DISCOVERY={
  "source_id":"WEBPREC-123","prec_seq":"123","domain":"civil","title":"손해배상(기)",
  "case_number":"2026다123","decision_date":"2026-01-01","court":"대법원",
  "source_url":"https://www.law.go.kr/precInfoP.do?precSeq=123"
}

def test_detail_collection_never_persists_credential():
    seen=[]
    def fake(url):
        seen.append(url)
        return {"PrecService":{"판례정보일련번호":"123","사건번호":"2026다123","사건명":"손해배상(기)"}}
    env=collect_precedent_detail("123",oc="top-secret",fetcher=fake)
    assert verify_detail_envelope(env)["valid"]
    assert "top-secret" in seen[0]
    assert "top-secret" not in json.dumps(env,ensure_ascii=False)
    assert env["credential_stored"] is False

def test_extract_detail_requires_exactly_one_object():
    raw={"x":{"판례정보일련번호":"123","사건번호":"2026다123","사건명":"손해배상(기)"}}
    x=extract_detail_object(raw)
    assert x["판례정보일련번호"]=="123"
    with pytest.raises(ValueError): extract_detail_object({"a":1})

def test_reconcile_verified_detail_ready():
    env=collect_precedent_detail("123",oc="x",fetcher=lambda url:{
      "PrecService":{"판례정보일련번호":"123","사건번호":"2026다123","사건명":"손해배상(기)",
                     "판시사항":"쟁점","판결요지":"요지","참조조문":"민법 제1조"}})
    r=reconcile_case(DISCOVERY,case_id="JAISL-D001",detail_envelope=env)
    assert r["status"]=="VERIFIED_DETAIL_READY"
    assert r["normalized_case"]["detail_verified"]
    assert len(r["normalized_hash"])==64

def test_reconcile_identity_difference_routes_review_not_silent_merge():
    env=collect_precedent_detail("123",oc="x",fetcher=lambda url:{
      "PrecService":{"판례정보일련번호":"123","사건번호":"2026다999","사건명":"다른 사건"}})
    r=reconcile_case(DISCOVERY,case_id="JAISL-D001",detail_envelope=env)
    assert r["status"]=="IDENTITY_REVIEW_REQUIRED"
    assert len(r["identity_differences"])==2
    assert r["normalized_case"] is None

def test_reconcile_rejects_envelope_identity_mismatch():
    env=collect_precedent_detail("999",oc="x",fetcher=lambda url:{
      "PrecService":{"판례정보일련번호":"999","사건번호":"2026다123","사건명":"손해배상(기)"}})
    with pytest.raises(ValueError):
        reconcile_case(DISCOVERY,case_id="JAISL-D001",detail_envelope=env)


def test_detail_envelope_rejects_api_error_payload():
    env=collect_precedent_detail("123",oc="bad",fetcher=lambda url:{"result":"fail","msg":"invalid credential"})
    with pytest.raises(ValueError,match="official detail payload required"):
        verify_detail_envelope(env)

def test_detail_envelope_rejects_wrong_precedent_identity():
    env=collect_precedent_detail("123",oc="x",fetcher=lambda url:{
      "PrecService":{"판례정보일련번호":"999","사건번호":"2026다123","사건명":"손해배상(기)"}})
    with pytest.raises(ValueError,match="precedent identity mismatch"):
        verify_detail_envelope(env)


def test_reconcile_accepts_official_trailing_bracket_annotation():
    discovery=dict(DISCOVERY,title="손해배상(기)")
    env=collect_precedent_detail("123",oc="x",fetcher=lambda url:{
      "PrecService":{"판례정보일련번호":"123","사건번호":"2026다123",
                     "사건명":"손해배상(기)[쟁점 설명]","판시사항":"쟁점","판결요지":"요지"}})
    r=reconcile_case(discovery,case_id="JAISL-D001",detail_envelope=env)
    assert r["status"]=="VERIFIED_DETAIL_READY"
    assert r["title_equivalence"]=="OFFICIAL_TRAILING_ANNOTATION"

def test_reconcile_accepts_discovery_etc_prefix_only_when_literal_prefix():
    discovery=dict(DISCOVERY,title="사기·업무상배임 등",case_number="2026도123")
    env=collect_precedent_detail("123",oc="x",fetcher=lambda url:{
      "PrecService":{"판례정보일련번호":"123","사건번호":"2026도123",
                     "사건명":"사기·업무상배임·횡령·사문서위조","판시사항":"쟁점","판결요지":"요지"}})
    r=reconcile_case(discovery,case_id="JAISL-D001",detail_envelope=env)
    assert r["status"]=="VERIFIED_DETAIL_READY"
    assert r["title_equivalence"]=="DISCOVERY_ETC_PREFIX"

def test_reconcile_does_not_overaccept_nonprefix_etc_title():
    discovery=dict(DISCOVERY,title="사기·업무상배임 등",case_number="2026도123")
    env=collect_precedent_detail("123",oc="x",fetcher=lambda url:{
      "PrecService":{"판례정보일련번호":"123","사건번호":"2026도123",
                     "사건명":"횡령·사기·업무상배임","판시사항":"쟁점","판결요지":"요지"}})
    r=reconcile_case(discovery,case_id="JAISL-D001",detail_envelope=env)
    assert r["status"]=="IDENTITY_REVIEW_REQUIRED"
