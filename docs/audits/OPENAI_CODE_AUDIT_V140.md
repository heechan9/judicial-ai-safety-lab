# OpenAI internal code/evidence audit — JAISL v14.0

Audit type: **internal implementation audit, not independent external audit**

## Frozen real-data target

- v13 frozen assessment target: `3de937f3833e08c3e0c141444ae71fcbf9fc5148`
- assessment hash: `4ee3e039c35d1a9d49ba8496d3a81be514df414ec8c4514fe3a81d7abb324ab2`
- expert packet hash: `ad6a033eee9d26a3633695901475f7b19a76b64a9be675dd3b762533b277fe27`

## Latest CI evidence

GitHub Actions JUnit artifact on v14.0 main:
- tests: **147**
- failures: **0**
- errors: **0**
- skipped: **0**

## PASS

### Expert review completion boundary
- at least two independent reviewers remain required
- every frozen case must receive sufficient reviewer coverage
- duplicate reviewer/case ratings are rejected
- unexpected case IDs are rejected
- critical-error flags block ordinary completion

### Ordinal reliability
- v14.0 adds quadratic weighted Cohen kappa for the five 1–5 dimensions
- the implementation requires exactly two reviewers and shared cases
- duplicate reviewer/case observations fail closed
- results are explicitly described as descriptive pilot reliability, not legal correctness

### Critical-error adjudication
- adjudication is additive and does not overwrite original ratings
- every record includes case, adjudicator, timestamp, disposition, rationale, and source rating IDs
- timezone-naive timestamps are rejected
- confirmed or unresolved critical errors keep the adjudication gate blocked

### Paper-claim traceability
- the v14 paper evidence matrix separates verified, reproduced, implemented, pending, and not-claimed states
- external audit requests remain distinct from completed external audit results

## FINDING / REMEDIATION

### ER-02 — ordinal agreement metric
Previous status: open methodological enhancement.

Remediation:
v14.0 adds quadratic weighted Cohen kappa per expert-review dimension while retaining exact agreement for transparent interpretation.

Status: **fixed and covered by tests**.

## NOT VERIFIED / PENDING

- actual independent expert ratings
- third-reviewer adjudication on any future critical errors
- Jules independent code/evidence audit result
- Claude independent UI/UX/research-claim re-audit result
- judicial institution approval or certification
- production security/operations readiness

## Conclusion

The v14.0 implementation strengthens the expert-review methodology without changing the study boundary. It supports evidence traceability, ordinal reviewer-reliability analysis, and additive disagreement adjudication.

This internal audit does **not** establish legal correctness, judicial certification, or independent external validation.
