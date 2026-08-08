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

Edit direct pins in `requirements.in`, then regenerate the Python 3.14 lock:

```bash
python -m pip install pip-tools
pip-compile --upgrade --resolver=backtracking --strip-extras \
  --output-file=requirements.txt requirements.in
```
