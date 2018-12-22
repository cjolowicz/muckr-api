'''Click commands.'''
import click
import flask.cli

from muckr.user.models import User
from muckr.extensions import database


@click.command()
@flask.cli.with_appcontext
def create_admin():
    '''Create admin user.'''
    admin = User(username='admin', email='admin@localhost', is_admin=True)
    admin.set_password('secret')
    database.session.add(admin)
    database.session.commit()
