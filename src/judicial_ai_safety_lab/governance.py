"""Governance, uncertainty, and second-look guards.

Research prototype: classify evidence states and route human review.
No function produces a final legal judgment.
"""
from dataclasses import dataclass
from typing import Iterable

UNCERTAINTY_STATES={"SUPPORTED","UNCERTAIN","CONFLICTING","CHANGED","UNSUPPORTED"}

@dataclass(frozen=True)
class EvidenceClaim:
    claim_id:str
    source_ids:tuple[str,...]=()
    source_supported:bool=True
    uncertain:bool=False
    conflicting:bool=False
    changed:bool=False
    missing_evidence:bool=False
    technical_failure:bool=False
    privacy_flags:tuple[str,...]=()

def uncertainty_guard(claim:EvidenceClaim):
    if claim.missing_evidence or not claim.source_supported: state="UNSUPPORTED"
    elif claim.conflicting: state="CONFLICTING"
    elif claim.changed: state="CHANGED"
    elif claim.uncertain: state="UNCERTAIN"
    else: state="SUPPORTED"
    return {
        "claim_id":claim.claim_id,
        "state":state,
        "requires_review":state!="SUPPORTED" or claim.technical_failure or bool(claim.privacy_flags),
        "reasons":[
            *([ "SOURCE_UNSUPPORTED" ] if state=="UNSUPPORTED" else []),
            *([ "SOURCE_CONFLICT" ] if state=="CONFLICTING" else []),
            *([ "SOURCE_CHANGED" ] if state=="CHANGED" else []),
            *([ "SOURCE_UNCERTAIN" ] if state=="UNCERTAIN" else []),
            *([ "TECHNICAL_FAILURE" ] if claim.technical_failure else []),
            *([ "RIGHTS_DATA_REVIEW" ] if claim.privacy_flags else []),
        ],
    }

def dual_safety_guard(*, legal_ok:bool, technical_ok:bool):
    reasons=[]
    if not legal_ok: reasons.append("LEGAL_EVIDENCE_GUARD")
    if not technical_ok: reasons.append("TECHNICAL_SAFETY_GUARD")
    return {"pass":not reasons,"requires_review":bool(reasons),"reasons":reasons}

def governance_loop(*, change_id:str, affected_scenarios:Iterable[str], failed_scenarios:Iterable[str]):
    affected=list(dict.fromkeys(affected_scenarios)); failed=list(dict.fromkeys(failed_scenarios))
    unexpected=[x for x in failed if x not in affected]
    if unexpected: raise ValueError(f"failed scenarios outside impact set: {unexpected}")
    return {
      "change_id":change_id,
      "impact_analysis":{"affected_scenarios":affected,"count":len(affected)},
      "targeted_regression":{"failed_scenarios":failed,"count":len(failed)},
      "human_review_required":bool(failed),
      "feedback_state":"PENDING_HUMAN_REVIEW" if failed else "NO_NEW_FAILURE",
    }

def rights_data_guard(*, personal_data=False, pseudonymized=False, purpose_basis=None,
                      cross_border=False, tdm=False, rights_reserved=None):
    flags=[]
    if personal_data and not pseudonymized: flags.append("PERSONAL_DATA_REVIEW")
    if personal_data and not purpose_basis: flags.append("PURPOSE_BASIS_UNCONFIRMED")
    if cross_border: flags.append("CROSS_BORDER_REVIEW")
    if tdm and rights_reserved is None: flags.append("TDM_RIGHTS_STATUS_UNCERTAIN")
    if tdm and rights_reserved is True: flags.append("TDM_RIGHTS_RESERVED")
    return {"flags":flags,"requires_review":bool(flags)}

def second_look(*, provisional_decision_id:str, omitted_sources=(), conflicting_sources=(),
                changed_sources=(), technical_findings=()):
    findings=[]
    for kind,values in (
      ("OMITTED_SOURCE",omitted_sources),("CONFLICTING_SOURCE",conflicting_sources),
      ("CHANGED_SOURCE",changed_sources),("TECHNICAL_FINDING",technical_findings)):
        findings.extend({"type":kind,"ref":v} for v in values)
    return {
      "provisional_decision_id":provisional_decision_id,
      "challenge_findings":findings,
      "requires_human_reconsideration":bool(findings),
      "note":"Decision-challenge aid only; no legal conclusion is generated.",
    }

def public_explanation(result):
    return {
      "SUPPORTED":"확인된 근거와 현재 평가가 서로 맞습니다.",
      "UNSUPPORTED":"필요한 근거가 충분히 확인되지 않았습니다.",
      "CONFLICTING":"서로 충돌하는 근거가 있어 사람이 확인해야 합니다.",
      "CHANGED":"참조한 법적 근거에 변경 신호가 있어 다시 확인해야 합니다.",
      "UNCERTAIN":"현재 정보만으로 확정하기 어려워 사람이 확인해야 합니다.",
    }.get(result.get("state"),"추가 확인이 필요한 평가 결과입니다.")
