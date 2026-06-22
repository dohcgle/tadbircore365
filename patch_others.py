import re

def patch_file(filepath, replacements):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    for pat, rep in replacements:
        content = re.sub(pat, rep, content)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

# CONTACT.PY
contact_replacements = [
    (r'from bot\.config import ADMIN_CHAT_ID', r'from bot.config import ADMIN_CHAT_ID\nfrom bot.locales import _, _btn, get_lang, BTNS'),
    (r'@contact_router\.message\(F\.text == "💬 Jonli chat"\)', r'@contact_router.message(F.text.in_([BTNS[\'uz\'][\'live_chat\'], BTNS[\'ru\'][\'live_chat\']]))'),
    (r'''text = \([\s\S]*?"👨‍💻 \*\*Operator bilan bog'lanish\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=end_chat_keyboard\(\)\)''', 
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("live_chat_start", lang), reply_markup=end_chat_keyboard(lang))'''),
    
    (r'@contact_router\.message\(F\.text == "❌ Chatni yakunlash"\)', r'@contact_router.message(F.text.in_([BTNS[\'uz\'][\'end_chat\'], BTNS[\'ru\'][\'end_chat\']]))'),
    (r'''await message\.answer\("Suhbat yakunlandi\. Asosiy menyudasiz:", reply_markup=main_menu_reply_keyboard\(\)\)''', 
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("chat_ended", lang), reply_markup=main_menu_reply_keyboard(lang))'''),
    
    (r'@contact_router\.message\(F\.text == "📝 Murojaat qoldirish"\)', r'@contact_router.message(F.text.in_([BTNS[\'uz\'][\'murojaat\'], BTNS[\'ru\'][\'murojaat\']]))'),
    (r'''text = \([\s\S]*?"📝 \*\*Murojaat qoldirish\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=ReplyKeyboardMarkup\([\s\S]*?\)''', 
     r'''lang = await get_lang(message.from_user.id)
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=_btn("cancel", lang))]], resize_keyboard=True)
    await message.answer(_("murojaat_start", lang), reply_markup=kb)'''),
    
    (r'@contact_router\.message\(ContactState\.WAITING_FOR_MESSAGE, F\.text == "❌ Bekor qilish"\)', r'@contact_router.message(ContactState.WAITING_FOR_MESSAGE, F.text.in_([BTNS[\'uz\'][\'cancel\'], BTNS[\'ru\'][\'cancel\']]))'),
    (r'''await message\.answer\("Murojaat yuborish bekor qilindi\.", reply_markup=main_menu_reply_keyboard\(\)\)''', 
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("murojaat_cancelled", lang), reply_markup=main_menu_reply_keyboard(lang))'''),
    
    (r'''await message\.answer\("✅ Murojaatingiz muvaffaqiyatli yuborildi! Tez orada mutaxassislarimiz aloqaga chiqishadi\.", reply_markup=main_menu_reply_keyboard\(\)\)''', 
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("murojaat_sent", lang), reply_markup=main_menu_reply_keyboard(lang))''')
]

patch_file("bot/handlers/contact.py", contact_replacements)

# CALCULATOR.PY
calc_replacements = [
    (r'from bot\.keyboards\.reply import main_menu_reply_keyboard, calculator_rate_keyboard, calculator_term_keyboard', r'from bot.keyboards.reply import main_menu_reply_keyboard, calculator_rate_keyboard, calculator_term_keyboard\nfrom bot.locales import _, _btn, get_lang, BTNS'),
    (r'@calculator_router\.message\(F\.text == "🧮 Kredit kalkulyatori"\)', r'@calculator_router.message(F.text.in_([BTNS[\'uz\'][\'calc\'], BTNS[\'ru\'][\'calc\']]))'),
    (r'''text = \([\s\S]*?"🧮 \*\*Kredit Kalkulyatori\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=calculator_type_keyboard\(\)\)''', 
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("calc_type", lang), reply_markup=calculator_type_keyboard(lang))'''),
    
    (r'''text = \([\s\S]*?"💰 \*\*Kredit summasi\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text\)''', 
     r'''lang = await get_lang(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(_("calc_amount", lang), reply_markup=ReplyKeyboardRemove())'''),
    
    (r'''await message\.answer\("Noto'g'ri qiymat\. Iltimos faqat raqamlar ishlating\."\)''', 
     r'''lang = await get_lang(message.from_user.id)
        await message.answer(_("calc_invalid_amount", lang))'''),
    
    (r'''text = \([\s\S]*?"📈 \*\*Yillik foiz stavkasi\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=calculator_rate_keyboard\(\)\)''', 
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("calc_rate", lang), reply_markup=calculator_rate_keyboard(lang))'''),
    
    (r'''text = \([\s\S]*?"🗓 \*\*Kredit muddati \(oylarda\)\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=calculator_term_keyboard\(\)\)''', 
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("calc_term", lang), reply_markup=calculator_term_keyboard(lang))'''),
    
    (r'''text = \([\s\S]*?"📊 \*\*Kalkulyator natijasi\*\* \(\{calc_type\}\)\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=main_menu_reply_keyboard\(\), parse_mode="Markdown"\)''', 
     r'''lang = await get_lang(message.from_user.id)
    text = _("calc_result", lang).format(
        type=calc_type,
        amount=f"{amount:,.0f}".replace(",", " "),
        rate=rate,
        term=term,
        total=f"{total_payment:,.0f}".replace(",", " "),
        overpay=f"{overpayment:,.0f}".replace(",", " "),
        schedule=schedule_str
    )
    await message.answer(text, reply_markup=main_menu_reply_keyboard(lang), parse_mode="Markdown")''')
]

patch_file("bot/handlers/calculator.py", calc_replacements)

# CABINET.PY
cabinet_replacements = [
    (r'from bot\.database import DATABASE_URL', r'from bot.database import DATABASE_URL\nfrom bot.locales import _, _btn, get_lang, BTNS'),
    (r'@cabinet_router\.message\(F\.text == "👤 Shaxsiy kabinet"\)', r'@cabinet_router.message(F.text.in_([BTNS[\'uz\'][\'cabinet\'], BTNS[\'ru\'][\'cabinet\']]))'),
    (r'''await message\.answer\("👤 \*\*Shaxsiy kabinet\*\*", reply_markup=kb, parse_mode="Markdown"\)''', 
     r'''lang = await get_lang(message.from_user.id)
    title = "👤 **Shaxsiy kabinet**" if lang == 'uz' else "👤 **Личный кабинет**"
    await message.answer(title, reply_markup=kb, parse_mode="Markdown")''')
]

patch_file("bot/handlers/cabinet.py", cabinet_replacements)
