import json
from pathlib import Path
from .core import *
from .dashboard import render
from .session import save_session
ROOT=Path(__file__).resolve().parents[2]
def main():
    sources=load_sources(ROOT/"data/legal_sources.sample.json"); findings=source_guard(sources)
    raw=json.loads((ROOT/"data/scenarios.json").read_text(encoding="utf-8")); rows=[Scenario(**x) for x in raw]
    ev=evaluate(rows); metrics={"accuracy":45,"procedural":55,"privacy":25,"security":40,"reproducibility":20}
    score,grade=risk(metrics); dw=drift(.80,ev["ai_pass_rate"]); q=review_queue(rows,findings)
    c={"model_version":"synthetic-ai-v1.5","prompt_hash":htext("court-prompt-v1.5"),"corpus_hash":htext(json.dumps([x.dict() for x in sources],sort_keys=True)),"scenario_manifest_hash":htext(json.dumps(raw,sort_keys=True)),"evaluation_contract":"baseline-vs-ai-v1.5"}
    report={"risk":{"score":score,"grade":grade,"metrics":metrics},"evaluation":ev,"source_findings":findings,"drift":dw,"verification_gate":rerun_gate(c),"human_review_queue":q,"decision":"HUMAN_REVIEW_REQUIRED" if grade=="HIGH" or dw["status"]=="WATCH" or q else "LIMITED_USE"}
    dump(ROOT/"results/assessment.json",report); dump(ROOT/"results/replay_manifest.json",{"contract":c,"scenario_ids":[x.scenario_id for x in rows]})
    render(report,ROOT/"web/index.html"); save_session(ROOT/"results/session_manifest.json",report,[x.dict() for x in sources],raw)
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
