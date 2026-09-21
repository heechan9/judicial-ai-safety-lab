"""Constitutional Court public-data capability contract.

The official Open Data portal exposes Korean precedent list/detail, recent
major decisions, sentence lists and other public datasets. v2.0 records the
supported fields and normalizes fixtures; it does not invent undocumented
request parameters.
"""
from .core import LegalSourceRecord

CCOURT_PORTAL="https://opendata.ccourt.go.kr"

CAPABILITIES={
 "korean_precedent_list":["case_number","case_name","case_type","result","final_date"],
 "korean_precedent_detail":["case_number","case_name","order","overview","subject","related_articles","judgment","conclusion","holding","reason","result","final_date"],
 "recent_major_decisions":["case_number","case_name","final_date","result","decision_summary"],
 "sentence_list":["case_number","case_name","result","decision_summary_link","decision_download_link"]
}

def capability_manifest():
    return {"institution":"ccourt","portal":CCOURT_PORTAL,"mode":"public_open_data","capabilities":CAPABILITIES}

def normalize_fixture(row):
    return LegalSourceRecord(source_id=row["source_id"],institution="ccourt",
      source_type=row.get("source_type","constitutional_decision"),title=row["title"],
      version=row["version"],status=row.get("status","effective"),
      effective_date=row.get("effective_date"),canonical_ref=row.get("canonical_ref"),
      constitutional_status=row.get("constitutional_status"),checksum=row.get("checksum"))
