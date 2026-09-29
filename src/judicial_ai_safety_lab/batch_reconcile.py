"""Batch reconcile a frozen discovery cohort against detail envelopes.

Missing envelopes remain pending; identity conflicts remain review items;
only exact reconciliations become verified detail evidence.
"""
import hashlib,json
from pathlib import Path
from .public_discovery import validate_public_discovery
from .case_catalog import build_case_catalog
from .evidence_reconcile import reconcile_case

def _hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def reconcile_discovery_batch(discovery,*,detail_envelopes):
    validate_public_discovery(discovery)
    catalog=build_case_catalog(discovery)
    by_source={row["source_id"]:row for row in discovery["cases"]}
    by_prec={str(k):v for k,v in (detail_envelopes or {}).items()}
    rows=[]; evidence={}
    for case in catalog["cases"]:
        prec=case["prec_seq"]
        row=by_source[case["source_id"]]
        env=by_prec.get(prec)
        if env is None:
            rows.append({"case_id":case["case_id"],"source_id":case["source_id"],"prec_seq":prec,
                         "status":"DETAIL_PENDING","raw_response_hash":None,"normalized_hash":None,
                         "identity_differences":[]})
            evidence[case["source_id"]]={"api_raw_verified":False,"normalized_detail_verified":False}
            continue
        result=reconcile_case(row,case_id=case["case_id"],detail_envelope=env)
        rows.append({"case_id":result["case_id"],"source_id":result["source_id"],"prec_seq":prec,
                     "status":result["status"],"raw_response_hash":result.get("raw_response_hash"),
                     "normalized_hash":result.get("normalized_hash"),
                     "identity_differences":result.get("identity_differences",[])})
        ok=result["status"]=="VERIFIED_DETAIL_READY"
        evidence[case["source_id"]]={"api_raw_verified":True,"normalized_detail_verified":ok}
    summary={"total":len(rows),
             "verified_detail_ready":sum(x["status"]=="VERIFIED_DETAIL_READY" for x in rows),
             "identity_review_required":sum(x["status"]=="IDENTITY_REVIEW_REQUIRED" for x in rows),
             "detail_pending":sum(x["status"]=="DETAIL_PENDING" for x in rows)}
    return {"schema":"jaisl.batch-reconcile.v1","summary":summary,"cases":rows,
            "evidence_by_source":evidence,"batch_hash":_hash(rows),
            "limitations":["batch reconciliation checks identity/provenance, not legal correctness",
                           "identity review items are not auto-corrected or silently merged",
                           "missing envelopes remain pending"]}

def load_detail_envelopes(directory):
    root=Path(directory)
    if not root.is_dir(): raise ValueError("detail directory required")
    out={}
    for path in sorted(root.glob("*.json")):
        value=json.loads(path.read_text(encoding="utf-8"))
        prec=str(value.get("prec_seq","")).strip()
        if not prec.isdigit(): raise ValueError(f"invalid detail envelope file: {path.name}")
        if prec in out: raise ValueError(f"duplicate precedent detail envelope: {prec}")
        out[prec]=value
    return out
