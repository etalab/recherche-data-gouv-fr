from dataclasses import asdict
from typing import Tuple
from elasticsearch import client, Elasticsearch
from elasticsearch.exceptions import NotFoundError
from app.domain.entities import Dataset
from app.domain.interfaces import SearchClient


class ElasticClient(SearchClient):

    def __init__(self, url: str):
        self.es: client.Elasticsearch = Elasticsearch([url])

    def clean_index(self, index: str) -> None:
        try:
            self.es.indices.delete(index=index)
        except NotFoundError:
            pass

    def index(self, object_to_index: object, index: str) -> None:
        self.es.index(index=index, body=asdict(object_to_index))

    def query(self, query_text: str, index: str) -> Tuple[int, list[Dataset]]:
        fields: list = [
            f"title^{2}",
            f"description^{2}",
            f"organization_name^{2}",
        ]

        query_body: dict = {
            "query": {
                "function_score": {
                    "query": {
                        "multi_match": {
                            "query": query_text,
                            "fields": fields
                        }
                    },
                    "functions": [
                        {
                            "filter": {
                                "match": {
                                    "featured": "true"
                                }
                            },
                            "weight": 1
                        },
                        {
                            "filter": {
                                "match": {
                                    "organization_badges": "public-service"
                                }
                            },
                            "weight": 1
                        }
                    ],
                    "score_mode": "multiply",
                    "boost_mode": "multiply"
                }
            }
        }
        result: dict = self.es.search(index=index, body=query_body, explain=True)
        results_number: int = result["hits"]["total"]["value"]
        res: list[Dataset] = [Dataset(**elem["_source"]) for elem in result["hits"]["hits"]]
        return results_number, res
