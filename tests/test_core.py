from judicial_ai_safety_lab.core import *
def test_risk(): assert risk({"accuracy":45,"procedural":55,"privacy":25,"security":40,"reproducibility":20})==(39.75,"WATCH")
def test_source_guard():
    r=LegalSourceRecord("A","assembly","bill","x","1","committee",checksum="x")
    assert "NOT_EFFECTIVE" in source_guard([r])[0]["flags"]
def test_gate(): assert not rerun_gate({})["ready"]
def test_asr(): assert evaluate([Scenario("a","normal",True,True),Scenario("b","attack",True,False,True)])["attack_success_rate"]==1.0
