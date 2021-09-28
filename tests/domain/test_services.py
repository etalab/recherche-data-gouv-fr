from unittest import mock
from app.domain.interfaces import SearchClient
from app.domain.services import DatasetService


def test_dataset_service_call(single_dataset):
    search_client = SearchClient()
    search_client.index = mock.MagicMock(return_value=None)
    search_client.query = mock.MagicMock(return_value=(0, []))

    dataset_service = DatasetService(search_client=search_client, dataset_page_size=20)

    dataset_service.feed(single_dataset)
    search_client.index.assert_called()

    results, results_number, total_pages = dataset_service.search('test', 1)
    search_client.query.assert_called()
    assert results == []
    assert results_number == 0
    assert total_pages == 1


def test_dataset_service(single_dataset):
    search_client = SearchClient()
    search_client.query = mock.MagicMock(return_value=(3, [single_dataset, single_dataset, single_dataset]))

    dataset_service = DatasetService(search_client=search_client, dataset_page_size=2)

    results, results_number, total_pages = dataset_service.search('test', 1)
    search_client.query.assert_called()
    assert len(results) == 3
    assert results_number == 3
    assert total_pages == 2
