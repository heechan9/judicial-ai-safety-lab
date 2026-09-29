# v10.0 full-cohort pilot freeze

The first JAISL real-data pilot freezes **all 30 discovered public Supreme Court precedents** before any JAISL outcome review.

This avoids a subtle source-selection problem: if the team waits to inspect model outputs and then chooses only the most convenient cases, the pilot can look better than the underlying system actually is.

## Cohort rule

- cohort ID: pilot-v1-all30
- inclusion: every case in `public_precedent_discovery_v1.json`
- membership: locked before model outcome review
- later exclusions: require a new cohort version and an explicit reason
- legal labels / scenario tags: may be enriched later, but membership does not silently change

## Commands

```bash
jaisl-cohort \
  --discovery data/pilot/public_precedent_discovery_v1.json \
  --cohort-id pilot-v1-all30 \
  --rule "include all 30 official public discovery cases before JAISL outcome review" \
  --cutoff "2026-09-29T00:00:00+09:00" \
  --output evidence/pilot/cohort-v1.json
```

Then build the official-detail work queue:

```bash
jaisl-catalog --discovery data/pilot/public_precedent_discovery_v1.json --output evidence/pilot/catalog.json
jaisl-enrichment --catalog evidence/pilot/catalog.json --output evidence/pilot/enrichment-queue.json
```

Current expected queue: 30 pending cases.

A case leaves the queue only after its API raw evidence and normalized detail are verified.
