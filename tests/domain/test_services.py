from unittest import mock
from app.domain.interfaces import SearchClient
from app.domain.services import DatasetService


def test_dataset_service_call(single_dataset):
    search_client = SearchClient()
    search_client.index = mock.MagicMock(return_value=None)
    search_client.query = mock.MagicMock(return_value=(0, []))

    dataset_service = DatasetService(search_client=search_client)

    dataset_service.feed(single_dataset)
    search_client.index.assert_called()

    dataset_service.search('test')
    search_client.query.assert_called()
