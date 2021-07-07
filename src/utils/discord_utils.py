import discord


def get_discord_color(color: tuple) -> discord.Color:
    """
    Given a tuple of rgb colors from each character, return the respective Discord color for it.

    :param color: A tuple with the r, g, b values
    :return: A discord Color value based on the given values
    """
    return discord.Color.from_rgb(color[0], color[1], color[2])
