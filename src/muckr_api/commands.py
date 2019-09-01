"""Click commands."""
import json
import subprocess
import urllib.parse

import click
import flask
import flask.cli

from muckr_api.user.models import User
from muckr_api.extensions import database
import muckr_api.client


@click.command()
@flask.cli.with_appcontext
def create_admin():
    """Create admin user."""
    config = flask.current_app.config
    user = User(
        username=config["ADMIN_USERNAME"], email=config["ADMIN_EMAIL"], is_admin=True
    )
    user.set_password(config["ADMIN_PASSWORD"])
    database.session.add(user)
    database.session.commit()


def _get_admin_credentials(url):
    app = _get_heroku_app_from_url(url)
    if app:
        process = subprocess.run(
            ["heroku", "config", "--json", f"--app={app}"], capture_output=True
        )
        config = json.loads(process.stdout)
    else:
        config = flask.current_app.config
    username = config.get("ADMIN_USERNAME", "admin")
    password = config["ADMIN_PASSWORD"]
    return username, password


def _get_heroku_app_from_url(url):
    url = urllib.parse.urlsplit(url)
    if "." in url.netloc:
        subdomain, domain = url.netloc.split(".", 1)
        if domain == "herokuapp.com":
            return subdomain


def _resolve_resource(api, resource):
    try:
        return {
            "user": api.users,
            "users": api.users,
            "artist": api.artists,
            "artists": api.artists,
            "venue": api.venues,
            "venues": api.venues,
        }[resource]
    except KeyError:
        raise Exception(f"invalid resource {resource}")


def _invoke_api(api, method, resource, args):
    resources = _resolve_resource(api, resource)
    args = dict(arg.split("=") for arg in args)

    if method == "list":
        return resources.list()

    if method == "get":
        return resources.get(args["id"])

    if method == "create":
        return resources.create(args)

    if method == "update":
        return resources.update(args["id"], args)

    if method == "delete":
        return resources.delete(args["id"])

    raise Exception(f"invalid method {method}")


@click.command()
@click.argument("url")
@click.argument("method")
@click.argument("resource")
@click.argument("args", nargs=-1)
@flask.cli.with_appcontext
def client(url, method, resource, args):
    """Simple HTTP client."""
    api = muckr_api.client.API(url)
    username, password = _get_admin_credentials(url)
    api.authenticate(username, password)

    result = _invoke_api(api, method, resource, args)

    click.echo(json.dumps(result))
