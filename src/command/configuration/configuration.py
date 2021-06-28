import logging

from discord.ext import commands
from discord.ext.commands import Context

from command.configuration.model.channel_type import ChannelType
from command.configuration.repository.server_repository import ServerRepository
from command.initializer import Initializer

LOG_ID = "ConfigurationCommand"
logging.basicConfig(level=logging.INFO)


class ConfigurationCommand(commands.Cog):
    """
    All Kuro bot discord commands that are related to its configuration.
    """

    def __init__(self, server_repository: ServerRepository, my_bot=commands.Bot):
        self.bot = my_bot
        self.server_repository = server_repository

    @commands.command(pass_context=True)
    async def birthday_announcements(self, ctx: Context, channel_name: str = None) -> None:
        """
        Allows the configuration of birthday announcements channel of preference for a Discord Server
        :param ctx: Discord context
        :param channel_name: Name of the channel where notification will be send
        :return: None
        """
        if channel_name is None:
            await ctx.send('Hmm...Please specify the channel name.'.format(channel_name))
            return

        channels = ctx.guild.channels
        logging.info('[{0}] - Looking for channel [{1}] in server [{2}]'.format(LOG_ID, channel_name, ctx.guild.name))
        for channel in channels:
            if channel.name == channel_name:
                logging.info('[{0}] - Channel [{1}] found'.format(LOG_ID, channel_name))
                self.server_repository.create_server(ctx.guild.id, ctx.guild.name, channel.id, channel.name,
                                                     ChannelType.BIRTHDAY)
                await ctx.send('Fait! - Birthday channel event [{0}] was set'.format(channel_name))
                return

        await ctx.send("Je suis desolé - I wasn't able to find  [{0}]".format(channel_name))


def setup(my_bot: commands.Bot) -> None:
    """
    Bot setup necessary to recognize its COG
    :param my_bot: the bot where the commands need to be register
    :return: None
    """
    initializer = Initializer()
    my_bot.add_cog(ConfigurationCommand(initializer.get_servers_repository(), my_bot))
