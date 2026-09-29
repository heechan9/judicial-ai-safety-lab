"""Separate invalid comparisons from valid-but-different results."""

def compare_records(reference,actual,*,identity_fields=("source_id","scenario_id"),comparable_fields=()):
    if not isinstance(reference,dict) or not isinstance(actual,dict):
        raise ValueError("comparison rows must be objects")
    for field in identity_fields:
        if field not in reference or field not in actual:
            raise ValueError(f"missing identity field: {field}")
        if reference[field]!=actual[field]:
            raise ValueError(f"identity mismatch: {field}")
    differences=[]
    for field in comparable_fields:
        if field not in reference or field not in actual:
            raise ValueError(f"missing comparable field: {field}")
        if reference[field]!=actual[field]:
            differences.append({"field":field,"reference":reference[field],"actual":actual[field]})
    return {"status":"DIFFERENT" if differences else "MATCH","differences":differences,
            "valid_comparison":True}

def collect_comparisons(pairs,*,identity_fields=("source_id","scenario_id"),comparable_fields=()):
    results=[]
    for reference,actual in pairs:
        results.append(compare_records(reference,actual,identity_fields=identity_fields,comparable_fields=comparable_fields))
    return {"status":"FAIL" if any(r["status"]=="DIFFERENT" for r in results) else "PASS",
            "comparisons":results}
