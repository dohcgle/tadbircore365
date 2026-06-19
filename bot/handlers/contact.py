import random
import re
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.states.credit_state import ContactState, MurojaatState
from bot.keyboards.reply import main_menu_reply_keyboard, end_chat_keyboard
from bot.database import save_contact_request, get_user_phone
from bot.config import ADMIN_CHAT_ID

contact_router = Router()

@contact_router.message(F.text == "💬 Jonli chat")
async def start_live_chat(message: Message, state: FSMContext):
    await state.set_state(ContactState.WAITING_FOR_TEXT)
    text = (
        "👨‍💻 **Operator bilan bog'lanish**\n\n"
        "Siz jonli chatga ulandingiz. Barcha savol va takliflaringizni shu yerda yozishingiz mumkin. "
        "Operatorlarimiz tez orada sizga shu yerning o'zida javob qaytarishadi.\n\n"
        "Suhbatni tugatish uchun pastdagi **❌ Chatni yakunlash** tugmasini bosing."
    )
    await message.answer(text, reply_markup=end_chat_keyboard())

@contact_router.callback_query(F.data == "leave_request")
async def start_live_chat_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ContactState.WAITING_FOR_TEXT)
    text = (
        "👨‍💻 **Operator bilan bog'lanish**\n\n"
        "Siz jonli chatga ulandingiz. Barcha savol va takliflaringizni shu yerda yozishingiz mumkin. "
        "Operatorlarimiz tez orada sizga shu yerning o'zida javob qaytarishadi.\n\n"
        "Suhbatni tugatish uchun pastdagi **❌ Chatni yakunlash** tugmasini bosing."
    )
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=end_chat_keyboard())
    await callback.answer()

@contact_router.message(ContactState.WAITING_FOR_TEXT)
async def process_live_chat_text(message: Message, state: FSMContext, bot: Bot):
    if message.text == "❌ Chatni yakunlash":
        await state.clear()
        return await message.answer("Suhbat yakunlandi. Asosiy menyudasiz:", reply_markup=main_menu_reply_keyboard())
        
    murojaat_text = message.text or message.caption or "Media xabar"
    user_id = message.from_user.id
    phone = await get_user_phone(user_id)
    
    # Generate random ID for database record
    req_id = f"MUR-{random.randint(10000, 99999)}"
    
    db_data = {
        'request_id': req_id,
        'user_id': user_id,
        'phone': phone,
        'message_text': murojaat_text,
        'req_type': 'livechat'
    }
    await save_contact_request(db_data)
    
    # Forward to Admin
    if ADMIN_CHAT_ID:
        try:
            admin_msg = (
                f"👤 Foydalanuvchi: {message.from_user.full_name}\n"
                f"🆔 ID: {user_id}\n"
                f"📞 Tel: {phone}\n\n"
                f"📝 Xabar:\n{murojaat_text}"
            )
            # If user sent photo/document, copy it instead of just text
            if message.photo or message.document or message.video:
                await message.copy_to(chat_id=ADMIN_CHAT_ID, caption=admin_msg)
            else:
                await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg)
        except Exception as e:
            print(f"Error sending message to admin: {e}")
            
    # Do not clear state, keep them in chat

@contact_router.message(F.text == "📝 Murojaat qoldirish")
async def start_murojaat(message: Message, state: FSMContext):
    await state.set_state(MurojaatState.WAITING_FOR_TEXT)
    text = (
        "📝 **Murojaat qoldirish**\n\n"
        "O'z taklif, shikoyat yoki savolingizni shu yerda yozib qoldirishingiz mumkin. "
        "Operatorlarimiz uni ko'rib chiqib, siz bilan bog'lanishadi.\n\n"
        "Bekor qilish va orqaga qaytish uchun quyidagi tugmani bosing."
    )
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    cancel_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="❌ Bekor qilish")]], resize_keyboard=True)
    await message.answer(text, reply_markup=cancel_kb)

@contact_router.message(MurojaatState.WAITING_FOR_TEXT)
async def process_murojaat_text(message: Message, state: FSMContext, bot: Bot):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        return await message.answer("Murojaat yuborish bekor qilindi.", reply_markup=main_menu_reply_keyboard())
        
    murojaat_text = message.text or message.caption or "Media xabar"
    user_id = message.from_user.id
    phone = await get_user_phone(user_id)
    
    req_id = f"MUR-{random.randint(10000, 99999)}"
    
    db_data = {
        'request_id': req_id,
        'user_id': user_id,
        'phone': phone,
        'message_text': murojaat_text,
        'req_type': 'murojaat'
    }
    await save_contact_request(db_data)
    
    if ADMIN_CHAT_ID:
        try:
            admin_msg = (
                f"📩 Yangi Murojaat:\n"
                f"👤 Foydalanuvchi: {message.from_user.full_name}\n"
                f"📞 Tel: {phone}\n\n"
                f"📝 Xabar:\n{murojaat_text}"
            )
            if message.photo or message.document or message.video:
                await message.copy_to(chat_id=ADMIN_CHAT_ID, caption=admin_msg)
            else:
                await bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg)
        except Exception as e:
            print(f"Error sending message to admin: {e}")
            
    await state.clear()
    await message.answer("✅ Murojaatingiz muvaffaqiyatli yuborildi! Tez orada mutaxassislarimiz aloqaga chiqishadi.", reply_markup=main_menu_reply_keyboard())

# Handler for Admin replies
@contact_router.message(F.reply_to_message)
async def admin_reply_handler(message: Message, bot: Bot):
    # Check if the chat is the admin chat
    if str(message.chat.id) != str(ADMIN_CHAT_ID):
        return

    original_text = message.reply_to_message.text or message.reply_to_message.caption
    if original_text and "🆔 ID:" in original_text:
        match = re.search(r"🆔 ID:\s*(\d+)", original_text)
        if match:
            user_id = int(match.group(1))
            reply_text = f"👨‍💻 **Operatordan javob:**\n\n{message.text}"
            try:
                # If admin sends photo, copy it. Else send text
                if message.photo or message.document or message.video:
                    await message.copy_to(chat_id=user_id, caption=reply_text)
                else:
                    await bot.send_message(chat_id=user_id, text=reply_text)
                await message.reply("✅ Javob foydalanuvchiga muvaffaqiyatli yetkazildi.")
            except Exception as e:
                await message.reply(f"❌ Xatolik yuz berdi. Foydalanuvchi botni bloklagan bo'lishi mumkin.\n\n({e})")
