# v13.0 real-data pilot status

## Frozen code target

- v13.0 code target: `3de937f3833e08c3e0c141444ae71fcbf9fc5148`
- GitHub Actions on that code target: **136/136 PASS**, 0 failures, 0 errors.
- Jules and Claude v13 audit request documents are pinned to the same target commit.

## Live PC evidence state

The credential-backed 30-case official precedent run has reached the evidence preflight boundary:

- official detail collection: **30 / 30 collected**
- failed collection: **0**
- reconciliation: **30 / 30 VERIFIED_DETAIL_READY**
- identity-review required: **0**
- detail pending: **0**
- pilot preflight: **PASS**
- blockers: **none**

These results establish evidence/provenance readiness for the frozen cohort. They do **not** establish legal correctness or judicial certification.

## Current next boundary

The next artifact is the frozen v13 real-data assessment:

```bat
jaisl-real-assessment ^
  --discovery data\pilot\public_precedent_discovery_v1.json ^
  --detail-dir evidence\detail\raw ^
  --preflight evidence\pilot\preflight.json ^
  --target-commit 3de937f3833e08c3e0c141444ae71fcbf9fc5148 ^
  --output evidence\pilot\real-assessment-v1.json
```

Then generate the blinded expert packet:

```bat
jaisl-real-expert-packet ^
  --assessment evidence\pilot\real-assessment-v1.json ^
  --output evidence\expert\real-pilot-v1.json
```

Do not substitute placeholders such as `FULL_SHA` or `TARGET_SHA`; the assessment contract requires an exact 40-character lowercase Git SHA.

## External validation state

- real official-data evidence preflight: **complete**
- frozen real-data assessment: **pending generation on the live PC evidence**
- blinded expert packet: **pending frozen assessment**
- expert review: **not started**
- Jules v13 code/evidence audit: **request prepared, result not yet completed**
- Claude v13 UI/claim re-audit: **request prepared, result not yet completed**
- external validation: **not complete**

Prepared audit requests are not counted as completed audits.
