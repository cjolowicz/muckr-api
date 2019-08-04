"""The app module, containing the app factory function."""
import importlib

import flask

import muckr_api
import muckr_api.extensions
import muckr_api.errors
import muckr_api.commands
import muckr_api.artist.views
import muckr_api.main.views
import muckr_api.user.views
import muckr_api.venue.views


def create_app(config_object="muckr_api.config"):
    app = flask.Flask(__name__)
    app.config.from_object(config_object)

    app.logger.info("muckr_api {version}".format(version=muckr_api.__version__))

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    return app


def register_extensions(app):
    muckr_api.extensions.database.init_app(app)
    muckr_api.extensions.migrate.init_app(app, muckr_api.extensions.database)
    muckr_api.extensions.bcrypt.init_app(app)
    muckr_api.extensions.cors.init_app(app)


def register_blueprints(app):
    app.register_blueprint(muckr_api.artist.views.blueprint)
    app.register_blueprint(muckr_api.venue.views.blueprint)
    app.register_blueprint(muckr_api.main.views.blueprint)
    app.register_blueprint(muckr_api.user.views.blueprint)


def register_errorhandlers(app):
    app.errorhandler(muckr_api.errors.APIError)(muckr_api.errors.APIError.handle)
    for status_code in [401, 404, 500]:
        app.errorhandler(status_code)(muckr_api.errors.handle_error)


def _import(name):
    module, attribute = name.rsplit(".", 1)
    value = getattr(importlib.import_module(module), attribute)
    return attribute, value


def register_shellcontext(app):
    @app.shell_context_processor
    def shell_context():
        return dict(
            _import(name)
            for name in ["muckr_api.extensions.database", "muckr_api.user.models.User"]
        )


def register_commands(app):
    app.cli.add_command(muckr_api.commands.create_admin)
    app.cli.add_command(muckr_api.commands.client)
