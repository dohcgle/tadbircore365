from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.database import update_credit_request_status

operator_router = Router()

@operator_router.callback_query(F.data.startswith("accept_AR-"))
async def process_operator_accept(callback: CallbackQuery):
    request_id = callback.data.replace("accept_", "")
    
    operator_name = callback.from_user.full_name
    
    # Ma'lumotlar bazasida holatni yangilash
    await update_credit_request_status(request_id, status="Qabul qilindi", accepted_by=operator_name)
    
    # Xabarni tahrirlash (tugmani olib tashlab, qabul qilgan operator ismini yozish)
    original_text = callback.message.text
    new_text = original_text + f"\n\n✅ **Ushbu ariza qabul qilindi:**\n👨‍💻 Operator: {operator_name}"
    
    await callback.message.edit_text(new_text, parse_mode="Markdown")
    await callback.answer("Ariza muvaffaqiyatli qabul qilindi!", show_alert=True)
