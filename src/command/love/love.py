import logging
import random

import discord
from discord.ext import commands
from discord.ext.commands import Context

from command.configuration.repository.server_repository import ServerRepository
from command.initializer import Initializer
from karthuria.repository.dress_repository import DressRepository
from karthuria.repository.equip_repository import EquipRepository
from utils.discord_utils import get_discord_color

LOG_ID = "LoveCommand"

DRESS_URL = 'https://cdn.karth.top/api/assets/dlc/res/dress/cg/{0}/image.png'
EQUIP_URL = 'https://cdn.karth.top/api/assets/dlc/res/equip/cg/{0}/image.png'

LOVE_RGB = (255, 141, 141)
NO_LOVE_RGB = (0, 150, 218)


class LoveCommand(commands.Cog):
    """
    All Kuro bot discord commands that are related to Kuro Love.
    """

    CLAUDINE_CHARACTER_ID = 104
    I_LOVE_YOU_TEXT = "Je t'aime {0}"
    I_LOVE_YOU_URL = "https://cdn.karth.top/api/assets/dlc/res/equip/cg/4000160/image.png"
    I_LOVE_YOU_URL_THUMBNAIL = "https://cdn.karth.top/api/assets/ww/res_en/res/item_root/medium/32_10413.png"
    NO_LOVE_URL_THUMBNAIL = "https://cdn.karth.top/api/assets/ww/res_en/res/item_root/medium/32_10412.png"

    def __init__(self, dress_repository: DressRepository, equip_repository: EquipRepository,
                 server_repository: ServerRepository, my_bot=commands.Bot):
        self.bot = my_bot
        self.dress_repository = dress_repository
        self.equip_repository = equip_repository
        self.server_repository = server_repository
        self.claudine_dresses = []
        self.claudine_equips = []

    @commands.command(pass_context=True)
    async def i_love_you(self, ctx: Context) -> None:
        """
        Randomly answers with either images of your favorite girl Cloudine or there is a chance
        that she says to you those three words back.

        :param ctx: Discord context
        :return: None
        """
        logging.debug('[{0}] - Love command called'.format(LOG_ID))

        if len(self.claudine_dresses) == 0:
            self.claudine_dresses = self.dress_repository.get_dresses_by_character_id(self.CLAUDINE_CHARACTER_ID)
        if len(self.claudine_equips) == 0:
            self.claudine_equips = self.equip_repository.get_equips_by_character_id(self.CLAUDINE_CHARACTER_ID)

        options = [self.I_LOVE_YOU_TEXT, get_random_dress(self.claudine_dresses), get_random_equip(self.claudine_equips)]
        random_option = random.choices(options, weights=(1, 50, 80), k=1)

        if random_option[0] == self.I_LOVE_YOU_TEXT:
            author = ctx.message.author.mention
            title = "Love"
            message = random_option[0].format(author)
            color = get_discord_color(LOVE_RGB)
            image = self.I_LOVE_YOU_URL
            thumbnail = self.I_LOVE_YOU_URL_THUMBNAIL
        else:
            author = ''
            title = "No Love"
            message = "Je suis désolé, but I don't. Here have a nice picture of me as consolation."
            color = get_discord_color(NO_LOVE_RGB)
            image = random_option[0]
            thumbnail = self.NO_LOVE_URL_THUMBNAIL

        embed = discord.Embed(title=title, description=message, color=color)
        embed.set_image(url=image)
        embed.set_thumbnail(url=thumbnail)

        await ctx.send(author, embed=embed)


def get_random_dress(dresses: list) -> str:
    """
    From a given list of dresses choose a random item to return the url image of that dress

    :param dresses: A list with all the different available dresses
    :return: An str Url of that dress
    """
    random_dress = random.choice(dresses)
    return DRESS_URL.format(random_dress.dress_id)


def get_random_equip(equips: list) -> str:
    """
    From a given list of equips choose a random item to return the url image of that equip

    :param equips: A list with all the different available equips
    :return: An str Url of that equip
    """
    random_equip = random.choice(equips)
    return EQUIP_URL.format(random_equip.equip_id)


def setup(my_bot: commands.Bot) -> None:
    """
    Bot setup necessary to recognize its COG
    :param my_bot: the bot where the commands need to be register
    :return: None
    """
    initializer = Initializer()
    my_bot.add_cog(LoveCommand(initializer.get_dress_repository(),
                               initializer.get_equip_repository(),
                               initializer.get_servers_repository(),
                               my_bot))
