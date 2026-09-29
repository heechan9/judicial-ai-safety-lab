"""Freeze evaluation inputs before results are inspected."""
import hashlib,json

REQUIRED=("source_snapshot","scenario_manifest","model_version","prompt_hash","evaluation_contract")

def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def freeze_baseline(contract):
    if not isinstance(contract,dict): raise ValueError("baseline contract must be an object")
    missing=[k for k in REQUIRED if not contract.get(k)]
    if missing: raise ValueError(f"missing baseline fields: {missing}")
    frozen=dict(contract)
    return {"frozen":frozen,"baseline_hash":canonical_hash(frozen),"status":"FROZEN"}

def verify_baseline(frozen,current):
    if frozen.get("status")!="FROZEN" or "baseline_hash" not in frozen: raise ValueError("invalid frozen baseline")
    now=freeze_baseline(current)
    same=now["baseline_hash"]==frozen["baseline_hash"]
    return {"status":"MATCH" if same else "BASELINE_CHANGED","matches":same,
            "expected_hash":frozen["baseline_hash"],"actual_hash":now["baseline_hash"]}
