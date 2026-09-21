import os
from urllib.parse import urlencode
BASE_SEARCH="https://www.law.go.kr/DRF/lawSearch.do"
BASE_SERVICE="https://www.law.go.kr/DRF/lawService.do"

def _oc(oc):
    x=oc or os.getenv("LAW_OC")
    if not x: raise ValueError("LAW_OC is required")
    return x

def law_change_history_url(reg_date,oc=None,display=100,page=1):
    return BASE_SEARCH+"?"+urlencode({"OC":_oc(oc),"target":"lsHstInf","type":"JSON","regDt":reg_date,"display":display,"page":page})

def article_change_history_url(law_id,article_code,oc=None,display=100,page=1):
    return BASE_SERVICE+"?"+urlencode({"OC":_oc(oc),"target":"lsJoHstInf","type":"JSON","ID":law_id,"JO":article_code,"display":display,"page":page})

def intelligent_search_url(query,oc=None,search=0,display=20,page=1):
    return BASE_SEARCH+"?"+urlencode({"OC":_oc(oc),"target":"aiSearch","type":"JSON","search":search,"query":query,"display":display,"page":page})
