# OpenAI-assisted code/evidence audit — v4.0

Scope: current repository code, tests, CI, and the cross-project methods ported into v4.0.

## Findings fixed during this pass

1. **UNCERTAIN state unreachable** — `EvidenceClaim` exposed the label but no code path produced it. Fixed with an explicit `uncertain` input and test.
2. **Non-effective legislative states incompletely guarded** — `passed`, `promulgated`, `rejected`, and `withdrawn` could bypass `source_guard`. Added a complete non-effective set and lifecycle validation.
3. **Unknown Assembly states accepted as generic non-effective** — `lifecycle_guard` now rejects unsupported values.
4. **Empty evaluation input** — previously could divide by zero. Now fails closed with `ValueError`.
5. **Governance loop inconsistency** — failed scenarios outside the impact set were accepted. Now rejected.
6. **Package version drift** — README, package metadata, and `__version__` were inconsistent. Aligned to v4.0.
7. **CI verifier incomplete** — initial CI did not install pytest. Fixed and JUnit evidence is retained as an artifact.
8. **Bundle integrity parser syntax defect** — CI caught an escaping defect in path validation. Fixed; subsequent CI passed.
9. **Integrity JSON permissiveness** — duplicate JSON keys/non-finite constants are now rejected.
10. **Snapshot path hardening** — absolute/backslash/colon/traversal-style paths are rejected.
11. **Quality-log timestamps** — now require timezone-aware timestamps.

## Cross-project methods ported

- TriGuard: requirement-level defect → fix → retest quality history with pinned revisions.
- AdversarialAI Security: read-only bundle integrity audit with explicit limitation that integrity is not authenticity or independent rerun.
- Bunkering AI: decision-boundary provenance principle adapted into a temporal evidence cutoff that blocks hindsight leakage.
- FabGuard AI: pinned evidence snapshot and source→analysis lineage comparison.

## Remaining external-review questions

- Whether current public wording still overstates connector readiness.
- Whether the second-look semantics could be misconstrued as automated judicial review.
- Whether integrity/provenance controls sufficiently distinguish authenticity, correctness, and reproducibility.
- Whether additional malformed-input/property-based testing is warranted.

External Jules and Claude request briefs are stored beside this audit.
