import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.database import init_db
from bot.handlers.start import start_router
from bot.handlers.credit import credit_router
from bot.handlers.contact import contact_router
from bot.handlers.cabinet import cabinet_router
from bot.handlers.calculator import calculator_router
from bot.handlers.operator import operator_router
from bot.handlers.stats import stats_router

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(start_router)
    dp.include_router(contact_router)
    dp.include_router(credit_router)
    dp.include_router(cabinet_router)
    dp.include_router(calculator_router)
    dp.include_router(operator_router)
    dp.include_router(stats_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
