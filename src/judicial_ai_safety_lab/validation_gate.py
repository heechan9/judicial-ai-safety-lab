"""Evidence-based external validation readiness gate.

States advance only when the required artifacts are explicitly present and valid.
No state implies judicial certification, legal correctness, or production approval.
"""
STATES=(
    "INTERNAL_VERIFIED",
    "REAL_DATA_PILOT_COMPLETE",
    "EXPERT_REVIEW_COMPLETE",
    "EXTERNAL_CODE_AUDIT_COMPLETE",
    "EXTERNALLY_VALIDATED_PILOT",
)

def external_validation_gate(*,internal_ci,real_data_manifest=None,pilot_selection=None,
                             expert_summary=None,audit_state=None,claim_audit=None):
    checks={
      "internal_ci":bool(internal_ci),
      "real_data_manifest":bool(real_data_manifest and real_data_manifest.get("valid")),
      "pilot_selection":bool(pilot_selection and pilot_selection.get("selected_count",0)>0 and pilot_selection.get("selection_hash")),
      "expert_review":bool(expert_summary and expert_summary.get("reviewer_count",0)>=2 and expert_summary.get("case_count",0)>0),
      "external_code_audit":bool(audit_state and audit_state.get("has_completed_code_audit")),
      "claim_audit":bool(claim_audit and not claim_audit.get("public_review_required",True)),
    }
    reached=[]
    if checks["internal_ci"]:
        reached.append("INTERNAL_VERIFIED")
    if all(checks[k] for k in ("internal_ci","real_data_manifest","pilot_selection")):
        reached.append("REAL_DATA_PILOT_COMPLETE")
    if "REAL_DATA_PILOT_COMPLETE" in reached and checks["expert_review"]:
        reached.append("EXPERT_REVIEW_COMPLETE")
    if checks["external_code_audit"]:
        reached.append("EXTERNAL_CODE_AUDIT_COMPLETE")
    if all(s in reached for s in ("REAL_DATA_PILOT_COMPLETE","EXPERT_REVIEW_COMPLETE","EXTERNAL_CODE_AUDIT_COMPLETE")) and checks["claim_audit"]:
        reached.append("EXTERNALLY_VALIDATED_PILOT")
    current=reached[-1] if reached else "NOT_READY"
    missing=[k for k,v in checks.items() if not v]
    return {
      "current_state":current,
      "reached_states":reached,
      "checks":checks,
      "missing":missing,
      "limitations":[
        "research validation state only; not judicial certification",
        "external validation does not prove legal correctness for unseen cases",
        "production deployment requires separate security, privacy, operations and institutional approval",
      ],
    }
