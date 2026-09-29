"""v6.0 end-to-end verification review session.

This orchestrates evidence intake, frozen baselines, review planning, human review
state, and packaging. Allowed actions are verification actions only.
"""
from dataclasses import dataclass, field, asdict
import hashlib
import json
import re
from .audit_chain import append_event, validate_chain

ALLOWED_ACTION_TYPES={
    "VERIFY_SOURCE",
    "CHECK_CONFLICT",
    "CHECK_CHANGE",
    "RERUN_TECHNICAL",
    "CHECK_CONSTITUTIONAL_STATUS",
    "CHECK_PRIVACY_DATA",
    "VERIFY_ORIGINAL",
}
SESSION_STATES={"COLLECTED","FROZEN","REVIEW_PENDING","REVIEWED","PACKAGED"}
SHA256_RE=re.compile(r"^[0-9a-f]{64}$")

@dataclass(frozen=True)
class ReviewActionContract:
    action_id:str
    action_type:str
    target_ref:str
    rationale:str

@dataclass
class ReviewSession:
    session_id:str
    baseline_hash:str
    state:str="COLLECTED"
    open_findings:list[str]=field(default_factory=list)
    actions:list[dict]=field(default_factory=list)
    audit_log:list[dict]=field(default_factory=list)
    human_disposition:str|None=None

def _hash(value):
    return hashlib.sha256(
        json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
    ).hexdigest()

def validate_action(action:ReviewActionContract):
    if not isinstance(action,ReviewActionContract):
        raise ValueError("invalid action contract")
    if not action.action_id or not action.target_ref or not action.rationale:
        raise ValueError("action id, target and rationale are required")
    if action.action_type not in ALLOWED_ACTION_TYPES:
        raise ValueError("only verification/review action types are allowed")
    return action

def create_session(*,session_id,baseline_hash,open_findings=()):
    if not isinstance(session_id,str) or not session_id.strip():
        raise ValueError("session id required")
    if not isinstance(baseline_hash,str) or not SHA256_RE.fullmatch(baseline_hash):
        raise ValueError("baseline hash must be lowercase SHA256")
    findings=list(dict.fromkeys(open_findings))
    s=ReviewSession(session_id.strip(),baseline_hash,open_findings=findings)
    append_event(s.audit_log,"SESSION_CREATED",data={"open_findings":list(findings)})
    return s

def freeze_session(session):
    if session.state!="COLLECTED":
        raise ValueError("session can only be frozen from COLLECTED")
    session.state="FROZEN"
    append_event(session.audit_log,"SESSION_FROZEN",data={"baseline_hash":session.baseline_hash})
    return session

def add_review_action(session,action:ReviewActionContract):
    if session.state not in {"FROZEN","REVIEW_PENDING"}:
        raise ValueError("session is not ready for review actions")
    validate_action(action)
    if any(x["action_id"]==action.action_id for x in session.actions):
        raise ValueError("duplicate action id")
    session.actions.append(asdict(action))
    session.state="REVIEW_PENDING"
    append_event(session.audit_log,"REVIEW_ACTION_ADDED",data={"action_id":action.action_id})
    return session

def record_human_review(session,*,disposition,resolved_findings=()):
    if session.state!="REVIEW_PENDING":
        raise ValueError("human review requires REVIEW_PENDING")
    if not isinstance(disposition,str) or not disposition.strip():
        raise ValueError("human disposition required")
    resolved=set(resolved_findings)
    unknown=resolved-set(session.open_findings)
    if unknown:
        raise ValueError(f"cannot resolve unknown findings: {sorted(unknown)}")
    session.open_findings=[x for x in session.open_findings if x not in resolved]
    session.human_disposition=disposition.strip()
    session.state="REVIEWED"
    append_event(session.audit_log,"HUMAN_REVIEW_RECORDED",data={
        "resolved_findings":sorted(resolved),
        "remaining_findings":list(session.open_findings),
    })
    return session

def package_session(session):
    if session.state!="REVIEWED":
        raise ValueError("only reviewed sessions can be packaged")
    chain_status=validate_chain(session.audit_log)
    payload={
        "session_id":session.session_id,
        "baseline_hash":session.baseline_hash,
        "open_findings":list(session.open_findings),
        "actions":[dict(x) for x in session.actions],
        "human_disposition":session.human_disposition,
        "audit_log":[dict(x) for x in session.audit_log],
        "audit_chain_head":chain_status["head_hash"],
    }
    package_hash=_hash(payload)
    package_event=append_event(session.audit_log,"SESSION_PACKAGED",data={"package_hash":package_hash})
    session.state="PACKAGED"
    return {
        "package_hash":package_hash,
        "state":session.state,
        "payload":payload,
        "package_event":package_event,
        "audit_chain":validate_chain(session.audit_log),
        "note":"Package records a human review process; it is not a legal judgment.",
    }
