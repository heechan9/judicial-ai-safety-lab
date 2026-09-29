# Judicial AI Safety Lab v12.0

대한민국 사법·법률 분야 생성형 AI를 **위험평가 → 동일조건 검증 → 적대적 테스트 → 독립검증 → 법적 근거 변경감지 → 지속 모니터링 → 인간검토** 순서로 점검하는 연구용 PoC입니다.

> **Research prototype only.** 공식 법원 시스템, 법률판단 도구 또는 인증 제품이 아닙니다.

## 프로젝트 방법론
- **TriGuard AI** — Risk/Source Inventory, source/status inspection
- **Bunkering AI** — baseline-vs-AI, stress scenarios, evaluation contract/replay
- **AdversarialAI Security** — clean/attack, ASR, independent rerun/evidence integrity
- **FabGuard AI** — frozen baseline, drift, prioritized human review/audit governance

## v3.0 — evidence metadata + legislative lifecycle
- v1.5 전체 파이프라인 유지
- 법제처 현행법령 connector contract
- **법령 변경이력 `lsHstInf` + 조문별 변경이력 `lsJoHstInf`**
- 법제처 지능형 법령검색 `aiSearch` URL builder
- **헌법재판소 공개데이터 capability manifest**
  - 한글판례 목록/상세
  - 최근 주요결정
  - 선고목록
- 위헌·헌법불합치·한정위헌 상태 → Human Review guard
- 변경된 법령/조문에 연결된 scenario만 골라 재검증하는 regression targeting
- 법률안/심사중 자료는 현행법으로 취급하지 않는 status guard
- 법원 connector는 승인/공개 endpoint 전까지 contract-only
- 국회는 다음 확장용 source slot 유지

## Run
```bash
python -m pip install -e .
python -m judicial_ai_safety_lab.cli
pytest -q
```

v2.0 검증 스냅샷: CLI 통합 실행 PASS, pytest 12/12 PASS. v2.5는 Claude UI/UX 감사 결과를 바탕으로 일반인이 먼저 이해할 수 있도록 시각화·용어·정보계층을 재설계한 웹데모 버전입니다.

## 데이터 경계
합성 fixture와 연구용 위험가중치를 사용합니다. 공식 데이터 connector는 read-only 원칙이며 인증키를 저장소에 커밋하지 않습니다. AI가 법적 판단을 확정하지 않고 고위험·불확실·헌법상태 영향 결과를 사람에게 넘깁니다.


## Contributors & verification
- **최희찬 (heechan9)** — research lead / human final decision
- **OpenAI ChatGPT / Codex** — architecture, implementation, tests, code/evidence audit, documentation and integration support
- **Anthropic Claude** — completed v2.5 UI/UX·정보구조·가독성 review; later re-audit briefs are tracked separately
- **Google Jules** — independent code/evidence audit role; prepared audit briefs are not marked complete without a verifiable result

See [CONTRIBUTORS.md](CONTRIBUTORS.md) and the [AI contribution ledger](docs/AI_CONTRIBUTION_LEDGER.md).


## 🌐 Web demo
사법정책 연구도구의 성격이 드러나도록 네이비·아이보리 기반의 공개 데모 UI를 제공합니다.

- [Demo source](docs/index.html)
- GitHub Pages를 `main /docs`로 활성화하면 공개 URL로 바로 사용할 수 있습니다.
- 화면의 수치는 현재 합성 fixture 기반 검증 결과이며 실제 법원·사건 성능을 의미하지 않습니다.


## UI/UX audit remediation
Anthropic Claude의 독립 UI/UX·정보구조 감사 finding을 검토해 v2.5 데모에 반영했습니다. 임의 threshold나 존재하지 않는 검증시각은 추가하지 않았습니다.

- [Claude UI/UX remediation record](docs/audits/CLAUDE_UI_UX_REMEDIATION.md)
- Live demo: https://heechan9.github.io/judicial-ai-safety-lab/


### v2.5 public-first design principle
첫 화면은 전문 지표보다 **왜 사람 확인이 필요한지**를 쉬운 한국어와 시각적 흐름으로 먼저 설명합니다. Risk/ASR/hash/manifest 등 전문정보는 단계적으로 펼쳐보도록 분리했습니다.


### v3.0 additions
- Evidence metadata schema: `evaluated_at`, `fixture_version`, `evaluation_version`, commit SHA
- Research risk thresholds disclosed in UI: LOW 0–29.99 / WATCH 30–59.99 / HIGH 60–100 (not an official judicial standard)
- 2D risk-weight visualization and expanded glossary
- National Assembly legislative lifecycle contract with strict `not effective law` guard for non-effective bill states
- Assembly live adapter remains pending until an official endpoint/schema is pinned and verified


## v3.5 — governance layer verified
- Added governance engine for evidence uncertainty states: SUPPORTED / UNCERTAIN / CONFLICTING / CHANGED / UNSUPPORTED.
- Added dual legal-evidence + technical-safety review routing.
- Added targeted change-impact/regression feedback loop.
- Added minimal rights/data review flags for personal-data, purpose-basis, cross-border and TDM status.
- Added second-look challenge output for omitted/conflicting/changed sources and technical findings.
- Added plain-language explanation mapping for public-facing UI.
- Full reconstructed repository test suite: **22/22 PASS** after v3.5 integration.

- v3.5 verification scope: source/test files were re-fetched from GitHub and executed in a clean local reconstruction with PYTHONPATH=src.


## v4.0 — audit provenance + temporal evidence guards
- Requirement-level defect/retest Quality Log with pinned Git revisions.
- Read-only evidence bundle integrity audit with SHA-256 manifest comparison.
- Frozen evidence cutoff to block hindsight leakage from later legal material.
- Pinned evidence snapshot contract and source→analysis lineage comparison.
- Non-effective legislative states expanded and fail-closed lifecycle validation.
- UNCERTAIN state made reachable and tested separately from CONFLICTING / CHANGED / UNSUPPORTED.
- Governance loop now rejects failed scenarios outside the affected set.
- GitHub Actions CI added with retained JUnit artifact.
- Latest verified CI on v4.0 code: **67/67 tests PASS**.

External audit request files:
- [Jules code audit request](docs/audits/JULES_CODE_AUDIT_REQUEST_V40.md)
- [Claude public-first UI/UX re-audit request](docs/audits/CLAUDE_UI_REAUDIT_REQUEST_V40.md)

`Integrity PASS`, `Ready to Reproduce`, `Independent verification`, and `Live connector` remain different states.


## v4.5 — verification planning + evidence semantics
- **Legal Belief State** for partial-observation verification status. This is not a probability of legal correctness.
- **Review Planner** ranks what to verify next using information gain / urgency / review cost. It never ranks legal outcomes.
- **Hard-invalid vs comparable-difference split**: identity/structure mismatches abort; valid result differences are collected for review.
- **Evidence Verification Level** separates VERIFIED / artifact-consistent / missing-original / conflicting / unsupported evidence states from legal uncertainty.
- **Frozen Evaluation Baseline** detects post-hoc changes to source snapshots, scenario manifests, model/prompt identifiers, or evaluation contracts.
- **Environment Fingerprint** records reproducibility metadata without claiming the same historical machine/environment.
- **Public Release Privacy Guard** distinguishes current public cleanup from unverified Git history, prior branches/copies, and external caches.
- v4.5 keeps planning strictly on the **verification/review path**, not judgment or sentencing recommendation.
- Latest GitHub Actions verification: **67/67 PASS**, 0 failures, 0 errors.


## v5.0 — claim audit + atomic evidence + review-path simulation
- **Claim-to-Evidence Audit** checks public/research claims against explicit evidence references and verification levels.
- **Evidence Quarantine** prevents invalid evidence from being silently dropped; records quarantine → fix → retest → close/reopen.
- **Atomic Evidence Package** writes per-run artifact SHA-256 + byte-size manifests with explicit limits: integrity is not authenticity or independent verification.
- **Counterfactual Review Simulator** explores verification actions only and ranks paths by unresolved findings and review cost. It does not search legal outcomes.
- Public-facing claims that are missing originals, conflicting, or unsupported are automatically marked for review.
- v5.0 preserves the human-final-decision boundary and keeps planning on verification/review actions only.


## v5.5 — review-session orchestration
- **Finding Registry** gives every unresolved verification issue a stable ID, kind, target and severity.
- **Verification-only Review Policy** blocks judgment/sentencing/verdict action types from the planner.
- **Human Review Session state machine**: COLLECTED → FROZEN → REVIEW_PENDING → REVIEWED → PACKAGED.
- A session cannot be packaged before an explicit human review disposition is recorded.
- Unknown findings cannot be silently marked resolved.
- CLI now builds a finding registry and review-action contracts, then intentionally stops at **REVIEW_PENDING** with `human_disposition = null`.
- The synthetic demo therefore demonstrates the handoff boundary rather than faking a completed human review.


## v6.0 — tamper-evident review provenance
- **Hash-chained audit events** detect later modification, deletion, insertion, or reordering within a recorded review log.
- The chain uses canonical JSON + SHA-256 with a predecessor hash and sequence number for each event.
- **Audit-chain integrity is not external notarization, timestamp authority, identity proof, or authenticity proof.**
- Review packages now freeze the pre-package audit payload, store its chain head, and append the package event separately so the package hash cannot silently exclude a returned mutation.
- `jaisl-review` provides an explicit operator step for recording human disposition and packaging a reviewed session; the main `jaisl` run still stops at REVIEW_PENDING.
- Latest verified GitHub Actions JUnit evidence: **67/67 PASS**, 0 failures, 0 errors.


## v6.5 — strict handoff and package verification
- Machine-readable **Assessment Contract** freezes the automated handoff at REVIEW_PENDING and forbids pre-filled human disposition.
- `jaisl-review` now refuses assessments whose contract baseline/finding set does not match the report body.
- New **Review Package Verifier** recomputes the package hash, validates the pre-package audit chain, checks the package-event predecessor/reference, and validates the final chain summary.
- New `jaisl-verify` CLI verifies packaged human-review records without trusting stored summary fields.
- Package integrity remains separate from legal correctness, operator identity, external notarization, and independent verification.
- Latest v6.5 code is under GitHub Actions verification; completion status is recorded only after CI finishes.


## v7.0 — real official-data pilot + expert evaluation
- Official precedent connector contract for 국가법령정보 공동활용 `target=prec` list/detail APIs; live use requires the owner's `LAW_OC` credential.
- Frozen **real-data manifest** records source identity/order, cutoff, selection rule, record count and canonical hash before evaluation.
- `jaisl-realdata` creates a non-overwriting manifest from normalized official records.
- **Expert Evaluation Contract** rates source traceability, status correctness, uncertainty appropriateness, human-review appropriateness and explanation clarity on 1–5 scales, with critical-error capture.
- `jaisl-expert` produces descriptive summaries and pairwise exact agreement without calling the result an official judicial certification.
- External validation plan, expert form, real-data checklist and audit-result template are committed under `docs/`.
- Verified GitHub Actions JUnit evidence for the v7.0 code/CLI set: **78/78 PASS**, 0 failures, 0 errors.


## v7.5 — frozen pilot + external-audit registry
- **Pre-registered Pilot Selection** freezes stratum targets, selected source IDs, stable order and a selection hash before outcome review.
- `jaisl-pilot` creates a non-overwriting pilot-selection artifact from candidate/target JSON.
- **Blinded Expert Packet** separates reviewer-facing case IDs from implementation context and limits evaluation to evidence handling / uncertainty / review routing / explanation quality.
- **External Audit Registry** accepts only traceable audit records with reviewer/tool, timestamp, exact target commit, scope, evidence reference and explicit COMPLETED/PARTIAL/FAILED status.
- `jaisl-audit` summarizes whether completed code/UI audits actually exist instead of inferring completion from prepared prompts.
- The project still requires a real `LAW_OC` credential and actual reviewer responses before the real-data/expert/external-validation states can move from READY to COMPLETE.


## v8.0 — external validation orchestration
- **External Validation Gate** advances only when required evidence artifacts actually exist and validate; prepared code/templates never count as completed validation.
- **Credential-safe precedent collection** stores official API responses and canonical hashes without persisting `LAW_OC`.
- `jaisl-precedent-collect` captures raw official precedent search responses for later normalization and frozen selection.
- `jaisl-expert-packet` builds a blinded reviewer packet from frozen case outputs.
- `jaisl-validation` computes the current research validation state from internal CI, real-data manifest, frozen pilot selection, expert-review summary, completed code-audit state and claim-audit state.
- Truthful current status remains: internal framework verified; real-data pilot, expert review and completed external code audit are still pending actual external inputs.
- See [v8 real-data runbook](docs/REAL_DATA_RUNBOOK_V8.md) and [external validation status](docs/EXTERNAL_VALIDATION_STATUS.md).


## v8.5 — credentialless public precedent discovery
- Added a **30-case real public Supreme Court precedent discovery pool** from official law.go.kr pages: 20 civil + 10 criminal.
- The pool is explicitly `discovery_only=true` and `pilot_selection_frozen=false`; it is **not** yet the frozen evaluation pilot.
- `jaisl-discovery` validates official HTTPS domain, `precSeq` identity, duplicate IDs, dates, required metadata and unfrozen status.
- This lets the project prepare real-case work before `LAW_OC` is available without pretending that public-web discovery equals API-backed raw evidence.
- See [public precedent discovery provenance](docs/PUBLIC_PRECEDENT_DISCOVERY_V1.md).


## v9.0 — discovery catalog + pilot readiness
- Added a stable **case catalog** between public discovery and the frozen real-data pilot.
- Every discovery-only case is explicitly marked `PUBLIC_WEB_DISCOVERY_ONLY`, with API/raw/normalized/pilot/expert readiness flags forced false.
- `jaisl-catalog` creates a deterministic case catalog with stable JAISL case IDs and a catalog hash.
- `jaisl-readiness` computes per-case missing evidence and allows `pilot_eligible=true` only when API raw evidence, normalized detail and frozen pilot selection are all present.
- Current truthful real-data state: 30 public precedents collected, **0/30 pilot-eligible** until LAW_OC-backed raw collection and normalization are completed.
- See [v9 case catalog](docs/V9_CASE_CATALOG.md) and [real-data progress](docs/REAL_DATA_PROGRESS.md).

- Latest verified GitHub Actions JUnit evidence for v9.0: **115/115 PASS**, 0 failures, 0 errors.


## v9.5 — normalization + verification mapping + expert templates
- Added a strict **NormalizedPrecedentCase** schema that preserves discovery metadata while leaving detail-dependent fields empty until verified official detail exists.
- Added conservative **source-to-verification scenario mappings** for source traceability, status, missing information, legal change and constitutional review; no legal-outcome action is introduced.
- Added **expert-review case templates** with blank system output and `NOT_STARTED` rating state so preparation cannot be mistaken for completed expert review.
- `jaisl-case-template` converts the committed 30-case discovery pool into normalized cases, verification mappings and expert-review templates.
- Current real-data boundary remains unchanged: **0/30 API raw verified, 0/30 detail verified, 0/30 pilot-eligible** until LAW_OC-backed evidence is captured.
- See [v9.5 expert-template flow](docs/V9_5_EXPERT_TEMPLATE_FLOW.md).


## v10.0 — full-cohort pilot freeze + enrichment queue
- The first real-data pilot now freezes **all 30 discovered public precedents** before outcome review, avoiding post-hoc case cherry-picking.
- `jaisl-cohort` locks cohort membership, source IDs, cutoff and cohort hash; later exclusions require a new version.
- `jaisl-enrichment` creates a deterministic 30-case LAW_OC work queue ordered by stable case ID.
- A case leaves the enrichment queue only after API raw evidence and normalized detail are verified.
- Current truthful state remains **30 discovered / 30 queued / 0 pilot-eligible** until LAW_OC-backed collection is performed.
- See [v10 full-cohort pilot](docs/V10_FULL_COHORT_PILOT.md).


## v10.5 — official detail reconciliation
- Added credential-safe **single-precedent detail collection** using the official `target=prec` detail endpoint contract.
- `jaisl-precedent-detail` stores raw detail response + canonical SHA-256 without persisting `LAW_OC`.
- `jaisl-reconcile` compares the frozen discovery identity against official detail before enrichment.
- Case-number/title/precedent-ID mismatches are routed to `IDENTITY_REVIEW_REQUIRED`; they are never silently merged.
- Only reconciled matching detail can become `VERIFIED_DETAIL_READY`, with both raw-response hash and normalized-case hash preserved.
- Current real-data state remains **0/30 verified** until the credential-backed detail commands are actually run.
- See [v10.5 detail reconciliation](docs/V10_5_DETAIL_RECONCILIATION.md).

- Latest verified GitHub Actions JUnit evidence for v10.5: **115/115 PASS**, 0 failures, 0 errors.


## v11.0 — resumable batch official-detail pipeline
- Added a resumable **30-case official-detail batch collector** that writes one non-overwriting evidence envelope per precedent and never persists `LAW_OC`.
- Existing detail files are skipped so interrupted runs can resume without overwriting prior evidence.
- Network/API failures are recorded explicitly and never counted as successful evidence.
- Added **batch identity reconciliation** across the frozen discovery cohort and a compact **evidence index** summarizing VERIFIED / REVIEW / PENDING status per source.
- `jaisl-detail-batch`, `jaisl-batch-reconcile` and `jaisl-evidence-index` complete the software path from the 30-case queue to per-case verified-detail readiness.
- Current truthful external-data status remains **0/30 verified** until an actual LAW_OC-backed batch run is executed.
- See [v11 batch detail pipeline](docs/V11_BATCH_DETAIL_PIPELINE.md).

- Latest verified GitHub Actions JUnit evidence for v11.0: **123/123 PASS**, 0 failures, 0 errors.


## v11.5 — fail-closed real-data pilot preflight
- Added `jaisl-preflight` to block the real-data run until every frozen cohort source has verified official detail evidence.
- The gate rejects missing/extra sources, pending details, identity-review cases and unknown evidence states.
- `ready_for_expert_packet` intentionally remains false even when all 30 details are verified, because expert packets require later frozen JAISL outputs.
- This separates **software readiness**, **evidence readiness**, and **expert-review readiness** as distinct states.
- Current truthful state without a LAW_OC-backed run remains **0 verified / 30 pending / preflight not ready**.
- See [v11.5 pilot preflight](docs/V11_5_PILOT_PREFLIGHT.md).

- Latest verified GitHub Actions JUnit evidence for v11.5: **127/127 PASS**, 0 failures, 0 errors.


## v12.0 — fail-closed official detail payload validation
- A live PC run exposed a real validation gap: an invalid placeholder `LAW_OC` produced API error objects shaped like `{result, msg}`, which the earlier collector hashed and counted as collected evidence.
- v12.0 now rejects any detail response that does not contain exactly one precedent-detail object with `판례정보일련번호` plus case identity fields.
- The returned precedent ID must exactly match the requested `prec_seq`; mismatches fail closed.
- API error/empty/non-detail payloads are now recorded as `FAILED`, never `COLLECTED`.
- Evidence generated before this fix with an invalid credential must be discarded and recollected with a real `LAW_OC`.
