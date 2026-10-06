"""Todo 애플리케이션의 SQLite 접근 함수."""

import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
)
"""


def init_db(database):
    with sqlite3.connect(database) as connection:
        connection.execute(SCHEMA)


def list_todos(connection):
    return connection.execute(
        "SELECT id, title, done, created_at FROM todos ORDER BY id DESC"
    ).fetchall()


def add_todo(connection, title):
    connection.execute("INSERT INTO todos (title) VALUES (?)", (title,))
    connection.commit()


def toggle_todo(connection, todo_id):
    cursor = connection.execute(
        "UPDATE todos SET done = 1 - done WHERE id = ?", (todo_id,)
    )
    if cursor.rowcount == 0:
        return False
    connection.commit()
    return True


def delete_todo(connection, todo_id):
    cursor = connection.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    if cursor.rowcount == 0:
        return False
    connection.commit()
    return True
