import discord
from discord.ext import commands
from discord.ext.commands import bot, Context

from command.birthday.repository.birthday_repository import BirthdayRepository
from utils.date_utils import convert_date_to_str


class BirthdayCommand(commands.Cog):

    def __init__(self, my_bot=commands.Bot):
        self.bot = my_bot
        self.birthday_repo = BirthdayRepository()

    @commands.command(pass_context=True)
    async def birthday(self, ctx: Context, name: str = None) -> None:
        """
        Show the birthday information for one character

        :param ctx: Discord context
        :param name: name of the character that you want to find its birthday
        :return: None
        """
        if name is None:
            await ctx.send('Méchante va! - Please specify the name of the girl.')
            return

        embed = None
        character = self.birthday_repo.get_character_by_name(name)
        if character:
            title = 'Birthday of {0}'.format(character.name)
            message = '{0} {1}'.format(_special_message_birthday(character.name),
                                       convert_date_to_str(character.birthday))
            embed = discord.Embed(title=title, description=message, color=discord.Color.from_rgb(254, 153, 82))
            embed.set_thumbnail(url=character.portrait)
        else:
            message = "I don't know who {0} is".format(name)
        await ctx.send(message, embed=embed)


def _special_message_birthday(name: str) -> str:
    message = 'Her birthday is'
    if 'claudine' in name.lower():
        message = 'My birthday is'
    if 'maya' in name.lower():
        message = 'Jum! That annoying woman birthday is'
    return message


def setup(my_bot: commands.Bot):
    my_bot.add_cog(BirthdayCommand(my_bot))
