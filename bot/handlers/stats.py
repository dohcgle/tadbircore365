from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import aiosqlite
from bot.database import DB_NAME
from bot.config import ADMIN_CHAT_ID

stats_router = Router()

@stats_router.message(Command("stats"))
async def cmd_stats(message: Message):
    if str(message.chat.id) != str(ADMIN_CHAT_ID) and str(message.from_user.id) != str(ADMIN_CHAT_ID):
        await message.answer("⚠️ Bu komanda faqat adminlar uchun!")
        return
        
    async with aiosqlite.connect(DB_NAME) as db:
        # Umumiy arizalar
        async with db.execute("SELECT COUNT(*) FROM credit_requests") as cursor:
            total = (await cursor.fetchone())[0]
            
        # Qabul qilingan
        async with db.execute("SELECT COUNT(*) FROM credit_requests WHERE status != 'Kutilyapti'") as cursor:
            accepted = (await cursor.fetchone())[0]
            
        # Kutilayotgan
        async with db.execute("SELECT COUNT(*) FROM credit_requests WHERE status = 'Kutilyapti'") as cursor:
            pending = (await cursor.fetchone())[0]
            
    text = (
        f"📊 **Qisqacha Statistika**\n\n"
        f"📑 **Jami arizalar:** {total}\n"
        f"✅ **Qabul qilinganlar:** {accepted}\n"
        f"⏳ **Kutilayotganlar:** {pending}\n\n"
        f"🌐 Batafsil statistika va grafiklar uchun Web Dashboard'ga kiring."
    )
    
    await message.answer(text, parse_mode="Markdown")
