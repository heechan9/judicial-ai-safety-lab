"""Build normalized discovery cases, scenario mappings, and expert templates."""
import argparse,json
from pathlib import Path
from .public_discovery import validate_public_discovery
from .precedent_normalization import normalize_discovery_case,case_dict
from .scenario_mapping import build_default_mappings,validate_mapping_set
from .expert_case_template import build_expert_case_template

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--discovery",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args(argv)

    doc=json.loads(args.discovery.read_text(encoding="utf-8"))
    validate_public_discovery(doc)
    cases=[]; mappings=[]; expert=[]
    for i,row in enumerate(sorted(doc["cases"],key=lambda x:(x["domain"],x["decision_date"],x["source_id"])),1):
        case=normalize_discovery_case(row,case_id=f"JAISL-D{i:03d}")
        ms=build_default_mappings(case)
        validate_mapping_set(ms)
        cases.append(case_dict(case))
        mappings.extend(ms)
        expert.append(build_expert_case_template(case,ms))
    payload={
      "schema":"jaisl.case-template-bundle.v1",
      "case_count":len(cases),
      "mapping_count":len(mappings),
      "cases":cases,
      "mappings":mappings,
      "expert_templates":expert,
      "limitations":[
        "discovery-only cases remain unverified until LAW_OC-backed detail is captured",
        "expert templates are not reviewer results",
        "scenario mappings define verification tasks, not legal outcomes",
      ],
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x",encoding="utf-8") as f:
        json.dump(payload,f,ensure_ascii=False,indent=2,allow_nan=False)
    print(json.dumps({"case_count":len(cases),"mapping_count":len(mappings),"expert_templates":len(expert)},ensure_ascii=False))

if __name__=="__main__":
    main()
