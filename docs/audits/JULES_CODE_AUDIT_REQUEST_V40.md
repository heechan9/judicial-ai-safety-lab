# Jules code-audit request — v4.0

Repository: https://github.com/heechan9/judicial-ai-safety-lab

Please audit the current main branch as an independent code/evidence reviewer. Do not modify code in the first pass.

Focus on:
- fail-closed behavior in source/legal lifecycle guards
- v3.5 uncertainty and second-look semantics
- v4.0 quality_log.py, temporal_guard.py, artifact_integrity.py, evidence_snapshot.py
- whether UNcertain/conflicting/changed/unsupported states can be confused
- whether non-effective legislative states can ever be treated as effective law
- temporal/hindsight leakage: later evidence must not silently enter an earlier frozen evaluation
- bundle/path/hash validation, duplicate/unsafe paths, symlink handling, malformed JSON and non-finite values
- CI/test coverage and any stale version/documentation claims
- readiness vs verified vs live distinctions
- public demo claims vs implementation
- Python input validation, edge cases, exceptions, reproducibility and provenance

Report:
1. Critical / High / Medium / Low findings
2. Exact file/function
3. Reproduction path
4. Why it matters
5. Minimal remediation
6. Missing tests
7. Claim-to-code inconsistencies
8. Final list of independently verified items vs unverified items

Do not treat a passing manifest hash as authenticity, legal validity, metric validity, or independent rerun. Do not infer live official integrations from connector/capability contracts.
