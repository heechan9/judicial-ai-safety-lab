# Jules independent code/evidence audit request — JAISL v13.0

Target repository: heechan9/judicial-ai-safety-lab  
Target commit: `3de937f3833e08c3e0c141444ae71fcbf9fc5148`

## Audit objective

Independently review the v13.0 research prototype for code/evidence integrity, fail-closed behavior, reproducibility, and consistency between implementation, tests, documentation, and claimed validation state.

## Required scope

Please audit at least:

1. Official-data evidence path
   - LAW_OC handling and credential non-persistence
   - precedent detail collection
   - semantic validation of API payloads
   - batch collection / resume behavior
   - raw-response hashing
   - title/identity reconciliation
   - evidence index
   - pilot preflight

2. v12.0/v12.5 live-remediation logic
   - invalid credential error payload must not become collected evidence
   - requested precedent ID must match returned official detail ID
   - conservative title equivalence must not over-accept unrelated/reordered titles

3. v13.0 real-data assessment
   - requires preflight PASS
   - exactly 30 verified cases
   - target commit validation
   - assessment hash construction
   - expert packet handoff
   - no hidden legal-outcome recommendation

4. Evidence semantics
   - integrity vs authenticity vs legal correctness
   - public discovery vs API-backed verification
   - expert-review readiness vs expert-review completion
   - external-audit request vs completed external audit

5. Tests and CI
   - identify missing negative tests
   - check environment-variable isolation
   - check non-overwrite behavior
   - check path/schema validation
   - check whether any documented PASS state exceeds what code/evidence supports

## Deliverable

Return a structured report with:

- target commit
- audit date
- scope actually inspected
- PASS / FINDING / NOT VERIFIED items
- severity for each finding
- exact file/function references
- reproduction steps where applicable
- unresolved limitations
- final statement that does **not** call the project judicially certified

A prepared audit request does not count as a completed audit. Completion requires a saved, reviewable result tied to this exact commit.
