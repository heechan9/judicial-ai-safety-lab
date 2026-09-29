"""Build a compact evidence index from batch reconciliation output."""

def build_evidence_index(batch):
    if not isinstance(batch,dict) or batch.get("schema")!="jaisl.batch-reconcile.v1":
        raise ValueError("invalid batch reconciliation object")
    rows=batch.get("cases")
    if not isinstance(rows,list): raise ValueError("batch cases required")
    index={}
    for row in rows:
        sid=row["source_id"]
        if sid in index: raise ValueError("duplicate source_id in batch")
        index[sid]={"case_id":row["case_id"],"prec_seq":row["prec_seq"],
                    "status":row["status"],"raw_response_hash":row.get("raw_response_hash"),
                    "normalized_hash":row.get("normalized_hash")}
    return {"schema":"jaisl.evidence-index.v1","case_count":len(index),"index":index,
            "verified_count":sum(x["status"]=="VERIFIED_DETAIL_READY" for x in index.values()),
            "review_count":sum(x["status"]=="IDENTITY_REVIEW_REQUIRED" for x in index.values()),
            "pending_count":sum(x["status"]=="DETAIL_PENDING" for x in index.values())}
