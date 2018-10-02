import flask_sqlalchemy
import flask_restless

def init_app(app):
    database = flask_sqlalchemy.SQLAlchemy(app)

    class Person(database.Model):
        id         = database.Column(database.Integer, primary_key=True)
        name       = database.Column(database.Unicode, unique=True)
        birth_date = database.Column(database.Date)

    class Computer(database.Model):
        id            = database.Column(database.Integer, primary_key=True)
        name          = database.Column(database.Unicode, unique=True)
        vendor        = database.Column(database.Unicode)
        purchase_time = database.Column(database.DateTime)
        owner_id      = database.Column(database.Integer,
                                        database.ForeignKey('person.id'))
        owner = database.relationship(
            'Person',
            backref=database.backref('computers', lazy='dynamic'))

    database.create_all()

    manager = flask_restless.APIManager(app, flask_sqlalchemy_db=database)

    # Create API endpoints, which will be available at /api/<tablename> by
    # default.
    manager.create_api(Person, methods=['GET', 'POST', 'DELETE'])
    manager.create_api(Computer, methods=['GET'])
