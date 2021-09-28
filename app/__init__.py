from flask import Flask
from app.config import Config
from app.containers import Container
from app import routes
from app import seed


def create_app(config: object = Config) -> Flask:
    container = Container()
    container.wire(modules=[routes, seed])

    app: Flask = Flask(__name__)
    app.container = container
    app.config.from_object(config)

    container.config.elasticsearch_url.from_value(app.config['ELASTICSEARCH_URL'])
    container.config.datasets_per_page.from_value(app.config['DATASETS_PER_PAGE'])

    # register the database command
    seed.init_app(app)

    app.register_blueprint(routes.bp)

    return app
