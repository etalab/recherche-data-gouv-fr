from typing import Tuple


class SearchClient:
    def clean_index(self, index: str) -> None:
        raise NotImplementedError()

    def index(self, object_to_index: object, index: str) -> None:
        raise NotImplementedError()

    def query(self, query_text: str, index: str, offset: int, page_size: int) -> Tuple[int, list[object]]:
        raise NotImplementedError()
