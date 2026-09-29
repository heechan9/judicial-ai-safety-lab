"""Official Korean precedent connector contract via 국가법령정보 공동활용.

The Law Open Data API exposes precedent list/detail endpoints. Live requests
require the user's own OC credential. This module only builds/normalizes requests.
"""
import os
from urllib.parse import urlencode
from .core import LegalSourceRecord

SEARCH="https://www.law.go.kr/DRF/lawSearch.do"
SERVICE="https://www.law.go.kr/DRF/lawService.do"

def _oc(value=None):
    token=value or os.getenv("LAW_OC")
    if not token:
        raise ValueError("LAW_OC is required for live precedent requests")
    return token

def precedent_search_url(query="",*,oc=None,search=1,display=20,page=1,org=None,curt=None):
    if search not in {1,2}: raise ValueError("search must be 1(title) or 2(body)")
    if not 1<=int(display)<=100 or int(page)<1: raise ValueError("invalid pagination")
    params={"OC":_oc(oc),"target":"prec","type":"JSON","search":search,
            "query":query,"display":display,"page":page}
    if org: params["org"]=org
    if curt: params["curt"]=curt
    return SEARCH+"?"+urlencode(params)

def precedent_detail_url(precedent_id,*,oc=None):
    value=str(precedent_id).strip()
    if not value.isdigit(): raise ValueError("precedent_id must be numeric")
    return SERVICE+"?"+urlencode({"OC":_oc(oc),"target":"prec","type":"JSON","ID":value})

def normalize_precedent(row):
    """Normalize one already-fetched official precedent object.

    Field names follow the official Korean response schema.
    """
    case_no=str(row.get("사건번호","")).strip()
    title=str(row.get("사건명","")).strip()
    final_date=str(row.get("선고일자","")).strip()
    serial=str(row.get("판례정보일련번호","")).strip()
    court=str(row.get("법원명","")).strip()
    if not serial or not case_no or not title:
        raise ValueError("precedent object missing required official identifiers")
    return LegalSourceRecord(
        source_id="PREC-"+serial,
        institution="court",
        source_type="precedent",
        title=title,
        version=final_date or "unknown-date",
        status="effective",
        effective_date=final_date or None,
        canonical_ref=f"{court} {case_no}".strip(),
        constitutional_status="none",
        checksum=None,
    )
