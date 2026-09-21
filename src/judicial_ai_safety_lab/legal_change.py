from dataclasses import dataclass

HIGH_IMPACT_RESULTS={"위헌","헌법불합치","한정위헌"}

def legal_change_guard(*, source_status, effective_date=None, constitutional_result=None):
    flags=[]
    if source_status in {"proposed","committee","pending"}:
        flags.append("NOT_EFFECTIVE")
    if constitutional_result in HIGH_IMPACT_RESULTS:
        flags.append("CONSTITUTIONAL_IMPACT")
    return {"flags":flags,"human_review":bool(flags)}

def regression_targets(changed_source_ids, scenario_source_map):
    changed=set(changed_source_ids)
    return sorted([sid for sid,sources in scenario_source_map.items() if changed.intersection(sources)])
