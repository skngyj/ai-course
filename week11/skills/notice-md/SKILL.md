---
name: notice-md
description: 공지, 안내문, 알림처럼 여러 사람에게 일정과 장소를 알리는 글을 마크다운(md) 파일로 만들 때 쓴다. 보고서나 회의록 같은 워드 문서, 엑셀 성적표에는 쓰지 않는다.
---

# 안내문 md 만들기

## 규칙

- 파일 이름은 `notice_YYYYMMDD.md` (오늘 날짜). 다른 이름을 쓰지 않는다.
- 첫 줄은 `# 제목`이다.
- 둘째 줄은 `> 게시일: YYYY-MM-DD` (오늘 날짜)다.
- 절은 `## 요약`, `## 세부 사항`, `## 문의` 세 개를 이 순서로 둔다.
- `## 요약`에는 받은 `내용:`의 문장을 고치지 않고 그대로 쓴다. 내용을 다른 절에 다시 쓰지 않는다.
- `## 세부 사항`은 대상, 일시, 장소, 준비물 순서의 목록이다. 각 줄은 `- **항목**: 값` 꼴이다. 받은 내용에 없는 항목은 줄을 빼지 말고 값에 `없음`이라고 쓴다.
- 일시의 날짜는 `2026년 11월 20일(금)`처럼 요일을 붙인다. **요일은 기억으로 쓰지 말고 아래 `korean_date`로 계산한다.**
- 받은 내용을 그대로 쓴다. 문장을 늘리거나 이모지를 넣지 않는다.

## 코드

다음 함수를 그대로 복사해 쓴다.

```python
from datetime import date

WEEK = "월화수목금토일"

def korean_date(s):
    d = date.fromisoformat(s)
    return f"{d.year}년 {d.month}월 {d.day}일({WEEK[d.weekday()]})"

today = date.today()
filename = f"notice_{today:%Y%m%d}.md"
```

파일은 `open(filename, "w", encoding="utf-8")`로 저장한다. 저장한 뒤 `print("saved", filename)`으로 파일 이름을 출력한다.
