from judicial_ai_safety_lab.governance import EvidenceClaim, uncertainty_guard, dual_safety_guard, governance_loop, rights_data_guard, second_look, public_explanation

def test_uncertainty_states():
    assert uncertainty_guard(EvidenceClaim("c1"))["state"]=="SUPPORTED"
    assert uncertainty_guard(EvidenceClaim("c2",conflicting=True))["state"]=="CONFLICTING"
    assert uncertainty_guard(EvidenceClaim("c3",changed=True))["state"]=="CHANGED"
    assert uncertainty_guard(EvidenceClaim("c4",missing_evidence=True))["state"]=="UNSUPPORTED"

def test_dual_safety():
    x=dual_safety_guard(legal_ok=True,technical_ok=False)
    assert not x["pass"] and x["requires_review"]

def test_governance_loop():
    x=governance_loop(change_id="L1",affected_scenarios=["J1","J2"],failed_scenarios=["J2"])
    assert x["impact_analysis"]["count"]==2 and x["human_review_required"]

def test_rights_data_review():
    x=rights_data_guard(personal_data=True,pseudonymized=False,cross_border=True)
    assert x["requires_review"] and "CROSS_BORDER_REVIEW" in x["flags"]

def test_tdm_uncertainty():
    assert rights_data_guard(tdm=True,rights_reserved=None)["flags"]==["TDM_RIGHTS_STATUS_UNCERTAIN"]

def test_second_look():
    x=second_look(provisional_decision_id="D1",omitted_sources=["S1"])
    assert x["requires_human_reconsideration"]

def test_plain_explanation():
    assert "충돌" in public_explanation({"state":"CONFLICTING"})
