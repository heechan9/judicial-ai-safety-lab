# Public precedent discovery v1 — provenance

This file documents the first credentialless real-case discovery pool committed to JAISL.

Dataset:
- `data/pilot/public_precedent_discovery_v1.json`
- 30 real public Supreme Court precedents discovered from official law.go.kr pages
- 20 civil / 10 criminal
- discovery date: 2026-09-29

Important boundary:
- This is **not** the frozen 30-case evaluation pilot.
- No LAW_OC-backed raw API response was captured for these 30 rows.
- No model outcomes were used to select these cases.
- The pool exists to prepare the official-data pilot before credential-backed collection.
- Pilot strata and final selection must still be frozen separately before evaluation.

Validation:
- Every row must use official HTTPS law.go.kr URL.
- URL `precSeq` must equal the stored `prec_seq`.
- source IDs and precedent sequence IDs must be unique.
- decision date, court, case number, title and domain must be present.
- `discovery_only=true` and `pilot_selection_frozen=false` are mandatory.

Command:
```bash
jaisl-discovery --input data/pilot/public_precedent_discovery_v1.json
```
