"""The app module, containing the app factory function."""
import importlib

import flask

import muckr
import muckr.extensions
import muckr.errors
import muckr.commands
import muckr.artist.views
import muckr.main.views
import muckr.user.views
import muckr.venue.views


def create_app(config_object="muckr.config"):
    app = flask.Flask(__name__)
    app.config.from_object(config_object)

    app.logger.info("muckr API {version}".format(version=muckr.__version__))

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    return app


def register_extensions(app):
    muckr.extensions.database.init_app(app)
    muckr.extensions.migrate.init_app(app, muckr.extensions.database)
    muckr.extensions.bcrypt.init_app(app)
    muckr.extensions.cors.init_app(app)


def register_blueprints(app):
    app.register_blueprint(muckr.artist.views.blueprint)
    app.register_blueprint(muckr.venue.views.blueprint)
    app.register_blueprint(muckr.main.views.blueprint)
    app.register_blueprint(muckr.user.views.blueprint)


def register_errorhandlers(app):
    app.errorhandler(muckr.errors.APIError)(muckr.errors.APIError.handle)
    for status_code in [401, 404, 500]:
        app.errorhandler(status_code)(muckr.errors.handle_error)


def _import(name):
    module, attribute = name.rsplit(".", 1)
    value = getattr(importlib.import_module(module), attribute)
    return attribute, value


def register_shellcontext(app):
    @app.shell_context_processor
    def shell_context():
        return dict(
            _import(name)
            for name in ["muckr.extensions.database", "muckr.user.models.User"]
        )


def register_commands(app):
    app.cli.add_command(muckr.commands.create_admin)
    app.cli.add_command(muckr.commands.client)
