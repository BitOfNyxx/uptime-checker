from datetime import timedelta

import requests

from uptime_checker import check_uptime


class FakeResponse:
    status_code = 200
    elapsed = timedelta(seconds=0.25)


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


def test_site_is_up(monkeypatch):
    def fake_get(url, timeout):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    assert check_uptime("https://example.com") == (200, 0.25, None)
