from unittest.mock import Mock

from requests import HTTPError

from karthuria.client import KarthuriaClient
from karthuria.repository.enemy_repository import EnemyRepository


class TestGetEnemyById:

    def test_when_enemy_is_found(self, enemy):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_enemy.return_value = enemy
        repository = EnemyRepository(mock_client)
        expected_name = 'Enemy Test'

        # Act
        response = repository.get_enemy_by_id(1)

        # Assert
        assert response.name == expected_name

    def test_when_enemy_is_not_found(self):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_enemy.side_effect = HTTPError('Ups')
        repository = EnemyRepository(mock_client)

        # Act
        response = repository.get_enemy_by_id(2)

        # Assert
        assert response is None
