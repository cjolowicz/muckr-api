import importlib

import flask

import muckr.extensions
import muckr.errors
import muckr.main.views
import muckr.user.views


def create_app(config_object='muckr.config'):
    app = flask.Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)

    return app


def register_extensions(app):
    muckr.extensions.database.init_app(app)
    muckr.extensions.migrate.init_app(app, muckr.extensions.database)
    muckr.extensions.bcrypt.init_app(app)


def register_blueprints(app):
    app.register_blueprint(muckr.main.views.blueprint)
    app.register_blueprint(muckr.user.views.blueprint)


def register_errorhandlers(app):
    def handle_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        status_code = getattr(error, 'code', 500)
        if status_code == 500:
            muckr.extensions.database.session.rollback()
        return muckr.errors.error_response(status_code)
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(handle_error)


def _import(name):
    module, attribute = name.rsplit('.', 1)
    value = getattr(importlib.import_module(module), attribute)
    return attribute, value


def register_shellcontext(app):
    @app.shell_context_processor
    def shell_context():
        return dict(_import(name) for name in [
            'muckr.extensions.database',
            'muckr.user.models.User',
        ])
