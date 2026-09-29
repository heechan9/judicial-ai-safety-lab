# JAISL v14.0 expert-review protocol

## Purpose

The expert round evaluates JAISL evidence handling, uncertainty, review routing, and explanation quality. It does not ask reviewers to select judgments, sentences, verdicts, or policy outcomes.

The frozen real-data assessment remains tied to v13.0 target commit:
`3de937f3833e08c3e0c141444ae71fcbf9fc5148`.

## Minimum review design

- at least 2 independent reviewers
- every frozen case receives at least 2 ratings
- stable reviewer IDs are used in research artifacts
- real reviewer identities/contact information remain outside the public repository unless publication consent is explicit

Recommended reviewer mix:
- one practicing attorney or former legal practitioner
- one legal researcher / law professor / judicial-policy researcher
- optional third reviewer for critical-error adjudication

## Rating dimensions

Each case is rated 1–5 on:
1. source traceability
2. status correctness
3. uncertainty appropriateness
4. human-review appropriateness
5. explanation clarity

Each rating also records:
- critical_error true/false
- short comment

## Completion gate

`jaisl-expert-review-gate` requires:
- at least two independent reviewers
- complete per-case coverage
- no duplicate reviewer/case ratings
- no unexpected case IDs

If any critical error exists, the ordinary summary remains blocked.

## Reliability analysis

v14.0 adds:

```bash
jaisl-expert-reliability --ratings evidence/expert/ratings.json --output evidence/expert/reliability.json
```

For exactly two reviewers, the tool reports quadratic weighted Cohen kappa for each 1–5 dimension. This supplements exact agreement and is reported as a descriptive pilot reliability measure, not as proof of legal correctness.

## Critical-error adjudication

Critical cases are preserved rather than overwritten. A third reviewer or designated adjudicator records an additive decision:

- NO_CHANGE
- CRITICAL_ERROR_CONFIRMED
- CRITICAL_ERROR_CLEARED
- MORE_REVIEW_REQUIRED

Then:

```bash
jaisl-expert-adjudication --critical-cases evidence/expert/critical-cases.json --records evidence/expert/adjudication.json --output evidence/expert/adjudication-gate.json
```

The adjudication gate is ready only when every critical case has an explicit record and no case remains confirmed/unresolved.

## Independence rule

- reviewers do not see another reviewer's scores before submission
- implementation authors do not edit submitted ratings
- original ratings are preserved after adjudication
- reviewer disagreement remains visible in the research record

## Completion boundary

Expert tooling being implemented does not mean expert review is complete. Completion still requires actual independent human ratings tied to the frozen packet.
