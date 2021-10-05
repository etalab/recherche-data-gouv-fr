from typing import Tuple, Optional
from app.domain.entities import Dataset
from app.domain.interfaces import SearchClient


class DatasetService:

    def __init__(self, search_client: SearchClient, dataset_page_size: int):
        self.search_client = search_client
        self.dataset_page_size = dataset_page_size

    def feed(self, dataset: Dataset) -> None:
        self.search_client.index_dataset(dataset)

    def search(self, search_text: str, page: int) -> Tuple[list[Dataset], int, int]:
        results: list[Dataset]
        results_number: int

        if page > 1:
            offset = self.dataset_page_size * (page - 1)
        else:
            offset = 0

        results_number, results = self.search_client.query_datasets(search_text, offset, self.dataset_page_size)
        total_pages = round(results_number / self.dataset_page_size) or 1
        return results, results_number, total_pages

    def find_one(self, dataset_id: str) -> Optional[Dataset]:
        return self.search_client.find_one(dataset_id) or None
