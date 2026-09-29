"""Tamper-evident hash chain for audit events.

The chain detects later modification, deletion, insertion, or reordering inside
the recorded log. It is not an external timestamp, signature, or authenticity proof.
"""
from datetime import datetime, timezone
import hashlib
import json
import re

SHA256_RE=re.compile(r"^[0-9a-f]{64}$")
GENESIS="0"*64

def _stamp(value=None):
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    parsed=datetime.fromisoformat(value.replace("Z","+00:00"))
    if parsed.utcoffset() is None:
        raise ValueError("audit event timestamp must include timezone")
    return value

def _hash(payload):
    return hashlib.sha256(
        json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
    ).hexdigest()

def append_event(chain,event,*,data=None,at=None):
    if not isinstance(chain,list):
        raise ValueError("audit chain must be a list")
    if not isinstance(event,str) or not event.strip():
        raise ValueError("event name required")
    prev=GENESIS if not chain else chain[-1].get("event_hash")
    if not SHA256_RE.fullmatch(prev or ""):
        raise ValueError("previous audit hash is invalid")
    payload={
        "seq":len(chain),
        "event":event.strip(),
        "at":_stamp(at),
        "data":data or {},
        "prev_hash":prev,
    }
    item={**payload,"event_hash":_hash(payload)}
    chain.append(item)
    return item

def validate_chain(chain):
    if not isinstance(chain,list):
        raise ValueError("audit chain must be a list")
    prev=GENESIS
    for index,item in enumerate(chain):
        if not isinstance(item,dict):
            raise ValueError("audit event must be an object")
        required={"seq","event","at","data","prev_hash","event_hash"}
        if set(item)!=required:
            raise ValueError("audit event schema mismatch")
        if item["seq"]!=index:
            raise ValueError("audit event sequence mismatch")
        if item["prev_hash"]!=prev:
            raise ValueError("audit chain predecessor mismatch")
        _stamp(item["at"])
        payload={k:item[k] for k in ("seq","event","at","data","prev_hash")}
        expected=_hash(payload)
        if item["event_hash"]!=expected:
            raise ValueError("audit event hash mismatch")
        prev=item["event_hash"]
    return {
        "valid":True,
        "event_count":len(chain),
        "head_hash":prev,
        "limitation":"Hash-chain integrity is not external notarization or authenticity proof.",
    }
