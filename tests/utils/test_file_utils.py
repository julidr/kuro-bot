import os
import pytest

from utils.file_utils import load_json_file


class TestLoadFiles:

    def test_when_load_is_successful(self):
        # Arrange
        settings_json = os.path.join(os.path.dirname(__file__), '../settings.json')
        expected_key = 'key'
        expected_value = 'value'

        # Act
        result = load_json_file(settings_json)

        # Assert
        assert result.get(expected_key) is not None
        assert result.get(expected_key) == expected_value

    def test_when_file_doesnt_exist(self):
        # Arrange
        bad_settings_json = 'test.json'
        expected_error_message = "No such file or directory: '{0}'".format(bad_settings_json)

        # Act
        with pytest.raises(FileNotFoundError) as exception:
            load_json_file(bad_settings_json)

        # Assert
        assert expected_error_message in str(exception.value)
