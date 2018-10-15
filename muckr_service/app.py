import flask

import muckr_service.config

def create_app(config_class=muckr_service.config.Config):
    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    import muckr_service.extensions
    muckr_service.extensions.database.init_app(app)

    import muckr_service.main
    app.register_blueprint(muckr_service.main.blueprint)

    return app

if __name__ == '__main__':
    create_app().run()
