"""Validate credentialless discovery pools before LAW_OC-backed pilot freezing."""
from datetime import date
from urllib.parse import urlparse,parse_qs

ALLOWED_DOMAINS={"civil","criminal","administrative","family","patent","tax"}

def validate_public_discovery(doc):
    if not isinstance(doc,dict): raise ValueError("discovery document must be an object")
    required={"schema","source_site","discovery_method","discovered_at","discovery_only","pilot_selection_frozen","note","cases"}
    if set(doc)!=required: raise ValueError("discovery schema mismatch")
    if doc["schema"]!="jaisl.public-precedent-discovery.v1": raise ValueError("unsupported discovery schema")
    if doc["discovery_only"] is not True or doc["pilot_selection_frozen"] is not False:
        raise ValueError("discovery pool must remain explicitly unfrozen")
    date.fromisoformat(doc["discovered_at"])
    cases=doc["cases"]
    if not isinstance(cases,list) or len(cases)<1: raise ValueError("discovery cases required")
    source_ids=set(); seqs=set(); rows=[]
    for row in cases:
        needed={"source_id","prec_seq","domain","title","case_number","decision_date","court","source_url"}
        if not isinstance(row,dict) or set(row)!=needed: raise ValueError("case schema mismatch")
        if row["source_id"] in source_ids or row["prec_seq"] in seqs: raise ValueError("duplicate precedent identity")
        source_ids.add(row["source_id"]); seqs.add(row["prec_seq"])
        if row["source_id"]!="WEBPREC-"+row["prec_seq"]: raise ValueError("source_id/prec_seq mismatch")
        if not str(row["prec_seq"]).isdigit(): raise ValueError("prec_seq must be numeric")
        if row["domain"] not in ALLOWED_DOMAINS: raise ValueError("unsupported domain")
        if not all(isinstance(row[k],str) and row[k].strip() for k in ("title","case_number","court","source_url")):
            raise ValueError("case text fields must be non-empty")
        date.fromisoformat(row["decision_date"])
        u=urlparse(row["source_url"])
        if u.scheme!="https" or u.netloc not in {"law.go.kr","www.law.go.kr"}:
            raise ValueError("source_url must be official law.go.kr HTTPS")
        seq=parse_qs(u.query).get("precSeq",[])
        if seq!=[row["prec_seq"]]: raise ValueError("source_url precSeq mismatch")
        rows.append(row)
    domains={}
    for row in rows: domains[row["domain"]]=domains.get(row["domain"],0)+1
    return {"valid":True,"case_count":len(rows),"domain_counts":domains,"discovery_only":True,"pilot_selection_frozen":False}
