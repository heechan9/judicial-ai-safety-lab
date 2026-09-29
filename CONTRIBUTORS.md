# Contributors and verification roles

This project separates **research ownership**, **AI-assisted implementation**, and **independent review** so that contribution credit is visible without overstating who verified what.

## Human owner / research lead

- **최희찬 (heechan9)** — research problem framing, scope and decision boundaries, cross-project methodology selection, review of evidence, repository ownership, and final integration / human decision.

## AI-assisted implementation

### OpenAI ChatGPT / Codex

**Role:** architecture, implementation support, test design, code/evidence audit, documentation, integration and verification assistance.

Documented work in this repository includes:

- v0.5–v2.0: source guard, stress/red-team evaluation, rerun readiness, legal-change targeting, Constitutional Court capability contract.
- v2.5: public-first UI remediation support and evidence/status wording cleanup.
- v3.0–v4.0: legislative lifecycle, uncertainty/governance guards, evidence metadata, temporal cutoff, quality log, bundle integrity, evidence snapshot/lineage, CI hardening.
- v4.5–v5.0: belief-state review planning, hard-invalid vs comparable-difference semantics, verification levels, frozen baseline, environment fingerprint, privacy-release guard, claim audit, quarantine, atomic evidence package, review-path simulation.
- v5.5–v6.0: finding registry, verification-only action policy, human-review state machine, explicit review CLI, immutable review package semantics, and tamper-evident SHA-256 audit chain.
- GitHub Actions failures discovered during implementation were retained and fixed rather than represented as successful runs.

Evidence:
- [OpenAI-assisted v4.0 code audit](docs/audits/OPENAI_CODE_AUDIT_V40.md)
- [v5 architecture](docs/V5_ARCHITECTURE.md)
- [v6 architecture](docs/V6_ARCHITECTURE.md)
- [CI workflow](.github/workflows/ci.yml)

AI-assisted code is subject to the repository's **human-final-decision** principle.

## Independent / secondary AI review

### Anthropic Claude

**Role:** UI/UX, information architecture, readability and secondary review.

Completed and incorporated work:
- v2.5 public-first UI/UX re-audit and remediation: 10-second comprehension, progressive disclosure, terminology/status separation, accessibility/ARIA, mobile readability, and avoidance of unnecessary 3D visualization.

Evidence:
- [Claude UI/UX remediation record](docs/audits/CLAUDE_UI_UX_REMEDIATION.md)

Prepared follow-up review briefs:
- [Claude v5.0 re-audit request](docs/audits/CLAUDE_UI_REAUDIT_REQUEST_V50.md)
- [Claude v6.0 re-audit request](docs/audits/CLAUDE_UI_REAUDIT_REQUEST_V60.md)

A prepared request is **not** recorded as a completed review until a verifiable Claude result is committed.

### Google Jules

**Role:** independent repository code/evidence audit.

Current status:
- Audit scopes and prompts have been prepared for independent review.
- **No Jules audit is marked completed until a verifiable Jules review/session result is committed to this repository.**

Prepared review briefs:
- [Jules v5.0 code audit request](docs/audits/JULES_CODE_AUDIT_REQUEST_V50.md)
- [Jules v6.0 code audit request](docs/audits/JULES_CODE_AUDIT_REQUEST_V60.md)

## Attribution rule

Contribution credit and verification claims are intentionally separate.

- “Contributed” means the tool materially assisted implementation, review, test design, documentation, or integration.
- “Verified” means a reproducible/auditable result exists for the stated scope.
- “Independent verification completed” is used only when an external reviewer actually completed a traceable review.
- AI tools are not represented as human authors or as legal decision-makers.

For version-by-version attribution, see [AI contribution ledger](docs/AI_CONTRIBUTION_LEDGER.md).
