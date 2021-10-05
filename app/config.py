import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ELASTICSEARCH_ADDR = os.environ.get(
        'DOKKU_ELASTICSEARCH_POC_RECHERCHE_INDEX_PORT_9200_TCP_ADDR') or 'localhost'
    ELASTICSEARCH_PORT = os.environ.get(
        'DOKKU_ELASTICSEARCH_POC_RECHERCHE_INDEX_PORT_9200_TCP_PORT') or '9200'
    ELASTICSEARCH_URL = f'http://{ELASTICSEARCH_ADDR}:{ELASTICSEARCH_PORT}'
    DATASET_CATALOG_URL = 'https://www.data.gouv.fr/fr/datasets/r/f868cca6-8da1-4369-a78d-47463f19a9a3'
    ORG_CATALOG_URL = 'https://www.data.gouv.fr/fr/datasets/r/b7bbfedc-2448-4135-a6c7-104548d396e7'
    DATASETS_PER_PAGE = 20
    SEARCH_DATASET_FIELDS = [
        'title^6',
        'description'
    ]
    SEARCH_DATASET_FEATURED_WEIGHT = 3
    SEARCH_DATASET_CERTIFIED_WEIGHT = 1.2


class Testing(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    ELASTICSEARCH_URL = 'http://localhost:9200'
