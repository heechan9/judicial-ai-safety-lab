"""Generate empty reviewer worksheets from a frozen expert packet."""

def build_rating_templates(packet,reviewer_ids):
    if not isinstance(packet,dict) or packet.get("schema")!="jaisl.expert-packet.v1":
        raise ValueError("expert packet required")
    reviewers=list(reviewer_ids)
    if len(reviewers)<2 or len(reviewers)!=len(set(reviewers)):
        raise ValueError("at least two unique reviewer IDs required")
    out={}
    for rid in reviewers:
        out[rid]=[
          {
            "reviewer_id":rid,
            "case_id":case["case_id"],
            "review_case_id":case["review_case_id"],
            "source_traceability":None,
            "status_correctness":None,
            "uncertainty_appropriateness":None,
            "human_review_appropriateness":None,
            "explanation_clarity":None,
            "critical_error":False,
            "comment":"",
          }
          for case in packet["cases"]
        ]
    return {
      "schema":"jaisl.expert-rating-template.v1",
      "target_commit":packet["target_commit"],
      "packet_hash":packet["packet_hash"],
      "reviewer_ids":reviewers,
      "templates":out,
      "instructions":"Replace each null 1-5 field independently; do not view other reviewers' ratings before submission.",
    }
