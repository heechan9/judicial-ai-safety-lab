"""Strict contract for machine-readable assessment handoff."""
import re

SHA256_RE=re.compile(r"^[0-9a-f]{64}$")
SCHEMA="jaisl.assessment.v6.5"

def build_assessment_contract(report):
    if not isinstance(report,dict):
        raise ValueError("assessment report must be an object")
    vp=report.get("verification_planning")
    if not isinstance(vp,dict):
        raise ValueError("missing verification_planning")
    baseline=vp.get("frozen_baseline")
    registry=vp.get("finding_registry")
    session=vp.get("review_session")
    if not isinstance(baseline,dict) or baseline.get("status")!="FROZEN":
        raise ValueError("missing frozen baseline")
    if not SHA256_RE.fullmatch(baseline.get("baseline_hash","")):
        raise ValueError("invalid baseline hash")
    if not isinstance(registry,dict) or not isinstance(registry.get("open_ids"),list):
        raise ValueError("invalid finding registry")
    if not isinstance(session,dict) or session.get("state")!="REVIEW_PENDING":
        raise ValueError("assessment must hand off at REVIEW_PENDING")
    if session.get("human_disposition") is not None:
        raise ValueError("automated assessment must not contain a human disposition")
    return {
        "schema":SCHEMA,
        "decision":report.get("decision"),
        "baseline_hash":baseline["baseline_hash"],
        "finding_ids":list(registry["open_ids"]),
        "review_session_id":session.get("session_id"),
        "review_actions":[dict(x) for x in session.get("actions",[])],
        "research_fixture_only":bool(vp.get("research_fixture_only")),
        "human_disposition":None,
    }

def validate_assessment_contract(contract):
    required={"schema","decision","baseline_hash","finding_ids","review_session_id","review_actions","research_fixture_only","human_disposition"}
    if not isinstance(contract,dict) or set(contract)!=required:
        raise ValueError("assessment contract schema mismatch")
    if contract["schema"]!=SCHEMA:
        raise ValueError("unsupported assessment schema")
    if not SHA256_RE.fullmatch(contract["baseline_hash"] or ""):
        raise ValueError("invalid baseline hash")
    if contract["human_disposition"] is not None:
        raise ValueError("assessment contract cannot pre-fill human disposition")
    if not isinstance(contract["finding_ids"],list) or len(contract["finding_ids"])!=len(set(contract["finding_ids"])):
        raise ValueError("finding ids must be a unique list")
    if not isinstance(contract["review_actions"],list):
        raise ValueError("review_actions must be a list")
    return {"valid":True,"schema":contract["schema"],"finding_count":len(contract["finding_ids"])}
