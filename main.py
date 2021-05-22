import configparser
import logging.config
from src.bot.bot import bot
from src.bot.gameobservers.utils import test

config = configparser.ConfigParser()
config.read('config.ini')

logging.config.fileConfig('config.ini')

if __name__ == '__main__':
    test()
    #bot.run()
