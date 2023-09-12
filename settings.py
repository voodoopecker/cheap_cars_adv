"""Settings:
TOKEN - your bot token taken from BotFather.
ADMIN_ID - telegram account ID who controls bot.
GROUP_ID - telegram group ID where posts send.
MAIN_LINK - source page link from where data scraps.
SCHEDULER_TIME - interval between runs in seconds

Create .env file in the same folder with all these constants filled with your private data (example):
TOKEN: str = '3452345344:DSA5-dfgKd3JAoQ7rj2D3NVRoQ0Qs-zx5Yp'
ADMIN_ID: int = 6786786734
GROUP_ID: int = -1007638736412
MAIN_LINK: str = 'https://XautoX.ru/moscow/cars'
"""
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN: str = str(os.environ.get('TOKEN'))
ADMIN_ID: int = int(os.environ.get('ADMIN_ID'))
GROUP_ID: int = int(os.environ.get('GROUP_ID'))
MAIN_LINK: str = str(os.environ.get('MAIN_LINK'))

SCHEDULER_TIME: int = 3600
