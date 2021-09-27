from typing import Tuple
from app.domain.entities import Dataset
from app.domain.interfaces import SearchClient


class DatasetService:

    def __init__(self, search_client: SearchClient):
        self.search_client = search_client

    def feed(self, dataset: Dataset) -> None:
        self.search_client.index(dataset, "dataset")

    def search(self, search_text: str) -> Tuple[int, list[Dataset]]:
        fields: list[str] = ["title", "description", "organization_name"]
        results: list[Dataset]
        results_number: int
        results_number, results = self.search_client.query(search_text, "dataset")
        return results_number, results
