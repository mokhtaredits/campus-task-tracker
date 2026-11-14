import os
import sqlite3
from contextlib import closing
from pathlib import Path

from flask import Flask, abort, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
database = Path(os.environ.get("TASK_DB", "data/tasks.db"))
database.parent.mkdir(parents=True, exist_ok=True)

with closing(sqlite3.connect(database)) as connection, connection:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)


@app.get("/")
def index():
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = sqlite3.Row
        tasks = connection.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return render_template("index.html", tasks=tasks)


@app.post("/tasks")
def add_task():
    title = request.form.get("title", "").strip()
    if not 1 <= len(title) <= 120:
        abort(400, "Enter a task title between 1 and 120 characters.")
    with closing(sqlite3.connect(database)) as connection, connection:
        connection.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    return redirect(url_for("index"), code=303)


@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    with closing(sqlite3.connect(database)) as connection, connection:
        result = connection.execute(
            "UPDATE tasks SET completed = 1 - completed WHERE id = ?", (task_id,)
        )
        if result.rowcount == 0:
            abort(404)
    return redirect(url_for("index"), code=303)


@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    with closing(sqlite3.connect(database)) as connection, connection:
        result = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if result.rowcount == 0:
            abort(404)
    return redirect(url_for("index"), code=303)


@app.get("/health")
def health():
    try:
        with closing(sqlite3.connect(database)) as connection:
            connection.execute("SELECT id FROM tasks LIMIT 1").fetchone()
    except sqlite3.Error:
        return jsonify(status="unavailable"), 503
    return jsonify(status="ok")
