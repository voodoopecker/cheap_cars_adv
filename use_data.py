'''Collection of functions used for posting messages to channel'''

__all__ = ['preparing_messages', 'post_message', 'formatting_messages', 'starter']

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
            await asyncio.sleep(0.01)
    return messages


async def formatting_messages():
    '''Function to format all items from data to one complete message'''

    messages = await preparing_messages()
    for saleid, data in messages.items():
        output_message = ''
        output_message += f"""{data['name']}
Цена: {data['price']}
Год выпуска: {data['year']}
Пробег: {data['mileage']}
Вилка цен: {data['price_range']}
Ниже рынка на: {data['lower_market_rate']}
{data['photo_link']}
Ссылка на объявление: {data['adv_link']}
"""
        yield output_message
        await asyncio.sleep(0.1)


async def post_message():
    '''Function to post messages to channel'''

    output_message = formatting_messages()
    async for post in output_message:
        await bot.send_message(chat_id=GROUP_ID, text=post)
        LOGGER.debug(post)
        await asyncio.sleep(3)


async def starter():
    '''Maintain all processes step by step'''

    await get_source.browser_open_source_page()
    await get_data.gathering_data()
    await post_message()
