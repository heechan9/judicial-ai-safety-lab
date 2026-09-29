"""Normalize official/public precedent records into a strict JAISL case schema.

This schema preserves source provenance and review-relevant legal metadata without
claiming legal correctness. Fields that require LAW_OC-backed detail remain null
until verified.
"""
from dataclasses import dataclass,asdict
from datetime import date
from urllib.parse import urlparse,parse_qs

@dataclass(frozen=True)
class NormalizedPrecedentCase:
    case_id:str
    source_id:str
    prec_seq:str
    domain:str
    title:str
    case_number:str
    decision_date:str
    court:str
    source_url:str
    source_mode:str
    api_raw_verified:bool=False
    detail_verified:bool=False
    holding_summary:str|None=None
    issue_summary:str|None=None
    related_articles:tuple[str,...]=()
    cited_precedents:tuple[str,...]=()
    constitutional_relevance:str="unknown"
    legal_change_relevance:str="unknown"

def normalize_discovery_case(row,*,case_id):
    required={"source_id","prec_seq","domain","title","case_number","decision_date","court","source_url"}
    if not isinstance(row,dict) or set(row)!=required:
        raise ValueError("discovery case schema mismatch")
    date.fromisoformat(row["decision_date"])
    if row["source_id"]!="WEBPREC-"+row["prec_seq"]:
        raise ValueError("source identity mismatch")
    u=urlparse(row["source_url"])
    if u.scheme!="https" or u.netloc not in {"law.go.kr","www.law.go.kr"}:
        raise ValueError("official source URL required")
    if parse_qs(u.query).get("precSeq")!=[row["prec_seq"]]:
        raise ValueError("precSeq mismatch")
    return NormalizedPrecedentCase(
        case_id=case_id,
        source_id=row["source_id"],
        prec_seq=row["prec_seq"],
        domain=row["domain"],
        title=row["title"],
        case_number=row["case_number"],
        decision_date=row["decision_date"],
        court=row["court"],
        source_url=row["source_url"],
        source_mode="PUBLIC_WEB_DISCOVERY_ONLY",
    )

def enrich_with_verified_detail(case,detail):
    """Return a new case with verified detail fields.

    The caller is responsible for verifying the LAW_OC-backed raw detail envelope.
    """
    if not isinstance(case,NormalizedPrecedentCase):
        raise ValueError("case must be NormalizedPrecedentCase")
    if not isinstance(detail,dict):
        raise ValueError("detail must be an object")
    serial=str(detail.get("판례정보일련번호","")).strip()
    if serial!=case.prec_seq:
        raise ValueError("detail precedent identity mismatch")
    return NormalizedPrecedentCase(
        **{**asdict(case),
           "source_mode":"LAW_OC_DETAIL_VERIFIED",
           "api_raw_verified":True,
           "detail_verified":True,
           "holding_summary":str(detail.get("판결요지") or "").strip() or None,
           "issue_summary":str(detail.get("판시사항") or "").strip() or None,
           "related_articles":tuple(x.strip() for x in str(detail.get("참조조문") or "").split(",") if x.strip()),
           "cited_precedents":tuple(x.strip() for x in str(detail.get("참조판례") or "").split(",") if x.strip()),
        }
    )

def case_dict(case):
    return asdict(case)
