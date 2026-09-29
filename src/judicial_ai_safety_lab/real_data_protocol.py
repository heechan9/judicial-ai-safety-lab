"""Real-data intake protocol for public official legal materials.

This module creates an auditable manifest around already-downloaded official
records. It does not scrape websites or infer legal correctness.
"""
from datetime import datetime
import hashlib,json,re

SHA256=re.compile(r"^[0-9a-f]{64}$")

def canonical_hash(value):
    return hashlib.sha256(json.dumps(
        value,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False
    ).encode()).hexdigest()

def build_real_data_manifest(records,*,source_name,source_url,cutoff,selection_rule,operator_note=""):
    if not isinstance(records,list) or not records:
        raise ValueError("records must be a non-empty list")
    dt=datetime.fromisoformat(cutoff.replace("Z","+00:00"))
    if dt.utcoffset() is None: raise ValueError("cutoff must include timezone")
    if not all(isinstance(x,dict) for x in records):
        raise ValueError("records must contain objects")
    ids=[]
    for row in records:
        sid=row.get("source_id")
        if not isinstance(sid,str) or not sid.strip():
            raise ValueError("each record requires source_id")
        if sid in ids: raise ValueError("duplicate source_id")
        ids.append(sid)
    return {
      "schema":"jaisl.real-data.v1",
      "source_name":source_name,
      "source_url":source_url,
      "cutoff":cutoff,
      "selection_rule":selection_rule,
      "record_count":len(records),
      "source_ids":ids,
      "records_hash":canonical_hash(records),
      "operator_note":operator_note,
      "limitations":[
        "public official source does not by itself prove task-label correctness",
        "selection rule must be fixed before outcome review",
        "later materials must not enter the frozen cutoff snapshot",
      ],
    }

def verify_real_data_manifest(records,manifest):
    if manifest.get("schema")!="jaisl.real-data.v1": raise ValueError("unsupported manifest schema")
    if len(records)!=manifest.get("record_count"): raise ValueError("record count mismatch")
    if [x.get("source_id") for x in records]!=manifest.get("source_ids"): raise ValueError("source ordering/identity mismatch")
    if canonical_hash(records)!=manifest.get("records_hash"): raise ValueError("record hash mismatch")
    return {"valid":True,"record_count":len(records),"records_hash":manifest["records_hash"]}
