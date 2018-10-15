import flask

import muckr.config
import muckr.extensions
import muckr.main.routes

def create_app(config_class=muckr.config.Config):
    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    muckr.extensions.database.init_app(app)

    app.register_blueprint(muckr.main.routes.blueprint)

    return app
