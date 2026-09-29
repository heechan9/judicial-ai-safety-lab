# JAISL v13.5 expert-review protocol

## Purpose

This protocol evaluates the quality of JAISL evidence handling and review routing.
It does **not** ask reviewers to choose a judgment, sentence, verdict, or preferred
legal-policy outcome.

The frozen real-data assessment remains tied to v13.0 target commit:
`3de937f3833e08c3e0c141444ae71fcbf9fc5148`.

v13.5 adds the completion controls used when human reviewers begin submitting ratings.

## Minimum panel

- at least **2 independent reviewers**
- each frozen case must receive at least **2 ratings**
- reviewers use stable IDs such as `R1`, `R2`, `R3`
- reviewer real identities/contact information should be stored outside the public repository unless publication consent is explicit

Recommended backgrounds:
- one practicing attorney / former legal practitioner
- one legal researcher, law professor, judicial-policy researcher, or comparable legal specialist
- an optional third reviewer for disagreement/critical-error adjudication

## Five rating dimensions

Each case is rated 1–5 on:

1. source traceability
2. status correctness
3. uncertainty appropriateness
4. human-review appropriateness
5. explanation clarity

Reviewers also record:
- `critical_error` true/false
- short comment

## Independence

Before submission:
- reviewers receive the same frozen packet
- reviewers must not see another reviewer's scores
- implementation authors must not edit submitted ratings

After submission:
- original ratings are preserved
- ordinary disagreement remains visible
- critical errors require an adjudication step before the review can be summarized as complete

## Commands

Generate blank templates after the frozen expert packet exists:

```bash
jaisl-expert-rating-template \
  --packet evidence/expert/real-pilot-v1.json \
  --reviewers evidence/expert/reviewer-ids.json \
  --output evidence/expert/rating-templates.json
```

After reviewer scores are converted to the ExpertRating JSON list:

```bash
jaisl-expert-review-gate \
  --ratings evidence/expert/ratings.json \
  --packet evidence/expert/real-pilot-v1.json \
  --output evidence/expert/review-gate.json
```

The gate fails closed on:
- fewer than two independent reviewers
- any case with insufficient reviewer coverage
- duplicate reviewer/case ratings
- unexpected case IDs
- any critical error that still requires adjudication

Only when coverage is complete and critical errors are cleared does
`ready_to_summarize=true`.

Then:

```bash
jaisl-expert --ratings evidence/expert/ratings.json --output evidence/expert/summary.json
```

## Completion boundary

Expert-review tooling being implemented does **not** mean expert review is complete.
Completion requires actual independent human ratings tied to the frozen packet.
