import os
import json
import sys
import discord
import logging
import traceback

from discord.ext import commands
from utils.settings_utils import config

logging.basicConfig(level=logging.INFO)

description = 'Your favorite french girl made a bot, that delivers basic information of Starlight franchise'
prefixes = config.get('prefixes')
modules = config.get('commands')
token = config.get('token')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(*prefixes), description=description)


@bot.event
async def on_ready():
    print('bot name: ' + bot.user.name)
    print('Loading commands...')
    if __name__ == '__main__':
        modules_loaded = 0
        for module in modules:
            try:
                bot.load_extension(module)
                print('\t' + module)
                modules_loaded += 1
            except Exception as details:
                traceback.print_exc()
                print(f'Error loading the extension {module}', file=sys.stderr)
                print(details)

        print(str(modules_loaded) + '/' + str(modules.__len__()) + ' modules loaded')
        print('Systems 100%')
    print('------')


if __name__ == "__main__":
    bot.run(token)
