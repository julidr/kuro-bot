import sys
import logging
import traceback

from discord.ext import commands
from utils.settings_utils import config

LOG_ID = 'KuroBotInitializer'
logging.basicConfig(level=logging.INFO)

description = 'Your favorite french girl made a bot, that delivers basic information of Starlight franchise'
prefixes = config.get('prefixes')
modules = config.get('commands')
token = config.get('token')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(*prefixes), description=description)


@bot.event
async def on_ready():
    logging.info('[{0}] Getting ready {1}'.format(LOG_ID, bot.user.name))
    logging.debug('[{0}] Loading commands...'.format(LOG_ID))
    if __name__ == '__main__':
        modules_loaded = 0
        for module in modules:
            try:
                bot.load_extension(module)
                logging.debug('\t' + module)
                modules_loaded += 1
            except Exception as details:
                traceback.print_exc()
                logging.error(f'Error loading the extension {module}', file=sys.stderr)
                logging.error(details)

        logging.debug(str(modules_loaded) + '/' + str(modules.__len__()) + ' modules loaded')
        logging.debug('[{0}] Systems 100%'.format(LOG_ID))
    logging.info('[{0}] Bot ready!'.format(LOG_ID))


if __name__ == "__main__":
    bot.run(token)
