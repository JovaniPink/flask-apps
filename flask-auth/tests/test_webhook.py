def test_root_is_alive(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"webhook is running" in response.data


def test_auth_webhook_with_token_returns_hasura_headers(client):
    response = client.get(
        "/auth-webhook",
        headers={"Authorization": "opaque-token"},
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["X-Hasura-Role"] == "user"
    assert body["X-Hasura-User-Id"] == "1"


def test_auth_webhook_without_token_returns_401(client):
    response = client.get("/auth-webhook")
    assert response.status_code == 401
