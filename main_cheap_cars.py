from loguru import logger as LOGGER
import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import handlers
from settings import TOKEN
from use_data import starter

LOGGER.add('logs/debug.log', format='{time}|{level}|{module}.{function}:{line} - {message}', level='DEBUG', rotation='00:00', compression='zip')

async def main():
    '''Main function. Start me to use bot.'''

    bot = Bot(TOKEN)
    dp = Dispatcher()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(starter, 'interval', seconds=3600)
    scheduler.start()

    dp.include_router(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    LOGGER.success('Bot started')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
