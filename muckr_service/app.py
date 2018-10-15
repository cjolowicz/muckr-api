import flask
import flask_sqlalchemy

import muckr_service.config

database = flask_sqlalchemy.SQLAlchemy()

def create_app(config_class=muckr_service.config.Config):
    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    database.init_app(app)

    import muckr_service.main
    app.register_blueprint(muckr_service.main.blueprint)

    return app

if __name__ == '__main__':
    create_app().run()
