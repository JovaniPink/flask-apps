# flask-auth

A minimal authentication webhook for [Hasura GraphQL Engine](https://hasura.io/docs/). Hasura calls this service with the original request headers and expects a JSON response of Hasura session variables (or HTTP 401 for unauthorized).

This is the single-file exception in the `flask-apps/` catalog — the whole app is ~30 lines. If you need DB, sessions, or business logic beyond a token lookup, use a different template.

## Run locally

```bash
pip install -e ".[dev]"
flask --app auth_webhook run --debug
# visit http://localhost:5000/
```

## Run in production

```bash
gunicorn auth_webhook:app -b 0.0.0.0:5000
```

## Run in Docker

```bash
docker build -t flask-auth .
docker run -p 5000:5000 flask-auth
```

## Configure Hasura

Point Hasura at the webhook via env:

```bash
HASURA_GRAPHQL_ADMIN_SECRET=myadminsecretkey
HASURA_GRAPHQL_AUTH_WEBHOOK=http://localhost:5000/auth-webhook
```

Docker networking notes:

1. If Hasura runs in a container and this webhook runs locally on Linux, bind both to the host network (`--net=host`) so Hasura can reach `localhost:5000`.
2. On Mac, use `http://host.docker.internal:5000/auth-webhook` from Hasura.
3. If both run as containers, join them on a shared `docker network` and use the container name as the host.

Further reading: [Hasura authentication](https://hasura.io/docs/latest/auth/authentication/webhook/).

## Extend

Replace the stub body of `get_details_for_token` in `auth_webhook.py`:

```python
def get_details_for_token(token: str | None) -> dict[str, str] | None:
    if not token:
        return None
    # call your real token service here
    return {"X-Hasura-Role": "user", "X-Hasura-User-Id": "1"}
```

Return `None` to reject the request with HTTP 401. Return a dict to forward the given Hasura session variables.

## Test

```bash
pytest
```

## License

MIT — see [`LICENSE.md`](../LICENSE.md).
