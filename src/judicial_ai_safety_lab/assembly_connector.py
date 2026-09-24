"""National Assembly lifecycle contract.

Non-effective legislative material is explicitly separated from effective law.
"""
from .core import LegalSourceRecord

LEGISLATIVE_STATES={"proposed","committee","passed","promulgated","effective","rejected","withdrawn"}

def normalize_bill_fixture(row):
    status=row["status"].lower()
    if status not in LEGISLATIVE_STATES:
        raise ValueError(f"unsupported legislative state: {status}")
    return LegalSourceRecord(
      source_id=row["source_id"], institution="assembly", source_type="bill",
      title=row["title"], version=row["version"], status=status,
      effective_date=row.get("effective_date"), canonical_ref=row.get("canonical_ref"),
      constitutional_status=row.get("constitutional_status","none"), checksum=row.get("checksum"))

def lifecycle_guard(status):
    status=status.lower()
    if status not in LEGISLATIVE_STATES:
        raise ValueError(f"unsupported legislative state: {status}")
    return {
      "status":status,
      "is_effective_law":status=="effective",
      "warning":None if status=="effective" else "LEGISLATIVE_MATERIAL_NOT_EFFECTIVE_LAW"
    }
