import json,os
from urllib.parse import urlencode
from urllib.request import urlopen,Request
LAW_SEARCH="https://www.law.go.kr/DRF/lawSearch.do"
LAW_SERVICE="https://www.law.go.kr/DRF/lawService.do"
def moleg_current_law_search_url(query,oc=None,display=20):
    oc=oc or os.getenv("LAW_OC")
    if not oc: raise ValueError("LAW_OC is required for live MOLEG requests")
    return LAW_SEARCH+"?"+urlencode({"OC":oc,"target":"eflaw","type":"JSON","query":query,"nw":"3","display":display})
def fetch_json(url,timeout=10):
    with urlopen(Request(url,headers={"User-Agent":"Judicial-AI-Safety-Lab/1.5"}),timeout=timeout) as r: return json.loads(r.read().decode("utf-8"))
def court_capability():
    return {"institution":"court","portal":"https://openapi.scourt.go.kr","mode":"contract_only","safe_default":"fixture/offline validation"}
