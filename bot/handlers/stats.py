from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:adminpassword@db:5432/tadbircore")
from bot.config import ADMIN_CHAT_ID

stats_router = Router()

@stats_router.message(Command("stats"))
async def cmd_stats(message: Message):
    if str(message.chat.id) != str(ADMIN_CHAT_ID) and str(message.from_user.id) != str(ADMIN_CHAT_ID):
        await message.answer("⚠️ Bu komanda faqat adminlar uchun!")
        return
        
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Umumiy arizalar
        total = await conn.fetchval("SELECT COUNT(*) FROM credit_requests")
        
        # Qabul qilingan
        accepted = await conn.fetchval("SELECT COUNT(*) FROM credit_requests WHERE status != 'Kutilyapti'")
        
        # Kutilayotgan
        pending = await conn.fetchval("SELECT COUNT(*) FROM credit_requests WHERE status = 'Kutilyapti'")
    finally:
        await conn.close()
            
    text = (
        f"📊 **Qisqacha Statistika**\n\n"
        f"📑 **Jami arizalar:** {total}\n"
        f"✅ **Qabul qilinganlar:** {accepted}\n"
        f"⏳ **Kutilayotganlar:** {pending}\n\n"
        f"🌐 Batafsil statistika va grafiklar uchun Web Dashboard'ga kiring."
    )
    
    await message.answer(text, parse_mode="Markdown")
