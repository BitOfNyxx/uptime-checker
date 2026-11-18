import sqlite3

from flask import Flask, render_template

from datetime import UTC, datetime, timedelta

from uptime_checker import DATABASE_NAME

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template(
        "index.html", rows=get_latest_checks(), uptime=get_uptime_24h()
    )


def get_latest_checks() -> list[tuple]:
    connection = sqlite3.connect(DATABASE_NAME)
    results = connection.execute(
        "SELECT url, MAX(checked_at), status_code, response_time, error FROM checks GROUP BY url"
    ).fetchall()
    connection.close()
    return results


def get_uptime_24h() -> dict[str, float]:
    cutoff = (datetime.now(UTC) - timedelta(hours=24)).isoformat()
    connection = sqlite3.connect(DATABASE_NAME)
    query = """SELECT url,
       ROUND(100.0 * SUM(CASE WHEN status_code < 400 THEN 1 ELSE 0 END) / COUNT(*), 1)
FROM checks
WHERE checked_at >= ?
GROUP BY url"""

    results = connection.execute(query, (cutoff,)).fetchall()
    connection.close()
    return dict(results)
