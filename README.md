# Judicial AI Safety Lab v1.5

대한민국 사법·법률 분야 생성형 AI를 **위험평가 → 동일조건 검증 → 적대적 테스트 → 독립검증 → 지속 모니터링 → 인간검토** 순서로 점검하는 연구용 PoC입니다.

> **Research prototype only.** 공식 법원 시스템, 법률판단 도구 또는 인증 제품이 아닙니다.

## 4개 프로젝트에서 가져온 방법론
- **TriGuard AI** — Composite Risk, Source Inventory, source/status inspection
- **Bunkering AI** — Evaluation Contract, baseline-vs-AI, stress scenarios, replay
- **AdversarialAI Security** — clean/attack, ASR, independent rerun gate, evidence integrity
- **FabGuard AI** — frozen baseline, drift watch, prioritized human review, audit governance

## v1.5
- Court / MOLEG / Constitutional Court / National Assembly source slots
- proposed/pending ≠ effective guard
- constitutional-status warning
- stress + prompt-injection scenarios
- independent verification gate
- frozen-baseline drift watch
- human-review queue
- SHA-256 evidence/session manifests
- static dashboard
- MOLEG eflaw official API URL builder (live use requires LAW_OC)
- Court connector remains contract-only until an approved/public endpoint is available

## Run
```bash
python -m pip install -e .
python -m judicial_ai_safety_lab.cli
pytest -q
```

Local verification before upload: **8 tests passed**.

Sample records and weights are synthetic research fixtures. High-risk or uncertain results are routed to human review.
