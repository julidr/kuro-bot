import logging
from datetime import datetime

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

from command.configuration.repository.server_repository import ServerRepository
from command.initializer import Initializer
from karthuria.model.event import Challenge, Boss, Event
from karthuria.repository.dress_repository import DressRepository
from karthuria.repository.enemy_repository import EnemyRepository
from karthuria.repository.event_repository import EventRepository
from utils.date_utils import get_days_diff
from utils.discord_utils import get_discord_color

LOG_ID = "EventCommand"

RELIVE_RGB = (234, 1, 36)


class EventCommand(commands.Cog):
    """
    All Kuro bot discord commands that are related to events. Either to get list of current events or to notify them
    """

    def __init__(self, event_repository: EventRepository, dress_repository: DressRepository,
                 enemy_repository: EnemyRepository, server_repository: ServerRepository, my_bot=commands.Bot):
        self.bot = my_bot
        self.event_repository = event_repository
        self.dress_repository = dress_repository
        self.enemy_repository = enemy_repository
        self.server_repository = server_repository
        self.events_reminder.start()

    @commands.command(pass_context=True)
    async def current_events(self, ctx: Context) -> None:
        """
        Show a list with the name and end date of ongoing events in all server of Relive.

        :param ctx: Discord Context
        :return: Message with the current events, challenges and bosses battles in relive
        """
        logging.debug('[{0}] - Current Events called with value'.format(LOG_ID))

        events_message = ''
        challenges_message = ''
        bosses_message = ''

        bullets_emoji = ':white_small_square:'
        message_format = '{0}{1} - {2} \n'
        title = 'List of Current Ongoing Events'
        description = 'This is what I could find:'
        embed = discord.Embed(title=title, description=description, color=get_discord_color(RELIVE_RGB))

        current_events = self.event_repository.get_current_events()
        events = self.__get_complete_event_data([inner for outer in current_events for inner in current_events[outer]])

        for event in events:
            if isinstance(event, Challenge):
                challenges_message += message_format.format(bullets_emoji, event.name, event.end_date)
            elif isinstance(event, Boss):
                bosses_message += message_format.format(bullets_emoji, event.name, event.end_date)
            else:
                events_message += message_format.format(bullets_emoji, event.name, event.end_date)

        embed.add_field(name='Events', value=events_message, inline=False) if events_message != '' else None
        embed.add_field(name='Challenges Revue', value=challenges_message,
                        inline=False) if challenges_message != '' else None
        embed.add_field(name='Score Attack Revue', value=bosses_message, inline=False) if bosses_message != '' else None

        await ctx.send(embed=embed)

    @tasks.loop(hours=24)
    async def events_reminder(self) -> None:
        """
        Background task that is executed one time each 24 hours to review if an event is about one day to end.
        If it is then sends a message to the respective announcement channel.

        :return: None
        """
        logging.info('[{0}] - Reviewing today events'.format(LOG_ID))

        self.event_repository.reload_events()

        events_about_to_end = []
        events_about_to_start = []
        current_events = self.event_repository.get_current_events()

        for current_event in current_events:
            events_about_to_end += get_events_about_to_end(current_events[current_event])
        for current_event in current_events:
            events_about_to_start += get_events_about_to_start(current_events[current_event])

        events_about_to_end_count = len(events_about_to_end)
        events_about_to_start_count = len(events_about_to_start)

        if events_about_to_end_count > 0:
            logging.info('[{0}] - Found {1} Events About to End'.format(LOG_ID, events_about_to_end_count))
            await self.__send_info_events_reminder(events_about_to_end, is_ending=True)

        if events_about_to_start_count > 0:
            logging.info('[{0}] - Found {1} Events About to Start'.format(LOG_ID, events_about_to_start_count))
            await self.__send_info_events_reminder(events_about_to_start, is_ending=False)

    @events_reminder.before_loop
    async def before_events_reminder(self):
        """
        Setup for events reminder.

        :return: None
        """
        logging.debug('[{0}] - Waiting to start events reminders...'.format(LOG_ID))
        await self.bot.wait_until_ready()
        logging.debug('[{0}] - Events reminders ready!'.format(LOG_ID))

    async def __send_info_events_reminder(self, events_about_to_remind: list, is_ending: bool):

        self.server_repository.reload_servers()

        events_about_to_remind = self.__get_complete_event_data(events_about_to_remind)
        super_event = events_about_to_remind[0]

        for guild in self.bot.guilds:
            server = self.server_repository.find_server_by_id(guild.id)
            if server is None:
                logging.warning('[{0}] - Missing configuration for server [{1}]'.format(LOG_ID, guild.name))
            else:
                if server.event_channel is not None:
                    channel = self.bot.get_channel(server.event_channel.channel_id)

                    embed = build_event_reminder_embed(super_event, events_about_to_remind,
                                                       server.event_channel.announcement_rol, is_ending)
                    await channel.send(embed=embed)
                else:
                    logging.warning('[{0}] - Missing configuration for event channel '
                                    'in server [{1}]'.format(LOG_ID, guild.name))

    def __get_complete_event_data(self, events: list) -> list:
        """
        Retrieve complete data from an Event, Challenge or Boss and return a list with that information.

        :param events: List of events to retrieve their information
        :return: A list of each event with its complete data like names, rarity or hp percentage.
        """
        complete_data = []
        for event in events:
            if isinstance(event, Challenge):
                dress = self.dress_repository.get_dress_by_id(event.event_id)
                event.set_name(dress.name)
                event.set_rarity(dress.rarity)
                complete_data.append(event)
            elif isinstance(event, Boss):
                enemy = self.enemy_repository.get_enemy_by_id(event.event_id)
                event.set_name(enemy.name)
                event.set_rarity(enemy.rarity)
                event.set_icon(enemy.icon)
                complete_data.append(event)
            else:
                event_name = self.event_repository.get_event_name_by_id(event.event_id)
                event.set_name(event_name)
                complete_data.append(event)
        return complete_data


def get_events_about_to_end(current_events: list) -> list:
    """
    For a given list, search for the events that ends in 1 day and return them.

    :param current_events: List of Events to validate its expiry date
    :return: A list with events that are about to end
    """
    today = datetime.now()
    return [current_event for current_event in current_events if get_days_diff(today, current_event.end_date) == -1]


def get_events_about_to_start(current_events: list) -> list:
    """
    For a given list, search for the events that start in 1 days and return them.

    :param current_events: List of Events to validate its start date
    :return: A list with events that are about to start
    """
    today = datetime.now()
    events_with_start_date = [current_event for current_event in current_events if current_event.start_date is not None]
    return [event for event in events_with_start_date if get_days_diff(today, event.start_date) == -1]


def build_event_reminder_embed(super_event: Event, events_about_to_remind: list, server_rol: int,
                               is_ending: bool) -> discord.Embed:
    """
    Build the event reminder message with the respective format and given information.

    :param super_event: Event that is going to be show with more details than others
    :param events_about_to_remind: List with all events that are about to finish
    :param server_rol: The rol that will be use to announce the event
    :param is_ending: Variable that indicates if an event is starting or ending
    :return: Discord Embed with the defined format to use
    """
    star_emoji = ':star:'
    end_or_start = 'End' if is_ending else 'Start'
    encourage_message = 'Hurry to finish them' if is_ending else 'Get ready for them'
    title = '{0} is About to {1}!!'.format(super_event.name, end_or_start)
    description = '<@&{0}> The following events {1} in one day!! ' \
                  '{2} - Pour moi :heart:'.format(server_rol, end_or_start.lower(), encourage_message)
    embed = discord.Embed(title=title, description=description, color=get_discord_color(RELIVE_RGB))

    date_field_name = '{0} Date'.format(end_or_start)
    date_field_value = super_event.end_date if is_ending else super_event.start_date

    embed.add_field(name=date_field_name, value=date_field_value, inline=False)
    embed.add_field(name='Name', value=super_event.name, inline=True)
    embed.set_image(url=super_event.icon)

    if isinstance(super_event, Challenge) or isinstance(super_event, Boss):
        embed.add_field(name='Rarity', value=star_emoji * super_event.rarity, inline=True)
    if isinstance(super_event, Boss):
        embed.add_field(name='Life', value='{}%'.format(super_event.hp_percentage), inline=True)

    events_about_to_remind_count = len(events_about_to_remind)

    if events_about_to_remind_count > 1:

        additional_events_message = ''
        additional_events_message_format = '{0} {1} \n'
        bullets_emoji = ':white_small_square:'

        for additional_events in events_about_to_remind[1::]:
            additional_events_message += additional_events_message_format.format(bullets_emoji,
                                                                                 additional_events.name)
        additional_field_name = 'Additional Events that {0}'.format('Ends' if is_ending else 'Start')
        embed.add_field(name=additional_field_name, value=additional_events_message, inline=False)

    return embed


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
                                initializer.get_servers_repository(),
                                my_bot))
