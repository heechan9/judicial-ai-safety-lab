# v5.0 architecture

v5.0 extends the verification path without adding any legal-outcome optimization.

## Internal flow

Evidence collection
→ Frozen temporal/baseline snapshot
→ Structural comparison validity
→ Comparable differences
→ Verification level + uncertainty/belief state
→ Claim-to-evidence audit
→ Review planner / counterfactual verification-path simulation
→ Human review
→ Quarantine / fix / retest log
→ Atomic evidence package

## Safety boundaries

- Belief state is not a probability that a legal conclusion is correct.
- Review Planner ranks verification actions, not judgments, sanctions, sentencing, or case outcomes.
- Review-path simulation searches how to reduce unresolved findings, not which legal result to choose.
- Integrity hashes establish file consistency only.
- Environment fingerprint matches metadata only.
- Missing originals remain unverified even when derived artifacts agree.
- Current public privacy cleanup does not prove erasure from Git history or external copies.
