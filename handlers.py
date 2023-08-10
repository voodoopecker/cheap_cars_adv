import asyncio

from aiogram import Bot
from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from settings import ADMIN_ID, GROUP_ID, TOKEN
import use_data

router = Router()
bot = Bot(TOKEN)

@router.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer('Hello, master!')

@router.message(F.text.startswith('post'), F.from_user.id == ADMIN_ID)
async def post_new_message(message: Message):
    messages = await use_data.post_message()
    for saleid, data in messages.items():
        print(saleid, data)
        await bot.send_message(chat_id=GROUP_ID, text=f'{saleid}{data}')
        await asyncio.sleep(3)

@router.message()
async def unknown_command(message: Message):
    await message.reply('Unknown command!')