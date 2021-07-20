import logging
from json import JSONDecodeError

from command.configuration.model.channel_type import ChannelType
from command.configuration.model.server import Server, Channel
from utils.file_utils import is_file, load_json_file, write_json_file

LOG_ID = "ServerRepository"


class ServerRepository:
    """
    Repository with the different servers information
    """

    def __init__(self, servers_path: str):
        self.file_path = servers_path
        self.servers = self.__load_servers()

    def find_server_by_id(self, server_id: int) -> Server:
        """
        Search for a server in the server list with the configured id
        :param server_id: Id that identify the server
        :return: A server that is related to the given id
        """
        for server in self.servers:
            if server.server_id == server_id:
                return server

    def create_server(self, server_id: int, server_name: str, channel_id: int, channel_name: str,
                      channel_type: ChannelType, channel_rol: int) -> None:
        """
        Create a Server with its respective channel information based on given information
        :param server_id: The id that identifies the server
        :param server_name: Name of the Server
        :param channel_id: The id that identifies the channel
        :param channel_name: Name of the channel
        :param channel_type: Channel type to be added or replaced in the server
        :param channel_rol: Channel Rol to announce information
        :return: None
        """
        server = self.find_server_by_id(server_id)

        channel = Channel(channel_id, channel_name, channel_rol)

        if server is None:
            server = Server(server_id, server_name)
        add_channel = getattr(server, 'add_{0}'.format(channel_type.value))
        add_channel(channel)
        self.__save_server(server)

    def __save_server(self, new_server: Server) -> None:
        """
        Saves into a pre configured json file the information of a server.
        If the server already exist then it will update it.

        This verification is done by the server name
        :param new_server: The server to save, it can be a new server or and old one
        :return: None
        """
        try:
            index = 0
            found = False
            for server in self.servers:
                if server.server_id == new_server.server_id:
                    found = True
                    self.servers[index] = new_server
                index += 1
            if not found:
                self.servers.append(new_server)
            write_json_file(self.file_path, [convert_to_dict(server) for server in self.servers])
            logging.debug('[{0}] - Successfully saved server [{1}] information'.format(LOG_ID, new_server.name))
        except (TypeError, FileNotFoundError) as error:
            logging.error("[{0}] - Couldn't saver server [{1}] information: {2}".format(LOG_ID, new_server.name, error))

    def __load_servers(self) -> list:
        """
        Load server information from a file if exists otherwise will return an empty list
        :return: A list with the server information
        """
        servers = []
        try:
            if is_file(self.file_path):
                servers_file = load_json_file(self.file_path)
                for server in servers_file:
                    servers.append(convert_to_server(server))
                logging.debug('[{0}] - Server information loaded successfully'.format(LOG_ID))
            else:
                logging.error("[{0}] - Couldn't load server information, Not file found".format(LOG_ID))
        except (JSONDecodeError, TypeError) as error:
            logging.error("[{0}] - Couldn't load server information: {1}".format(LOG_ID, error))
        return servers

    def reload_servers(self) -> None:
        """
        Refresh the current server information of the file into the ServerRepository.
        This is a measure to keep data updated.

        :return: None
        """
        self.servers = self.__load_servers()


def convert_to_server(server_dict: dict) -> Server:
    """
    Transform a dictionary with the server and channel information.

    :param server_dict: Server dictionary that was retrieved from a JSON file
    :return: A new instance of the Server model with the given information
    """
    server = Server(server_dict['server_id'],
                    server_dict['name'])

    if server_dict.get('birthday_channel') != '':
        birthday_channel = Channel(server_dict['birthday_channel']['channel_id'],
                                   server_dict['birthday_channel']['name'],
                                   server_dict['birthday_channel']['announcement_rol'])
        server.add_birthday_channel(birthday_channel)

    if server_dict.get('event_channel') != '':
        event_channel = Channel(server_dict['event_channel']['channel_id'],
                                server_dict['event_channel']['name'],
                                server_dict['event_channel']['announcement_rol'])
        server.add_event_channel(event_channel)

    return server


def convert_to_dict(server: Server) -> dict:
    """
    Transform a Server object into a dict, including its channels

    :param server: Server Object that needs to be transformed
    :return: A dictionary with the server information
    """
    server_dict = {'server_id': server.server_id, 'name': server.name}

    birthday_channel = '' if server.birthday_channel is None else server.birthday_channel.__dict__
    event_channel = '' if server.event_channel is None else server.event_channel.__dict__

    server_dict['birthday_channel'] = birthday_channel
    server_dict['event_channel'] = event_channel

    return server_dict
