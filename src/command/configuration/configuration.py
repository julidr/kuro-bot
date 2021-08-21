from discord.ext import commands
from discord.ext.commands import Context

from command.configuration.model.channel_type import ChannelType
from command.configuration.repository.server_repository import ServerRepository
from command.initializer import Initializer
from utils.discord_utils import get_rol, get_channel_by_name

LOG_ID = "ConfigurationCommand"


class ConfigurationCommand(commands.Cog):
    """
    All Kuro bot discord commands that are related to its configuration.
    """

    def __init__(self, server_repository: ServerRepository, my_bot=commands.Bot):
        self.bot = my_bot
        self.server_repository = server_repository

    @commands.command(pass_context=True)
    async def birthday_announcements(self, ctx: Context, channel_name: str = None,
                                     announcement_rol: str = None) -> None:
        """
        Allows the configuration of birthday announcements channel of preference for a Discord Server

        :param ctx: Discord context
        :param channel_name: Name of the channel where notification will be send
        :param announcement_rol: The rol that will be use to notify in the birthday channel.
            If is not set then everyone will be by default.
        :return: None
        """
        await self.__configure_announcement(ctx, channel_name, announcement_rol, ChannelType.BIRTHDAY)

    @commands.command(pass_context=True)
    async def events_announcements(self, ctx: Context, channel_name: str = None, announcement_rol: str = None) -> None:
        """
        Allows the configuration of events announcements channel of preference for a Discord Server

        :param ctx: Discord context
        :param channel_name: Name of the channel where notification will be send.
        :param announcement_rol: The rol that will be use to notify in the birthday channel.
            If is not set then everyone will be by default.
        :return: None
        """
        await self.__configure_announcement(ctx, channel_name, announcement_rol, ChannelType.EVENT)

    async def __configure_announcement(self, ctx: Context, channel_name: str, announcement_rol: str,
                                       channel_type: ChannelType):
        """
        Configure an Event or Birthday channel announcement with its respective rol if is specified.

        :param ctx: Discord context
        :param channel_name: Name of the channel where notification will be send.
        :param announcement_rol: The rol that will be use to notify in the birthday or event channel.
            If is not set then everyone will be by default.
        :param channel_type: The type of channel that is being configured, either EVENT or BIRTHDAY
        :return: None
        """
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('Désolé, tout utilisateur. Only server admins can use this command.')
            return

        if channel_name is None:
            await ctx.send('Hmm...Please specify the channel name.')
            return

        channel = get_channel_by_name(ctx, channel_name)
        rol = ctx.guild.default_role if announcement_rol is None else get_rol(ctx, announcement_rol)

        if rol is None:
            await ctx.send("Je suis desolé - I wasn't able to find role [{0}]".format(announcement_rol))
            return

        if channel is not None:
            log_rol = rol.name if rol.name != '@everyone' else rol.name[1::]
            self.server_repository.create_server(ctx.guild.id, ctx.guild.name, channel.id, channel.name, channel_type,
                                                 rol.id)
            channel_type_message = 'Event' if channel_type == ChannelType.EVENT else 'Birthday'
            await ctx.send('Fait! - {0} channel [{1}] was set with role [{2}]'.format(channel_type_message,
                                                                                      channel_name, log_rol))
            return

        await ctx.send("Je suis desolé - I wasn't able to find channel [{0}]".format(channel_name))


def setup(my_bot: commands.Bot) -> None:
    """
    Bot setup necessary to recognize its COG
    :param my_bot: the bot where the commands need to be register
    :return: None
    """
    initializer = Initializer()
    my_bot.add_cog(ConfigurationCommand(initializer.get_servers_repository(), my_bot))
