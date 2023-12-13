from unittest.mock import patch

import pytest
import requests
from requests import HTTPError

from karthuria.client import KarthuriaClient
from karthuria.model.color import Color
from karthuria.model.school import School

client = KarthuriaClient('test_url', 'test_cdn_url')


class TestGetCharacters:

    def test_when_response_is_successful(self, ok_characters_response):
        # Arrange
        expected_name = 'Claudine Saijo'

        # Act
        with patch.object(requests, 'get', return_value=ok_characters_response) as requests_mock:
            response = client.get_characters()

        # Assert
        requests_mock.assert_called()
        assert len(response) == 1
        assert response[0].name == expected_name
        assert response[0].school.description == School.SEISHO.description
        assert str(response[0].school) == str(School.SEISHO.value)

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange
        expected_error_message = 'Ups'

        # Act
        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_characters()

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message


class TestGetCharacter:

    def test_when_response_is_successful(self, ok_character_response):
        # Arrange
        expected_name = 'Claudine Saijo'
        expected_seiyuu = 'Aina Aiba'

        # Act
        with patch.object(requests, 'get', return_value=ok_character_response) as requests_mock:
            response = client.get_character(1)

        # Assert
        requests_mock.assert_called()
        assert response is not None
        assert response.name == expected_name
        assert response.seiyuu == expected_seiyuu
        assert response.color.rgb == Color.CLAUDINE.rgb
        assert str(response.color) == Color.CLAUDINE.value

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange
        expected_error_message = 'Ups'

        # Act
        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_character(1)

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message


class TestGetDress:

    def test_when_response_is_successful(self, ok_dress_response):
        # Arrange
        expected_name = 'Tristan'

        # Act
        with patch.object(requests, 'get', return_value=ok_dress_response) as requests_mock:
            response = client.get_dress(1)

        # Assert
        requests_mock.assert_called()
        assert response is not None
        assert response.name == expected_name

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange
        expected_error_message = 'Ups'

        # Act
        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_dress(1)

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message


class TestGetDresses:

    def test_when_response_is_successful(self, ok_dresses_response):
        # Arrange
        expected_id = 1010002

        # Act
        with patch.object(requests, 'get', return_value=ok_dresses_response) as requests_mock:
            response = client.get_dresses()

        # Assert
        requests_mock.assert_called()
        assert len(response) == 2
        assert response[1].dress_id == expected_id

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange
        expected_error_message = 'Ups'

        # Act
        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_dresses()

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message


class TestGetEquips:

    def test_when_response_is_successful(self, ok_equips_response):
        # Arrange
        expected_id = '2000021'

        # Act
        with patch.object(requests, 'get', return_value=ok_equips_response) as requests_mock:
            response = client.get_equips()

        # Assert
        requests_mock.assert_called()
        assert len(response) == 2
        assert response[0].equip_id == expected_id
        assert len(response[0].characters) == 1
        assert response[1].characters is None

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange
        expected_error_message = 'Ups'

        # Act
        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_equips()

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message


class TestGetEnemy:

    def test_when_response_is_successful(self, ok_enemy_response):
        # Arrange
        expected_name = 'Resentful Andrew'
        expected_rarity = 1

        # Act
        with patch.object(requests, 'get', return_value=ok_enemy_response) as requests_mock:
            response = client.get_enemy(1)

        # Assert
        requests_mock.assert_called()
        assert response is not None
        assert response.name == expected_name
        assert response.rarity == expected_rarity

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange
        expected_error_message = 'Ups'

        # Act
        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_enemy(1)

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message


class TestGetEvents:

    def test_when_response_is_successful(self, ok_events_response):
        # Arrange
        expected_name = 'Hello to Halloween'
        expected_event_id = '101'

        # Act
        with patch.object(requests, 'get', return_value=ok_events_response) as requests_mock:
            response = client.get_events()

        # Assert
        requests_mock.assert_called()
        assert response is not None
        assert len(response) == 2
        assert response[0].name == expected_name
        assert response[1].event_id == expected_event_id

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange
        expected_error_message = 'Ups'

        # Act
        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_events()

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message


class TestGetCurrentEvents:
    def test_when_response_is_successful(self, ok_current_events_response):
        # Arrange
        expected_event_id = 118
        expected_challenge_id = 1080009
        expected_boss_id = 900620202

        # Act
        with patch.object(requests, 'get', return_value=ok_current_events_response) as requests_mock:
            response = client.get_current_events()

        # Assert
        requests_mock.assert_called()
        assert response is not None
        assert len(response['events']) == 1
        assert response['events'][0].event_id == expected_event_id
        assert len(response['challenges']) == 2
        assert response['challenges'][1].event_id == expected_challenge_id
        assert len(response['bosses']) == 2
        assert response['bosses'][0].event_id == expected_boss_id

    def test_when_only_challenge_is_present(self, only_challenge_current_events_response):
        # Arrange
        expected_challenge_id = 1080009

        # Act
        with patch.object(requests, 'get', return_value=only_challenge_current_events_response) as requests_mock:
            response = client.get_current_events()

        # Assert
        requests_mock.assert_called()
        assert response is not None
        assert len(response['challenges']) == 2
        assert response['challenges'][1].event_id == expected_challenge_id
        assert 'events' not in response
        assert 'bosses' not in response

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange
        expected_error_message = 'Ups'

        # Act
        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_current_events()

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message
