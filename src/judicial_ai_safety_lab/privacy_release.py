"""Public-release privacy scope guard.

This is a disclosure-scope checklist, not a promise of complete erasure.
"""

def privacy_release_guard(*,public_files_clean,public_ui_clean,git_history_checked=False,
                          prior_branches_checked=False,external_caches_checked=False):
    checks={
      "public_files":bool(public_files_clean),
      "public_ui":bool(public_ui_clean),
      "git_history":bool(git_history_checked),
      "prior_branches":bool(prior_branches_checked),
      "external_caches":bool(external_caches_checked),
    }
    current_public_clean=checks["public_files"] and checks["public_ui"]
    residual=[k for k,v in checks.items() if not v and k not in {"public_files","public_ui"}]
    return {"current_public_clean":current_public_clean,
            "residual_scope_unverified":residual,
            "requires_review":not current_public_clean or bool(residual),
            "note":"Current public cleanup does not prove removal from history, prior copies, or external caches."}
