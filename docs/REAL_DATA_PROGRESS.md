# Real-data progress

Current state:

- Public official precedent discovery: **30 cases collected**
- Full 30-case cohort freeze machinery: **implemented**
- Discovery validation: **implemented**
- Stable case catalog: **implemented**
- Discovery normalization schema: **implemented**
- Source-to-verification scenario mapping: **implemented**
- Expert-review case-template generator: **implemented**
- LAW_OC enrichment queue: **implemented**
- Credential-safe single-detail collector: **implemented**
- Resumable batch detail collector: **implemented**
- Discovery/detail identity reconciliation: **implemented**
- Batch reconciliation + compact evidence index: **implemented**
- Real-data pilot preflight gate: **implemented**
- API raw evidence verification: **pending actual LAW_OC-backed run**
- Normalized detail verification: **pending actual LAW_OC-backed run**
- Pilot preflight ready: **no**
- Pilot-eligible cases: **0 / 30**
- Expert-packet-ready cases: **0 / 30**
- Expert ratings: **not started**

The software path now reaches a fail-closed pilot preflight gate.
The project still does not claim real-data validation until the 30-case credential-backed evidence run is actually completed.


## Live PC validation finding (v12.0)
A credential placeholder was intentionally/accidentally supplied during the first live batch attempt. The upstream API returned error objects with `result`/`msg`; the pre-v12 collector incorrectly counted those hashable JSON objects as collected evidence. v12.0 fixes this by requiring an actual precedent-detail object and exact precedent identity match before an envelope can validate. The 30 pre-fix raw files are invalid research evidence and must be deleted before recollection.
