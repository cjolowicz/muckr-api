import flask_sqlalchemy
import flask_migrate
import flask_bcrypt

database = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
bcrypt = flask_bcrypt.Bcrypt()
