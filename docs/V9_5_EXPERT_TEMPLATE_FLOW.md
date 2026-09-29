# v9.5 normalization → scenario mapping → expert template flow

v9.5 prepares the 30 discovered public precedents for later credential-backed enrichment and expert review without pretending that missing official detail is already known.

## 1. Normalize discovery metadata

Each discovery row becomes a strict `NormalizedPrecedentCase` with:

- stable JAISL case ID
- source ID / precedent sequence ID
- domain
- case title / case number
- decision date
- court
- official source URL
- evidence mode
- API raw/detail verification flags
- optional holding / issue / related-article / cited-precedent fields

For discovery-only rows, all detail-dependent fields remain empty and verification flags remain false.

## 2. Create verification scenario mappings

Default mappings are conservative and verification-only:

- SOURCE_TRACEABILITY
- STATUS_CHECK
- MISSING_INFORMATION
- LEGAL_CHANGE_CHECK
- CONSTITUTIONAL_CHECK

No mapping selects or recommends a judgment, sentence, verdict or penalty.

## 3. Build expert-review templates

Each case template includes:

- public case metadata
- current evidence status
- verification tasks
- blank system output
- review reason
- expert rating status = NOT_STARTED
- explicit boundary excluding judgment/sentence selection

The template is a preparation artifact, not an expert-review result.

## 4. Generate bundle

```bash
jaisl-case-template   --discovery data/pilot/public_precedent_discovery_v1.json   --output evidence/pilot/case-template-bundle.json
```

Expected current result:
- 30 normalized discovery cases
- at least 90 verification mappings
- 30 expert-review templates
- 0 API raw verified
- 0 detail verified

## 5. LAW_OC-backed upgrade path

After official detail is collected and verified, `enrich_with_verified_detail` can populate:

- 판시사항
- 판결요지
- 참조조문
- 참조판례

Only after matching `판례정보일련번호` and verified raw evidence should a case move out of discovery-only status.
