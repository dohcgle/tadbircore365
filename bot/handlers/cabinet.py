from aiogram import Router, F
from aiogram.types import Message
from bot.database import get_user_credit_requests

cabinet_router = Router()

@cabinet_router.message(F.text == "👤 Shaxsiy kabinet")
async def process_cabinet(message: Message):
    user_id = message.from_user.id
    requests = await get_user_credit_requests(user_id)
    
    if not requests:
        await message.answer("Sizda hozircha hech qanday kredit arizalari mavjud emas.")
        return
    
    text_lines = ["👤 **Shaxsiy kabinet**\nSizning joriy arizalaringiz:\n"]
    
    for req in requests:
        status_display = req.get('status', 'Kutilyapti')
        if status_display == 'Kutilyapti':
            status_display = f"🟡 {status_display}"
        elif status_display == 'Tasdiqlandi':
            status_display = f"🟢 {status_display}"
        elif status_display == 'Rad etildi':
            status_display = f"🔴 {status_display}"
            
        date_str = req.get('created_at', '')
        if date_str:
            # Simplistic parsing of isoformat "YYYY-MM-DDTHH:MM:SS..."
            try:
                date_str = date_str.split("T")[0]
            except Exception:
                pass
                
        nomalum_text = "Noma'lum"
        req_text = (
            f"🆔 **Ariza:** {req.get('request_id', nomalum_text)}\n"
            f"💰 **Summa:** {req.get('amount', nomalum_text)}\n"
            f"🏦 **Bank:** {req.get('selected_bank', nomalum_text)}\n"
            f"📊 **Holati:** {status_display}\n"
            f"🗓 **Sana:** {date_str}\n"
            "---"
        )
        text_lines.append(req_text)
    
    final_text = "\n".join(text_lines)
    await message.answer(final_text, parse_mode="Markdown")
