# flask-auth

A stateless HTTP webhook that Hasura GraphQL Engine calls to resolve a user's role from an authorization token.

## Contents

- `auth_webhook.py` — The single-file Flask app.
- `Dockerfile` — Container build.
- `Procfile` — Heroku process type.

## Local truths

- **Entrypoint**: `auth_webhook.py` (module-level `app = Flask(__name__)`).
- **No package layout.** This is the single-file exception (module name is `auth_webhook`, not `app`).
- **No DB.** `get_details_for_token(token)` is a stub to be replaced with a real lookup.
- **Routes**: `GET /` health check, `GET /auth-webhook` token resolution.
- **Container**: `Dockerfile` copies `auth_webhook.py` and runs under gunicorn on 5000.
- **Heroku**: `Procfile` runs `gunicorn -b 0.0.0.0:$PORT auth_webhook:app`.

## Commands

```bash
# install
pip install -e ".[dev]"

# run dev
flask --app auth_webhook run --debug

# run like prod
gunicorn auth_webhook:app -b 0.0.0.0:5000

# tests
pytest

# container
docker build -t flask-auth .
docker run -p 5000:5000 flask-auth
```

## Modernization status

- [x] Pin dependencies in `pyproject.toml`.
- [x] Upgrade to Flask 3.1.
- [x] Add `.env.example` (placeholder — no env vars read today).
- [x] Add `tests/test_webhook.py` with smoke + 401 tests.
- [x] Rename `auth-webhook.py` → `auth_webhook.py` so it's Python-importable.

## Do not

- Do not add a database or session management here; this is intentionally stateless.
- Do not split into packages; the single-file structure is the point of this template.
