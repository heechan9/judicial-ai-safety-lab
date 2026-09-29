# Jules code/evidence audit request — v6.0

Audit current main read-only.

Priority review:
1. review_session.py state transitions and whether any path bypasses explicit human disposition.
2. audit_chain.py canonical hashing, sequence/predecessor validation, timestamp handling, and mutation/reordering detection.
3. review_cli.py reconstruction from assessment and output overwrite behavior.
4. finding_registry.py stable identity and severity validation.
5. review_policy.py + ReviewActionContract: verify that legal-outcome actions cannot enter executable review sessions.
6. package hash semantics: confirm returned payload is the immutable pre-package snapshot and SESSION_PACKAGED is a separate chain event.
7. Claim Audit / Frozen Baseline / Temporal Guard / Quarantine / Evidence Package integration boundaries.
8. README/web claims versus executable code and CI evidence.

Explicitly distinguish hash-chain integrity from external notarization, authenticity, identity proof, and independent verification.
Report severity, exact function, reproduction, minimal remediation, and missing tests.
