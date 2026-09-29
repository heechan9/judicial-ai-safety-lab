"""Human operator step for a v5.5 verification review session.

Reads an assessment produced by the main CLI, records an explicit human
disposition, and packages the reviewed session. It does not create or infer a
legal judgment.
"""
import argparse
import json
from pathlib import Path
from .review_session import (
    ReviewActionContract,create_session,freeze_session,add_review_action,
    record_human_review,package_session,
)
from .review_policy import guard_review_plan
from .assessment_contract import validate_assessment_contract

def review_assessment(report,*,disposition,resolved_findings=()):
    if not isinstance(report,dict): raise ValueError("assessment must be an object")
    contract=report.get("assessment_contract")
    if not isinstance(contract,dict): raise ValueError("assessment lacks assessment_contract")
    validate_assessment_contract(contract)
    vp=report.get("verification_planning")
    if not isinstance(vp,dict): raise ValueError("assessment lacks verification_planning")
    baseline=vp.get("frozen_baseline") or {}
    registry=vp.get("finding_registry") or {}
    prior=vp.get("review_session") or {}
    if baseline.get("status")!="FROZEN" or len(baseline.get("baseline_hash",""))!=64:
        raise ValueError("assessment lacks a valid frozen baseline")
    open_ids=registry.get("open_ids")
    if contract["baseline_hash"]!=baseline["baseline_hash"]: raise ValueError("assessment contract baseline mismatch")
    if contract["finding_ids"]!=open_ids: raise ValueError("assessment contract finding mismatch")
    if not isinstance(open_ids,list): raise ValueError("assessment lacks finding registry")
    actions=prior.get("actions")
    if not isinstance(actions,list) or not actions: raise ValueError("assessment lacks review actions")

    policy=guard_review_plan(actions)
    if not policy["allowed"]: raise ValueError("assessment contains blocked action types")

    session=create_session(
        session_id=prior.get("session_id") or "review-session",
        baseline_hash=baseline["baseline_hash"],
        open_findings=open_ids,
    )
    freeze_session(session)
    for item in actions:
        add_review_action(session,ReviewActionContract(
            item["action_id"],item["action_type"],item["target_ref"],item["rationale"]))
    record_human_review(session,disposition=disposition,resolved_findings=resolved_findings)
    return package_session(session)

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--assessment",required=True,type=Path)
    p.add_argument("--disposition",required=True)
    p.add_argument("--resolve",action="append",default=[])
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)

    report=json.loads(args.assessment.read_text(encoding="utf-8"))
    packaged=review_assessment(report,disposition=args.disposition,resolved_findings=args.resolve)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(packaged,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"state":packaged["state"],"package_hash":packaged["package_hash"],
                      "remaining_findings":packaged["payload"]["open_findings"]},
                     ensure_ascii=False))

if __name__=="__main__":
    main()
