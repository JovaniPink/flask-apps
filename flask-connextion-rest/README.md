# Flask Connexion REST example

This example runs on Python 3.14 with Connexion 3, Flask 3, SQLAlchemy 2,
and Marshmallow 4. The OpenAPI contract owns the JSON API under `/api`, while
Flask renders the example pages. Connexion validates request payloads and
successful responses against that contract; SQLAlchemy independently enforces
the required persistence fields.

## API contract

- Person creation requires `fname` and `lname`; each value is 1–32 characters.
- Person updates require at least one recognized name field.
- Note creation and updates require non-empty `content`.
- Undeclared request properties are rejected instead of being silently ignored.

Keep `swagger.yml`, the SQLAlchemy model constraints, and contract tests aligned
when changing a write payload.

## Local use

This unauthenticated sample is for local demonstration. `build_database.py` drops
and recreates tables in the configured `DATABASE_URL` (local SQLite by default);
run it only against a disposable database. Do not point it at retained or live data.

```bash
python -m pip install -r requirements.txt
python build_database.py
python server.py
```

For a containerized run:

```bash
docker build -t flask-connexion-rest .
docker run --rm -p 5000:5000 flask-connexion-rest
```

## Validation

```bash
python -m pytest -q
python -m compileall -q .
python -m openapi_spec_validator swagger.yml
```

Edit direct pins in `requirements.in`, then use the root README to install the
pinned uv generator and regenerate Linux/Python 3.14 locks from this directory:

```bash
cd ..
./scripts/compile-python-locks.sh
```
