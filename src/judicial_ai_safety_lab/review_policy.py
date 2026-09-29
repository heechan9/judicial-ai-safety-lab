"""Policy guard for verification-only planning."""

LEGAL_OUTCOME_TERMS={
    "DECIDE_GUILTY","DECIDE_NOT_GUILTY","RECOMMEND_SENTENCE","RECOMMEND_JUDGMENT",
    "SELECT_VERDICT","SET_PENALTY",
}

def guard_review_plan(actions):
    blocked=[]
    for action in actions:
        action_type=action.get("action_type") if isinstance(action,dict) else None
        if action_type in LEGAL_OUTCOME_TERMS:
            blocked.append(action_type)
    return {
      "allowed":not blocked,
      "blocked_action_types":blocked,
      "policy":"verification_actions_only",
    }
