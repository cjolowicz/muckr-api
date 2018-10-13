import flask
import flask_sqlalchemy
import flask_restless

database = flask_sqlalchemy.SQLAlchemy()
manager = flask_restless.APIManager()

def create_app(config=None):
    app = flask.Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config is not None:
        app.config.from_mapping(config)

    database.init_app(app)
    manager.init_app(app, flask_sqlalchemy_db=database)

    from muckr_service.models import Person, Computer

    # Create API endpoints, which will be available at /api/<tablename> by
    # default.
    manager.create_api(Person, methods=['GET', 'POST', 'DELETE'])
    manager.create_api(Computer, methods=['GET'])

    return app

if __name__ == '__main__':
    create_app().run()
