import flask

from . import monkeypatch

def create_app(config=None):
    app = flask.Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config is not None:
        app.config.from_mapping(config)

    from . import models
    models.init_app(app)

    return app

if __name__ == '__main__':
    create_app().run()
