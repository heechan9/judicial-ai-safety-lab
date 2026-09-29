# AI contribution ledger

This ledger records **material contribution scope** separately from **independent verification status**.

| Version / scope | OpenAI ChatGPT / Codex | Anthropic Claude | Google Jules | Verification note |
|---|---|---|---|---|
| v0.5–v2.0 | Architecture, Python implementation, tests, evidence/replay/status contracts | — | — | Internal implementation/testing only |
| v2.5 public-first UI | Implementation/remediation integration | UI/UX + IA + readability audit findings | — | Claude review evidence recorded in remediation document |
| v3.0 | Legislative lifecycle, evidence metadata, UI terminology | — | — | CI / test evidence where recorded |
| v3.5 | Uncertainty, dual-safety, governance, second-look implementation | Follow-up audit brief prepared | Audit slot prepared | Prepared brief ≠ completed audit |
| v4.0 | Quality log, temporal guard, artifact integrity, evidence snapshot/lineage, CI hardening, code audit | Follow-up audit brief prepared | Code-audit brief prepared | OpenAI-assisted audit recorded; external audit pending |
| v4.5 | Belief state, review planner, comparison guard, verification levels, frozen baseline, environment fingerprint, privacy-release guard | — | — | Verification-only planning boundary |
| v5.0 | Claim audit, quarantine, atomic evidence package, review simulation, CLI integration | Re-audit brief prepared | Code-audit brief prepared | External results not yet recorded |
| v5.5 | Finding registry, review policy, review-session state machine, operator CLI | — | — | Explicit human disposition required |
| v6.0 | Hash-chained audit events, immutable review package snapshot, provenance hardening | Re-audit brief prepared | Code-audit brief prepared | Latest completed external results still tracked separately |
| v6.5 | Strict assessment handoff contract, review-package verifier, jaisl-verify | — | — | Human disposition remains explicit; stored summaries are revalidated |
| v7.0 | Official precedent connector contract, real-data manifest, expert evaluation contract/CLI | — | — | Real-data/expert workflow ready; actual external inputs pending |
| v7.5 | Frozen pilot selection, blinded expert packet, external audit registry | — | — | Prepared audits do not count as completed |
| v8.0 | External validation gate, credential-safe raw precedent collection, expert-packet/validation CLIs, real-data runbook | — | — | Internal framework ready; live pilot/expert/external audit still pending |
| v8.5 | 30-case official public precedent discovery pool + validator | — | — | Discovery-only; frozen pilot not claimed |
| v9.0 | Stable case catalog, per-case pilot readiness gate, catalog/readiness CLIs, 99-test CI verification | — | — | 30 discovered cases, 0/30 pilot-eligible until raw API + normalized detail + frozen selection |

## How this is intended to appear on GitHub

GitHub's built-in **Contributors** graph is based primarily on Git commit authorship / recognized co-authorship. It does not reliably represent AI-tool assistance when commits are made through the repository owner's authenticated GitHub connection.

Therefore this repository uses:
1. `CONTRIBUTORS.md` for human-readable attribution;
2. this ledger for version-by-version scope;
3. audit files for review evidence;
4. commit / CI history for implementation verification.

We do **not** fabricate GitHub identities, email addresses, or completed reviews merely to make an AI tool appear in GitHub's automatic contributor graph.

| v9.5 | Discovery normalization, scenario mapping, expert-review templates | — | — | Detail remains unverified until credential-backed evidence |
| v10.0 | Full 30-case cohort freeze + deterministic LAW_OC enrichment queue | — | — | Cohort fixed before outcome review |
| v10.5 | Credential-safe detail collector, frozen identity reconciliation, raw/normalized hashing | — | — | 115/115 CI PASS; live LAW_OC execution still pending |
