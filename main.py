import configparser
import logging.config
from src.bot.bot import bot

config = configparser.ConfigParser()
config.read('config.ini')

logging.config.fileConfig('config.ini')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    bot.run()
