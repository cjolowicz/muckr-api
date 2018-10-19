'''Extensions module.

Each extension is initialized in the app factory located
in app.py.
'''
import flask_sqlalchemy
import flask_migrate
import flask_bcrypt

database = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
bcrypt = flask_bcrypt.Bcrypt()
