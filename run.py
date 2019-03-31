import logging

from grabber import Grabber
from database import config

logger = logging.getLogger('youtuber')
handler = logging.FileHandler('error.log')
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    grabber = Grabber(config.get('api_key', ''), config.get('channels', []))
    grabber.run()
