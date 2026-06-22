import re

with open("bot/handlers/credit.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add imports
content = content.replace("from bot.config import ADMIN_CHAT_ID", 
                          "from bot.config import ADMIN_CHAT_ID\nfrom bot.locales import _, _btn, get_lang, BTNS")

# 1. start_credit filter
content = re.sub(
    r'@credit_router\.message\(F\.text == "🏢 Kredit tanlash"\)',
    r"@credit_router.message(F.text.in_([BTNS['uz']['credit'], BTNS['ru']['credit']]))",
    content
)

content = re.sub(
    r'async def start_credit\(message: Message, state: FSMContext\):([\s\S]*?)text = \([\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=ReplyKeyboardRemove\(\)\)',
    r'''async def start_credit(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.set_state(CreditState.ASK_INN)
    await message.answer(_("credit_step1", lang), reply_markup=ReplyKeyboardRemove())''',
    content
)

content = re.sub(
    r'await message\.answer\("Siz noto\'g\'ri kiritdingiz, iltimos to\'g\'ri kiriting"\)',
    r'''lang = await get_lang(message.from_user.id)
        await message.answer(_("credit_invalid_inn", lang))''',
    content
)

# Step 2
content = re.sub(
    r'''text_info = \([\s\S]*?f"✅ \*\*Mijoz ma'lumotlari topildi:\*\*\n"[\s\S]*?\)[\s]*await state\.set_state\(CreditState\.ASK_AMOUNT\)[\s]*await message\.answer\(text_info, reply_markup=amount_keyboard\(\), parse_mode="Markdown"\)''',
    r'''lang = await get_lang(message.from_user.id)
    text_info = _("credit_step2_base", lang).format(
        type=business['type'],
        name=business['name'],
        bank=business['bank'],
        account=business['account']
    )
    await state.set_state(CreditState.ASK_AMOUNT)
    await message.answer(text_info, reply_markup=amount_keyboard(lang), parse_mode="Markdown")''',
    content
)

# process_amount_callback
content = re.sub(
    r'''text = \([\s\S]*?"🗓 \*\*3-qadam: Kredit muddati\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=term_keyboard\(\)\)''',
    r'''lang = await get_lang(callback.from_user.id)
    await callback.message.edit_text(_("credit_step3", lang), reply_markup=term_keyboard(lang))''',
    content
)

content = re.sub(
    r'''await message\.answer\("⚠️ Iltimos, summani faqat raqamlarda kiriting yoki tugmalardan foydalaning:", reply_markup=amount_keyboard\(\)\)''',
    r'''lang = await get_lang(message.from_user.id)
        await message.answer(_("calc_invalid_amount", lang), reply_markup=amount_keyboard(lang))''',
    content
)

content = re.sub(
    r'''text = \([\s\S]*?"🗓 \*\*3-qadam: Kredit muddati\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=term_keyboard\(\)\)''',
    r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("credit_step3", lang), reply_markup=term_keyboard(lang))''',
    content
)

# purpose
content = re.sub(
    r'''text = \([\s\S]*?"🎯 \*\*4-qadam: Kredit maqsadi\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=purpose_keyboard\(\)\)''',
    r'''lang = await get_lang(callback.from_user.id)
    await callback.message.edit_text(_("credit_step4", lang), reply_markup=purpose_keyboard(lang))''',
    content
)

content = re.sub(
    r'''text = \([\s\S]*?"🎯 \*\*4-qadam: Kredit maqsadi\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=purpose_keyboard\(\)\)''',
    r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("credit_step4", lang), reply_markup=purpose_keyboard(lang))''',
    content
)

# collateral
content = re.sub(
    r'''text = \([\s\S]*?"🛡 \*\*5-qadam: Ta'minot \(Garov\)\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=collateral_keyboard\(\)\)''',
    r'''lang = await get_lang(callback.from_user.id)
    await callback.message.edit_text(_("credit_step5", lang), reply_markup=collateral_keyboard(lang))''',
    content
)

# photo
content = re.sub(
    r'''text = \([\s\S]*?f"📸 \*\*Ta'minot rasmi\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.delete\(\)[\s]*await callback\.message\.answer\(text, reply_markup=skip_photo_keyboard\(\)\)''',
    r'''lang = await get_lang(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(_("credit_step_photo1", lang), reply_markup=skip_photo_keyboard(lang))''',
    content
)

content = re.sub(
    r'''text = \([\s\S]*?"🏦 \*\*6-qadam: Banklarni tanlash\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=banks_keyboard\(recommended_banks\)\)''',
    r'''lang = await get_lang(message.from_user.id)
    await state.set_state(CreditState.ASK_BANKS)
    await message.answer(_("credit_step6", lang), reply_markup=banks_keyboard(recommended_banks, lang))''',
    content
)

content = re.sub(
    r'''text = \([\s\S]*?"🏦 \*\*6-qadam: Banklarni tanlash\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=banks_keyboard\(recommended_banks\)\)''',
    r'''lang = await get_lang(callback.from_user.id)
    await state.set_state(CreditState.ASK_BANKS)
    await callback.message.edit_text(_("credit_step6", lang), reply_markup=banks_keyboard(recommended_banks, lang))''',
    content
)

# success
content = re.sub(
    r'''banks_text = "\\n"\.join\(\[f"{i}\. \{b\}" for i, b in enumerate\(banks, 1\)\]\)[\s]*selected_bank_display = f"Barcha tavsiya etilgan banklar:\\n\{banks_text\}"''',
    r'''lang = await get_lang(user_id)
    banks_text = "\\n".join([f"{i}. {b}" for i, b in enumerate(banks, 1)])
    selected_bank_display = _("banks_all_display", lang).format(banks_text=banks_text)''',
    content
)

content = re.sub(
    r'''text = \([\s\S]*?"🎉 \*\*Arizangiz muvaffaqiyatli qabul qilindi!\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=main_menu_reply_keyboard\(\), parse_mode="Markdown"\)''',
    r'''text = _("credit_success", lang).format(
        amount=amount,
        term=term,
        purpose=purpose,
        collateral=collateral,
        req_id=req_id,
        selected_bank_display=selected_bank_display
    )
    await message.answer(text, reply_markup=main_menu_reply_keyboard(lang), parse_mode="Markdown")''',
    content
)

with open("bot/handlers/credit.py", "w", encoding="utf-8") as f:
    f.write(content)
