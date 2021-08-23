from unittest.mock import patch

import pytest

from utils.discord_utils import get_discord_color, get_rol, get_channel_by_name


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


class TestGetRol:

    def test_when_rol_exist(self, discord_role):
        # Arrange
        test_rol = 'Test'

        # Act
        with patch('discord.ext.commands.Context') as mock_context:
            mock_context.guild.roles = [discord_role]
            result = get_rol(mock_context, test_rol)

        # Assert
        assert result is not None
        assert result.name == test_rol

    def test_when_rol_dont_exist(self, discord_role):
        # Arrange
        test_rol = 'Test 2'

        # Act
        with patch('discord.ext.commands.Context') as mock_context:
            mock_context.guild.roles = [discord_role]
            result = get_rol(mock_context, test_rol)

        # Assert
        assert result is None


class TestGetChannelByName:

    def test_when_channel_exist(self, discord_channel):
        # Arrange
        test_channel = 'Test'

        # Act
        with patch('discord.ext.commands.Context') as mock_context:
            mock_context.guild.channels = [discord_channel]
            result = get_channel_by_name(mock_context, test_channel)

        # Assert
        assert result is not None
        assert result.name == test_channel

    def test_when_channel_dont_exist(self, discord_channel):
        # Arrange
        test_channel = 'Test 2'

        # Act
        with patch('discord.ext.commands.Context') as mock_context:
            mock_context.guild.channels = [discord_channel]
            result = get_channel_by_name(mock_context, test_channel)

        # Assert
        assert result is None
