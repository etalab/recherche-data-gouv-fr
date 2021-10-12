from dataclasses import asdict
from typing import Tuple, Optional
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from app.domain.entities import Dataset
from app.domain.interfaces import SearchClient


class ElasticClient(SearchClient):

    def __init__(self, url: str):
        self.es = Elasticsearch([url])

    def clean_index(self, index: str) -> None:
        try:
            self.es.indices.delete(index=index)
        except NotFoundError:
            pass

    def create_index(self) -> None:
        # Définition d'un analyzer français (repris ici : https://jolicode.com/blog/construire-un-bon-analyzer-francais-pour-elasticsearch)
        # Ajout dans la filtre french_synonym, des synonymes que l'on souhaite implémenter (ex : AMD / Administrateur des Données)
        # Création du mapping en indiquant les champs sur lesquels cet analyzer va s'appliquer (title, description, concat, organization)
        # et en spécifiant les types de champs que l'on va utiliser pour calculer notre score de pertinence
        mapping_with_analyzer = {
            "settings": {
                "analysis": {
                    "filter": {
                        "french_elision": {
                            "type": "elision",
                            "articles_case": True,
                            "articles": ["l", "m", "t", "qu", "n", "s", "j", "d", "c", "jusqu", "quoiqu", "lorsqu", "puisqu"]
                        },
                        "french_stop": {
                            "type":       "stop",
                            "stopwords":  "_french_"
                        },
                        "french_synonym": {
                            "type": "synonym",
                            "ignore_case": True,
                            "expand": True,
                            "synonyms": [
                                "AMD, administrateur ministériel des données, AMDAC",
                                "lolf, loi de finance",
                                "waldec, RNA, répertoire national des associations",
                                "ovq, baromètre des résultats",
                                "contour, découpage"
                            ]
                        },
                        "french_stemmer": {
                            "type": "stemmer",
                            "language": "light_french"
                        }
                    },
                    "analyzer": {
                        "french_dgv": {
                            "tokenizer": "icu_tokenizer",
                            "filter": [
                                "french_elision",
                                "icu_folding",
                                "french_synonym",
                                "french_stemmer",
                                "french_stop"
                            ]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "id": {
                        "type": "text"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "french_dgv"
                    },
                    "description": {
                        "type": "text",
                        "analyzer": "french_dgv"
                    },
                    "organization": {
                        "type": "text",
                        "analyzer": "french_dgv"
                    },
                    "es_orga_sp": {
                        "type": "integer"
                    },
                    "es_orga_followers": {
                        "type": "integer"
                    },
                    "es_dataset_views": {
                        "type": "integer"
                    },
                    "es_dataset_followers": {
                        "type": "integer"
                    },
                    "es_concat_title_org": {
                        "type": "text",
                        "analyzer": "french_dgv"
                    },
                    "es_dataset_featured": {
                        "type": "integer"
                    },

                }
            }
        }
        self.es.indices.create(index='dataset', body=mapping_with_analyzer)

    def index_dataset(self, to_index: Dataset) -> None:
        self.es.index(index='dataset',  id=to_index.id, body=asdict(to_index))

    def query_datasets(self, query_text: str, offset: int, page_size: int) -> Tuple[int, list[Dataset]]:
        query_body = {
            "from": offset,
            "size": page_size,
            "query": {
                "bool": {
                    "should": [{
                        "function_score": {
                            "query": {
                                "bool": {
                                    "should": [
                                        {
                                            "multi_match": {
                                                "query": query_text,
                                                "type": "phrase",
                                                "fields": [
                                                    "title^15",
                                                    "description^8",
                                                    "organization^8"
                                                ]
                                            }
                                        }
                                    ]
                                }
                            },
                            "functions": [
                                {
                                    "field_value_factor": {
                                        "field": "es_orga_sp",
                                        "factor": 8,
                                        "modifier": "sqrt",
                                        "missing": 1
                                    }
                                },
                                {
                                    "field_value_factor": {
                                        "field": "es_dataset_views",
                                        "factor": 4,
                                        "modifier": "sqrt",
                                        "missing": 1
                                    }
                                },
                                {
                                    "field_value_factor": {
                                        "field": "es_dataset_followers",
                                        "factor": 4,
                                        "modifier": "sqrt",
                                        "missing": 1
                                    }
                                },
                                {
                                    "field_value_factor": {
                                        "field": "es_orga_followers",
                                        "factor": 1,
                                        "modifier": "sqrt",
                                        "missing": 1
                                    }
                                },
                                {
                                    "field_value_factor": {
                                        "field": "es_dataset_featured",
                                        "factor": 1,
                                        "modifier": "sqrt",
                                        "missing": 1
                                    }
                                }
                            ]
                        }
                    },
                        {
                            "function_score": {
                                "query": {
                                    "bool": {
                                        "must": [
                                            {
                                                "match": {
                                                    "es_concat_title_org": {
                                                        "query": query_text,
                                                        "operator": "and",
                                                        "boost": 8
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                "functions": [
                                    {
                                        "field_value_factor": {
                                            "field": "es_orga_sp",
                                            "factor": 8,
                                            "modifier": "sqrt",
                                            "missing": 1
                                        }
                                    },
                                    {
                                        "field_value_factor": {
                                            "field": "es_dataset_views",
                                            "factor": 4,
                                            "modifier": "sqrt",
                                            "missing": 1
                                        }
                                    },
                                    {
                                        "field_value_factor": {
                                            "field": "es_dataset_followers",
                                            "factor": 4,
                                            "modifier": "sqrt",
                                            "missing": 1
                                        }
                                    },
                                    {
                                        "field_value_factor": {
                                            "field": "es_orga_followers",
                                            "factor": 1,
                                            "modifier": "sqrt",
                                            "missing": 1
                                        }
                                    },
                                    {
                                        "field_value_factor": {
                                            "field": "es_dataset_featured",
                                            "factor": 1,
                                            "modifier": "sqrt",
                                            "missing": 1
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "multi_match": {
                                "query": query_text,
                                "type": "most_fields",
                                "fields": [
                                    "title",
                                    "organization"
                                ],
                                "fuzziness": "AUTO"

                            }
                        }
                    ]
                }
            }
        }
        result = self.es.search(index='dataset', body=query_body, explain=True)
        results_number = result["hits"]["total"]["value"]
        res = [Dataset(**elem["_source"]) for elem in result["hits"]["hits"]]
        return results_number, res

    def find_one(self, dataset_id: str) -> Optional[Dataset]:
        query_body = {
            "query": {
                "term": {
                    "id": {
                        "value": dataset_id
                    }
                }
            }
        }
        result = self.es.search(index='dataset', body=query_body, explain=True)
        if result['hits']['hits']:
            return Dataset(**result['hits']['hits'][0]['_source'])
        return None
