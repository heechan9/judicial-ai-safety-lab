"""Counterfactual review-path simulator.

This explores verification actions only. It never searches over legal outcomes.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReviewAction:
    action_id:str
    resolves:tuple[str,...]=()
    introduces:tuple[str,...]=()
    cost:float=0.0

def simulate_review_path(initial_open,actions,max_depth=3):
    if max_depth<1 or max_depth>6: raise ValueError("max_depth must be 1..6")
    initial=tuple(sorted(set(initial_open)))
    actions=list(actions)
    seen_ids=set()
    for a in actions:
        if not isinstance(a,ReviewAction) or not a.action_id or a.action_id in seen_ids:
            raise ValueError("review actions must have unique non-empty ids")
        if a.cost<0: raise ValueError("review action cost must be non-negative")
        seen_ids.add(a.action_id)
    frontier=[{"open":initial,"path":[],"cost":0.0}]
    results=[]
    for _ in range(max_depth):
        next_frontier=[]
        for node in frontier:
            for a in actions:
                if a.action_id in node["path"]: continue
                open_set=set(node["open"])
                open_set.difference_update(a.resolves)
                open_set.update(a.introduces)
                child={"open":tuple(sorted(open_set)),
                       "path":node["path"]+[a.action_id],
                       "cost":round(node["cost"]+a.cost,6)}
                results.append(child); next_frontier.append(child)
        frontier=next_frontier
        if not frontier: break
    results.sort(key=lambda x:(len(x["open"]),x["cost"],len(x["path"]),x["path"]))
    return {
      "initial_open":initial,
      "best_path":results[0] if results else {"open":initial,"path":[],"cost":0.0},
      "explored":results,
      "note":"Counterfactual verification planning only; not a legal-outcome search.",
    }
