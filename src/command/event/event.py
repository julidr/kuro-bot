import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context

from command.initializer import Initializer
from karthuria.repository.dress_repository import DressRepository
from karthuria.repository.enemy_repository import EnemyRepository
from karthuria.repository.event_repository import EventRepository
from utils.discord_utils import get_discord_color

LOG_ID = "EventCommand"
logging.basicConfig(level=logging.INFO)

RELIVE_RGB = (234, 1, 36)


class EventCommand(commands.Cog):
    """
    All Kuro bot discord commands that are related to events. Either to get list of current events or to notify them
    """

    def __init__(self, event_repository: EventRepository, dress_repository: DressRepository,
                 enemy_repository: EnemyRepository, my_bot=commands.Bot):
        self.bot = my_bot
        self.event_repository = event_repository
        self.dress_repository = dress_repository
        self.enemy_repository = enemy_repository

    @commands.command(pass_context=True)
    async def current_events(self, ctx: Context):
        """
        Show a list with the name and end date of the ongoing events in all server of Relive.

        :param ctx: Discord Context
        :return: Message with the current events, challenges and bosses battles in relive
        """
        logging.debug('[{0}] - Current Events called with value'.format(LOG_ID))

        bullets_emoji = ':white_small_square:'
        message_format = '{0}{1} - {2} \n'
        title = 'List of Current Ongoing Events'
        description = 'This is what I could find:'
        embed = discord.Embed(title=title, description=description, color=get_discord_color(RELIVE_RGB))

        current_events = self.event_repository.get_current_events()

        if 'events' in current_events:
            events_message = ''

            events = self.__get_complete_events_list(current_events['events'])
            for event in events:
                events_message += message_format.format(bullets_emoji, event.name, event.end_date)
            embed.add_field(name='Events', value=events_message, inline=False)

        if 'challenges' in current_events:
            challenges_message = ''
            challenges = self.__get_complete_challenges_list(current_events['challenges'])
            for challenge in challenges:
                challenges_message += message_format.format(bullets_emoji, challenge.name, challenge.end_date)
            embed.add_field(name='Challenges Revue', value=challenges_message, inline=False)

        if 'bosses' in current_events:
            bosses_message = ''
            bosses = self.__get_complete_bosses_list(current_events['bosses'])
            for boss in bosses:
                bosses_message += message_format.format(bullets_emoji, boss.name, boss.end_date)
            embed.add_field(name='Score Attack Revue', value=bosses_message, inline=False)

        await ctx.send(embed=embed)

    def __get_complete_events_list(self, events: list) -> list:
        """
        Complete events information, like their name and returns a list with the events updated

        :param events: List of current events
        :return: A new list of events with its respective names
        """
        events_list = []
        for event in events:
            event_name = self.event_repository.get_event_name_by_id(event.event_id)
            event.set_name(event_name if event_name is not None else 'NN')
            events_list.append(event)
        return events_list

    def __get_complete_challenges_list(self, challenges: list) -> list:
        """
        Complete challenges information, like their name and returns a list with the challenges updated

        :param challenges: List of current challenges
        :return: A new list of challenges with its respective names
        """
        challenges_list = []
        for challenge in challenges:
            dress = self.dress_repository.get_dress_by_id(challenge.event_id)
            dress_name = dress.name if dress is not None else 'NN'
            challenge.set_name(dress_name)
            challenges_list.append(challenge)
        return challenges_list

    def __get_complete_bosses_list(self, bosses: list) -> list:
        """
        Complete bosses information, like their name and returns a list with the bosses updated

        :param bosses: List of current bosses
        :return: A new list of bosses with its respective names
        """
        bosses_list = []
        for boss in bosses:
            enemy = self.enemy_repository.get_enemy_by_id(boss.event_id)
            enemy_name = enemy.name if enemy is not None else 'NN'
            boss.set_name(enemy_name)
            bosses_list.append(boss)
        return bosses_list


def setup(my_bot: commands.Bot) -> None:
    """
    Bot setup necessary to recognize its COG
    :param my_bot: the bot where the commands need to be register
    :return: None
    """
    initializer = Initializer()
    my_bot.add_cog(EventCommand(initializer.get_event_repository(),
                                initializer.get_dress_repository(),
                                initializer.get_enemy_repository(),
                                my_bot))
