from fastapi import FastAPI
from app.config import settings
from app.containers import Container
from app.presentation import seed, routes, api

from app.presentation.api.api_v1 import api_router


def create_app():
    container = Container()
    container.wire(modules=[api, routes, seed])

    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
        )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    app.container = container

    container.config.elasticsearch_url.from_value(settings.ELASTICSEARCH_URL)
    container.config.search_synonyms.from_value(settings.SEARCH_SYNONYMS)

    # register the database command
    seed.init_app(app)

    app.register_blueprint(api.bp)

    return app
