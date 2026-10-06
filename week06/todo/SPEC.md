# 할 일 관리 웹앱 스펙 (todo)

## 1. 기술
- Python Flask와 SQLite(`sqlite3`)를 사용한다.
- 화면은 Jinja 템플릿으로 만든 HTML과 CSS만 사용한다. 외부 CSS 프레임워크(부트스트랩 등)와 JavaScript 프레임워크는 쓰지 않는다.
- 로그인은 없다. 개인용 앱이다.

## 2. 파일
| 파일 | 내용 |
| --- | --- |
| `SPEC.md` | 이 문서 |
| `app.py` | Flask 서버. DB 연결과 라우트 |
| `templates/index.html` | 목록 화면. 추가 폼과 각 할 일의 조작 폼 |
| `test_app.py` | pytest 테스트 |

## 3. 데이터
- SQLite 테이블 `todos`. 할 일에는 제목, 완료 여부, 만든 시각만 둔다.

| 컬럼 | 타입 | 설명 |
| --- | --- | --- |
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | 행을 가리키는 키. 라우트에서 `/todos/<id>`로 쓴다 |
| `title` | TEXT NOT NULL | 제목 |
| `done` | INTEGER NOT NULL DEFAULT 0 | 0이면 미완료, 1이면 완료 |
| `created_at` | TEXT NOT NULL DEFAULT (datetime('now','localtime')) | 만든 시각 |

- DB 파일은 앱이 있는 디렉터리의 `todo.db`다. 테스트에서는 임시 DB를 쓴다.

## 4. 동작
- `GET /` : 전체 목록을 index.html에 보여 준다.
- `POST /todos` : 제목을 받아 할 일을 추가하고 `/`로 돌아온다.
- `POST /todos/<id>/toggle` : 완료 여부를 반전하고(완료 표시와 해제), `/`로 돌아온다.
- `POST /todos/<id>/delete` : 할 일을 삭제하고 `/`로 돌아온다.
- 모든 변경은 HTML form의 POST로만 한다.
- 없는 `id`면 404를 준다.
- 제목이 빈 문자열이면 추가하지 않고 목록으로 돌아온다.

## 5. 화면
- 맨 위에 제목 입력창과 추가 버튼이 있는 폼을 둔다.
- 각 할 일은 제목, 완료 상태, 토글 버튼(완료 표시/해제), 삭제 버튼을 보여 준다.
- 완료된 할 일은 취소선으로 표시한다.
- CSS는 HTML 안에 인라인으로 쓴다.

## 6. 테스트
`test_app.py`에서 다음을 검증한다. 각 테스트는 임시 SQLite DB를 만들고 끝나면 지운다.
1. 할 일 추가
2. 목록 표시
3. 완료 처리와 완료 해제 (toggle 반전 확인)
4. 삭제

실행:
```powershell
cd week06\todo
python -m pip install pytest
python -m pytest test_app.py -v
python app.py   # http://localhost:5000
```

## 7. 하지 않는 것
제목 수정, 마감일, 중요도, 태그, 우선순위, 로그인, 외부 CSS 프레임워크, JavaScript 프레임워크는 만들지 않는다.
