import json
from pathlib import Path
import pytest
from judicial_ai_safety_lab.cohort_freeze import freeze_full_cohort
from judicial_ai_safety_lab.batch_reconcile import reconcile_discovery_batch
from judicial_ai_safety_lab.evidence_index import build_evidence_index
from judicial_ai_safety_lab.pilot_preflight import pilot_preflight
from judicial_ai_safety_lab.preflight_cli import main as preflight_main

def _discovery():
    p=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    return json.loads(p.read_text(encoding="utf-8"))

def _cohort(d):
    return freeze_full_cohort(d,cohort_id="pilot-v1-all30",rule="all30",
                              cutoff="2026-09-29T00:00:00+09:00")

def test_preflight_blocks_pending_detail():
    d=_discovery()
    batch=reconcile_discovery_batch(d,detail_envelopes={})
    idx=build_evidence_index(batch)
    x=pilot_preflight(cohort=_cohort(d),batch_reconciliation=batch,evidence_index=idx)
    assert not x["ready_for_real_data_run"]
    assert x["pending_count"]==30
    assert "DETAIL_PENDING" in x["blockers"]
    assert not x["ready_for_expert_packet"]

def test_preflight_detects_identity_review():
    d=_discovery()
    first=sorted(d["cases"],key=lambda x:(x["domain"],x["decision_date"],x["source_id"]))[0]
    raw={"PrecService":{"판례정보일련번호":first["prec_seq"],"사건번호":"DIFFERENT","사건명":"다른 사건"}}
    import hashlib
    h=hashlib.sha256(json.dumps(raw,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
    env={"schema":"jaisl.precedent-detail-raw.v1","source":"국가법령정보 공동활용",
         "endpoint_contract":{"target":"prec","type":"JSON","mode":"detail"},
         "prec_seq":first["prec_seq"],"retrieved_at":"2026-09-29T00:00:00+00:00",
         "raw_response":raw,"raw_response_hash":h,"credential_stored":False,"limitations":[]}
    batch=reconcile_discovery_batch(d,detail_envelopes={first["prec_seq"]:env})
    idx=build_evidence_index(batch)
    x=pilot_preflight(cohort=_cohort(d),batch_reconciliation=batch,evidence_index=idx)
    assert x["identity_review_count"]==1
    assert "IDENTITY_REVIEW_REQUIRED" in x["blockers"]

def test_preflight_can_be_ready_only_when_all_30_verified():
    d=_discovery()
    import hashlib
    envs={}
    for row in d["cases"]:
        raw={"PrecService":{"판례정보일련번호":row["prec_seq"],
                           "사건번호":row["case_number"],"사건명":row["title"],
                           "판시사항":"쟁점","판결요지":"요지"}}
        h=hashlib.sha256(json.dumps(raw,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
        envs[row["prec_seq"]]={"schema":"jaisl.precedent-detail-raw.v1","source":"국가법령정보 공동활용",
            "endpoint_contract":{"target":"prec","type":"JSON","mode":"detail"},
            "prec_seq":row["prec_seq"],"retrieved_at":"2026-09-29T00:00:00+00:00",
            "raw_response":raw,"raw_response_hash":h,"credential_stored":False,"limitations":[]}
    batch=reconcile_discovery_batch(d,detail_envelopes=envs)
    idx=build_evidence_index(batch)
    x=pilot_preflight(cohort=_cohort(d),batch_reconciliation=batch,evidence_index=idx)
    assert x["ready_for_real_data_run"]
    assert x["verified_count"]==30 and x["blockers"]==[]
    assert not x["ready_for_expert_packet"]

def test_preflight_cli(tmp_path):
    d=_discovery()
    cohort=_cohort(d)
    batch=reconcile_discovery_batch(d,detail_envelopes={})
    idx=build_evidence_index(batch)
    cp=tmp_path/"cohort.json"; bp=tmp_path/"batch.json"; ip=tmp_path/"index.json"
    cp.write_text(json.dumps(cohort,ensure_ascii=False),encoding="utf-8")
    bp.write_text(json.dumps(batch,ensure_ascii=False),encoding="utf-8")
    ip.write_text(json.dumps(idx,ensure_ascii=False),encoding="utf-8")
    out=tmp_path/"preflight.json"
    preflight_main(["--cohort",str(cp),"--batch",str(bp),"--evidence-index",str(ip),"--output",str(out)])
    result=json.loads(out.read_text(encoding="utf-8"))
    assert result["pending_count"]==30 and not result["ready_for_real_data_run"]
