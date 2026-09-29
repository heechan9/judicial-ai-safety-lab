import json,hashlib
from pathlib import Path
import pytest
from judicial_ai_safety_lab.cohort_freeze import freeze_full_cohort
from judicial_ai_safety_lab.batch_reconcile import reconcile_discovery_batch
from judicial_ai_safety_lab.evidence_index import build_evidence_index
from judicial_ai_safety_lab.pilot_preflight import pilot_preflight
from judicial_ai_safety_lab.real_case_assessment import build_real_case_assessment
from judicial_ai_safety_lab.real_expert_packet_cli import main as expert_packet_main

def _discovery():
    p=Path(__file__).resolve().parents[1]/"data/pilot/public_precedent_discovery_v1.json"
    return json.loads(p.read_text(encoding="utf-8"))

def _env(row):
    raw={"PrecService":{"판례정보일련번호":row["prec_seq"],"사건번호":row["case_number"],
         "사건명":row["title"],"판시사항":"쟁점","판결요지":"요지","참조조문":"민법 제1조"}}
    h=hashlib.sha256(json.dumps(raw,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
    return {"schema":"jaisl.precedent-detail-raw.v1","source":"국가법령정보 공동활용",
      "endpoint_contract":{"target":"prec","type":"JSON","mode":"detail"},
      "prec_seq":row["prec_seq"],"retrieved_at":"2026-09-29T00:00:00+00:00",
      "raw_response":raw,"raw_response_hash":h,"credential_stored":False,"limitations":[]}

def _ready_inputs():
    d=_discovery()
    envs={r["prec_seq"]:_env(r) for r in d["cases"]}
    batch=reconcile_discovery_batch(d,detail_envelopes=envs)
    idx=build_evidence_index(batch)
    cohort=freeze_full_cohort(d,cohort_id="pilot-v1-all30",rule="all30",
        cutoff="2026-09-29T00:00:00+09:00")
    pre=pilot_preflight(cohort=cohort,batch_reconciliation=batch,evidence_index=idx)
    return d,envs,pre

def test_real_assessment_requires_ready_preflight():
    d,envs,pre=_ready_inputs()
    bad=dict(pre,ready_for_real_data_run=False)
    with pytest.raises(ValueError):
        build_real_case_assessment(d,envs,bad,target_commit="a"*40)

def test_real_assessment_freezes_all_30_and_opens_expert_handoff():
    d,envs,pre=_ready_inputs()
    result=build_real_case_assessment(d,envs,pre,target_commit="a"*40)
    assert result["case_count"]==30 and result["verified_count"]==30
    assert result["frozen"] and result["expert_packet_ready"]
    assert len(result["assessment_hash"])==64
    assert all(x["verification_status"]=="VERIFIED_DETAIL_READY" for x in result["cases"])
    assert all("판결의 법적 옳고 그름" in x["system_output"] for x in result["cases"])

def test_real_assessment_rejects_short_commit():
    d,envs,pre=_ready_inputs()
    with pytest.raises(ValueError):
        build_real_case_assessment(d,envs,pre,target_commit="abc")

def test_real_expert_packet_cli(tmp_path):
    d,envs,pre=_ready_inputs()
    result=build_real_case_assessment(d,envs,pre,target_commit="a"*40)
    assessment=tmp_path/"assessment.json"
    assessment.write_text(json.dumps(result,ensure_ascii=False),encoding="utf-8")
    out=tmp_path/"packet.json"
    expert_packet_main(["--assessment",str(assessment),"--output",str(out)])
    packet=json.loads(out.read_text(encoding="utf-8"))
    assert len(packet["cases"])==30
    assert packet["target_commit"]=="a"*40
