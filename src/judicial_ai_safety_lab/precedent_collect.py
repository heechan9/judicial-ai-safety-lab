"""Credential-safe raw collection envelope for official precedent API responses."""
from datetime import datetime, timezone
import hashlib,json
from .precedent_fetch import search_precedents

def _hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def collect_raw_precedents(query,*,oc=None,fetcher=None,display=20,page=1,org=None,curt=None):
    kwargs={"oc":oc,"display":display,"page":page,"org":org,"curt":curt}
    if fetcher is not None:
        kwargs["fetcher"]=fetcher
    result=search_precedents(query,**kwargs)
    raw=result["response"]
    return {
      "schema":"jaisl.precedent-raw.v1",
      "source":"국가법령정보 공동활용",
      "endpoint_contract":{"target":"prec","type":"JSON","mode":"search"},
      "query":query,
      "page":page,
      "display":display,
      "org":org,
      "curt":curt,
      "retrieved_at":datetime.now(timezone.utc).isoformat(),
      "raw_response":raw,
      "raw_response_hash":_hash(raw),
      "credential_stored":False,
      "limitations":[
        "raw retrieval does not establish legal-label correctness",
        "selection must be frozen separately before outcome review",
      ],
    }

def verify_raw_collection(envelope):
    if envelope.get("schema")!="jaisl.precedent-raw.v1":
        raise ValueError("unsupported raw collection schema")
    if envelope.get("credential_stored") is not False:
        raise ValueError("credential storage is not permitted")
    if _hash(envelope.get("raw_response"))!=envelope.get("raw_response_hash"):
        raise ValueError("raw response hash mismatch")
    return {"valid":True,"raw_response_hash":envelope["raw_response_hash"]}
