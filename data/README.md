# 데이터 업데이트 가이드 (비개발자용)

이 문서는 두 부분으로 나뉩니다.

- **A. 정기 업데이트 체크리스트** — 매달·분기마다 순서대로 따라 하면 됩니다.
- **B. 파일별 설명** — 각 데이터 파일이 무엇이고 어떻게 채우는지 참고용으로 찾아볼 때 씁니다.

---

## A. 정기 업데이트 체크리스트

### 매달 할 일 — 없음

1단계(지금)는 분기 단위 수동 업데이트입니다. 매달 할 일은 없습니다.
(뉴스만 더 자주 올리고 싶다면 5번 `news.csv`만 수시로 갱신해도 됩니다.)

### 분기마다 할 일

1. **원본 자료를 받는다**
   - QIA(농림축산검역본부) 수입 통계 엑셀
   - Stats NZ 수출 통계 CSV (`Harmonised Trade - Exports (Monthly)`)
   - 이번 분기 보고서 (워드 또는 PDF)

2. **원본을 저장소의 `sources` 폴더에 올린다**
   GitHub 웹 → `sources` 폴더 → **Add file → Upload files** → 원본 파일 업로드 → Commit

3. **수치 CSV를 갱신한다**
   - 클로드코드를 쓸 수 있다면: "sources 폴더에 새 원본 올렸으니 imports.csv랑
     nz-exports.csv 갱신해줘"라고 요청하면 아래 스크립트를 대신 실행해 줍니다
   - 직접 실행하려면 터미널에서:
     ```
     python3 scripts/convert_quarantine.py "sources/<검역 flat CSV 파일명>"
     python3 scripts/convert_nz_exports.py "sources/<NZ 수출 flat CSV 파일명>"
     ```
   - 실행하면 화면에 **처리한 행 수 · 기간 · 연도별 합계**가 출력됩니다.
     이 숫자가 원본의 합계와 맞는지 눈으로 한 번 확인하세요.

4. **요약문·카드·해설문을 새 분기 내용으로 고친다**
   `summary.txt`, `cards.csv`, `imports-notes.txt`, `nz-exports-notes.txt`
   (아래 B절 참고. 클로드코드에게 "이번 분기 보고서 내용으로 요약이랑 카드
   갱신해줘"라고 요청해도 됩니다.)

5. **뉴스를 추린다**
   분기 보고서의 "Korean news" 섹션에서 기사를 골라 `news.csv`에 추가합니다.

6. **보고서 PDF를 아카이브에 올린다**
   워드 파일은 PDF로 변환해서 `reports` 폴더에 올리고, `reports.csv`에 한 줄 추가합니다.

7. **커밋하고 1~2분 뒤 실제 사이트에서 확인한다**
   맨 위부터 맨 아래까지 스크롤해서 빈 화면·깨진 차트가 없는지 확인합니다.

---

## B. 파일별 설명

### 1. `summary.txt` — 첫 화면 요약문

- **첫 줄**: 기간 표시 (예: `Q3 2026`)
- **둘째 줄부터**: 요약 문단 (영문, 3~5문장)

메모장이나 아무 텍스트 편집기로 열어서 수정하면 됩니다.

### 2. `cards.csv` — 숫자 카드 3개

엑셀에서 열어 수정한 뒤 **CSV 형식 그대로 저장**하세요.
첫 줄(제목 줄)은 지우지 말고, 아래 3줄의 값만 바꿉니다.

| 열 | 의미 | 예시 |
|---|---|---|
| `label` | 카드 제목 | Quarterly import volume |
| `value` | 큰 숫자 | 182 |
| `unit` | 단위 (없으면 비워둠) | tonnes |
| `delta` | 증감 (+/- 로 시작) | +6.4% |
| `delta_note` | 비교 기준 | vs previous quarter |

### 3. `imports.csv` / `imports-monthly.csv` / `imports-annual.csv` — 수입량 추이 차트

- **`imports-monthly.csv`**: QIA 검역 월 단위 원본. 연도 × 월 × 국가 ×
  형태(dried/frozen) × kg. **손으로 고치지 마세요** — `convert_quarantine.py`가
  검역 flat CSV에서 자동 생성합니다.
- **`imports.csv`**: 차트가 실제로 읽는 "건조 환산 톤" 파일 (건조 kg + 냉동 kg
  × 0.33, ÷1000). 2019년 이후는 월 단위(`imports-monthly.csv`)에서 집계하고,
  2013~2018년은 예전 연간 통계(`imports-annual.csv`)에서 보존합니다.
- **`imports-annual.csv`**: 2013~2018 과거분을 담은 연간 통계 (예전 QIA 엑셀 기반).

검역 flat CSV를 새로 받으면 손으로 고치지 말고 `scripts/convert_quarantine.py`를
실행하세요 (A절 참고).

| 열(imports.csv) | 의미 | 예시 |
|---|---|---|
| `year` | 연도 | 2025 |
| `country` | 국가명 (영문) | New Zealand |
| `tonnes` | 건조 환산 수입량 (톤) | 40.0 |

> **참고 1 — 진행 중인 해**: 12개월이 다 차지 않은 해(예: 2026)는 차트에서
> 자동으로 제외됩니다. 월별 상세는 `imports-monthly.csv`와 다운로드 파일에 남습니다.
>
> **참고 2 — 2026년 검역 건수(Cases)**: 2026년부터 검역 건수에는 일반 여행객의
> 핸드캐리(직접 소지) 반입 건이 포함되어 건수가 크게 늘 수 있습니다. 다만 차트는
> 건수가 아니라 kg만 사용하므로 그래프에는 영향이 없습니다.

### 4. `imports-notes.txt` — 수입량 차트 아래 해설문

차트 아래에 표시되는 해설 문단(영문 3~5문장)입니다.
메모장으로 열어 내용 전체를 바꾸면 됩니다.

### 5. `nz-exports.csv` / `nz-exports-monthly.csv` — NZ 수출 추이 차트

- **`nz-exports-monthly.csv`**: 원본에 가까운 자료. 연도 × 월 × 목적지 국가 ×
  형태 × kg. **손으로 고치지 마세요** — `convert_statsnz.py`가 자동 생성합니다.
- **`nz-exports.csv`**: 위 파일을 연도별로 합산한 톤 수치이며, 차트가 실제로
  읽는 파일입니다. 녹용 3품목(건조/냉동/기타)을 **전체 목적지 합산**한 값입니다
  (뿔·분말 제외). 한국만 따로 보고 싶으면 월 단위 파일의 `destination` 열을 쓰세요.

NZ 수출 flat CSV를 새로 받으면 `scripts/convert_nz_exports.py`를 실행하세요 (A절 참고).

### 6. `nz-exports-notes.txt` — NZ 수출 차트 아래 해설문

`imports-notes.txt`와 동일한 방식. 메모장으로 내용을 바꾸면 됩니다.

### 7. `news.csv` — 뉴스 하이라이트

최근 기사 목록입니다. **오늘 기준 90일 이내** 날짜의 기사만 사이트에 표시됩니다
(오래된 행은 지우지 않아도 자동으로 숨겨집니다).

| 열 | 의미 | 예시 |
|---|---|---|
| `date` | 기사 날짜 (연-월-일) | 2026-07-02 |
| `title` | 기사 제목 (영문) | Korea's health food market grows |
| `summary` | 한 줄 요약 (영문) | Velvet products led growth... |
| `source` | 매체명 (없으면 비워둠) | Korea Herald |
| `url` | 기사 링크 (없으면 비워둠) | https://... |

※ 제목이나 요약에 쉼표(,)가 들어가면 그 칸 전체를 큰따옴표("...")로 감싸세요.
엑셀에서 CSV로 저장하면 자동으로 처리됩니다.

### 8. `reports.csv` + `reports` 폴더 — 분기 보고서 아카이브

1. PDF 파일을 저장소 최상위의 `reports` 폴더에 업로드합니다
   (GitHub 웹: `reports` 폴더 → **Add file → Upload files**).
   워드(.docx) 원본만 있다면 PDF로 변환한 뒤 올려주세요.
2. `data/reports.csv`에 한 줄 추가합니다

| 열 | 의미 | 예시 |
|---|---|---|
| `quarter` | 분기 표시 | 2026 Q3 |
| `title` | 보고서 제목 (사이트에 표시됨) | Korean Velvet Market Quarterly Report — Q3 2026 |
| `file` | PDF 경로 (`reports/파일명.pdf`) | reports/2026-Q3.pdf |

### 9. `references.csv` — 참고자료 링크

| 열 | 의미 | 예시 |
|---|---|---|
| `title` | 출처 이름 | Korea Customs Service |
| `url` | 링크 | https://... |
| `note` | 한 줄 설명 (없으면 비워둠) | Official import statistics |

### 10. 데이터 CSV 다운로드

각 섹션 하단의 "Download data (CSV)" 링크는 그 섹션이 실제로 읽는 CSV 파일을
그대로 내려받는 링크입니다. 화면의 숫자와 다운로드 파일은 항상 같은 파일이므로
따로 맞출 필요가 없습니다.

### 11. 반영하기 (GitHub 웹에서)

1. GitHub 저장소의 `data` 폴더로 이동
2. 바꿀 파일 클릭 → 오른쪽 연필(✏️) 아이콘 클릭
3. 내용 수정 후 **Commit changes** 버튼 클릭
4. 1~2분 뒤 사이트에 자동 반영됩니다
