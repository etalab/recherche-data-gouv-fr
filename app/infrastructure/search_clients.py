from dataclasses import asdict
from typing import Tuple, Optional
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from app.domain.entities import Dataset
from app.domain.interfaces import SearchClient


class ElasticClient(SearchClient):

    def __init__(
            self,
            url: str,
            search_dataset_fields: list,
            search_dataset_featured_weight: int,
            search_dataset_certified_weight: int
    ):
        self.es = Elasticsearch([url])
        self.search_dataset_fields = search_dataset_fields
        self.search_dataset_featured_weight = search_dataset_featured_weight
        self.search_dataset_certified_weight = search_dataset_certified_weight

    def clean_index(self, index: str) -> None:
        try:
            self.es.indices.delete(index=index)
        except NotFoundError:
            pass

    def index_dataset(self, to_index: Dataset) -> None:
        self.es.index(index='dataset',  id=to_index.id, body=asdict(to_index))

    def query_datasets(self, query_text: str, offset: int, page_size: int) -> Tuple[int, list[Dataset]]:
        query_body: dict = {
            "from": offset,
            "size": page_size,
            "query": {
                "function_score": {
                    "query": {
                        "multi_match": {
                            "query": query_text,
                            "fields": self.search_dataset_fields
                        }
                    },
                    "functions": [
                        {
                            "filter": {
                                "match": {
                                    "featured": "true"
                                }
                            },
                            "weight": self.search_dataset_featured_weight
                        },
                        {
                            "filter": {
                                "match": {
                                    "organization_badges": "public-service"
                                }
                            },
                            "weight": self.search_dataset_certified_weight
                        }
                    ],
                    "score_mode": "multiply",
                    "boost_mode": "multiply"
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
