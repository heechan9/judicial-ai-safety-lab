"""Build a stable catalog from public precedent discovery records.

Catalog entries preserve what is actually known and keep credential-backed /
normalized verification flags false until corresponding evidence exists.
"""
import hashlib,json
from .public_discovery import validate_public_discovery

def _hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def build_case_catalog(discovery):
    check=validate_public_discovery(discovery)
    rows=sorted(discovery["cases"],key=lambda x:(x["domain"],x["decision_date"],x["source_id"]))
    cases=[]
    for i,row in enumerate(rows,1):
        cases.append({
          "case_id":f"JAISL-D{i:03d}",
          "source_id":row["source_id"],
          "prec_seq":row["prec_seq"],
          "domain":row["domain"],
          "title":row["title"],
          "case_number":row["case_number"],
          "decision_date":row["decision_date"],
          "court":row["court"],
          "source_url":row["source_url"],
          "evidence_status":"PUBLIC_WEB_DISCOVERY_ONLY",
          "api_raw_verified":False,
          "normalized_detail_verified":False,
          "pilot_eligible":False,
          "expert_packet_ready":False,
        })
    return {
      "schema":"jaisl.case-catalog.v1",
      "source_schema":discovery["schema"],
      "case_count":check["case_count"],
      "domain_counts":check["domain_counts"],
      "cases":cases,
      "catalog_hash":_hash(cases),
      "limitations":[
        "catalog entries are discovery records until API raw evidence is captured",
        "pilot_eligible remains false until raw and normalized evidence are verified",
        "expert_packet_ready remains false until pilot selection and JAISL outputs are frozen",
      ],
    }

def validate_case_catalog(catalog):
    if catalog.get("schema")!="jaisl.case-catalog.v1": raise ValueError("unsupported catalog schema")
    cases=catalog.get("cases")
    if not isinstance(cases,list) or len(cases)!=catalog.get("case_count"): raise ValueError("catalog count mismatch")
    ids=[x.get("case_id") for x in cases]; sources=[x.get("source_id") for x in cases]
    if len(ids)!=len(set(ids)) or len(sources)!=len(set(sources)): raise ValueError("duplicate catalog identity")
    if _hash(cases)!=catalog.get("catalog_hash"): raise ValueError("catalog hash mismatch")
    for row in cases:
        if row.get("evidence_status")!="PUBLIC_WEB_DISCOVERY_ONLY":
            raise ValueError("unexpected evidence status in discovery catalog")
        if any(row.get(k) is not False for k in ("api_raw_verified","normalized_detail_verified","pilot_eligible","expert_packet_ready")):
            raise ValueError("discovery catalog cannot pre-claim verification/readiness")
    return {"valid":True,"case_count":len(cases),"catalog_hash":catalog["catalog_hash"]}
