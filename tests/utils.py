import base64


def create_basic_auth_header(username, password):
    payload = b":".join((username.encode("utf-8"), password.encode("utf-8")))

    return {
        "Authorization": "Basic {base64}".format(
            base64=base64.b64encode(payload).decode("utf-8")
        )
    }


def create_token_auth_header(token):
    return {"Authorization": "Bearer {token}".format(token=token)}


def assert_response_has(response, status_code, json):
    assert response.status_code == status_code
    assert response.get_json() == json


def assert_get_request_returns_json(client, endpoint, token, json, **kwargs):
    response = client.get(endpoint, headers=create_token_auth_header(token), **kwargs)

    assert_response_has(response, 200, json)
