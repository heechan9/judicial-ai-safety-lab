# v11.0 batch official-detail pipeline

v11.0 turns the 30-case LAW_OC enrichment step into a resumable, auditable batch workflow.

## Flow

frozen 30-case cohort
→ deterministic enrichment queue
→ batch official-detail collection
→ per-case raw envelope + SHA-256
→ batch identity reconciliation
→ compact evidence index
→ pilot readiness recomputation

## Commands

1. Build the queue:
```bash
jaisl-catalog --discovery data/pilot/public_precedent_discovery_v1.json --output evidence/pilot/catalog.json
jaisl-enrichment --catalog evidence/pilot/catalog.json --output evidence/pilot/enrichment-queue.json
```

2. With LAW_OC configured locally, collect detail for every pending case:
```bash
jaisl-detail-batch   --queue evidence/pilot/enrichment-queue.json   --output-dir evidence/detail/raw   --report evidence/detail/batch-collection.json
```

The collector:
- never stores LAW_OC
- writes one non-overwriting envelope per precedent
- skips already existing files so a stopped run can resume
- records network/API failures explicitly
- never counts a failed request as successful evidence

3. Reconcile every collected detail:
```bash
jaisl-batch-reconcile   --discovery data/pilot/public_precedent_discovery_v1.json   --detail-dir evidence/detail/raw   --output evidence/detail/reconciliation.json
```

4. Build an evidence index:
```bash
jaisl-evidence-index   --batch evidence/detail/reconciliation.json   --output evidence/detail/evidence-index.json
```

## Status semantics

- DETAIL_PENDING: no detail envelope exists
- IDENTITY_REVIEW_REQUIRED: official detail and discovery identity disagree
- VERIFIED_DETAIL_READY: raw envelope verified and identity reconciliation passed

Only VERIFIED_DETAIL_READY can contribute normalized-detail readiness.
