from dataclasses import asdict
from typing import Tuple, Optional
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from app.domain.entities import Dataset
from app.domain.interfaces import SearchClient


class ElasticClient(SearchClient):

    def __init__(self, url: str, search_synonyms: list):
        self.es = Elasticsearch([url])
        self.synonyms = search_synonyms

    def delete_index(self) -> None:
        try:
            self.es.indices.delete(index='dataset')
        except NotFoundError:
            pass

    def create_index(self) -> None:
        # Définition d'un analyzer français (repris ici : https://jolicode.com/blog/construire-un-bon-analyzer-francais-pour-elasticsearch)
        # Ajout dans la filtre french_synonym, des synonymes que l'on souhaite implémenter (ex : AMD / Administrateur des Données)
        # Création du mapping en indiquant les champs sur lesquels cet analyzer va s'appliquer (title, description, concat, organization)
        # et en spécifiant les types de champs que l'on va utiliser pour calculer notre score de pertinence
        settings = {
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
                        "synonyms": self.synonyms
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
        }
        mappings = {
            "properties": {
                "id": {
                    "type": "text"
                },
                "title": {
                    "type": "text",
                    "analyzer": "french_dgv"
                },
                "acronym": {
                    "type": "text"
                },
                "description": {
                    "type": "text",
                    "analyzer": "french_dgv"
                },
                "organization": {
                    "type": "text",
                    "analyzer": "french_dgv"
                },
                "orga_sp": {
                    "type": "integer"
                },
                "orga_followers": {
                    "type": "integer"
                },
                "dataset_views": {
                    "type": "integer"
                },
                "dataset_followers": {
                    "type": "integer"
                },
                "concat_title_org": {
                    "type": "text",
                    "analyzer": "french_dgv"
                },
                "dataset_featured": {
                    "type": "integer"
                },

            }
        }
        self.es.indices.create(index='dataset', mappings=mappings, settings=settings)

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
                                                    "acronym^15",
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
                                        "field": "orga_sp",
                                        "factor": 8,
                                        "modifier": "sqrt",
                                        "missing": 1
                                    }
                                },
                                {
                                    "field_value_factor": {
                                        "field": "dataset_views",
                                        "factor": 4,
                                        "modifier": "sqrt",
                                        "missing": 1
                                    }
                                },
                                {
                                    "field_value_factor": {
                                        "field": "dataset_followers",
                                        "factor": 4,
                                        "modifier": "sqrt",
                                        "missing": 1
                                    }
                                },
                                {
                                    "field_value_factor": {
                                        "field": "orga_followers",
                                        "factor": 1,
                                        "modifier": "sqrt",
                                        "missing": 1
                                    }
                                },
                                {
                                    "field_value_factor": {
                                        "field": "dataset_featured",
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
                                                    "concat_title_org": {
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
                                            "field": "orga_sp",
                                            "factor": 8,
                                            "modifier": "sqrt",
                                            "missing": 1
                                        }
                                    },
                                    {
                                        "field_value_factor": {
                                            "field": "dataset_views",
                                            "factor": 4,
                                            "modifier": "sqrt",
                                            "missing": 1
                                        }
                                    },
                                    {
                                        "field_value_factor": {
                                            "field": "dataset_followers",
                                            "factor": 4,
                                            "modifier": "sqrt",
                                            "missing": 1
                                        }
                                    },
                                    {
                                        "field_value_factor": {
                                            "field": "orga_followers",
                                            "factor": 1,
                                            "modifier": "sqrt",
                                            "missing": 1
                                        }
                                    },
                                    {
                                        "field_value_factor": {
                                            "field": "dataset_featured",
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
