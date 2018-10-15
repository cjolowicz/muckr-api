import flask_sqlalchemy
import flask_migrate

database = flask_sqlalchemy.SQLAlchemy()
migrate = flask_migrate.Migrate()
