# Judicial AI Safety Lab v2.0

대한민국 사법·법률 분야 생성형 AI를 **위험평가 → 동일조건 검증 → 적대적 테스트 → 독립검증 → 법적 근거 변경감지 → 지속 모니터링 → 인간검토** 순서로 점검하는 연구용 PoC입니다.

> **Research prototype only.** 공식 법원 시스템, 법률판단 도구 또는 인증 제품이 아닙니다.

## 프로젝트 방법론
- **TriGuard AI** — Risk/Source Inventory, source/status inspection
- **Bunkering AI** — baseline-vs-AI, stress scenarios, evaluation contract/replay
- **AdversarialAI Security** — clean/attack, ASR, independent rerun/evidence integrity
- **FabGuard AI** — frozen baseline, drift, prioritized human review/audit governance

## v2.0
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

v1.5 로컬 기준 8 tests PASS. v2.0은 새 법령변경·헌재 계층에 대한 테스트를 추가했습니다.

## 데이터 경계
합성 fixture와 연구용 위험가중치를 사용합니다. 공식 데이터 connector는 read-only 원칙이며 인증키를 저장소에 커밋하지 않습니다. AI가 법적 판단을 확정하지 않고 고위험·불확실·헌법상태 영향 결과를 사람에게 넘깁니다.
