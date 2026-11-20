# AI 협업 프로그래밍 11주차 실습 (테스트 코드 생성 및 비교)

## 1. What (무엇을 하는 프로젝트인가)
성적 CSV 파일을 읽어 검증하는 `load_scores(path)` 함수와 논리 버그가 포함된 `bug3_logic.py`를 대상으로, AI에게 **코드**를 줬을 때와 **명세서**를 줬을 때 생성되는 `pytest` 단위 테스트의 품질과 차이를 실험·비교하는 저장소입니다.

## 2. Why (왜 만들었는가)
- AI에게 구현 코드만 제공하고 테스트를 요청할 때 발생할 수 있는 누락 케이스 및 버그 굳힘(bug cementing) 위험을 확인하기 위함입니다.
- 10주차에 작성한 6칸 명세서 기반으로 테스트를 요청했을 때 예외 처리와 코드 커버리지가 어떻게 달라지는지 수치로 검증하기 위함입니다.

## 3. How (설치 및 실행 방법)
### 사전 준비
Python 3 환경에서 `pytest`와 `pytest-cov`를 설치합니다.

```bash
python -m pip install pytest pytest-cov
```

### 테스트 실행
저장소 최상위 폴더에서 아래 명령어를 실행합니다.

```bash
# 프롬프트 A (코드 제공) 테스트 및 커버리지
pytest test_ai_A.py --cov=week11_files --cov-report=term-missing -v

# 프롬프트 B (명세 제공) 테스트 및 커버리지
pytest test_ai_B.py --cov=week11_files --cov-report=term-missing -v

# 버그 코드 함정 실험
pytest test_bug3_logic.py -v
```

## 4. 테스트 방법 및 결과
| 테스트 파일 | 프롬프트 조건 | 테스트 개수 | 통과 여부 | `load_scores.py` 커버리지 | 주요 특징 |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `test_ai_A.py` | 코드 전체 제공 | 13개 | 13 / 13 통과 | 75% | 기본 정상·경계값 및 `FileNotFoundError` 1종 검증 |
| `test_ai_B.py` | 10주차 명세 6칸 제공 | 20개 | 20 / 20 통과 | 83% | 헤더·디렉터리·UTF-8 인코딩 등 예외 4종(`raises` 7건) 추가 검증 |
| `test_bug3_logic.py` | 버그 코드 제공 | 4개 | 2 failed / 2 passed | - | `find_max` 버그는 감지했으나 `count_pass` 첫 케이스에서 버그 값(`3`)을 기대값으로 기록 |

## 5. 파일 구성
```text
.
├── .gitignore                 # 가상환경 및 pytest 캐시 제외 설정
├── README.md                  # 프로젝트 설명 및 실험 결과 문서
├── test_ai_A.py               # 프롬프트 A(코드 제공)로 생성한 pytest 테스트
├── test_ai_B.py               # 프롬프트 B(명세 제공)로 생성한 pytest 테스트
├── test_bug3_logic.py         # 버그 코드(bug3_logic.py) 대상 함정 실험 테스트
└── week11_files/
    ├── load_scores.py         # 테스트 대상 성적 CSV 로더 함수
    └── bug3_logic.py          # 논리 버그가 포함된 실험용 코드
```

## 6. 만든 사람 및 AI 활용 내역
- **만든 사람**: 2026100176 권태욱 (한국기술교육대학교 기계공학부)
- **AI 활용 내역**:
  - `test_ai_A.py`: `load_scores.py` 코드를 입력해 AI로 단위 테스트 자동 생성
  - `test_ai_B.py`: 10주차 6칸 명세서(역할·목표·제약·점검 항목·단계·재검토)를 입력해 AI로 단위 테스트 자동 생성
  - `test_bug3_logic.py`: 의도적 논리 버그가 있는 `bug3_logic.py`를 AI에게 입력해 버그 굳힘 여부 검증
  - 모든 생성 테스트는 직접 `pytest` 및 `pytest-cov`로 실행하여 수치와 실패 원인을 검증함
