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
