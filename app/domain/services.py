from typing import Tuple, Optional, List
from app.domain.entities import Dataset, Organization, Reuse
from app.domain.interfaces import SearchClient


class OrganizationService:

    def __init__(self, search_client: SearchClient):
        self.search_client = search_client

    def feed(self, organization: Organization) -> None:
        self.search_client.index_organization(organization)

    def search(self, search_text: str, page: int, page_size: int) -> Tuple[List[Organization], int, int]:
        results: List[Organization]
        results_number: int

        if page > 1:
            offset = page_size * (page - 1)
        else:
            offset = 0

        results_number, results = self.search_client.query_organizations(search_text, offset, page_size)
        results = [Organization(**hit) for hit in results]
        total_pages = round(results_number / page_size) or 1
        return results, results_number, total_pages

    def find_one(self, organization_id: str) -> Optional[Organization]:
        found = self.search_client.find_one_organization(organization_id)
        return Organization(**found) if found else None


class DatasetService:

    def __init__(self, search_client: SearchClient):
        self.search_client = search_client

    def feed(self, dataset: Dataset) -> None:
        self.search_client.index_dataset(dataset)

    def search(self, search_text: str, page: int, page_size: int) -> Tuple[List[Dataset], int, int]:
        results: List[Dataset]
        results_number: int

        if page > 1:
            offset = page_size * (page - 1)
        else:
            offset = 0

        results_number, results = self.search_client.query_datasets(search_text, offset, page_size)
        results = [Dataset(**hit) for hit in results]
        total_pages = round(results_number / page_size) or 1
        return results, results_number, total_pages

    def find_one(self, dataset_id: str) -> Optional[Dataset]:
        found = self.search_client.find_one_dataset(dataset_id)
        return Dataset(**found) if found else None


class ReuseService:

    def __init__(self, search_client: SearchClient):
        self.search_client = search_client

    def feed(self, reuse: Reuse) -> None:
        self.search_client.index_reuse(reuse)

    def search(self, search_text: str, page: int, page_size: int) -> Tuple[List[Reuse], int, int]:
        results: List[Reuse]
        results_number: int

        if page > 1:
            offset = page_size * (page - 1)
        else:
            offset = 0

        results_number, results = self.search_client.query_reuses(search_text, offset, page_size)
        results = [Reuse(**hit) for hit in results]
        total_pages = round(results_number / page_size) or 1
        return results, results_number, total_pages

    def find_one(self, reuse_id: str) -> Optional[Reuse]:
        found = self.search_client.find_one_reuse(reuse_id)
        return Reuse(**found) if found else None
