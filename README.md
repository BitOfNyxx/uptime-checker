# uptime-checker

[![CI](https://github.com/BitOfNyxx/uptime-checker/actions/workflows/ci.yml/badge.svg)](https://github.com/BitOfNyxx/uptime-checker/actions/workflows/ci.yml)

Checks a list of URLs and reports whether each site is up, with its status code and response time. Results are saved to SQLite and shown on a small status page with each site's latest check and 24-hour uptime.

A learning project: it starts as a small Python script and grows into a containerised service with CI, Kubernetes and Terraform.

## Run it with Docker Compose

```
docker compose up --build
```

This starts two containers from the same image:

- **checker** checks every URL in `urls.txt`, then waits and repeats
- **web** serves the status page with gunicorn on http://localhost:8000

Both share a named volume (`uptime-data`), where the database lives, so history survives restarts.

To change which sites are checked, edit `urls.txt` (one URL per line) and run:

```
docker compose restart checker
```

To stop:

```
docker compose down      # keeps the check history
docker compose down -v   # also deletes the history
```

## Run it locally

```
uv sync
uv run uptime-checker
```

The checker runs until you stop it with Ctrl+C. In another terminal, start the status page:

```
uv run gunicorn --bind 0.0.0.0:8000 uptime_checker.web:app
```

## Checks

Every pull request runs a GitHub Actions workflow (`.github/workflows/ci.yml`) with three jobs:

- **lint** runs `ruff check` and `ruff format --check`
- **test** runs the pytest tests in `tests/`
- **build** builds the Docker image, but only after lint and test pass

To run the same checks locally:

```
uv run ruff check
uv run ruff format --check
uv run pytest
```

## Settings

| Variable | Default | What it does |
| --- | --- | --- |
| `UPTIME_DB` | `uptime.db` | Path to the SQLite database |
| `CHECK_INTERVAL` | `60` | Seconds to wait between rounds of checks |

Each request times out after 5 seconds.

## Roadmap

- [x] Script that checks URLs from a file
- [x] Store results in SQLite
- [x] Status page with 24-hour uptime
- [x] Docker Compose
- [x] GitHub Actions
- [ ] Local Kubernetes (kind/k3d)
- [ ] Terraform