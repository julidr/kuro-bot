import discord
from discord import Role
from discord.abc import GuildChannel
from discord.ext.commands import Context


def get_discord_color(color: tuple) -> discord.Color:
    """
    Given a tuple of rgb colors from each character, return the respective Discord color for it.

    :param color: A tuple with the r, g, b values
    :return: A discord Color value based on the given values
    """
    return discord.Color.from_rgb(color[0], color[1], color[2])


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


def get_channel_by_name(ctx: Context, channel_name: str) -> GuildChannel:
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
