# Flask Apps

A maintained collection of Flask reference applications for APIs, server-rendered sites,
dashboards, and background-worker architectures.

This repository is a multi-application workspace, not one deployable service. Each application
owns its runtime, dependency lock, tests, and deployment boundary. The shared GitHub Actions
workflow validates the actively maintained applications without coupling their Python packages
together.

## Supported Runtime

- Python 3.14
- Docker for container-backed applications
- Docker Compose for the SQL/Celery integration stack
- `pip-tools`-compiled dependency locks

## Maintained Applications

| Application | Architecture | Validation |
| --- | --- | --- |
| [`flask-auth-dash-bootstrap`](flask-auth-dash-bootstrap/) | Flask authentication, SQLAlchemy, migrations, and an embedded Dash application | Python install, dependency check, pytest, and security audit |
| [`flask-bootstrap`](flask-bootstrap/) | Server-rendered Flask application with user and administration flows | Python install, dependency check, pytest, and security audit |
| [`flask-connextion-rest`](flask-connextion-rest/) | Connexion/OpenAPI API with Flask, SQLAlchemy, and Marshmallow | Python install, dependency check, contract tests, and security audit |
| [`flask-mongo-celery`](flask-mongo-celery/) | Flask, MongoDB-oriented data access, and Celery background work | Dependency audit plus container build and containerized tests |
| [`flask-sql-celery`](flask-sql-celery/) | Flask, SQLAlchemy, Celery, and a composed service stack | Python tests, dependency audit, Compose validation, build, startup, and health check |

The remaining directories are historical or experimental examples. They are useful for reference,
but they are not covered by the current CI matrix and should not be treated as release-ready until
they gain an explicit test and dependency-maintenance contract.

## Dependency Contract

Maintained applications use two coordinated files:

- `requirements.in` is the reviewed source of direct dependency pins.
- `requirements.txt` is the complete compiled installation artifact used by CI and containers.

Change both files together. Compile locks in Linux so environment-marked dependencies such as
SQLAlchemy's `greenlet` support are preserved for CI and production containers.

For example, to regenerate the Connexion API lock with the currently validated toolchain:

```bash
docker run --rm \
  --volume "$PWD/flask-connextion-rest:/work" \
  --workdir /work \
  python:3.14-slim \
  sh -c 'python -m pip install pip==26.0.1 pip-tools==7.6.0 && pip-compile --output-file=requirements.txt --strip-extras requirements.in'
```

The pip and `pip-tools` pins above describe the current reproducible generator pair. Update them
together after validating compatibility; do not regenerate a Linux lock on macOS and assume the
result contains the same platform dependencies.

## Run an Application Locally

Create an isolated environment inside the application you are changing. For the Connexion API:

```bash
cd flask-connextion-rest
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python server.py
```

Use the application-level README when a sample has additional database, worker, or Compose setup.

## Validation

For a directly installed application:

```bash
python -m pip install -r requirements.txt
python -m pip check
python -m pytest -q
python -m pip install pip-audit==2.10.1
python -m pip_audit -r requirements.txt
```

Container-backed lanes must also pass their repository workflow commands:

```bash
docker build --tag flask-mongo-celery:test flask-mongo-celery
docker run --rm flask-mongo-celery:test python -m pytest -q

cd flask-sql-celery
docker compose config --quiet
docker compose build
docker compose up --detach --wait
curl --fail --silent --show-error http://localhost:5000/healthz
docker compose down --volumes
```

The full CI workflow also validates [`renovate.json`](renovate.json). A green job for one sample is
not evidence that another sample or an archival directory is supported.

## Architecture Principles

- Keep application dependencies isolated; do not introduce a repository-wide Python environment.
- Keep OpenAPI, request validation, persistence, and serialization boundaries explicit in API
  samples.
- Exercise worker-backed applications through their container or Compose boundary, not only unit
  tests that bypass infrastructure.
- Treat `requirements.txt` as a generated, reviewable artifact and audit the exact lock that ships.
- Add a CI lane before describing an experimental directory as maintained or release-ready.

Core project documentation:

- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Connexion](https://connexion.readthedocs.io/en/stable/)
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Celery](https://docs.celeryq.dev/en/stable/)

## Contributing

1. Work in one application scope.
2. Update its source dependency file and compiled lock together when dependencies change.
3. Run the application-specific tests, dependency check, audit, and container gates.
4. Document whether the change affects only one sample or a shared repository contract.
5. Open a focused pull request with the exact validation evidence.

## License

This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md).
