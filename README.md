# Flask Apps

A collection of independent Flask service and application starters. Each
top-level directory is its own runnable example; this repository is not one
installable monolith.

## Example inventory

| Directory | Purpose | Runtime status |
| --- | --- | --- |
| `flask-auth-dash-bootstrap` | Flask authentication around an embedded Dash app | Python 3.14, locked and tested |
| `flask-bootstrap` | Server-rendered Flask application with authentication and admin views | Python 3.14, locked and tested; frontend remains Bootstrap 4 |
| `flask-connextion-rest` | Connexion/OpenAPI people and notes CRUD service | Python 3.14, locked and tested |
| `flask-mongo-celery` | Flask, MongoDB, Celery, and browser-scraping example | Python 3.14, locked and container-tested |
| `flask-auth` | Small authentication-webhook prototype | Legacy; modernization required |
| `flask-dash-bootstrap` | Dash and Bootstrap prototype | Legacy Python 3.9/Pipenv |
| `flask-graphene-sqlalchemy` | GraphQL and SQLAlchemy prototype | Legacy Python 3.9/Pipenv |
| `flask-sql-celery` | SQL-backed Celery deployment prototype | Legacy Python 3.9.5/Pipenv |

“Legacy” means the directory is preserved as a reference and is not covered by
the repository CI matrix. Do not infer current production readiness from its
presence here.

## Working with an example

Read the example's own README first. For one of the Python 3.14 examples, the
usual local flow is:

```sh
cd flask-connextion-rest
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Each example owns its environment variables, database behavior, ports, and
startup command. Do not install every `requirements.txt` into one environment;
the examples intentionally have different dependency graphs.

## Validation

GitHub Actions runs the supported examples independently:

- Python 3.14 clean installs, `pip check`, pytest, and advisory audits for the
  authentication, Bootstrap, and Connexion examples.
- A production-image build and containerized browser/test run for
  `flask-mongo-celery`, plus an audit of its lock.
- Renovate configuration validation.

When changing a legacy example, add a focused validation gate for that directory
before treating a dependency update as mergeable.

## Dependency contract

Four modern examples use `pip-compile`:

```text
requirements.in  -> direct dependency intent
requirements.txt -> generated, fully resolved lock
```

Edit the `.in` file and regenerate its matching lock with Python 3.14:

```sh
python -m pip install pip-tools pip-audit==2.10.1
pip-compile --upgrade --resolver=backtracking --strip-extras \
  --output-file=requirements.txt requirements.in
python -m pip check
python -m pytest -q
python -m pip_audit -r requirements.txt
```

Renovate is configured to update those source files through its `pip-compile`
manager. Direct edits to transitive pins in generated `requirements.txt` files
are disabled because they can violate exact dependency constraints.

The `flask-bootstrap` templates still load Bootstrap 4. Popper 2 updates are
held until that template and data-attribute migration is performed as one
browser-tested Bootstrap 5 change. Bootstrap 4 expects the Popper 1 dependency
line; merely changing the CDN URL to a newer Popper 2 release is not compatible.

The raw requirement files in legacy examples remain independently managed until
those directories are migrated to a reproducible lock format.

## Repository layout

Each example generally contains some combination of:

```text
app/ or app.py       Flask application code
requirements.in      Direct Python dependency pins
requirements.txt     Installed or generated dependency set
Dockerfile           Container runtime contract
test/ or tests/      Example-local validation
README.md             Example-local setup and limitations
```

## Contributing

Keep pull requests scoped to one example or one repository-wide maintenance
contract. State which examples were exercised, preserve generated-lock
provenance, and do not use a passing test from one directory as evidence for
another.

## License

See [LICENSE.md](./LICENSE.md).
