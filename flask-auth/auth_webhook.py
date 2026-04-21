"""Hasura GraphQL Engine authentication webhook."""

from flask import Flask, abort, jsonify, request

app = Flask(__name__)


def get_details_for_token(token: str | None) -> dict[str, str] | None:
    """Resolve an ``Authorization`` header value to Hasura session variables.

    Replace this stub with a real token lookup (DB, cache, or remote API).
    Return ``None`` to reject the request with HTTP 401.
    """
    if not token:
        return None
    return {"X-Hasura-Role": "user", "X-Hasura-User-Id": "1"}


@app.route("/")
def hello() -> str:
    return "webhook is running"


@app.route("/auth-webhook")
def auth_webhook():
    token = request.headers.get("Authorization")
    variables = get_details_for_token(token)
    if variables is None:
        abort(401)
    return jsonify(variables)
