# Flask Connexion REST example

This example runs on Python 3.14 with Connexion 3, Flask 3, SQLAlchemy 2,
and Marshmallow 4. The OpenAPI contract owns the JSON API under `/api`, while
Flask renders the example pages.

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
```

Edit direct pins in `requirements.in`, then regenerate the Python 3.14 lock:

```bash
python -m pip install pip-tools
pip-compile --upgrade --resolver=backtracking --strip-extras \
  --output-file=requirements.txt requirements.in
```
