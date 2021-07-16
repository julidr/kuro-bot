import pytest

from utils.discord_utils import get_discord_color


class TestGetDiscordColor:

    def test_when_color_is_found_int_tuple(self):
        # Arrange
        color_tuple = (0, 0, 0)

        # Act
        result = get_discord_color(color_tuple)

        # Assert
        assert result.value == 0

    def test_when_color_is_str_tuple(self):
        # Arrange
        color_tuple = ('hi', 'test', 'lol')
        expected_error_message = 'unsupported operand type(s)'

        # Act
        with pytest.raises(TypeError) as exception:
            get_discord_color(color_tuple)

        # Assert
        assert expected_error_message in str(exception.value)
