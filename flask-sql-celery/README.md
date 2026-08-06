# Flask SQL + Celery

A small Flask API backed by PostgreSQL and a RabbitMQ/Celery worker. The
example is container-first and is intended for local development and CI, not as
a production deployment template.

## Stack

- Python 3.14
- Flask 3 and Flask-SQLAlchemy 3
- Celery 5 with RabbitMQ 4
- PostgreSQL 18
- Gunicorn running as an unprivileged container user

## Start the stack

```sh
docker compose up --build --wait
curl --fail http://localhost:5000/healthz
curl --fail http://localhost:5000/
```

Stop the containers without deleting database data:

```sh
docker compose down
```

The Compose project stores PostgreSQL 18 data in the `pgdata18` named volume,
mounted at `/var/lib/postgresql` as required by the official PostgreSQL 18
image layout.

## Local tests

```sh
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
APP_ENV=Test python -m pytest -q
python -m pip check
python -m pip_audit -r requirements.txt
docker compose config --quiet
```

`requirements.in` contains direct dependency intent. `requirements.txt` is the
generated lock and should be refreshed with `pip-compile`, not edited by hand.

## PostgreSQL 13 to 18 boundary

Changing the container tag does not upgrade an existing PostgreSQL data
directory in place. The new Compose file intentionally uses a different
`pgdata18` volume and leaves any old PostgreSQL 13 volume untouched.

For real data, stop writes, create a logical backup with PostgreSQL 13 tools,
start PostgreSQL 18 with the new volume, restore the backup, and verify the row
counts and application behavior before retiring the old volume. Do not delete
the old volume until the restored database has been accepted.

## Configuration

The Compose defaults are development-only. Override these environment variables
for any shared environment:

- `DATABASE_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

Do not reuse the checked-in example credentials outside local development.
