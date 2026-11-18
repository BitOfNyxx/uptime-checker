import sqlite3

from flask import Flask

from uptime_checker import DATABASE_NAME

app = Flask(__name__)


@app.route("/")
def home() -> str:
    rows = get_latest_checks()
    lines = []
    for url, checked_at, status_code, response_time, error in rows:
        lines.append(f"{url} - {status_code} - {error}")
    return "<br>".join(lines)


def get_latest_checks() -> list[tuple]:
    connection = sqlite3.connect(DATABASE_NAME)
    results = connection.execute("SELECT url, MAX(checked_at), status_code, response_time, error FROM checks GROUP BY url").fetchall()
    connection.close()
    return results