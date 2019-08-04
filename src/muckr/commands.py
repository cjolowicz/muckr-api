"""Click commands."""
import json
import subprocess
import urllib.parse

import click
import flask
import flask.cli
import requests

from muckr.user.models import User
from muckr.extensions import database


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
    if "heroku" in url:
        process = subprocess.run(
            ["heroku", "config", "--json", "--app=muckr-api"], capture_output=True
        )
        config = json.loads(process.stdout)
    else:
        config = flask.current_app.config
    username = config.get("ADMIN_USERNAME", "admin")
    password = config["ADMIN_PASSWORD"]
    return username, password


def _get_baseurl(url):
    url = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit([url.scheme, url.netloc, "", "", ""])


def _get_token(baseurl, auth):
    response = requests.post(f"{baseurl}/tokens", auth=auth)
    return response.json()["token"]


@click.command()
@click.argument("method")
@click.argument("url")
@click.argument("args", nargs=-1)
@flask.cli.with_appcontext
def client(method, url, args):
    """Simple HTTP client."""
    token = _get_token(_get_baseurl(url), _get_admin_credentials(url))
    args += (f"Authorization: Bearer {token}",)
    subprocess.run(["http", "--print=b", method, url, *args])
