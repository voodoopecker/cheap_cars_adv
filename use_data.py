"""Collection of functions used for posting messages to channel"""

__all__ = ['preparing_messages', 'post_message', 'formatting_messages', 'starter']

import json
import asyncio
import os
from loguru import logger as LOGGER
from aiogram import Bot
from aiogram.utils.markdown import hide_link  # hides link in message

import get_source
import get_data
from settings import ADMIN_ID, GROUP_ID, TOKEN

bot = Bot(TOKEN, parse_mode="HTML")  # additional mode HTML markdown to hide link in messages


async def preparing_messages():
    """Function to filter new adv"""

    if not os.path.exists('posted_data.json'):
        with open('posted_data.json', 'w', encoding='utf-8') as output_file:
            output_file.write('[]')

    with (open('filtered_data.json', 'r', encoding='utf-8') as filtered_data_file,
          open('posted_data.json', 'r', encoding='utf-8') as posted_data_file
          ):
        filtered_data = json.load(filtered_data_file)
        posted_data = json.load(posted_data_file)
        messages = {}
        for saleid, data in filtered_data.items():
            if saleid in posted_data:
                continue
            else:
                messages[saleid] = data
                posted_data += [saleid]
            await asyncio.sleep(0.01)

    with open('posted_data.json', 'w', encoding='utf-8') as output_file:
        json.dump(posted_data, output_file)
    LOGGER.success('posted_data.json has been updated with new data')

    return messages


async def formatting_messages():
    """Function to format all items from data to one complete message"""

    messages = await preparing_messages()
    for saleid, data in messages.items():
        output_message = ''
        output_message += f"""{data['name']}
Цена: {data['price']}
Год выпуска: {data['year']}
Пробег: {data['mileage']}
Вилка цен: {data['price_range']}
Ниже рынка на: {data['lower_market_rate']}
{hide_link(data['photo_link'])}
Ссылка на объявление: {data['adv_link']}
"""
        yield output_message
        await asyncio.sleep(0.1)


async def post_message():
    """Function to post messages to channel"""

    posts_counter = 0
    output_message = formatting_messages()
    async for post in output_message:
        await bot.send_message(chat_id=GROUP_ID, text=post)
        posts_counter += 1
        LOGGER.debug(post)
        await asyncio.sleep(3)

    await bot.send_message(chat_id=ADMIN_ID, text=f'{posts_counter} messages were send.')
# asyncio.run(post_message())


async def starter():
    """Maintain all processes step by step"""

    LOGGER.debug('Starter is working ...')
    await bot.send_message(chat_id=ADMIN_ID, text='Starter is working ...')

    await get_source.browser_open_source_page()
    await get_data.gathering_data()
    await post_message()
    LOGGER.debug('Done! Waiting for the next launch ...')
# asyncio.run(starter())
