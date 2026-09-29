# v11.5 real-data pilot preflight gate

v11.5 adds a fail-closed gate between evidence collection/reconciliation and the real-data JAISL run.

## Required inputs

- frozen 30-case cohort
- batch reconciliation result
- evidence index

## Ready condition

The cohort is ready for the real-data JAISL run only when:
- every frozen cohort source appears in the evidence index
- there are no extra sources
- there are no DETAIL_PENDING cases
- there are no IDENTITY_REVIEW_REQUIRED cases
- all cohort members are VERIFIED_DETAIL_READY

The gate still reports `ready_for_expert_packet=false` because expert review requires a later frozen JAISL output package.

## Command

```bash
jaisl-preflight \
  --cohort evidence/pilot/cohort-v1.json \
  --batch evidence/detail/reconciliation.json \
  --evidence-index evidence/detail/evidence-index.json \
  --output evidence/pilot/preflight.json
```

## Current expected state without LAW_OC-backed evidence

- verified_count = 0
- pending_count = 30
- ready_for_real_data_run = false
- ready_for_expert_packet = false

This gate prevents software-readiness from being confused with evidence-readiness.
