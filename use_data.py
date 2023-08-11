'''Collection of functions used for posting messages to channel'''

__all__ = ['preparing_messages', 'post_message', 'starter']

import json
import asyncio
from loguru import logger as LOGGER
from aiogram import Bot

import get_source
import get_data
from settings import ADMIN_ID, GROUP_ID, TOKEN

bot = Bot(TOKEN)


async def preparing_messages():
    '''Function to filter new adv'''

    with (open('filtered_data.json', 'r', encoding='utf-8') as filtered_data_file,
          open('cleared_data.json', 'r', encoding='utf-8') as cleared_data_file
          ):
        filtered_data = json.load(filtered_data_file)
        cleared_data = json.load(cleared_data_file)
        messages = {}
        for saleid, data in filtered_data.items():
            if saleid in cleared_data.keys():
                continue
            else:
                messages[saleid] = data
    return messages


async def post_message():
    '''Function to post messages to channel'''

    messages = await preparing_messages()
    for saleid, data in messages.items():
        await bot.send_message(chat_id=GROUP_ID, text=f'{saleid}{data}')
        LOGGER.debug(saleid, data)
        await asyncio.sleep(3)


async def starter():
    '''Maintain all processes step by step'''

    await get_source.browser_open_source_page()
    await get_data.gathering_data()
    await post_message()
