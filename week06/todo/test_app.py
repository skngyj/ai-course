import sqlite3

import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    db_path = str(tmp_path / "test.db")
    app = create_app(db_path)
    app.config["TESTING"] = True
    client = app.test_client()
    client.db_path = db_path
    return client


def fetch_all(client):
    conn = sqlite3.connect(client.db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM todos ORDER BY id").fetchall()
    conn.close()
    return rows


def test_add_todo(client):
    response = client.post("/todos", data={"title": "우유 사기"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    rows = fetch_all(client)
    assert len(rows) == 1
    assert rows[0]["title"] == "우유 사기"
    assert rows[0]["done"] == 0
    assert rows[0]["created_at"]


def test_add_empty_title_is_ignored(client):
    client.post("/todos", data={"title": "   "})
    assert fetch_all(client) == []


def test_list_todos(client):
    client.post("/todos", data={"title": "첫 번째 일"})
    client.post("/todos", data={"title": "두 번째 일"})

    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "첫 번째 일" in html
    assert "두 번째 일" in html


def test_list_empty(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "할 일이 없습니다." in response.get_data(as_text=True)


def test_toggle_done_and_undo(client):
    client.post("/todos", data={"title": "운동하기"})
    todo_id = fetch_all(client)[0]["id"]

    response = client.post(f"/todos/{todo_id}/toggle")
    assert response.status_code == 302
    assert fetch_all(client)[0]["done"] == 1

    client.post(f"/todos/{todo_id}/toggle")
    assert fetch_all(client)[0]["done"] == 0


def test_delete_todo(client):
    client.post("/todos", data={"title": "지울 일"})
    client.post("/todos", data={"title": "남길 일"})
    target = [r for r in fetch_all(client) if r["title"] == "지울 일"][0]

    response = client.post(f"/todos/{target['id']}/delete")
    assert response.status_code == 302

    titles = [r["title"] for r in fetch_all(client)]
    assert titles == ["남길 일"]
    html = client.get("/").get_data(as_text=True)
    assert "지울 일" not in html


def test_missing_id_returns_404(client):
    assert client.post("/todos/999/toggle").status_code == 404
    assert client.post("/todos/999/delete").status_code == 404
