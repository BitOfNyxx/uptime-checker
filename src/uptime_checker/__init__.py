import os
import sqlite3
import time
from datetime import UTC, datetime

import requests

TIMEOUT = 5
DATABASE_NAME = os.environ.get("UPTIME_DB", "uptime.db")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "60"))

def main() -> None:
    connection = init_db()
    while True:
        run_checks(connection)
        time.sleep(CHECK_INTERVAL)
    connection.close()


def run_checks(connection):
        with open("urls.txt") as file:
            for url in file:
                url = url.strip()
                if not url:
                    continue

                status_code, time_elapsed, error = check_uptime(url)
                checked_at = datetime.now(UTC).isoformat()
                connection.execute(
                    "INSERT INTO checks (url, checked_at, status_code, response_time, error) VALUES (?, ?, ?, ?, ?)",
                    (url, checked_at, status_code, time_elapsed, error),
                )
                if error:
                    if error == "unreachable":
                        print(f"The website {url} is not reachable.")
                    elif error == "timeout":
                        print(
                            f"The website {url} took longer than {TIMEOUT} seconds to reply."
                        )
                    else:
                        print(f"The lookup of {url} failed due to an error. {error}")
                    continue

                print(
                    f"The site, {url} returned status code {status_code} and took {time_elapsed * 1000:.0f} milliseconds to respond."
                )
        connection.commit()

def check_uptime(url: str) -> tuple[int | None, float | None, str | None]:
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.ConnectionError:
        return None, None, "unreachable"
    except requests.ReadTimeout:
        return None, None, "timeout"
    except requests.RequestException as e:
        return None, None, f"error: {e}"
    return response.status_code, response.elapsed.total_seconds(), None


def init_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("""CREATE TABLE IF NOT EXISTS checks (
    id INTEGER PRIMARY KEY,
    url TEXT NOT NULL,
    checked_at TEXT NOT NULL,
    status_code INTEGER,
    response_time REAL,
    error TEXT
)""")
    return conn
