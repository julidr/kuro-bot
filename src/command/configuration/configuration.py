import logging

from discord import Role
from discord.abc import GuildChannel
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
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('Désolé, tout utilisateur. Only server admins can use this command.')
            return

        if channel_name is None:
            await ctx.send('Hmm...Please specify the channel name.')
            return

        channel = get_channel_id(ctx, channel_name)
        rol = ctx.guild.default_role if announcement_rol is None else get_rol(ctx, announcement_rol)

        if rol is None:
            await ctx.send("Je suis desolé - I wasn't able to find role [{0}]".format(announcement_rol))
            return

        if channel is not None:
            log_rol = rol.name if rol.name != '@everyone' else rol.name[1::]
            self.server_repository.create_server(ctx.guild.id, ctx.guild.name, channel.id, channel.name,
                                                 ChannelType.BIRTHDAY, rol.id)
            await ctx.send('Fait! - Birthday channel [{0}] was set with role [{1}]'.format(channel_name, log_rol))
            return

        await ctx.send("Je suis desolé - I wasn't able to find channel [{0}]".format(channel_name))

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
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send('Désolé, tout utilisateur. Only server admins can use this command.')
            return

        if channel_name is None:
            await ctx.send('Hmm...Please specify the channel name.')
            return

        channel = get_channel_id(ctx, channel_name)
        rol = ctx.guild.default_role if announcement_rol is None else get_rol(ctx, announcement_rol)

        if rol is None:
            await ctx.send("Je suis desolé - I wasn't able to find role [{0}]".format(announcement_rol))
            return

        if channel is not None:
            log_rol = rol.name if rol.name != '@everyone' else rol.name[1::]
            self.server_repository.create_server(ctx.guild.id, ctx.guild.name, channel.id, channel.name,
                                                 ChannelType.EVENT, rol.id)
            await ctx.send('Fait! - Event channel [{0}] was set with role [{1}]'.format(channel_name, log_rol))
            return

        await ctx.send("Je suis desolé - I wasn't able to find  [{0}]".format(channel_name))


def get_rol(ctx: Context, role_name: str) -> Role:
    """
    Look for the respective rol in a Guild based on the specified rol name

    :param ctx: Discord Context of execution
    :param role_name: the rol to find
    :return: Instance of Role for the specified name
    """
    roles = ctx.guild.roles
    for rol in roles:
        if rol.name == role_name:
            return rol


def get_channel_id(ctx: Context, channel_name: str) -> GuildChannel:
    """
    Look for the respective channel in a Guild based on the specified channel name

    :param ctx: Discord Context of execution
    :param channel_name: the channel to find
    :return: Instance of GuildChannel for the specified name
    """
    channels = ctx.guild.channels
    for channel in channels:
        if channel.name == channel_name:
            return channel


def setup(my_bot: commands.Bot) -> None:
    """
    Bot setup necessary to recognize its COG
    :param my_bot: the bot where the commands need to be register
    :return: None
    """
    initializer = Initializer()
    my_bot.add_cog(ConfigurationCommand(initializer.get_servers_repository(), my_bot))
