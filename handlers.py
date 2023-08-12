"""Handlers to control bot"""

from aiogram import Bot
from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

from settings import ADMIN_ID, TOKEN
import use_data

router = Router()
bot = Bot(TOKEN)


@router.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer('Greetings and welcome... I want to play a game.')


@router.message(F.text.startswith('post'), F.from_user.id == ADMIN_ID)  # manual launcher
async def post_new_message(message: Message):
    await use_data.starter()


@router.message()
async def unknown_command(message: Message):
    await message.reply('Unknown command!')
