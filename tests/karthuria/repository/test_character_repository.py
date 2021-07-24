from unittest.mock import Mock

from requests import HTTPError

from karthuria.client import KarthuriaClient
from karthuria.repository.character_repository import CharacterRepository


class TestLoadCharacters:

    def test_when_characters_load_successful(self, character):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_characters.return_value = [character]
        repository = CharacterRepository(mock_client)

        # Act
        response = repository.get_characters()

        # Assert
        assert len(response) == 1
        assert response[0].description == 'Beautiful'

    def test_when_characters_load_unsuccessful(self):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_characters.side_effect = HTTPError('Ups')
        repository = CharacterRepository(mock_client)

        # Act
        response = repository.get_characters()

        # Assert
        assert len(response) == 0


class TestGetCharactersByName:

    def test_when_somebody_is_found(self, character):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_characters.return_value = [character]
        repository = CharacterRepository(mock_client)
        expected_name = 'Claudine Saijo'

        # Act
        response = repository.get_character_by_name('Claudine')

        # Assert
        assert response.name == expected_name

    def test_when_nobody_is_found(self, character):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_characters.return_value = [character]
        repository = CharacterRepository(mock_client)

        # Act
        response = repository.get_character_by_name('Maya')

        # Assert
        assert response is None


class TestGetCharacterBirthday:

    def test_when_is_somebody_birthday(self, character):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_characters.return_value = [character]
        mock_client.get_character.return_value = character
        repository = CharacterRepository(mock_client)
        expected_name = 'Claudine Saijo'

        # Act
        response = repository.get_character_birthday('01/08')

        # Assert
        assert response.name == expected_name

    def test_when_is_nobody_birthday(self, character):
        # Arrange
        mock_client = Mock(spec=KarthuriaClient)
        mock_client.get_characters.return_value = [character]
        mock_client.get_character.return_value = character
        repository = CharacterRepository(mock_client)

        # Act
        response = repository.get_character_birthday('01/09')

        # Assert
        assert response is None
