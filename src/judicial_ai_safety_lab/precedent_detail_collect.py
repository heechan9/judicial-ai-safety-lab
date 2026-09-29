"""Credential-safe detail collection envelope for one official precedent.

The LAW_OC credential is used only to build the live request and is never
returned or persisted in the evidence envelope.
"""
from datetime import datetime, timezone
import hashlib,json
from .precedent_fetch import fetch_precedent_detail

def _hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def collect_precedent_detail(precedent_id,*,oc=None,fetcher=None):
    kwargs={"oc":oc}
    if fetcher is not None:
        kwargs["fetcher"]=fetcher
    raw=fetch_precedent_detail(precedent_id,**kwargs)
    return {
      "schema":"jaisl.precedent-detail-raw.v1",
      "source":"국가법령정보 공동활용",
      "endpoint_contract":{"target":"prec","type":"JSON","mode":"detail"},
      "prec_seq":str(precedent_id).strip(),
      "retrieved_at":datetime.now(timezone.utc).isoformat(),
      "raw_response":raw,
      "raw_response_hash":_hash(raw),
      "credential_stored":False,
      "limitations":[
        "raw detail retrieval does not establish legal correctness",
        "identity reconciliation against the frozen cohort is required",
      ],
    }

def _find_detail_objects(raw):
    if not isinstance(raw,dict):
        return []
    found=[]
    stack=[raw]
    while stack:
        value=stack.pop()
        if isinstance(value,dict):
            serial=str(value.get("판례정보일련번호","")).strip()
            case_no=str(value.get("사건번호","")).strip()
            case_name=str(value.get("사건명","")).strip()
            if serial and (case_no or case_name):
                found.append(value)
            stack.extend(value.values())
        elif isinstance(value,list):
            stack.extend(value)
    unique={}
    for row in found:
        key=(str(row.get("판례정보일련번호","")).strip(),
             str(row.get("사건번호","")).strip(),
             str(row.get("사건명","")).strip())
        unique[key]=row
    return list(unique.values())

def verify_detail_envelope(envelope):
    if envelope.get("schema")!="jaisl.precedent-detail-raw.v1":
        raise ValueError("unsupported detail envelope schema")
    if envelope.get("credential_stored") is not False:
        raise ValueError("credential storage is not permitted")
    prec_seq=str(envelope.get("prec_seq","")).strip()
    if not prec_seq.isdigit():
        raise ValueError("prec_seq must be numeric")
    raw=envelope.get("raw_response")
    if _hash(raw)!=envelope.get("raw_response_hash"):
        raise ValueError("raw detail hash mismatch")
    objects=_find_detail_objects(raw)
    if len(objects)!=1:
        raise ValueError(f"official detail payload required; found {len(objects)} detail objects")
    actual=str(objects[0].get("판례정보일련번호","")).strip()
    if actual!=prec_seq:
        raise ValueError("official detail precedent identity mismatch")
    return {"valid":True,"prec_seq":prec_seq,"raw_response_hash":envelope["raw_response_hash"]}
