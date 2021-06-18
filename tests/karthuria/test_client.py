from unittest.mock import patch

import pytest
import requests
from requests import HTTPError

from karthuria.model.color import Color
from karthuria.client import KarthuriaClient
from karthuria.model.school import School

client = KarthuriaClient('test_url')


class TestGetCharacters:

    def test_when_response_is_successful(self, ok_characters_response):
        # Arrange and Act
        with patch.object(requests, 'get', return_value=ok_characters_response) as requests_mock:
            response = client.get_characters()

        # Assert
        requests_mock.assert_called()
        assert len(response) == 1
        assert response[0].name == 'Claudine Saijo'
        assert response[0].school.description == School.SEISHO.description
        assert str(response[0].school) == str(School.SEISHO.value)

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange and Act
        expected_error_message = 'Ups'

        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_characters()

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message


class TestGetCharacter:

    def test_when_response_is_successful(self, ok_character_response):
        # Arrange and Act
        with patch.object(requests, 'get', return_value=ok_character_response) as requests_mock:
            response = client.get_character(1)

        # Assert
        requests_mock.assert_called()
        assert response is not None
        assert response.name == 'Claudine Saijo'
        assert response.seiyuu == 'Aina Aiba'
        assert response.color.rgb == Color.CLAUDINE.rgb
        assert str(response.color) == Color.CLAUDINE.value

    def test_when_response_is_no_successful(self, bad_response):
        # Arrange and Act
        expected_error_message = 'Ups'

        with patch.object(requests, 'get', return_value=bad_response) as requests_mock:
            with pytest.raises(HTTPError) as exception:
                client.get_characters()

        # Assert
        requests_mock.assert_called()
        assert str(exception.value) == expected_error_message
