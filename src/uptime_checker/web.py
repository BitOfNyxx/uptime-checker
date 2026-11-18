import sqlite3

from flask import Flask, render_template

from uptime_checker import DATABASE_NAME

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("index.html", rows=get_latest_checks())


def get_latest_checks() -> list[tuple]:
    connection = sqlite3.connect(DATABASE_NAME)
    results = connection.execute(
        "SELECT url, MAX(checked_at), status_code, response_time, error FROM checks GROUP BY url"
    ).fetchall()
    connection.close()
    return results
