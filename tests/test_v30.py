from judicial_ai_safety_lab.assembly_connector import lifecycle_guard,normalize_bill_fixture
from judicial_ai_safety_lab.evidence_schema import build_evidence_metadata

def test_bill_not_effective():
    assert not lifecycle_guard("committee")["is_effective_law"]
    assert lifecycle_guard("effective")["is_effective_law"]

def test_bill_fixture():
    x=normalize_bill_fixture({"source_id":"B1","title":"합성 법률안","version":"1","status":"proposed","checksum":"x"})
    assert x.institution=="assembly" and x.status=="proposed"

def test_evidence_metadata():
    x=build_evidence_metadata(fixture_version="fixture-v3",evaluation_version="eval-v3",commit_sha="abc")
    assert x["schema"]=="jaisl.evidence.v3"
    assert x["commit_sha"]=="abc"
    assert x["evaluated_at"].endswith("+00:00")
