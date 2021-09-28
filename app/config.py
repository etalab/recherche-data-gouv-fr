import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ELASTICSEARCH_URL = os.environ.get('DOKKU_ELASTICSEARCH_RECHERCHE_URL') or 'http://localhost:9200'
    DATASET_CATALOG_URL = 'https://www.data.gouv.fr/fr/datasets/r/f868cca6-8da1-4369-a78d-47463f19a9a3'
    ORG_CATALOG_URL = 'https://www.data.gouv.fr/fr/datasets/r/b7bbfedc-2448-4135-a6c7-104548d396e7'
    DATASETS_PER_PAGE = 20


class Testing:
    TESTING = True
    WTF_CSRF_ENABLED = False
    ELASTICSEARCH_URL = 'http://localhost:9200'
    DATASETS_PER_PAGE = 20
