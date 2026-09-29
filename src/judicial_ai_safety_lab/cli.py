import json
from pathlib import Path
from .core import *
from .dashboard import render
from .session import save_session
from .baseline_guard import freeze_baseline
from .review_planner import belief_state, ReviewCandidate, plan_reviews
from .claim_audit import ClaimEvidence, audit_claims

ROOT=Path(__file__).resolve().parents[2]

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
        "next_review_plan":planner,
        "claim_audit":claims,
      },
      "human_review_queue":q,
      "decision":"HUMAN_REVIEW_REQUIRED" if grade=="HIGH" or dw["status"]=="WATCH" or q else "LIMITED_USE",
    }
    dump(ROOT/"results/assessment.json",report)
    dump(ROOT/"results/replay_manifest.json",{"contract":c,"scenario_ids":[x.scenario_id for x in rows]})
    render(report,ROOT/"web/index.html")
    save_session(ROOT/"results/session_manifest.json",report,[x.dict() for x in sources],raw)
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
