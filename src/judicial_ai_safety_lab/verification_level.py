"""Evidence verification levels are separate from legal uncertainty."""

LEVELS={"VERIFIED","CONSISTENT_WITH_ARTIFACT","UNVERIFIABLE_MISSING_ORIGINAL","CONFLICTING","UNSUPPORTED"}

def verification_level(*,original_available,artifact_consistent=False,independently_recomputed=False,
                       conflicting=False,supported=True):
    if not supported: level="UNSUPPORTED"
    elif conflicting: level="CONFLICTING"
    elif not original_available: level="UNVERIFIABLE_MISSING_ORIGINAL"
    elif independently_recomputed: level="VERIFIED"
    elif artifact_consistent: level="CONSISTENT_WITH_ARTIFACT"
    else: level="UNVERIFIABLE_MISSING_ORIGINAL"
    return {"level":level,
            "note":"Evidence-verification status only; not a legal-validity determination."}
