import logging
from datetime import datetime

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

from command.configuration.repository.server_repository import ServerRepository
from command.initializer import Initializer
from karthuria.model.character import Character
from karthuria.repository.character_repository import CharacterRepository
from utils.date_utils import convert_date_to_str
from utils.discord_utils import get_discord_color

LOG_ID = "BirthdayCommand"


class BirthdayCommand(commands.Cog):
    """
    All Kuro bot discord commands that are related to birthdays. Either to get birthday information or to notify them
    """

    def __init__(self, character_repository: CharacterRepository, server_repository: ServerRepository, cdn_url: str,
                 my_bot=commands.Bot):
        self.bot = my_bot
        self.character_repository = character_repository
        self.server_repository = server_repository
        self.birthday_reminder.start()
        self.school_icon_url = '{0}/{1}'.format(cdn_url, 'res/ui/images/chat/icon_school_{0}.png')

    @commands.command(pass_context=True)
    async def birthday(self, ctx: Context, name: str = None) -> None:
        """
        Show the birthday information for one character based on the given name

        :param ctx: Discord context
        :param name: Character name to search and show its birthday information
        :return: None
        """
        logging.debug('[{0}] - Birthday called with value [{1}]'.format(LOG_ID, name))
        if name is None:
            await ctx.send('Méchante va! - Please specify the name of the girl.')
            return

        embed = None
        character = self.character_repository.get_character_by_name(name)
        if character:
            title = 'Birthday of {0}'.format(character.name)
            message = '{0} {1}'.format(special_message_birthday(character.name),
                                       convert_date_to_str(character.birthday))
            rgb = character.color.rgb
            embed = discord.Embed(title=title, description=message, color=get_discord_color(rgb))
            embed.set_thumbnail(url=character.portrait)
        else:
            message = "Je suis désolé, I don't know who '{0}' is".format(name)
        await ctx.send(message, embed=embed)

    @tasks.loop(hours=24)
    async def birthday_reminder(self) -> None:
        """
        Background task that is executed one time each 24 hours to review if it is the birthday of
        any stage girl. If it is then sends a message to the respective announcement channel.

        :return: None
        """
        logging.info('[{0}] - Reviewing today birthdays'.format(LOG_ID))
        self.server_repository.reload_servers()
        today = convert_date_to_str(datetime.today().date(), '%d/%m')
        birthday_girl = self.character_repository.get_character_birthday(today)

        if birthday_girl is not None:
            logging.info('[{0}] - Birthday of {1} found'.format(LOG_ID, birthday_girl.name))

            for guild in self.bot.guilds:
                server = self.server_repository.find_server_by_id(guild.id)
                if server is None:
                    logging.warning('[{0}] - Missing configuration for server [{1}]'.format(LOG_ID, guild.name))
                else:
                    if server.birthday_channel is not None:
                        channel = self.bot.get_channel(server.birthday_channel.channel_id)
                        rol = guild.get_role(server.birthday_channel.announcement_rol)
                        embed = build_birthday_reminder_embed(birthday_girl, self.school_icon_url)
                        await channel.send(rol.mention, embed=embed)
                    else:
                        logging.warning('[{0}] - Missing configuration for birthday channel '
                                        'in server [{1}]'.format(LOG_ID, guild.name))

    @birthday_reminder.before_loop
    async def before_birthday_reminder(self):
        """
        Setup for the birthday reminder.

        :return: None
        """
        logging.debug('[{0}] - Waiting to start birthdays reminders...'.format(LOG_ID))
        await self.bot.wait_until_ready()
        logging.debug('[{0}] - Birthday reminders ready!'.format(LOG_ID))


def build_birthday_reminder_embed(birthday_girl: Character, school_icon_url: str) -> discord.Embed:
    """
    Build the birthday reminder message with the respective format and given information.

    :param birthday_girl: The stage girl that is celebrating its birthday
    :param school_icon_url: The url of the school shield
    :return: Discord Embed with the defined format to use
    """

    title = 'Bon anniversaire {0}!!'.format(birthday_girl.name)
    pronoun = 'my' if 'Claudine' in birthday_girl.name else birthday_girl.name
    message = "Today is {0} birthday!! Let's celebrate it.".format(pronoun)
    rgb = birthday_girl.color.rgb

    embed = discord.Embed(title=title, description=message, color=get_discord_color(rgb))
    embed.set_thumbnail(url=birthday_girl.portrait)
    embed.set_image(url=school_icon_url.format(birthday_girl.school))
    embed.add_field(name='Description', value=birthday_girl.description, inline=False)
    embed.add_field(name='Birthday', value=convert_date_to_str(birthday_girl.birthday), inline=False)
    embed.add_field(name='Voice Actor', value=birthday_girl.seiyuu, inline=False)
    embed.add_field(name='Likes', value=birthday_girl.likes, inline=True)
    embed.add_field(name='Dislikes', value=birthday_girl.dislikes, inline=True)
    embed.add_field(name='School', value=birthday_girl.school.description, inline=False)

    return embed


def special_message_birthday(name: str) -> str:
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


def setup(my_bot: commands.Bot) -> None:
    """
    Bot setup necessary to recognize its COG
    :param my_bot: the bot where the commands need to be register
    :return: None
    """
    initializer = Initializer()
    my_bot.add_cog(BirthdayCommand(initializer.get_character_repository(),
                                   initializer.get_servers_repository(),
                                   initializer.get_cdn_url(),
                                   my_bot))
