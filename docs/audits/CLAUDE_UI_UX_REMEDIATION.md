# Claude UI/UX Audit — Remediation Record

## Scope
Independent UI/UX and information-architecture review supplied by Anthropic Claude against the public research demo and repository materials.

## Accepted findings
- C1 terminology lacked inline explanation
- C2 Source → Scenario → Test → Review relationship was not visible
- C3 Composite Risk scale/weights were not exposed
- H1 connector readiness states were too visually similar
- H4 constitutional status needed first-class treatment
- M1 Ready-to-Reproduce could be confused with independently verified
- M2 evidence/provenance visibility was weak
- M3 stress and adversarial tests needed clearer separation
- M4 methodology-to-UI mapping needed improvement

## v2.1 remediation
- Added inline tooltips and glossary
- Added 0–100 research-risk scale and weights; explicitly not an official judicial threshold
- Added Source → J005 → Regression FAIL → Human Review trace
- Split adversarial test into a separate panel
- Added Constitutional Status tab and human-review guard language
- Changed rerun wording to **Ready to Reproduce** with **Independent verification: Pending**
- Added Evidence & Provenance view
- Added connector-state semantics: Contract Only / Connector Ready / Public Data Capability / Planned
- Added ARIA tab roles, aria-selected state, keyboard arrow navigation and table header scopes
- Fixed mobile Korean title wrapping using keep-all / protected phrase
- Preserved navy / ivory / gold visual identity

## Human decision notes
No arbitrary pass-rate threshold was added. Claude's illustrative 60% threshold was not evidence-backed, so the UI displays **기준선 미확정**.
No fabricated verification timestamp, fixture version, or independent-verification claim was added.

## Next audit
Claude should re-review the live v2.1 demo after GitHub Pages redeploys. Google Jules remains the separate code/evidence audit track.
