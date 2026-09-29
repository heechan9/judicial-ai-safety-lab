"""Claim-to-evidence audit for research and public-facing statements.

A claim can be supported by implementation/test artifacts, consistent with a
document, unverifiable because an original is missing, conflicting, or
unsupported. This module never upgrades a claim beyond the supplied evidence.
"""
from dataclasses import dataclass

ALLOWED={"VERIFIED","CONSISTENT_WITH_ARTIFACT","UNVERIFIABLE_MISSING_ORIGINAL","CONFLICTING","UNSUPPORTED"}

@dataclass(frozen=True)
class ClaimEvidence:
    claim_id:str
    claim_text:str
    evidence_refs:tuple[str,...]=()
    verification_level:str="UNSUPPORTED"
    public_claim:bool=False

def audit_claims(claims):
    out=[]
    seen=set()
    for claim in claims:
        if not isinstance(claim,ClaimEvidence): raise ValueError("claims must be ClaimEvidence")
        if not claim.claim_id or claim.claim_id in seen: raise ValueError("claim ids must be unique and non-empty")
        if claim.verification_level not in ALLOWED: raise ValueError("unsupported verification level")
        seen.add(claim.claim_id)
        refs=[x for x in claim.evidence_refs if isinstance(x,str) and x.strip()]
        if claim.verification_level in {"VERIFIED","CONSISTENT_WITH_ARTIFACT"} and not refs:
            raise ValueError("supported claims require evidence references")
        status="PASS" if claim.verification_level in {"VERIFIED","CONSISTENT_WITH_ARTIFACT"} else "REVIEW"
        out.append({
          "claim_id":claim.claim_id,
          "claim_text":claim.claim_text,
          "verification_level":claim.verification_level,
          "evidence_refs":refs,
          "public_claim":claim.public_claim,
          "status":status,
        })
    return {
      "claims":out,
      "pass_count":sum(x["status"]=="PASS" for x in out),
      "review_count":sum(x["status"]=="REVIEW" for x in out),
      "public_review_required":any(x["public_claim"] and x["status"]!="PASS" for x in out),
    }
