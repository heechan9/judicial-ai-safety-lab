"""Credential-safe live precedent retrieval helper.

The helper never logs or returns LAW_OC. Tests inject a fake fetcher; live use
still requires the repository owner's credential and network access.
"""
from .precedent_connector import precedent_search_url,precedent_detail_url
from .official_connectors import fetch_json

def search_precedents(query,*,oc=None,fetcher=fetch_json,display=20,page=1,org=None,curt=None):
    url=precedent_search_url(query,oc=oc,display=display,page=page,org=org,curt=curt)
    data=fetcher(url)
    return {"query":query,"page":page,"display":display,"response":data}

def fetch_precedent_detail(precedent_id,*,oc=None,fetcher=fetch_json):
    url=precedent_detail_url(precedent_id,oc=oc)
    return fetcher(url)
