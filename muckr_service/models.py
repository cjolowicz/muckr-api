import flask
import flask.cli
import flask_restless
import click

from muckr_service import database as db

def init_database():
    db.create_all()

@click.command('init-database')
@flask.cli.with_appcontext
def init_database_command():
    '''Initialize the database.'''
    init_database()
    click.echo('Initialized the database.')

class Person(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.Unicode, unique=True)
    birth_date = db.Column(db.Date)

class Computer(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.Unicode, unique=True)
    vendor        = db.Column(db.Unicode)
    purchase_time = db.Column(db.DateTime)
    owner_id      = db.Column(db.Integer, db.ForeignKey('person.id'))
    owner = db.relationship(
        'Person',
        backref=db.backref('computers', lazy='dynamic'))

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default.
manager.create_api(Person, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Computer, methods=['GET'])

app.cli.add_command(init_database_command)
