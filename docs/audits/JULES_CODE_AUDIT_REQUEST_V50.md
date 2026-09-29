# Jules code/evidence audit request — v5.0

Repository: https://github.com/heechan9/judicial-ai-safety-lab

Please audit current main as an independent reviewer. First pass is read-only.

Focus especially on:
- claim_audit.py: can public/research claims be marked PASS without sufficient evidence?
- quarantine.py: can invalid evidence disappear without a fix/retest trace?
- evidence_package.py + artifact_integrity.py: path escape, symlink, duplicate path/key, non-finite JSON, hash/size semantics
- review_simulator.py + review_planner.py: must never optimize legal outcomes; only verification actions
- comparison_guard.py: structural/identity mismatch must abort; valid differences should be collected
- baseline_guard.py + temporal_guard.py: post-hoc baseline edits and hindsight leakage
- verification_level.py: legal uncertainty vs missing-original/unverified evidence
- environment_fingerprint.py: metadata match must never be called historical identity proof
- privacy_release.py: current public cleanup vs Git history/prior copies/external caches
- CLI integration: synthetic fixture-only claims and unsupported independent-verification claim must remain explicit
- stale README/web claims, version drift, CI evidence, and readiness/live/verified terminology

Report Critical/High/Medium/Low findings, exact file/function, reproduction, minimal fix, missing tests, claim-to-code inconsistencies, and a final verified/unverified boundary.
