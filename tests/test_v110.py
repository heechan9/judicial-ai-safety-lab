import json
from pathlib import Path
import pytest
from judicial_ai_safety_lab.batch_reconcile import reconcile_discovery_batch,load_detail_envelopes
from judicial_ai_safety_lab.evidence_index import build_evidence_index
from judicial_ai_safety_lab.batch_reconcile_cli import main as batch_main
from judicial_ai_safety_lab.evidence_index_cli import main as index_main

def _discovery():
    p=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    return json.loads(p.read_text(encoding="utf-8"))

def _env(prec_seq,case_number,title):
    raw={"PrecService":{"판례정보일련번호":prec_seq,"사건번호":case_number,"사건명":title,
                        "판시사항":"쟁점","판결요지":"요지"}}
    import hashlib
    h=hashlib.sha256(json.dumps(raw,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
    return {"schema":"jaisl.precedent-detail-raw.v1","source":"국가법령정보 공동활용",
            "endpoint_contract":{"target":"prec","type":"JSON","mode":"detail"},
            "prec_seq":prec_seq,"retrieved_at":"2026-09-29T00:00:00+00:00",
            "raw_response":raw,"raw_response_hash":h,"credential_stored":False,
            "limitations":[]}

def test_batch_reconcile_leaves_missing_cases_pending():
    d=_discovery()
    first=sorted(d["cases"],key=lambda x:(x["domain"],x["decision_date"],x["source_id"]))[0]
    result=reconcile_discovery_batch(d,detail_envelopes={
        first["prec_seq"]:_env(first["prec_seq"],first["case_number"],first["title"])
    })
    assert result["summary"]["total"]==30
    assert result["summary"]["verified_detail_ready"]==1
    assert result["summary"]["detail_pending"]==29
    assert result["evidence_by_source"][first["source_id"]]["normalized_detail_verified"] is True

def test_batch_reconcile_routes_identity_conflict():
    d=_discovery()
    first=sorted(d["cases"],key=lambda x:(x["domain"],x["decision_date"],x["source_id"]))[0]
    result=reconcile_discovery_batch(d,detail_envelopes={
        first["prec_seq"]:_env(first["prec_seq"],"DIFFERENT","다른 사건")
    })
    assert result["summary"]["identity_review_required"]==1
    row=next(x for x in result["cases"] if x["source_id"]==first["source_id"])
    assert row["status"]=="IDENTITY_REVIEW_REQUIRED"
    assert result["evidence_by_source"][first["source_id"]]["api_raw_verified"] is True
    assert result["evidence_by_source"][first["source_id"]]["normalized_detail_verified"] is False

def test_evidence_index_counts_statuses():
    d=_discovery()
    first=sorted(d["cases"],key=lambda x:(x["domain"],x["decision_date"],x["source_id"]))[0]
    batch=reconcile_discovery_batch(d,detail_envelopes={
        first["prec_seq"]:_env(first["prec_seq"],first["case_number"],first["title"])
    })
    idx=build_evidence_index(batch)
    assert idx["case_count"]==30
    assert idx["verified_count"]==1
    assert idx["pending_count"]==29

def test_batch_and_index_clis(tmp_path):
    d=_discovery()
    source=tmp_path/"discovery.json"
    source.write_text(json.dumps(d,ensure_ascii=False),encoding="utf-8")
    details=tmp_path/"details"; details.mkdir()
    first=sorted(d["cases"],key=lambda x:(x["domain"],x["decision_date"],x["source_id"]))[0]
    (details/(first["prec_seq"]+".json")).write_text(
        json.dumps(_env(first["prec_seq"],first["case_number"],first["title"]),ensure_ascii=False),
        encoding="utf-8")
    batch_path=tmp_path/"batch.json"
    batch_main(["--discovery",str(source),"--detail-dir",str(details),"--output",str(batch_path)])
    batch=json.loads(batch_path.read_text(encoding="utf-8"))
    assert batch["summary"]["verified_detail_ready"]==1
    index_path=tmp_path/"index.json"
    index_main(["--batch",str(batch_path),"--output",str(index_path)])
    idx=json.loads(index_path.read_text(encoding="utf-8"))
    assert idx["verified_count"]==1

def test_load_detail_envelopes_rejects_duplicate_identity(tmp_path):
    env=_env("123","2026다1","사건")
    (tmp_path/"a.json").write_text(json.dumps(env,ensure_ascii=False),encoding="utf-8")
    (tmp_path/"b.json").write_text(json.dumps(env,ensure_ascii=False),encoding="utf-8")
    with pytest.raises(ValueError):
        load_detail_envelopes(tmp_path)

def test_detail_batch_collect_and_resume(tmp_path):
    from judicial_ai_safety_lab.detail_batch_collect import collect_detail_batch
    items=[{"case_id":"JAISL-D001","prec_seq":"101"},{"case_id":"JAISL-D002","prec_seq":"102"}]
    def fake(url):
        import re
        seq=re.search(r"ID=(\d+)",url).group(1)
        return {"PrecService":{"판례정보일련번호":seq,"사건번호":"2026다"+seq,"사건명":"사건"+seq}}
    out=tmp_path/"details"
    first=collect_detail_batch(items,output_dir=out,oc="secret",fetcher=fake)
    assert first["collected"]==2 and first["failed"]==0 and first["complete"]
    second=collect_detail_batch(items,output_dir=out,oc="secret",fetcher=fake)
    assert second["skipped_existing"]==2 and second["complete"]

def test_detail_batch_collect_records_failure_without_fake_success(tmp_path):
    from judicial_ai_safety_lab.detail_batch_collect import collect_detail_batch
    items=[{"case_id":"JAISL-D001","prec_seq":"101"},{"case_id":"JAISL-D002","prec_seq":"102"}]
    def fake(url):
        if "ID=102" in url: raise RuntimeError("network failure")
        return {"PrecService":{"판례정보일련번호":"101","사건번호":"2026다101","사건명":"사건101"}}
    result=collect_detail_batch(items,output_dir=tmp_path/"details",oc="secret",fetcher=fake)
    assert result["collected"]==1 and result["failed"]==1
    assert not result["complete"]
    failed=next(x for x in result["results"] if x["status"]=="FAILED")
    assert failed["prec_seq"]=="102"

def test_detail_batch_cli_with_monkeypatched_collector(tmp_path,monkeypatch):
    import judicial_ai_safety_lab.detail_batch_cli as mod
    queue=tmp_path/"queue.json"
    queue.write_text(json.dumps({"items":[{"case_id":"JAISL-D001","prec_seq":"101"}]}),encoding="utf-8")
    monkeypatch.setattr(mod,"collect_detail_batch",lambda items,output_dir,stop_on_error=False:{
      "schema":"jaisl.detail-batch-collect.v1","requested":1,"collected":1,"failed":0,
      "skipped_existing":0,"results":[],"credential_stored":False,"complete":True})
    report=tmp_path/"report.json"
    mod.main(["--queue",str(queue),"--output-dir",str(tmp_path/"details"),"--report",str(report)])
    data=json.loads(report.read_text(encoding="utf-8"))
    assert data["complete"] and data["collected"]==1
