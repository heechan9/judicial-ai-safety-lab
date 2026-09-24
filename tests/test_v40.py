import hashlib, json
from judicial_ai_safety_lab.core import LegalSourceRecord, source_guard, evaluate
from judicial_ai_safety_lab.governance import EvidenceClaim, uncertainty_guard, governance_loop
from judicial_ai_safety_lab.assembly_connector import lifecycle_guard
from judicial_ai_safety_lab.quality_log import create_record, transition
from judicial_ai_safety_lab.temporal_guard import freeze_evidence
from judicial_ai_safety_lab.evidence_snapshot import validate_snapshot, lineage_match
from judicial_ai_safety_lab.artifact_integrity import audit_bundle

def test_uncertain_is_reachable():
    assert uncertainty_guard(EvidenceClaim("u",uncertain=True))["state"]=="UNCERTAIN"

def test_non_effective_lifecycle_is_guarded():
    for status in ("proposed","committee","passed","promulgated","rejected","withdrawn"):
        r=LegalSourceRecord("x","assembly","bill","x","1",status,checksum="x")
        assert "NOT_EFFECTIVE" in source_guard([r])[0]["flags"]
        assert not lifecycle_guard(status)["is_effective_law"]

def test_empty_scenarios_fail_closed():
    import pytest
    with pytest.raises(ValueError): evaluate([])

def test_quality_log_state_machine():
    r=create_record(record_id="Q1",requirement="source hash",expected="same",observed="different",
        revision="a"*40,at="2026-09-25T00:00:00+09:00")
    assert r.status=="open"
    transition(r,action="fixed",note="re-exported",revision="b"*40,at="2026-09-25T01:00:00+09:00")
    transition(r,action="pass",note="retest passed",revision="c"*40,at="2026-09-25T02:00:00+09:00")
    assert r.status=="closed"

def test_temporal_guard_excludes_future():
    rows=[{"source_id":"S1","observed_at":"2026-01-01T00:00:00+09:00"},
          {"source_id":"S2","observed_at":"2026-02-01T00:00:00+09:00"}]
    x=freeze_evidence(rows,cutoff="2026-01-15T00:00:00+09:00")
    assert [r["source_id"] for r in x["admitted"]]==["S1"]
    assert [r["source_id"] for r in x["excluded_future"]]==["S2"]

def test_snapshot_and_lineage():
    snap={"repository":"x/y","revision":"a"*40,"checked_at":"2026-09-25",
          "files":{"a.json":{"sha256":"b"*64,"role":"source"}}}
    assert validate_snapshot(snap)["valid"]
    assert lineage_match(source_hash="b"*64,analysis_input_hash="b"*64)["matches"]

def test_bundle_integrity(tmp_path):
    raw=b"hello"; (tmp_path/"a.txt").write_bytes(raw)
    sha=hashlib.sha256(raw).hexdigest()
    (tmp_path/"manifest.json").write_text(json.dumps({"artifact_sha256":{"a.txt":sha}}),encoding="utf-8")
    assert audit_bundle(tmp_path)["integrity_status"]=="PASS"

def test_governance_rejects_failure_outside_impact():
    import pytest
    with pytest.raises(ValueError):
        governance_loop(change_id="L",affected_scenarios=["J1"],failed_scenarios=["J2"])
