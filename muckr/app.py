import flask

import muckr.extensions
import muckr.main.views


def create_app(config_object='muckr.config'):
    app = flask.Flask(__name__)
    app.config.from_object(config_object)

    muckr.extensions.database.init_app(app)
    muckr.extensions.migrate.init_app(app, muckr.extensions.database)
    muckr.extensions.bcrypt.init_app(app)

    app.register_blueprint(muckr.main.views.blueprint)

    return app
