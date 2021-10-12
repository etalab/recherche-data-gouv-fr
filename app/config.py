import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'localhost:9200'

    DATASET_CATALOG_URL = 'https://www.data.gouv.fr/fr/datasets/r/f868cca6-8da1-4369-a78d-47463f19a9a3'
    ORG_CATALOG_URL = 'https://www.data.gouv.fr/fr/datasets/r/b7bbfedc-2448-4135-a6c7-104548d396e7'

    # BASEROW_API_TOKEN = os.environ.get('POC_RECHERCHE_BASEROW_API_TOKEN') or 'secret'
    # BASEROW_ORG_TYPOLOGY_URL = 'https://api.baserow.io/api/database/rows/table/18703/'
    # BASEROW_ORG_BADGES_TO_BOOST_URL = 'https://api.baserow.io/api/database/rows/table/18698/'

    # SEARCH_DATASET_FIELDS = [
    #     'title^6',
    #     'description'
    # ]
    # SEARCH_DATASET_FEATURED_WEIGHT = 3
    # SEARCH_DATASET_CERTIFIED_WEIGHT = 1.2


class Testing(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    ELASTICSEARCH_URL = 'http://localhost:9200'
