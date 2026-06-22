import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN, ADMIN_CHAT_ID
from bot.database import init_db
from bot.handlers.start import start_router
from bot.handlers.credit import credit_router
from bot.handlers.contact import contact_router
from bot.handlers.cabinet import cabinet_router
from bot.handlers.calculator import calculator_router
from bot.handlers.operator import operator_router
from bot.handlers.stats import stats_router

async def on_startup(bot: Bot):
    if ADMIN_CHAT_ID:
        try:
            await bot.send_message(chat_id=ADMIN_CHAT_ID, text="✅ **TadbirCore Bot ishga tushdi va xizmat ko'rsatishga tayyor!**", parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Failed to send startup message: {e}")

async def on_shutdown(bot: Bot):
    if ADMIN_CHAT_ID:
        try:
            await bot.send_message(chat_id=ADMIN_CHAT_ID, text="❌ **TadbirCore Bot to'xtadi! (Xizmat ko'rsatish vaqtincha to'xtatildi)**", parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Failed to send shutdown message: {e}")

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    dp.include_router(start_router)
    dp.include_router(contact_router)
    dp.include_router(credit_router)
    dp.include_router(cabinet_router)
    dp.include_router(calculator_router)
    dp.include_router(operator_router)
    dp.include_router(stats_router)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
