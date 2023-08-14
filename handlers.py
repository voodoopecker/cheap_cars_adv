"""Handlers to control bot"""

from aiogram import Bot
from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from settings import ADMIN_ID, TOKEN
import keyboard
import use_data

router = Router()
bot = Bot(TOKEN)


@router.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer('Greetings and welcome... I want to play a game.', reply_markup=keyboard.admin_keyboard)


@router.message(F.text.startswith('Post'), F.from_user.id == ADMIN_ID)  # manual launcher
async def post_new_message(message: Message):
    await use_data.starter()


@router.message(F.text.startswith('Screenshot'), F.from_user.id == ADMIN_ID)  # send screenshot from browser
async def send_screenshot(message: Message):
    image = FSInputFile('screenshot.png')
    await bot.send_photo(chat_id=ADMIN_ID, photo=image)


@router.message()
async def unknown_command(message: Message):
    await message.reply('Game Over!')
