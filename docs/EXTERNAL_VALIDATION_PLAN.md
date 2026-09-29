# External validation plan — v7.0

This plan moves JAISL from an internally verified research framework toward an externally reviewed, real-data research prototype.

## 1. Real official-data pilot

Primary source:
- 국가법령정보 공동활용 precedent API (target=prec), using the repository owner's own LAW_OC credential.
- Start with public precedents only. Do not ingest private case records.

Pilot size:
- 30 cases minimum for the first external round.
- Pre-register the selection rule before looking at model outcomes.
- Suggested strata: 10 ordinary/source-stable cases, 10 conflict/ambiguity cases, 10 legal-change/constitutional-impact cases.
- Freeze a cutoff timestamp and keep later material out of the initial evaluation.

For every case preserve:
- official source ID / case number / court / decision date
- retrieval timestamp
- source URL/endpoint contract
- raw-response hash
- normalized-record hash
- scenario ID
- model/prompt/evaluation contract
- resulting findings and human-review route

Do not claim representativeness from the pilot sample.

## 2. Expert review

Recommended first panel:
- 1 practicing attorney or former practitioner with litigation experience
- 1 legal researcher / law professor / legal-policy researcher
- 1 additional legal professional (attorney, judicial-policy researcher, or experienced legal-tech reviewer)

If recruiting 3 experts is difficult, start with 2 independent reviewers and use the third as adjudicator for disagreements.

Review blind to implementation authorship where practical.

Rate each case on 1–5:
1. source traceability
2. legal/status correctness
3. uncertainty appropriateness
4. human-review routing appropriateness
5. explanation clarity

Also capture:
- critical error yes/no
- free-text reason
- whether additional source checking is required

The experts should evaluate the **verification output**, not be asked which judgment or sentence the AI should choose.

## 3. External code/evidence audit

Preferred:
- Jules: repository/code/evidence audit using the committed v6/v7 audit brief.
- Claude: UI/UX + public-first wording + secondary code/evidence review.
- At least one human developer/researcher should review the reproducibility package if available.

An audit counts as completed only when the result is committed with:
- reviewer/tool identity
- date
- target commit SHA
- scope
- findings
- unresolved limits

## 4. Acceptance gates

Do not call the project externally validated until all are present:
- frozen real-data manifest
- reproducible evaluation run
- expert-review records
- documented disagreements/critical errors
- external audit result
- claim audit updated against the real-data evidence

Suggested labels:
- INTERNAL VERIFIED
- REAL-DATA PILOT COMPLETE
- EXPERT REVIEW COMPLETE
- EXTERNAL CODE AUDIT COMPLETE
- EXTERNALLY VALIDATED PILOT

These labels are project research states, not judicial certification.

## 5. Privacy and ethics

Use public official records only for the first pilot.
Do not add names/contact details of private reviewers without consent.
Store reviewer identity separately from public rating IDs if anonymity is requested.
Do not publish confidential legal advice, private case files, or access credentials.
