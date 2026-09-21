import pytest
from judicial_ai_safety_lab.official_connectors import moleg_current_law_search_url,court_capability
from judicial_ai_safety_lab.session import canonical_hash
def test_moleg_key():
    with pytest.raises(ValueError): moleg_current_law_search_url("형법",oc=None)
def test_moleg_url(): assert "target=eflaw" in moleg_current_law_search_url("형법",oc="demo")
def test_court(): assert court_capability()["mode"]=="contract_only"
def test_hash(): assert canonical_hash({"a":1,"b":2})==canonical_hash({"b":2,"a":1})
