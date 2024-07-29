import asyncio
from aiogram import Bot, Dispatcher
import logging

from config import bot, dp, database
from handlers.echo import echo_router
from handlers.survey import survey_router


async def on_startup(dispatcher: Dispatcher):
    await database.create_tables()


async def main():
    dp.startup.register(on_startup)
    dp.include_router(survey_router)
    dp.include_router(echo_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
