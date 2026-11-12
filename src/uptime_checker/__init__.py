import requests

TIMEOUT = 5


def main() -> None:
    with open("urls.txt") as file:
        for url in file:
            url = url.strip()
            if not url:
                continue

            try:
                status_code, time_elapsed = check_uptime(url)
                print(
                    f"The website {url} responded with status code {status_code} and took {time_elapsed * 1000:.0f} milliseconds to reply."
                )
            except requests.ConnectionError:
                print(f"The website {url} is not reachable.")
            except requests.ReadTimeout:
                print(f"The website {url} took longer than {TIMEOUT} seconds to reply.")
            except requests.RequestException as e:
                print(f"The lookup of {url} failed due to an error. {e}")


def check_uptime(url: str) -> tuple[int, float]:
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code, response.elapsed.total_seconds()
