"""Reconcile frozen discovery identity with credential-backed detail evidence."""
import hashlib,json,re
from .precedent_detail_collect import verify_detail_envelope
from .precedent_normalization import normalize_discovery_case,enrich_with_verified_detail,case_dict

def _hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def extract_detail_object(raw):
    """Find the single precedent-detail object without guessing missing fields."""
    if not isinstance(raw,dict): raise ValueError("detail response must be an object")
    candidates=[]
    stack=[raw]
    while stack:
        value=stack.pop()
        if isinstance(value,dict):
            if "판례정보일련번호" in value and ("사건번호" in value or "사건명" in value):
                candidates.append(value)
            stack.extend(value.values())
        elif isinstance(value,list):
            stack.extend(value)
    unique=[]
    seen=set()
    for row in candidates:
        serial=str(row.get("판례정보일련번호","")).strip()
        key=(serial,str(row.get("사건번호","")).strip(),str(row.get("사건명","")).strip())
        if key not in seen:
            seen.add(key); unique.append(row)
    if len(unique)!=1:
        raise ValueError(f"expected exactly one precedent detail object, found {len(unique)}")
    return unique[0]

def _normalize_title_text(value):
    text=str(value or "").strip()
    text=re.sub(r"\s+"," ",text)
    return text

def _strip_bracket_annotation(value):
    text=_normalize_title_text(value)
    return re.sub(r"\[[^\]]*\]\s*$","",text).strip()

def _title_equivalent(discovery_title,official_title):
    """Conservative equivalence for public-list vs official-detail titles.

    Accepted:
    1) exact match after whitespace normalization;
    2) official detail only appends one trailing explanatory [..] annotation;
    3) discovery title ends with ' 등' and is a literal prefix summary of the
       longer official charge list.
    """
    d=_normalize_title_text(discovery_title)
    o=_normalize_title_text(official_title)
    if d==o:
        return True,"EXACT"
    stripped=_strip_bracket_annotation(o)
    if d==stripped:
        return True,"OFFICIAL_TRAILING_ANNOTATION"
    if d.endswith(" 등"):
        prefix=d[:-2].rstrip()
        if prefix and stripped.startswith(prefix):
            return True,"DISCOVERY_ETC_PREFIX"
    return False,None

def reconcile_case(discovery_row,*,case_id,detail_envelope):
    verified=verify_detail_envelope(detail_envelope)
    case=normalize_discovery_case(discovery_row,case_id=case_id)
    if verified["prec_seq"]!=case.prec_seq:
        raise ValueError("detail envelope/discovery precedent identity mismatch")
    detail=extract_detail_object(detail_envelope["raw_response"])
    if str(detail.get("판례정보일련번호","")).strip()!=case.prec_seq:
        raise ValueError("detail object/discovery precedent identity mismatch")

    official_case_no=str(detail.get("사건번호","")).strip()
    official_title=str(detail.get("사건명","")).strip()
    identity_differences=[]
    if official_case_no and official_case_no not in case.case_number:
        identity_differences.append({"field":"case_number","discovery":case.case_number,"detail":official_case_no})
    title_equivalence=None
    if official_title:
        equivalent,title_equivalence=_title_equivalent(case.title,official_title)
        if not equivalent:
            identity_differences.append({"field":"title","discovery":case.title,"detail":official_title})
    if identity_differences:
        return {
          "status":"IDENTITY_REVIEW_REQUIRED",
          "case_id":case.case_id,
          "source_id":case.source_id,
          "raw_response_hash":verified["raw_response_hash"],
          "identity_differences":identity_differences,
          "title_equivalence":title_equivalence,
          "normalized_case":None,
        }

    enriched=enrich_with_verified_detail(case,detail)
    normalized=case_dict(enriched)
    return {
      "status":"VERIFIED_DETAIL_READY",
      "case_id":case.case_id,
      "source_id":case.source_id,
      "raw_response_hash":verified["raw_response_hash"],
      "identity_differences":[],
      "title_equivalence":title_equivalence,
      "normalized_case":normalized,
      "normalized_hash":_hash(normalized),
    }
