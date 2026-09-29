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

## Frozen assessment / expert packet fingerprints

The v13 hash contract was independently recomputed from the saved 30-case evidence index and target commit.

- assessment hash: `4ee3e039c35d1a9d49ba8496d3a81be514df414ec8c4514fe3a81d7abb324ab2`
- blinded expert packet hash: `ad6a033eee9d26a3633695901475f7b19a76b64a9be675dd3b762533b277fe27`

These fingerprints match the current research-paper draft and the deterministic v13 code path. The public repository does not treat expert review as complete until actual reviewer ratings exist.

## Reproduction command

The frozen v13 real-data assessment is reproduced with:

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
- frozen real-data assessment fingerprint: **reproduced from saved evidence log + v13 contract**
- blinded expert packet fingerprint: **reproduced from frozen case ordering and v13 packet contract**
- expert review: **not started**
- Jules v13 code/evidence audit: **request prepared, result not yet completed**
- Claude v13 UI/claim re-audit: **request prepared, result not yet completed**
- external validation: **not complete**

Prepared audit requests are not counted as completed audits.
