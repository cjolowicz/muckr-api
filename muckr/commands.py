'''Click commands.'''
import click
import flask
import flask.cli

from muckr.user.models import User
from muckr.extensions import database


@click.command()
@flask.cli.with_appcontext
def create_admin():
    '''Create admin user.'''
    config = flask.current_app.config
    user = User(
        username=config['ADMIN_USERNAME'], email=config['ADMIN_EMAIL'], is_admin=True
    )
    user.set_password(config['ADMIN_PASSWORD'])
    database.session.add(user)
    database.session.commit()
