class Channel:
    """
    Model class of a Discord Channel in Kuro Bot Domain
    """

    def __init__(self, channel_id: int, name: str, announcement_rol: int):
        self.channel_id = channel_id
        self.name = name
        self.announcement_rol = announcement_rol


class Server:
    """
    Model class of a Discord Server (guild) in Kuro Bot Domain
    """

    def __init__(self, server_id: int, name: str, birthday_channel: Channel = None, event_channel: Channel = None):
        self.server_id = server_id
        self.name = name
        self.birthday_channel = birthday_channel
        self.event_channel = event_channel

    def add_birthday_channel(self, birthday_channel: Channel) -> None:
        """
        Add a Channel to birthday configuration if it wasn't specified before
        :param birthday_channel: The channel that will be save
        :return: None
        """
        self.birthday_channel = birthday_channel

    def add_event_channel(self, event_channel: Channel) -> None:
        """
        Add a Channel to event configuration if it wasn't specified before
        :param event_channel: The channel that will be save
        :return: None
        """
        self.event_channel = event_channel
