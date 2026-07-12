# 데이터 교체 방법 (비개발자용)

사이트의 숫자와 요약문은 이 폴더의 파일 **2개**만 바꾸면 갱신됩니다.
코드는 건드릴 필요 없습니다.

## 1. `summary.txt` — 첫 화면 요약문

- **첫 줄**: 기간 표시 (예: `Q3 2026`)
- **둘째 줄부터**: 요약 문단 (영문, 3~5문장)

메모장이나 아무 텍스트 편집기로 열어서 수정하면 됩니다.

## 2. `cards.csv` — 숫자 카드 3개

엑셀에서 열어 수정한 뒤 **CSV 형식 그대로 저장**하세요.
첫 줄(제목 줄)은 지우지 말고, 아래 3줄의 값만 바꿉니다.

| 열 | 의미 | 예시 |
|---|---|---|
| `label` | 카드 제목 | Quarterly import volume |
| `value` | 큰 숫자 | 182 |
| `unit` | 단위 (없으면 비워둠) | tonnes |
| `delta` | 증감 (+/- 로 시작) | +6.4% |
| `delta_note` | 비교 기준 | vs previous quarter |

## 3. `imports.csv` — 수입량 추이 차트

연도·국가별 수입량 데이터입니다. 엑셀에서 열어 수정한 뒤 **CSV 형식 그대로 저장**하세요.
첫 줄(제목 줄)은 지우지 말고, 행을 추가/수정하면 됩니다. 국가를 추가하면
차트의 국가 선택 목록에 자동으로 나타납니다.

| 열 | 의미 | 예시 |
|---|---|---|
| `year` | 연도 (숫자 4자리) | 2025 |
| `country` | 국가명 (영문) | New Zealand |
| `tonnes` | 수입량 (톤, 숫자만) | 198 |

## 4. `imports-notes.txt` — 차트 아래 해설문

차트 아래에 표시되는 해설 문단(영문 3~5문장)입니다.
메모장으로 열어 내용 전체를 바꾸면 됩니다.

## 5. `news.csv` — 뉴스 하이라이트

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

## 6. `reports.csv` + `reports` 폴더 — 분기 보고서 아카이브

1. PDF 파일을 저장소 최상위의 `reports` 폴더에 업로드합니다
   (GitHub 웹: `reports` 폴더 → **Add file → Upload files**)
2. `data/reports.csv`에 한 줄 추가합니다

| 열 | 의미 | 예시 |
|---|---|---|
| `quarter` | 분기 표시 | 2026 Q3 |
| `title` | 보고서 제목 (사이트에 표시됨) | Korean Velvet Market Quarterly Report — Q3 2026 |
| `file` | PDF 경로 (`reports/파일명.pdf`) | reports/2026-Q3.pdf |

## 7. `references.csv` — 참고자료 링크

| 열 | 의미 | 예시 |
|---|---|---|
| `title` | 출처 이름 | Korea Customs Service |
| `url` | 링크 | https://... |
| `note` | 한 줄 설명 (없으면 비워둠) | Official import statistics |

## 8. 반영하기 (GitHub 웹에서)

1. GitHub 저장소의 `data` 폴더로 이동
2. 바꿀 파일 클릭 → 오른쪽 연필(✏️) 아이콘 클릭
3. 내용 수정 후 **Commit changes** 버튼 클릭
4. 1~2분 뒤 사이트에 자동 반영됩니다
