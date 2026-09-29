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

def verify_detail_envelope(envelope):
    if envelope.get("schema")!="jaisl.precedent-detail-raw.v1":
        raise ValueError("unsupported detail envelope schema")
    if envelope.get("credential_stored") is not False:
        raise ValueError("credential storage is not permitted")
    if not str(envelope.get("prec_seq","")).isdigit():
        raise ValueError("prec_seq must be numeric")
    if _hash(envelope.get("raw_response"))!=envelope.get("raw_response_hash"):
        raise ValueError("raw detail hash mismatch")
    return {"valid":True,"prec_seq":envelope["prec_seq"],"raw_response_hash":envelope["raw_response_hash"]}
