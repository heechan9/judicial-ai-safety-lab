# v10.5 official detail reconciliation

v10.5 closes the gap between the frozen discovery cohort and credential-backed official precedent detail.

## Flow

frozen discovery cohort
→ LAW_OC-backed detail fetch
→ raw detail envelope + SHA-256
→ identity reconciliation
→ verified normalized detail
→ pilot readiness update

## New commands

```bash
jaisl-precedent-detail --prec-seq 621987 --output evidence/detail/621987.raw.json
jaisl-reconcile --discovery-row evidence/discovery/621987.json --case-id JAISL-D001 --detail-envelope evidence/detail/621987.raw.json --output evidence/detail/621987.reconciled.json
```

## Reconciliation rule

The system never silently merges a detail response when:
- envelope precedent ID differs from the frozen discovery record,
- detail object precedent ID differs,
- official case number conflicts with the discovery record,
- official case title conflicts with the discovery record.

Identity conflicts are routed to `IDENTITY_REVIEW_REQUIRED`.

Only a matching detail object can become `VERIFIED_DETAIL_READY`.

## Evidence boundary

A verified detail result preserves:
- raw-response hash
- normalized-case hash
- source / case identity
- 판시사항
- 판결요지
- 참조조문
- 참조판례

This still does not establish legal correctness or external expert validation.
