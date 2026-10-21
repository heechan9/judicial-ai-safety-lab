# 사건별 재실행 결과 대조

2026-10-22 추가. 기존 v13의 30건 평가·전문가 패킷 해시 및 평가 결과는 변경하지 않는다.

## 해결하는 문제

기존 파일 무결성 검증과 단일 행 비교만으로는 재실행에서 빠진 사건, 달라진 판례 근거, 같은 근거에서 달라진 출력·검토 경로를 한꺼번에 확인하기 어렵다. 또한 v13 `assessment_hash`는 대상 커밋과 입력 해시를 고정하며 출력 문구까지 보증하지 않는다.

`jaisl-assessment-replay`는 기존 `jaisl.real-assessment.v1` 파일 두 개를 읽어 입력과 출력을 별도로 대조한다. v13 입력 해시를 재계산하고, 정규화 데이터의 해시·식별정보·사건 중복·개수·필수 필드를 확인한 뒤 사건 ID로 대응시킨다. 원문·출력 전문·연락처를 보고서에 복제하지 않는다.

## 다른 프로젝트에서 적용한 설계

직접 코드를 복사하지 않고 다음 구현을 검토해 법률 AI 자료 구조에 맞게 구현했다. 외부 패키지 의존성은 추가하지 않았다.

| 프로젝트와 검토 커밋 | 확인한 구현 | 이번 적용 |
| --- | --- | --- |
| Bunkering AI `0c14adb15d09437894fd6ff0a3c870fdc90e148a` | `evaluation/contract.py`, `validate_fair_evaluation_plan` | 사건 집합과 입력 조건이 같은 경우에만 출력 비교 허용 |
| AdversarialAI Security `75defef0d69c1741025306e0150c770e84b23a30` | `configs/stage_b_verification_contract.json` | 입력 고정과 결과 대조 분리, 산출물 비교와 독립 실행 인증 구분 |
| TriGuard AI `d0db55a5c0cbbad6c70970fbf7f3228430843a17` | `scripts/source_manifest.py` | 사건 추가·누락·근거 변경 목록과 재검증 대상 산출 |
| FabGuard AI `519654ea2362accf2127f4255a4379132402383c` | `src/fabguard/independent_validation.py` | 입력 계약 오류 시 중단, 구조 검증과 실제 성능 검증 범위 명시 |

## 실행

```bash
python -m pip install -e .
jaisl-assessment-replay --reference evidence/pilot/real-assessment-v1.json --candidate evidence/pilot/real-assessment-rerun.json --output evidence/pilot/replay-comparison.json
```

입력 파일은 수정하지 않으며 출력 경로에 기존 파일이 있으면 덮어쓰지 않는다. 새 후보 평가 파일은 별도로 실제 실행해 생성해야 한다. 이 명령은 평가 엔진을 실행하지 않는다.

| 결과 | 의미 | 종료 코드 |
| --- | --- | --- |
| MATCH | 동일 사건·입력에서 대조 대상 출력 필드 일치 | 0 |
| OUTPUT_CHANGED | 동일 입력에서 출력·검토 경로 변경 | 1 |
| NOT_COMPARABLE | 사건 추가·누락, 식별정보 또는 입력 근거 변경 | 1 |
| 입력 오류 | 해시 불일치, 중복 사건, 잘못된 JSON 등 | 2 |

커밋 변경 자체는 비교를 막지 않는다. 동일 입력에서 새 코드의 출력 변화를 살피기 위해 두 커밋을 보고서에 표시한다. 배열 순서가 바뀌어도 사건 ID로 비교하지만 각 원본의 v13 해시는 원래 순서대로 검증한다. 전체 산출물 해시도 함께 기록한다.

## 검증 한계

MATCH는 대상 필드의 일치이며 법률적 정확성, 실제 재실행 수행, 실행자 독립성, 전문가 평가 완료를 뜻하지 않는다. 원응답 본문이 assessment에 포함되지 않으므로 원응답 해시는 기록값 사이에서 비교하며, 원파일 무결성 검사는 기존 `jaisl-audit`를 함께 사용한다. 결과가 달라진 사건은 사람이 검토해야 하며 자동으로 개선·악화 판정을 하지 않는다. 새 실제 판례 평가나 전문가 점수는 이번 작업에서 생성하지 않았다.
