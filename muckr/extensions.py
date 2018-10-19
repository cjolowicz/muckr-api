'''Extensions module.

Each extension is initialized in the app factory located
in app.py.
'''
import flask_sqlalchemy
import flask_migrate
import flask_bcrypt
import flask_cors

database = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
bcrypt = flask_bcrypt.Bcrypt()
cors = flask_cors.CORS()
