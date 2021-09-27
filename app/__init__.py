import os
import yaml
from flask import Flask
from app.containers import Container
from app import routes
from app import seed


def create_app() -> Flask:
    container = Container()
    container.config.from_yaml('config.yml')
    container.wire(modules=[routes, seed])

    app: Flask = Flask(__name__)
    app.container = container

    with open(os.path.join(app.root_path, 'config.yml'), "r") as fh:
        data = yaml.load(fh, Loader=yaml.SafeLoader)
        app.config.from_object(data)

    # register the database command
    seed.init_app(app)

    app.register_blueprint(routes.bp)

    return app
