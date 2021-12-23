import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    ELASTICSEARCH_ADDR = os.environ.get(
        'DOKKU_ELASTICSEARCH_POC_RECHERCHE_PORT_9200_TCP_ADDR') or 'localhost'
    ELASTICSEARCH_PORT = os.environ.get(
        'DOKKU_ELASTICSEARCH_POC_RECHERCHE_PORT_9200_TCP_PORT') or '9200'
    ELASTICSEARCH_URL = f'http://{ELASTICSEARCH_ADDR}:{ELASTICSEARCH_PORT}'

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

    SEARCH_SYNONYMS = [
        "AMD, administrateur ministériel des données, AMDAC",
        "lolf, loi de finance",
        "waldec, RNA, répertoire national des associations",
        "ovq, baromètre des résultats",
        "contour, découpage"
    ]

    MD_ALLOWED_TAGS = [
        'a',
        'abbr',
        'acronym',
        'b',
        'br',
        'blockquote',
        'code',
        'dd',
        'del',
        'dl',
        'dt',
        'em',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'hr',
        'i',
        'img',
        'li',
        'ol',
        'p',
        'pre',
        'small',
        'span',
        'strong',
        'ul',
        'sup',
        'sub',
        'table',
        'td',
        'th',
        'tr',
        'tbody',
        'thead',
        'tfooter',
        # 'title',
    ]

    MD_ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title', 'rel', 'data-tooltip'],
        'abbr': ['title'],
        'acronym': ['title'],
        'img': ['src', 'title']
    }

    MD_ALLOWED_STYLES = []

    # Extracted from https://github.github.com/gfm/#disallowed-raw-html-extension-
    MD_FILTERED_TAGS = [
        'title',
        'textarea',
        'style',
        'xmp',
        'iframe',
        'noembed',
        'noframes',
        'script',
        'plaintext',
    ]

    MD_ALLOWED_PROTOCOLS = ['http', 'https', 'ftp', 'ftps']


class Testing(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    ELASTICSEARCH_URL = 'http://localhost:9200'
