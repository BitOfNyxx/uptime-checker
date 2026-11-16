import sqlite3

import requests

TIMEOUT = 5
DATABASE_NAME = "uptime.db"


def main() -> None:
    init_db()
    with open("urls.txt") as file:
        for url in file:
            url = url.strip()
            if not url:
                continue

            status_code, time_elapsed, error = check_uptime(url)
            if error:
                print(error)
                continue

            print(
                f"The site, {url} returned status code {status_code} and took {time_elapsed * 1000:.0f} milliseconds to respond."
            )


def check_uptime(url: str) -> tuple[int | None, float | None, str | None]:
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.ConnectionError:
        return None, None, f"The website {url} is not reachable."
    except requests.ReadTimeout:
        return (
            None,
            None,
            f"The website {url} took longer than {TIMEOUT} seconds to reply.",
        )
    except requests.RequestException as e:
        return None, None, f"The lookup of {url} failed due to an error. {e}"
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