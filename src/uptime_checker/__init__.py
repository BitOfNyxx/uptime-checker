import requests


def main() -> None:
    with open("urls.txt") as file:
        for url in file:
            url = url.strip()
            if not url:
                continue
            
            try:
                print(check_uptime(url))
            except requests.ConnectionError:
                print(f"The website {url} is not reachable.")

def check_uptime(url):
    response = requests.get(url, timeout=5)
    return response.status_code, response.elapsed.total_seconds()