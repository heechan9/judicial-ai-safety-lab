import json
from pathlib import Path
from .core import *
from .dashboard import render
from .session import save_session
from .baseline_guard import freeze_baseline
from .review_planner import belief_state, ReviewCandidate, plan_reviews
from .claim_audit import ClaimEvidence, audit_claims
from .finding_registry import Finding, register_findings
from .review_session import ReviewActionContract, create_session, freeze_session, add_review_action
from .review_policy import guard_review_plan
from .assessment_contract import build_assessment_contract

ROOT=Path(__file__).resolve().parents[2]

def _finding_registry(source_findings,rows):
    items=[]
    n=1
    flag_kind={
      "NOT_EFFECTIVE":"SOURCE_UNSUPPORTED",
      "CONSTITUTIONAL_STATUS":"CONSTITUTIONAL_IMPACT",
      "MISSING_CHECKSUM":"SOURCE_UNSUPPORTED",
    }
    for source in source_findings:
        for flag in source["flags"]:
            items.append(Finding(f"F{n:03d}",flag_kind.get(flag,"SOURCE_UNCERTAIN"),
                                 "source:"+source["source_id"],4,
                                 f"{source['source_id']}: {flag}"))
            n+=1
    for row in rows:
        if row.source_changed:
            items.append(Finding(f"F{n:03d}","SOURCE_CHANGED",row.scenario_id,row.severity,
                                 "source change requires targeted re-verification")); n+=1
        if row.category=="contradictory" and not row.ai_pass:
            items.append(Finding(f"F{n:03d}","SOURCE_CONFLICT",row.scenario_id,row.severity,
                                 "conflicting-evidence scenario failed")); n+=1
        if row.attacked and not row.ai_pass:
            items.append(Finding(f"F{n:03d}","TECHNICAL_FAILURE",row.scenario_id,row.severity,
                                 "adversarial scenario failed")); n+=1
        if row.category=="information_missing" and not row.ai_pass:
            items.append(Finding(f"F{n:03d}","SOURCE_UNSUPPORTED",row.scenario_id,row.severity,
                                 "required information is missing")); n+=1
    return register_findings(items)

def main():
    sources=load_sources(ROOT/"data/legal_sources.sample.json"); findings=source_guard(sources)
    raw=json.loads((ROOT/"data/scenarios.json").read_text(encoding="utf-8")); rows=[Scenario(**x) for x in raw]
    ev=evaluate(rows); metrics={"accuracy":45,"procedural":55,"privacy":25,"security":40,"reproducibility":20}
    score,grade=risk(metrics); dw=drift(.80,ev["ai_pass_rate"]); q=review_queue(rows,findings)
    c={"model_version":"synthetic-ai-v1.5","prompt_hash":htext("court-prompt-v1.5"),
       "corpus_hash":htext(json.dumps([x.dict() for x in sources],sort_keys=True)),
       "scenario_manifest_hash":htext(json.dumps(raw,sort_keys=True)),
       "evaluation_contract":"baseline-vs-ai-v1.5"}

    baseline=freeze_baseline({
      "source_snapshot":c["corpus_hash"],
      "scenario_manifest":c["scenario_manifest_hash"],
      "model_version":c["model_version"],
      "prompt_hash":c["prompt_hash"],
      "evaluation_contract":c["evaluation_contract"],
    })
    flagged=sum(1 for x in findings if x["requires_review"])
    belief=belief_state(
      supported=max(1,len(findings)-flagged),
      uncertain=1 if flagged else 0,
      changed=sum(1 for r in rows if r.source_changed),
      conflicting=sum(1 for r in rows if r.category=="contradictory" and not r.ai_pass),
      unsupported=sum(1 for r in rows if r.category=="information_missing" and not r.ai_pass),
    )
    planner=plan_reviews([
      ReviewCandidate("review-source-change","변경된 법적 근거 확인",1.0,1.0,0.2),
      ReviewCandidate("review-conflict","상충 근거 확인",0.9,0.8,0.2),
      ReviewCandidate("review-attack","기술적 공격 실패 확인",0.7,0.7,0.2),
    ])
    claims=audit_claims([
      ClaimEvidence("DEMO-001","현재 공개 수치는 합성 fixture 기반이다",
                    ("data/legal_sources.sample.json","data/scenarios.json"),"CONSISTENT_WITH_ARTIFACT",True),
      ClaimEvidence("DEMO-002","독립 검증이 완료되었다",(),"UNSUPPORTED",True),
    ])

    registry=_finding_registry(findings,rows)
    session=create_session(session_id="synthetic-review-v5.5",baseline_hash=baseline["baseline_hash"],
                           open_findings=registry["open_ids"])
    freeze_session(session)
    action_contracts=[
      ReviewActionContract("review-source-change","CHECK_CHANGE","legal-sources","변경된 근거와 영향 범위를 확인"),
      ReviewActionContract("review-conflict","CHECK_CONFLICT","conflicting-evidence","상충 근거를 나란히 확인"),
      ReviewActionContract("review-attack","RERUN_TECHNICAL","adversarial-scenarios","기술적 실패를 동일 조건에서 재검증"),
    ]
    policy=guard_review_plan([{"action_type":x.action_type} for x in action_contracts])
    if not policy["allowed"]:
        raise ValueError("review plan violates verification-only policy")
    for action in action_contracts:
        add_review_action(session,action)

    report={
      "risk":{"score":score,"grade":grade,"metrics":metrics},
      "evaluation":ev,
      "source_findings":findings,
      "drift":dw,
      "verification_gate":rerun_gate(c),
      "verification_planning":{
        "research_fixture_only":True,
        "frozen_baseline":baseline,
        "belief_state":belief,
        "finding_registry":registry,
        "next_review_plan":planner,
        "review_policy":policy,
        "review_session":{
          "session_id":session.session_id,
          "state":session.state,
          "open_findings":session.open_findings,
          "actions":session.actions,
          "human_disposition":session.human_disposition,
          "note":"Synthetic review session stops at REVIEW_PENDING until a human disposition is explicitly recorded.",
        },
        "claim_audit":claims,
      },
      "human_review_queue":q,
      "decision":"HUMAN_REVIEW_REQUIRED" if grade=="HIGH" or dw["status"]=="WATCH" or q else "LIMITED_USE",
    }
    report["assessment_contract"]=build_assessment_contract(report)
    dump(ROOT/"results/assessment.json",report)
    dump(ROOT/"results/replay_manifest.json",{"contract":c,"scenario_ids":[x.scenario_id for x in rows]})
    render(report,ROOT/"web/index.html")
    save_session(ROOT/"results/session_manifest.json",report,[x.dict() for x in sources],raw)
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
