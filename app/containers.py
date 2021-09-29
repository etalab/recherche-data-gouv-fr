from dependency_injector import containers, providers
from app.domain.services import DatasetService
from app.infrastructure.search_clients import ElasticClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    search_client = providers.Singleton(
        ElasticClient,
        url=config.elasticsearch_url,
        search_dataset_featured_weight=config.search_dataset_featured_weight,
        search_dataset_certified_weight=config.search_dataset_certified_weight
    )

    dataset_service = providers.Factory(
        DatasetService,
        search_client=search_client,
        dataset_page_size=config.datasets_per_page
    )
