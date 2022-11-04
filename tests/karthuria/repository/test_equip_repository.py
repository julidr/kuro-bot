from unittest.mock import Mock

from requests import HTTPError

from karthuria.client import KarthuriaClient
from karthuria.repository.equip_repository import EquipRepository


class TestGetEquipByCharacterId:

    def test_when_character_equips_are_found(self, equip):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_equips.return_value = [equip]
        repository = EquipRepository(mock_client)
        expected_id = 1

        # Act
        response = repository.get_equips_by_character_id(104)

        # Assert
        assert len(response) == 1
        assert response[0].equip_id == expected_id

    def test_when_character_equips_are_not_found(self):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_equips.side_effect = HTTPError('Ups')
        repository = EquipRepository(mock_client)

        # Act
        response = repository.get_equips_by_character_id(105)

        # Assert
        assert response is None
