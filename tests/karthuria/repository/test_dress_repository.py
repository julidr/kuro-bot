from unittest.mock import Mock

from requests import HTTPError

from karthuria.client import KarthuriaClient
from karthuria.repository.dress_repository import DressRepository


class TestGetDressById:

    def test_when_dress_is_found(self, dress):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_dress.return_value = dress
        repository = DressRepository(mock_client)
        expected_name = 'Dress Test'

        # Act
        response = repository.get_dress_by_id(1)

        # Assert
        assert response.name == expected_name

    def test_when_dress_is_not_found(self):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_dress.side_effect = HTTPError('Ups')
        repository = DressRepository(mock_client)

        # Act
        response = repository.get_dress_by_id(2)

        # Assert
        assert response is None


class TestGetDressesByCharacterId:

    def test_when_character_dresses_are_found(self, dress):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_dresses.return_value = [dress]
        repository = DressRepository(mock_client)
        expected_id = 1

        # Act
        response = repository.get_dresses_by_character_id(104)

        # Assert
        assert len(response) == 1
        assert response[0].dress_id == expected_id

    def test_when_character_dresses_are_not_found(self):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_dresses.side_effect = HTTPError('Ups')
        repository = DressRepository(mock_client)

        # Act
        response = repository.get_dresses_by_character_id(104)

        # Assert
        assert response is None
