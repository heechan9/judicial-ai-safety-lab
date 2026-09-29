# OpenAI internal code/evidence audit — JAISL v13.5

Audit type: **internal implementation audit, not independent external audit**

## Targets

Frozen real-data assessment code target:
`3de937f3833e08c3e0c141444ae71fcbf9fc5148`

Current expert-review tooling:
JAISL v13.5

Latest v13.5 CI evidence inspected:
**142/142 PASS**, 0 failures, 0 errors, 0 skipped.

## PASS

### Official-data fail-closed validation
- detail envelopes require a real precedent-detail object
- requested `prec_seq` must match the returned official precedent identity
- error JSON cannot pass merely because it is valid JSON/hashable
- credential value is not persisted in the evidence envelope

### Conservative identity reconciliation
- case identity mismatch routes to `IDENTITY_REVIEW_REQUIRED`
- title equivalence is limited to exact normalized text, one trailing official annotation, or the documented public-list `등` prefix expansion
- unrelated title differences are not silently fuzzy-matched

### Frozen cohort and preflight
- cohort membership is fixed before outcome review
- missing/extra sources, pending details, identity review, and unknown states block readiness
- live evidence log shows 30 verified / 0 pending / 0 identity review / blockers=[]

### Frozen assessment handoff
- assessment requires preflight PASS
- target commit requires a full lowercase 40-character SHA
- all 30 cases must be VERIFIED_DETAIL_READY
- assessment hash binds target commit, case IDs, raw-response hashes, and normalized hashes
- expert packet is derived only after a frozen assessment

### Expert review boundary
- v13.5 adds a completion gate requiring at least two independent reviewers
- duplicate reviewer/case ratings are rejected
- incomplete case coverage blocks completion
- critical-error flags block `ready_to_summarize` until adjudicated
- blank rating templates do not pre-fill scores

## FINDING / REMEDIATION

### ER-01 — expert-review completeness was previously under-specified
Severity: Medium

Before v13.5, `summarize_ratings` could summarize a partial set of expert ratings and
did not by itself prove that every frozen case had two independent reviewers.

Remediation:
v13.5 adds `expert_review_gate`, which checks reviewer count, per-case coverage,
duplicates, unexpected case IDs, and unresolved critical errors before the review is
considered ready to summarize.

Status: **fixed and covered by tests**.

### ER-02 — agreement metric remains intentionally simple
Severity: Low

The current public implementation reports pairwise exact 1–5 agreement. This is
transparent and reproducible but less informative than ordinal reliability measures
such as weighted kappa or ICC.

Status: **open methodological enhancement**, not a blocker for the first pilot.
The paper should describe the current metric accurately and avoid overstating
inter-rater reliability.

### CODE-01 — minor dead variables in v13 assessment builder
Severity: Low

The v13 assessment builder creates local `index` and `by_source` variables that
are not subsequently used. This does not change the frozen hash or validation result,
but cleanup would improve maintainability.

Status: **non-blocking cleanup**.

## NOT VERIFIED / PENDING

- actual independent legal-expert ratings
- Jules independent code/evidence audit result
- Claude independent UI/UX/research-claim re-audit result
- judicial institution approval/certification
- production security/operations readiness

## Conclusion

The inspected implementation supports the project's stated research boundary:
evidence provenance, fail-closed validation, frozen reproducibility, and explicit
human-review handoff.

This audit does **not** establish legal correctness, judicial certification, or
independent external validation.
