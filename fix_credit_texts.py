import re

with open("bot/handlers/credit.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace hardcoded texts with `_(...)`
replacements = [
    # 2-qadam
    (r'''text_info = \([\s\S]*?f"✅ \*\*Mijoz ma'lumotlari topildi:\*\*\n"[\s\S]*?\)[\s]*await state\.set_state\(CreditState\.ASK_AMOUNT\)[\s]*await message\.answer\(text_info, reply_markup=amount_keyboard\(\), parse_mode="Markdown"\)''',
     r'''lang = await get_lang(message.from_user.id)
    text_info = _("credit_step2_base", lang).format(
        type=business.get('type', ''),
        name=business.get('name', ''),
        bank=business.get('bank', ''),
        account=business.get('account', '')
    )
    await state.set_state(CreditState.ASK_AMOUNT)
    await message.answer(text_info, reply_markup=amount_keyboard(lang), parse_mode="Markdown")'''),

    # 3-qadam callback
    (r'''text = \([\s\S]*?"🗓 \*\*3-qadam: Kredit muddati\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=term_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
    await callback.message.edit_text(_("credit_step3", lang), reply_markup=term_keyboard(lang))'''),
    
    # 3-qadam message
    (r'''text = \([\s\S]*?"🗓 \*\*3-qadam: Kredit muddati\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=term_keyboard\(\)\)''',
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("credit_step3", lang), reply_markup=term_keyboard(lang))'''),

    # 4-qadam callback
    (r'''text = \([\s\S]*?"🎯 \*\*4-qadam: Kredit maqsadi\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=purpose_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
    await callback.message.edit_text(_("credit_step4", lang), reply_markup=purpose_keyboard(lang))'''),
    
    # 4-qadam message
    (r'''text = \([\s\S]*?"🎯 \*\*4-qadam: Kredit maqsadi\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=purpose_keyboard\(\)\)''',
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("credit_step4", lang), reply_markup=purpose_keyboard(lang))'''),

    # 5-qadam callback
    (r'''text = \([\s\S]*?"🛡 \*\*5-qadam: Ta'minot \(Garov\)\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=collateral_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
    await callback.message.edit_text(_("credit_step5", lang), reply_markup=collateral_keyboard(lang))'''),

    # 5-qadam photo
    (r'''text = \([\s\S]*?f"📸 \*\*Ta'minot rasmi\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.delete\(\)[\s]*await callback\.message\.answer\(text, reply_markup=skip_photo_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(_("credit_step_photo1", lang).format(collateral=collateral), reply_markup=skip_photo_keyboard(lang))'''),

    # 6-qadam banks
    (r'''text = \([\s\S]*?"🏦 \*\*6-qadam: Banklarni tanlash\*\*\n\n"[\s\S]*?\)[\s]*await message\.answer\(text, reply_markup=banks_keyboard\(recommended_banks\)\)''',
     r'''lang = await get_lang(message.from_user.id)
    await message.answer(_("credit_step6", lang), reply_markup=banks_keyboard(recommended_banks, lang))'''),

    # Banks selection finish
    (r'''banks_text = "\\n"\.join\(\[f"🏦 \*\*\{i\+1\}\. \{b\}\*\*" for i, b in enumerate\(recommended_banks\)\]\)[\s]*selected_bank_display = f"Barcha tavsiya etilgan banklar:\\n\{banks_text\}"''',
     r'''lang = await get_lang(callback.from_user.id)
        banks_text = "\n".join([f"🏦 **{i+1}. {b}**" for i, b in enumerate(recommended_banks)])
        selected_bank_display = _("banks_all_display", lang).format(banks_text=banks_text)'''),
    
    (r'''text = \([\s\S]*?f"🎉 \*\*Arizangiz muvaffaqiyatli qabul qilindi!\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.delete\(\)[\s]*await callback\.message\.answer\(text, reply_markup=main_menu_reply_keyboard\(\), parse_mode="Markdown"\)''',
     r'''lang = await get_lang(callback.from_user.id)
    text = _("credit_success", lang).format(
        amount=amount,
        term=term,
        purpose=purpose,
        collateral=collateral,
        req_id=req_id,
        selected_bank_display=selected_bank_display
    )
    
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=main_menu_reply_keyboard(lang), parse_mode="Markdown")'''),

    # Nav Back 1-qadam
    (r'''text = \([\s\S]*?"🆔 \*\*1-qadam: Mijozni identifikatsiya qilish\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.delete\(\)[\s]*await callback\.message\.answer\(text, reply_markup=ReplyKeyboardRemove\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.delete()
        await callback.message.answer(_("credit_step1", lang), reply_markup=ReplyKeyboardRemove())'''),

    # Nav Back 2-qadam
    (r'''text_info = \([\s\S]*?f"✅ \*\*Mijoz ma'lumotlari topildi:\*\*\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text_info, reply_markup=amount_keyboard\(\), parse_mode="Markdown"\)''',
     r'''lang = await get_lang(callback.from_user.id)
        text_info = _("credit_step2_base", lang).format(
            type=business.get('type', ''),
            name=business.get('name', ''),
            bank=business.get('bank', ''),
            account=business.get('account', '')
        )
        await callback.message.edit_text(text_info, reply_markup=amount_keyboard(lang), parse_mode="Markdown")'''),

    # Nav Back 3-qadam
    (r'''text = \([\s\S]*?"🗓 \*\*3-qadam: Kredit muddati\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=term_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.edit_text(_("credit_step3", lang), reply_markup=term_keyboard(lang))'''),
    
    # Nav Back 4-qadam
    (r'''text = \([\s\S]*?"🎯 \*\*4-qadam: Kredit maqsadi\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=purpose_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.edit_text(_("credit_step4", lang), reply_markup=purpose_keyboard(lang))'''),
    
    # Nav Back 5-qadam
    (r'''text = \([\s\S]*?"🛡 \*\*5-qadam: Ta'minot \(Garov\)\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=collateral_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.edit_text(_("credit_step5", lang), reply_markup=collateral_keyboard(lang))'''),

    # Nav Back Photo
    (r'''text = \([\s\S]*?f"📸 \*\*Ta'minot rasmi\*\*\n\n"[\s\S]*?\)[\s]*await callback\.message\.edit_text\(text, reply_markup=skip_photo_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.edit_text(_("credit_step_photo1", lang).format(collateral=collateral), reply_markup=skip_photo_keyboard(lang))'''),

    # Nav Next Alerts
    (r'''return await callback\.answer\("⚠️ Iltimos, avval tanlovni amalga oshiring!", show_alert=True\)''',
     r'''lang = await get_lang(callback.from_user.id)
            return await callback.answer(_("alert_select_first", lang), show_alert=True)'''),
    
    (r'''return await callback\.answer\("⚠️ Iltimos, rasm yuklang yoki 'Rasmsiz davom etish' ni tanlang!", show_alert=True\)''',
     r'''lang = await get_lang(callback.from_user.id)
            return await callback.answer(_("alert_upload_photo", lang), show_alert=True)'''),
    
    (r'''return await callback\.answer\("⚠️ Iltimos, ro'yxatdan banklardan birini tanlang!", show_alert=True\)''',
     r'''lang = await get_lang(callback.from_user.id)
        return await callback.answer(_("alert_select_bank", lang), show_alert=True)'''),

    # Nav Next steps
    (r'''text = "🗓 \*\*3-qadam: Kredit muddati\*\*\n\nQarzni qancha muddatda qaytarishni rejalashtiryapsiz\?"[\s]*await callback\.message\.edit_text\(text, reply_markup=term_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.edit_text(_("credit_step3", lang), reply_markup=term_keyboard(lang))'''),
    
    (r'''text = "🎯 \*\*4-qadam: Kredit maqsadi\*\*\n\nKredit mablag'larini qanday maqsadda ishlatmoqchisiz\?"[\s]*await callback\.message\.edit_text\(text, reply_markup=purpose_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.edit_text(_("credit_step4", lang), reply_markup=purpose_keyboard(lang))'''),
    
    (r'''text = "🛡 \*\*5-qadam: Ta'minot \(Garov\)\*\*\n\nQanday ta'minot turini taqdim eta olasiz\?"[\s]*await callback\.message\.edit_text\(text, reply_markup=collateral_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.edit_text(_("credit_step5", lang), reply_markup=collateral_keyboard(lang))'''),
    
    (r'''text = f"📸 \*\*Ta'minot rasmi\*\*\n\nSiz \*\*\{collateral\}\*\* turini tanladingiz\. Iltimos, mulk rasmini yoki hujjatini yuklang\.\nYoki rasmsiz davom etishingiz mumkin:"[\s]*await callback\.message\.edit_text\(text, reply_markup=skip_photo_keyboard\(\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.edit_text(_("credit_step_photo1", lang).format(collateral=collateral), reply_markup=skip_photo_keyboard(lang))'''),
    
    (r'''text = "🏦 \*\*6-qadam: Banklarni tanlash\*\*\n\nSizning so'rovingizga mos keladigan banklar topildi\. Qaysi bankka arizangizni yuboraylik\?"[\s]*await callback\.message\.edit_text\(text, reply_markup=banks_keyboard\(recommended_banks\)\)''',
     r'''lang = await get_lang(callback.from_user.id)
        await callback.message.edit_text(_("credit_step6", lang), reply_markup=banks_keyboard(recommended_banks, lang))'''),
]

for pat, rep in replacements:
    content = re.sub(pat, rep, content)

with open("bot/handlers/credit.py", "w", encoding="utf-8") as f:
    f.write(content)

# We also need to check if bot/locales.py has the correct strings
