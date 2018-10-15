import flask
import flask_sqlalchemy
import flask_restless

import muckr_service.config

database = flask_sqlalchemy.SQLAlchemy()
manager = flask_restless.APIManager()

def create_app(config_class=muckr_service.config.Config):
    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    database.init_app(app)
    manager.init_app(app, flask_sqlalchemy_db=database)

    import muckr_service.models

    manager.create_api(muckr_service.models.Person, methods=['GET', 'POST', 'DELETE'])
    manager.create_api(muckr_service.models.Computer, methods=['GET'])

    return app

if __name__ == '__main__':
    create_app().run()
