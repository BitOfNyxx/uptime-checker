import requests

from uptime_checker import check_uptime


def test_unreachable_site(monkeypatch):
    def fake_get(url, timeout):
        raise requests.ConnectionError

    monkeypatch.setattr(requests, "get", fake_get)

    assert check_uptime("https://example.com") == (None, None, "unreachable")


def test_timeout(monkeypatch):
    def fake_get(url, timeout):
        raise requests.ReadTimeout

    monkeypatch.setattr(requests, "get", fake_get)

    assert check_uptime("https://example.com") == (None, None, "timeout")
