import click
import flask.cli

import muckr_api.app


@click.group(cls=flask.cli.FlaskGroup, create_app=muckr_api.app.create_app)
def main():
    """Management script for the muckr API."""
