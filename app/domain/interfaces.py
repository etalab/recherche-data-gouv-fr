from abc import ABC, abstractmethod
from typing import Tuple
from app.domain.entities import Dataset


class SearchClient(ABC):

    @abstractmethod
    def clean_index(self, index: str) -> None:
        pass

    @abstractmethod
    def index_dataset(self, to_index: Dataset) -> None:
        pass

    @abstractmethod
    def query_datasets(self, query_text: str, offset: int, page_size: int) -> Tuple[int, list[Dataset]]:
        pass
