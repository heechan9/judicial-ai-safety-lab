# Judicial AI Safety Lab v4.0

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
- 최희찬 — research lead / human final decision
- OpenAI ChatGPT / Codex — AI-assisted implementation, tests and documentation
- Google Jules — independent audit slot; completion is recorded only after a verifiable audit

See [CONTRIBUTORS.md](CONTRIBUTORS.md).


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
- Latest verified CI on v4.0 code: **33/33 tests PASS**.

External audit request files:
- [Jules code audit request](docs/audits/JULES_CODE_AUDIT_REQUEST_V40.md)
- [Claude public-first UI/UX re-audit request](docs/audits/CLAUDE_UI_REAUDIT_REQUEST_V40.md)

`Integrity PASS`, `Ready to Reproduce`, `Independent verification`, and `Live connector` remain different states.
