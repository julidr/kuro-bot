from unittest.mock import patch

from command.configuration.model.channel_type import ChannelType
from command.configuration.repository.server_repository import ServerRepository

TEST_JSON = 'test.json'
TEST_SERVER = 'Test Server'


class TestLoadServers:

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    def test_when_load_is_file(self, mock_load_json, mock_is_file, complete_server_info):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = complete_server_info
        expected_name = TEST_SERVER

        # Act
        repository = ServerRepository(TEST_JSON)
        result = repository.servers

        # Assert
        assert len(result) != 0
        assert result[0].name == expected_name

    @patch('command.configuration.repository.server_repository.is_file')
    def test_when_load_is_not_file(self, mock_is_file):
        # Arrange
        mock_is_file.return_value = False

        # Act
        repository = ServerRepository(TEST_JSON)
        result = repository.servers

        # Assert
        assert len(result) == 0

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    def test_when_is_not_json(self, mock_load_json, mock_is_file):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = "No Json"

        # Act
        repository = ServerRepository('test.json')
        result = repository.servers

        # Assert
        assert len(result) == 0


class TestFindServerById:

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    def test_when_server_is_found(self, mock_load_json, mock_is_file, complete_server_info):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = complete_server_info
        repository = ServerRepository(TEST_JSON)
        expected_name = TEST_SERVER

        # Act
        result = repository.find_server_by_id(1)

        # Assert
        assert result.name == expected_name

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    def test_when_server_is_not_found(self, mock_load_json, mock_is_file, complete_server_info):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = complete_server_info
        repository = ServerRepository(TEST_JSON)

        # Act
        result = repository.find_server_by_id(2)

        # Assert
        assert result is None


class TestCreateServer:

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    @patch('command.configuration.repository.server_repository.write_json_file')
    def test_when_server_has_birthday_channel(self, mock_write_json, mock_load_json, mock_is_file,
                                              server_with_channels):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = []
        mock_write_json.return_value = None
        repository = ServerRepository(TEST_JSON)

        expected_server_id = server_with_channels.server_id
        expected_server_name = server_with_channels.name
        expected_channel_id = server_with_channels.birthday_channel.channel_id
        expected_channel_name = server_with_channels.birthday_channel.name
        expected_channel_rol = server_with_channels.birthday_channel.announcement_rol

        # Act
        repository.create_server(expected_server_id,
                                 expected_server_name,
                                 expected_channel_id,
                                 expected_channel_name,
                                 ChannelType.BIRTHDAY,
                                 expected_channel_rol)

        # Assert
        assert len(repository.servers) != 0
        assert repository.servers[0].name == expected_server_name
        assert repository.servers[0].birthday_channel is not None
        assert repository.servers[0].birthday_channel.name == expected_channel_name
        assert repository.servers[0].birthday_channel.announcement_rol == expected_channel_rol
        assert repository.servers[0].event_channel is None

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    @patch('command.configuration.repository.server_repository.write_json_file')
    def test_when_server_has_event_channel(self, mock_write_json, mock_load_json, mock_is_file, server_with_channels):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = []
        mock_write_json.return_value = None
        repository = ServerRepository(TEST_JSON)

        expected_server_id = server_with_channels.server_id
        expected_server_name = server_with_channels.name
        expected_channel_id = server_with_channels.event_channel.channel_id
        expected_channel_name = server_with_channels.event_channel.name
        expected_channel_rol = server_with_channels.event_channel.announcement_rol

        # Act
        repository.create_server(expected_server_id,
                                 expected_server_name,
                                 expected_channel_id,
                                 expected_channel_name,
                                 ChannelType.EVENT,
                                 expected_channel_rol)

        # Assert
        assert len(repository.servers) != 0
        assert repository.servers[0].name == expected_server_name
        assert repository.servers[0].event_channel is not None
        assert repository.servers[0].event_channel.name == expected_channel_name
        assert repository.servers[0].event_channel.announcement_rol == expected_channel_rol
        assert repository.servers[0].birthday_channel is None

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    @patch('command.configuration.repository.server_repository.write_json_file')
    def test_when_server_already_exist(self, mock_write_json, mock_load_json, mock_is_file, server_with_channels,
                                       one_channels_server_info):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = one_channels_server_info
        mock_write_json.return_value = None
        repository = ServerRepository(TEST_JSON)

        expected_server_id = server_with_channels.server_id
        expected_server_name = TEST_SERVER
        expected_event_channel_id = server_with_channels.event_channel.channel_id
        expected_event_channel_name = server_with_channels.event_channel.name
        expected_event_channel_rol = server_with_channels.event_channel.announcement_rol
        expected_birthday_channel_name = 'birthday-channel'

        # Act
        repository.create_server(expected_server_id,
                                 expected_server_name,
                                 expected_event_channel_id,
                                 expected_event_channel_name,
                                 ChannelType.EVENT,
                                 expected_event_channel_rol)

        # Assert
        assert len(repository.servers) != 0
        assert repository.servers[0].name == expected_server_name
        assert repository.servers[0].event_channel is not None
        assert repository.servers[0].event_channel.name == expected_event_channel_name
        assert repository.servers[0].event_channel.announcement_rol == expected_event_channel_rol
        assert repository.servers[0].birthday_channel is not None
        assert repository.servers[0].birthday_channel.name == expected_birthday_channel_name

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    @patch('command.configuration.repository.server_repository.write_json_file')
    def test_when_server_dsa(self, mock_write_json, mock_load_json, mock_is_file):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = []
        mock_write_json.side_effect = FileNotFoundError('Ups')
        repository = ServerRepository(TEST_JSON)

        expected_server_id = 1
        expected_server_name = TEST_SERVER
        expected_event_channel_id = 1
        expected_event_channel_name = 'Test Channel'
        expected_event_channel_rol = 1

        # Act
        repository.create_server(expected_server_id,
                                 expected_server_name,
                                 expected_event_channel_id,
                                 expected_event_channel_name,
                                 ChannelType.EVENT,
                                 expected_event_channel_rol)

        # Assert
        assert len(repository.servers) != 0


class TestReloadServers:

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    def test_when_new_data_is_added(self, mock_load_json, mock_is_file, complete_server_info, one_channels_server_info):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = complete_server_info
        repository = ServerRepository(TEST_JSON)
        mock_load_json.return_value = one_channels_server_info
        expected_name = TEST_SERVER

        # Act
        repository.reload_servers()
        result = repository.servers

        # Assert
        assert result[0].name == expected_name
        assert result[0].event_channel is None

    @patch('command.configuration.repository.server_repository.is_file')
    @patch('command.configuration.repository.server_repository.load_json_file')
    def test_when_data_is_the_same(self, mock_load_json, mock_is_file, complete_server_info):
        # Arrange
        mock_is_file.return_value = True
        mock_load_json.return_value = complete_server_info
        repository = ServerRepository(TEST_JSON)
        mock_load_json.return_value = complete_server_info
        expected_name = TEST_SERVER
        expected_event_channel_name = 'event-channel'

        # Act
        repository.reload_servers()
        result = repository.servers

        # Assert
        assert result[0].name == expected_name
        assert result[0].event_channel is not None
        assert result[0].event_channel.name == expected_event_channel_name
