"""Verify a packaged human-review record without trusting stored summary fields."""
import hashlib
import json
import re
from .audit_chain import validate_chain

SHA256_RE=re.compile(r"^[0-9a-f]{64}$")

def _hash(value):
    return hashlib.sha256(
        json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
    ).hexdigest()

def verify_review_package(package):
    if not isinstance(package,dict):
        raise ValueError("review package must be an object")
    required={"package_hash","state","payload","package_event","audit_chain","note"}
    if set(package)!=required:
        raise ValueError("review package schema mismatch")
    if package["state"]!="PACKAGED":
        raise ValueError("review package state must be PACKAGED")
    if not SHA256_RE.fullmatch(package["package_hash"] or ""):
        raise ValueError("package_hash must be lowercase SHA256")
    payload=package["payload"]
    if not isinstance(payload,dict):
        raise ValueError("payload must be an object")
    payload_required={"session_id","baseline_hash","open_findings","actions","human_disposition","audit_log","audit_chain_head"}
    if set(payload)!=payload_required:
        raise ValueError("payload schema mismatch")
    if _hash(payload)!=package["package_hash"]:
        raise ValueError("package hash mismatch")
    pre=validate_chain(payload["audit_log"])
    if pre["head_hash"]!=payload["audit_chain_head"]:
        raise ValueError("payload audit-chain head mismatch")

    event=package["package_event"]
    if not isinstance(event,dict) or event.get("event")!="SESSION_PACKAGED":
        raise ValueError("missing package event")
    if event.get("prev_hash")!=payload["audit_chain_head"]:
        raise ValueError("package event predecessor mismatch")
    if event.get("data",{}).get("package_hash")!=package["package_hash"]:
        raise ValueError("package event hash reference mismatch")

    combined=[dict(x) for x in payload["audit_log"]]+[dict(event)]
    final=validate_chain(combined)
    if package["audit_chain"].get("head_hash")!=final["head_hash"] or package["audit_chain"].get("event_count")!=final["event_count"]:
        raise ValueError("stored audit-chain summary mismatch")
    return {
        "valid":True,
        "package_hash":package["package_hash"],
        "session_id":payload["session_id"],
        "remaining_findings":list(payload["open_findings"]),
        "audit_events":final["event_count"],
        "limitations":[
            "valid package integrity is not legal correctness",
            "valid hash chain is not external notarization",
            "operator identity is not proven by this verifier",
        ],
    }
