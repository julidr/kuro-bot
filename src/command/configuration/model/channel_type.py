from enum import Enum


class ChannelType(Enum):
    """
    Enum with all the available configurable channels in the bot.
    The channel variable name to be saved in a server.
    """

    BIRTHDAY = 'birthday_channel'
    EVENT = 'event_channel'
