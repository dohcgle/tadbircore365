import re

with open("bot/handlers/contact.py", "r", encoding="utf-8") as f:
    content = f.read()

replacements = [
    (r'''@contact_router\.message\(F\.text\.in_\(\[BTNS\['uz'\]\['live_chat'\], BTNS\['ru'\]\['live_chat'\]\]\)\)
async def start_live_chat\(message: Message, state: FSMContext\):
    await state\.set_state\(ContactState\.WAITING_FOR_TEXT\)
    text = \(
        "👨‍💻 \*\*Operator bilan bog'lanish\*\*\\n\\n"
        "Siz jonli chatga ulandingiz\. Barcha savol va takliflaringizni shu yerda yozishingiz mumkin\. "
        "Operatorlarimiz tez orada sizga shu yerning o'zida javob qaytarishadi\.\\n\\n"
        "Suhbatni tugatish uchun pastdagi \*\*❌ Chatni yakunlash\*\* tugmasini bosing\."
    \)
    await message\.answer\(text, reply_markup=end_chat_keyboard\(\)\)''',
     r'''@contact_router.message(F.text.in_([BTNS['uz']['live_chat'], BTNS['ru']['live_chat']]))
async def start_live_chat(message: Message, state: FSMContext):
    await state.set_state(ContactState.WAITING_FOR_TEXT)
    lang = await get_lang(message.from_user.id)
    await message.answer(_("live_chat_start", lang), reply_markup=end_chat_keyboard(lang))'''),

    (r'''@contact_router\.callback_query\(F\.data == "leave_request"\)
async def start_live_chat_callback\(callback: CallbackQuery, state: FSMContext\):
    await state\.set_state\(ContactState\.WAITING_FOR_TEXT\)
    text = \(
        "👨‍💻 \*\*Operator bilan bog'lanish\*\*\\n\\n"
        "Siz jonli chatga ulandingiz\. Barcha savol va takliflaringizni shu yerda yozishingiz mumkin\. "
        "Operatorlarimiz tez orada sizga shu yerning o'zida javob qaytarishadi\.\\n\\n"
        "Suhbatni tugatish uchun pastdagi \*\*❌ Chatni yakunlash\*\* tugmasini bosing\."
    \)
    await callback\.message\.delete\(\)
    await callback\.message\.answer\(text, reply_markup=end_chat_keyboard\(\)\)''',
     r'''@contact_router.callback_query(F.data == "leave_request")
async def start_live_chat_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ContactState.WAITING_FOR_TEXT)
    lang = await get_lang(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(_("live_chat_start", lang), reply_markup=end_chat_keyboard(lang))'''),

    (r'''@contact_router\.message\(F\.text\.in_\(\[BTNS\['uz'\]\['murojaat'\], BTNS\['ru'\]\['murojaat'\]\]\)\)
async def start_murojaat\(message: Message, state: FSMContext\):
    await state\.set_state\(MurojaatState\.WAITING_FOR_TEXT\)
    text = \(
        "📝 \*\*Murojaat qoldirish\*\*\\n\\n"
        "O'z taklif, shikoyat yoki savolingizni shu yerda yozib qoldirishingiz mumkin\. "
        "Operatorlarimiz uni ko'rib chiqib, siz bilan bog'lanishadi\.\\n\\n"
        "Bekor qilish va orqaga qaytish uchun quyidagi tugmani bosing\."
    \)
    from aiogram\.types import ReplyKeyboardMarkup, KeyboardButton
    cancel_kb = ReplyKeyboardMarkup\(keyboard=\[\[KeyboardButton\(text="❌ Bekor qilish"\)\]\], resize_keyboard=True\)
    await message\.answer\(text, reply_markup=cancel_kb\)''',
     r'''@contact_router.message(F.text.in_([BTNS['uz']['murojaat'], BTNS['ru']['murojaat']]))
async def start_murojaat(message: Message, state: FSMContext):
    await state.set_state(MurojaatState.WAITING_FOR_TEXT)
    lang = await get_lang(message.from_user.id)
    
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    cancel_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=_btn("cancel", lang))]], resize_keyboard=True)
    await message.answer(_("murojaat_start", lang), reply_markup=cancel_kb)'''),
    
    (r'''reply_markup=end_chat_keyboard\(\)''', r'''reply_markup=end_chat_keyboard(lang)''')
]

for pat, rep in replacements:
    content = re.sub(pat, rep, content)

with open("bot/handlers/contact.py", "w", encoding="utf-8") as f:
    f.write(content)
