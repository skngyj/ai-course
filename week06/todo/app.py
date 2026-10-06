import os
import sqlite3

from flask import Flask, abort, g, redirect, render_template, request, url_for

from db import add_todo as db_add_todo
from db import delete_todo as db_delete_todo
from db import init_db
from db import list_todos
from db import toggle_todo as db_toggle_todo


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app(database=None):
    app = Flask(__name__)
    app.config["DATABASE"] = database or os.path.join(BASE_DIR, "todo.db")

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    init_db(app.config["DATABASE"])

    @app.get("/")
    def index():
        todos = list_todos(get_db())
        return render_template("index.html", todos=todos)

    @app.post("/todos")
    def add_todo():
        title = request.form.get("title", "").strip()
        if title:
            db_add_todo(get_db(), title)
        return redirect(url_for("index"))

    @app.post("/todos/<int:todo_id>/toggle")
    def toggle_todo(todo_id):
        db = get_db()
        if not db_toggle_todo(db, todo_id):
            abort(404)
        return redirect(url_for("index"))

    @app.post("/todos/<int:todo_id>/delete")
    def delete_todo(todo_id):
        db = get_db()
        if not db_delete_todo(db, todo_id):
            abort(404)
        return redirect(url_for("index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
