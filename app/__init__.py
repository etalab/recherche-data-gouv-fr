import jinja_partials

from flask import Flask
from whitenoise import WhiteNoise
from app.config import Config
from app.containers import Container
from app.presentation import seed, routes, api, markdown


def create_app(config: object = Config) -> Flask:
    container = Container()
    container.wire(modules=[api, routes, seed])

    app: Flask = Flask(__name__)
    app.container = container
    app.config.from_object(config)

    container.config.elasticsearch_url.from_value(app.config['ELASTICSEARCH_URL'])
    container.config.search_synonyms.from_value(app.config['SEARCH_SYNONYMS'])

    # register the database command
    seed.init_app(app)
    markdown.init_app(app)

    app.register_blueprint(routes.bp)
    app.register_blueprint(api.bp)

    app.wsgi_app = WhiteNoise(app.wsgi_app, root='app/static/')

    jinja_partials.register_extensions(app)

    return app
