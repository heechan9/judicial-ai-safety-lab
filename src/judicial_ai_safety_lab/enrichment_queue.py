"""Build a deterministic LAW_OC enrichment queue from a discovery catalog."""

def build_enrichment_queue(catalog):
    cases=catalog.get("cases") if isinstance(catalog,dict) else None
    if not isinstance(cases,list): raise ValueError("catalog cases required")
    queue=[]
    for row in sorted(cases,key=lambda x:x["case_id"]):
        missing=[]
        if not row.get("api_raw_verified"): missing.append("API_RAW")
        if not row.get("normalized_detail_verified"): missing.append("DETAIL")
        if missing:
            queue.append({
              "case_id":row["case_id"],
              "source_id":row["source_id"],
              "prec_seq":row["prec_seq"],
              "case_number":row["case_number"],
              "title":row["title"],
              "missing":missing,
              "next_action":"FETCH_OFFICIAL_DETAIL" if "API_RAW" in missing else "NORMALIZE_DETAIL",
            })
    return {
      "schema":"jaisl.enrichment-queue.v1",
      "pending_count":len(queue),
      "items":queue,
      "note":"Queue order is deterministic by case_id and does not depend on model outcome.",
    }
