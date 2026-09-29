# JAISL v14.0 paper evidence matrix

This matrix links paper claims to the strongest currently available repository evidence.

| Paper claim | Evidence state | Repository evidence | Boundary |
|---|---|---|---|
| Official precedent pilot contains 30 public Supreme Court cases | Verified | frozen discovery pool + live evidence index | Does not establish legal correctness |
| LAW_OC-backed detail collection completed | Verified | 30 collected / 0 failed | Credential value itself is never stored |
| Identity reconciliation completed | Verified | 30 VERIFIED_DETAIL_READY / 0 review / 0 pending | Title equivalence remains conservative |
| Real-data preflight passed | Verified | blockers=[] / ready_for_real_data_run=true | Preflight is evidence readiness, not legal accuracy |
| v13 assessment fingerprint | Reproduced | assessment hash `4ee3e039c35d1a9d49ba8496d3a81be514df414ec8c4514fe3a81d7abb324ab2` | Public repository need not contain raw credentialed evidence |
| Blinded expert packet fingerprint | Reproduced | packet hash `ad6a033eee9d26a3633695901475f7b19a76b64a9be675dd3b762533b277fe27` | Packet readiness is not expert-review completion |
| Expert completion controls | Implemented | min 2 reviewers, complete case coverage, duplicate rejection, critical-error gate | Actual expert ratings are pending |
| Ordinal inter-rater reliability | Implemented in v14.0 | quadratic weighted Cohen kappa per dimension | Descriptive pilot reliability only |
| Critical-error adjudication | Implemented in v14.0 | additive adjudication record + fail-closed gate | Original ratings are never overwritten |
| Jules external code/evidence audit | Pending | v13 audit request pinned to target commit | Request is not a completed audit |
| Claude external UI/claim audit | Pending | v13 re-audit request pinned to target commit | Request is not a completed audit |
| Judicial certification / production approval | Not claimed | explicit research-only boundaries | Outside current study |

## Frozen technical identifiers

- frozen v13 code target: `3de937f3833e08c3e0c141444ae71fcbf9fc5148`
- assessment hash: `4ee3e039c35d1a9d49ba8496d3a81be514df414ec8c4514fe3a81d7abb324ab2`
- expert packet hash: `ad6a033eee9d26a3633695901475f7b19a76b64a9be675dd3b762533b277fe27`
- latest pre-v14 verified CI baseline: v13.5 **142/142 PASS**

The v14.0 code changes add expert reliability/adjudication methods; their test count is recorded only after GitHub Actions completes.
