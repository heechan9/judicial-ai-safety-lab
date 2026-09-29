"""Batch collect official precedent details without persisting LAW_OC.

Each successful case is written as its own non-overwriting raw envelope.
Failures are reported explicitly; they never masquerade as missing/successful data.
"""
import json
from pathlib import Path
from .precedent_detail_collect import collect_precedent_detail,verify_detail_envelope

def collect_detail_batch(items,*,output_dir,oc=None,fetcher=None,stop_on_error=False):
    rows=list(items)
    outdir=Path(output_dir)
    outdir.mkdir(parents=True,exist_ok=True)
    seen=set(); results=[]
    for item in rows:
        prec=str(item.get("prec_seq","")).strip() if isinstance(item,dict) else ""
        case_id=str(item.get("case_id","")).strip() if isinstance(item,dict) else ""
        if not prec.isdigit() or not case_id:
            raise ValueError("each batch item requires case_id and numeric prec_seq")
        if prec in seen: raise ValueError("duplicate prec_seq in batch")
        seen.add(prec)
        target=outdir/(prec+".json")
        if target.exists():
            results.append({"case_id":case_id,"prec_seq":prec,"status":"SKIPPED_EXISTING","path":str(target)})
            continue
        try:
            kwargs={"oc":oc}
            if fetcher is not None: kwargs["fetcher"]=fetcher
            env=collect_precedent_detail(prec,**kwargs)
            verify_detail_envelope(env)
            with target.open("x",encoding="utf-8") as f:
                json.dump(env,f,ensure_ascii=False,indent=2,allow_nan=False)
            results.append({"case_id":case_id,"prec_seq":prec,"status":"COLLECTED",
                            "path":str(target),"raw_response_hash":env["raw_response_hash"]})
        except Exception as exc:
            results.append({"case_id":case_id,"prec_seq":prec,"status":"FAILED",
                            "path":None,"error":str(exc)})
            if stop_on_error: break
    return {"schema":"jaisl.detail-batch-collect.v1",
            "requested":len(rows),
            "collected":sum(x["status"]=="COLLECTED" for x in results),
            "failed":sum(x["status"]=="FAILED" for x in results),
            "skipped_existing":sum(x["status"]=="SKIPPED_EXISTING" for x in results),
            "results":results,
            "credential_stored":False,
            "complete":len(results)==len(rows) and not any(x["status"]=="FAILED" for x in results)}
