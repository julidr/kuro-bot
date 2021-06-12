import discord
from discord.ext import commands
from discord.ext.commands import Context

from karthuria.repository.character_repository import CharacterRepository
from src.utils.date_utils import convert_date_to_str


class BirthdayCommand(commands.Cog):

    def __init__(self, my_bot=commands.Bot):
        self.bot = my_bot
        self.character_repo = CharacterRepository()

    @commands.command(pass_context=True)
    async def birthday(self, ctx: Context, name: str = None) -> None:
        """
        Show the birthday information for one character based on the given name

        :param ctx: Discord context
        :param name: Character name to search and show its birthday information
        :return: None
        """
        if name is None:
            await ctx.send('Méchante va! - Please specify the name of the girl.')
            return

        embed = None
        character = self.character_repo.get_character_by_name(name)
        if character:
            title = 'Birthday of {0}'.format(character.name)
            message = '{0} {1}'.format(_special_message_birthday(character.name),
                                       convert_date_to_str(character.birthday))
            rgb = character.color.rgb
            embed = discord.Embed(title=title, description=message, color=_get_discord_color(rgb))
            embed.set_thumbnail(url=character.portrait)
        else:
            message = "Je suis désolé, I don't know who '{0}' is".format(name)
        await ctx.send(message, embed=embed)


def _special_message_birthday(name: str) -> str:
    """
    Retrieve an special birthday message based on which character was queried.

    At the moment only claudine and maya have special messages.

    :param name: The name of the character that was queried
    :return: An special message for the bot to return with the birthday info
    """
    message = 'Her birthday is'
    if 'claudine' in name.lower():
        message = 'My birthday is'
    if 'maya' in name.lower():
        message = 'Jum! That annoying woman birthday is'
    return message


def _get_discord_color(color: tuple) -> discord.Color:
    """
    Given a tuple of rgb colors from each character, return the respective Discord color for it.

    :param color: A tuple with the r, g, b values
    :return: A discord Color value based on the given values
    """
    return discord.Color.from_rgb(color[0], color[1], color[2])


def setup(my_bot: commands.Bot) -> None:
    """
    Bot setup necessary to recognize its COG
    :param my_bot: the bot where the commands need to be register
    :return: None
    """
    my_bot.add_cog(BirthdayCommand(my_bot))
