import flask

import muckr_service.config
import muckr_service.extensions
import muckr_service.main.routes

def create_app(config_class=muckr_service.config.Config):
    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    muckr_service.extensions.database.init_app(app)

    app.register_blueprint(muckr_service.main.routes.blueprint)

    return app

if __name__ == '__main__':
    create_app().run()
