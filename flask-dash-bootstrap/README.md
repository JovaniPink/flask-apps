# Flask Dash Bootstrap Reference

A maintained multipage [Dash](https://dash.plotly.com/) application using
[dash-bootstrap-components](https://www.dash-bootstrap-components.com/). It demonstrates a small
presentation boundary without implying that a data source, model, authentication system, or
persistence layer exists.

## Architecture

- `app.py` owns the single Dash application, WSGI `server`, navigation, and `/healthz` boundary.
- `pages/` owns page registration, metadata, and layouts through Dash Pages.
- `requirements.in` contains reviewed direct pins; `requirements.txt` is the generated Linux and
  Python 3.14 installation artifact.
- `test/test_app.py` verifies the page registry, unique navigation, Dash endpoints, application
  shell, custom not-found content, and machine-readable health response.
- `Dockerfile` installs the exact lock and runs Gunicorn as the unprivileged `app` user.

Routing and navigation share `dash.page_registry`; do not add a second pathname callback or a
separate hard-coded route list. Page modules must not import the application instance because Dash
Pages discovers them while the application is being constructed.

## Local Development

From this directory:

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
.venv/bin/python app.py
```

Open <http://127.0.0.1:8050/>. Development mode is intentionally enabled only when `app.py` is
executed directly; Gunicorn imports the WSGI server without enabling the debugger.

## Container Boundary

```bash
docker build --tag flask-dash-bootstrap:local .
docker run --rm --publish 5000:5000 flask-dash-bootstrap:local
curl --fail http://127.0.0.1:5000/healthz
```

The image exposes port `5000`, runs as `app`, and includes a health check that exercises the same
Gunicorn/Flask process serving Dash. `/healthz` proves process availability only; it does not claim
that an external data source or analytical result is fresh.

## Dependency and Validation Contract

Regenerate every maintained lock from the repository root with the pinned `uv` version:

```bash
python3.14 -m venv .lock-venv
.lock-venv/bin/python -m pip install uv==0.12.3
PATH="$PWD/.lock-venv/bin:$PATH" ./scripts/compile-python-locks.sh
```

Before publication, run:

```bash
PATH="$PWD/.lock-venv/bin:$PATH" ./scripts/compile-python-locks.sh --check
cd flask-dash-bootstrap
python -m pip install -r requirements.txt
python -m pip check
python -m pytest -q
python -m pip_audit -r requirements.txt
docker build --tag flask-dash-bootstrap:test .
```

CI repeats the Python checks and validates that the container starts, answers `/healthz`, and
declares the non-root runtime user.

## Release and Rollback

Release only an exact pull-request head that passes lock reproducibility, tests, audit, container,
and repository hygiene checks. Roll back by redeploying the prior validated image or reverting the
merge; never rewrite the compiled lock independently of `requirements.in`.

This sample has no database or mutable storage, so rollback does not require a data migration.
