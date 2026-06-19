import json
import os
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.states.credit_state import CreditState
from bot.database import save_credit_request, get_user_phone
from bot.keyboards.reply import request_contact_keyboard, main_menu_reply_keyboard
from bot.keyboards.inline import (
    amount_keyboard,
    term_keyboard,
    purpose_keyboard,
    collateral_keyboard,
    skip_photo_keyboard,
    banks_keyboard,
    operator_accept_keyboard
)
from bot.config import ADMIN_CHAT_ID

credit_router = Router()

def get_mock_business(inn: str):
    file_path = "data/mock_businesses.json"
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        if item.get("inn_jshshir") == inn:
            return item
    return None

ALL_BANKS = [
    "Agro Bank", "Aloqa Bank", "Asaka Bank", "Biznesni Rivojlantirish Banki",
    "Mikrokredit Bank", "O‘zmilliybank (NBU)", "Sanoat Qurilish Bank", "Turon Bank",
    "Xalq Bank", "Anor Bank", "Asia Alliance Bank", "Davr Bank", "Garant Bank",
    "Hamkor Bank", "Infin Bank", "Ipak Yuli Bank", "Kapital Bank", "Orient Finans Bank",
    "TBC Bank", "Tenge Bank", "Trast Bank", "Universal Bank"
]

@credit_router.message(F.text == "🏢 Kredit tanlash")
async def start_credit(message: Message, state: FSMContext):
    await state.set_state(CreditState.ASK_INN)
    text = (
        "🆔 **1-qadam: Mijozni identifikatsiya qilish**\n\n"
        "Iltimos, o'zingizning INN (9 xonali) yoki JSHSHIR (14 xonali) raqamingizni kiriting:"
    )
    await message.answer(text, reply_markup=ReplyKeyboardRemove())

@credit_router.message(CreditState.ASK_INN)
async def process_inn(message: Message, state: FSMContext):
    inn = message.text.strip()
    if not inn.isdigit() or len(inn) not in [9, 14]:
        await message.answer("Siz noto'g'ri kiritdingiz, iltimos to'g'ri kiriting")
        return

    business = get_mock_business(inn)
    if not business:
        await message.answer("Siz noto'g'ri kiritdingiz, iltimos to'g'ri kiriting")
        return

    # Ma'lumotlarni saqlaymiz
    await state.update_data(business_info=business)
    
    text_info = (
        f"✅ **Mijoz ma'lumotlari topildi:**\n"
        f"🏢 {business['type']} - **{business['name']}**\n"
        f"🏦 Bank: **{business['bank']}**\n"
        f"💳 H/r: **{business['account']}**\n\n"
        "💰 **2-qadam: Kredit summasi**\n\n"
        "Sizga qancha miqdorda kredit zarur? Quyidagi variantlardan birini tanlang yoki "
        "summani raqamlar bilan kiriting (masalan: 120 000 000):"
    )
    await state.set_state(CreditState.ASK_AMOUNT)
    await message.answer(text_info, reply_markup=amount_keyboard(), parse_mode="Markdown")

@credit_router.callback_query(CreditState.ASK_AMOUNT, F.data.startswith("amount_"))
async def process_amount_callback(callback: CallbackQuery, state: FSMContext):
    val = callback.data.replace("amount_", "")
    amount_map = {
        "50m": "50 mln so'mgacha",
        "50-100m": "50-100 mln so'm",
        "100-500m": "100-500 mln so'm",
        "500m_plus": "500 mln so'mdan ko'p"
    }
    amount = amount_map.get(val, val)
    await state.update_data(amount=amount)
    
    await state.set_state(CreditState.ASK_TERM)
    text = (
        "🗓 **3-qadam: Kredit muddati**\n\n"
        "Qarzni qancha muddatda qaytarishni rejalashtiryapsiz?"
    )
    await callback.message.edit_text(text, reply_markup=term_keyboard())
    await callback.answer()

@credit_router.message(CreditState.ASK_AMOUNT)
async def process_amount_message(message: Message, state: FSMContext):
    if not message.text.replace(" ", "").isdigit():
        await message.answer("⚠️ Iltimos, summani faqat raqamlarda kiriting yoki tugmalardan foydalaning:", reply_markup=amount_keyboard())
        return
    
    amount_val = int(message.text.replace(" ", ""))
    amount_str = f"{amount_val:,} so'm".replace(",", " ")
    await state.update_data(amount=amount_str)
    
    await state.set_state(CreditState.ASK_TERM)
    text = (
        "🗓 **3-qadam: Kredit muddati**\n\n"
        "Qarzni qancha muddatda qaytarishni rejalashtiryapsiz?"
    )
    await message.answer(text, reply_markup=term_keyboard())

@credit_router.callback_query(CreditState.ASK_TERM, F.data.startswith("term_"))
async def process_term_callback(callback: CallbackQuery, state: FSMContext):
    term = callback.data.replace("term_", "")
    await state.update_data(term=f"{term} oy")
    
    await state.set_state(CreditState.ASK_PURPOSE)
    text = (
        "🎯 **4-qadam: Kredit maqsadi**\n\n"
        "Kredit mablag'larini qanday maqsadda ishlatmoqchisiz?"
    )
    await callback.message.edit_text(text, reply_markup=purpose_keyboard())
    await callback.answer()

@credit_router.message(CreditState.ASK_TERM)
async def process_term_message(message: Message, state: FSMContext):
    await state.update_data(term=f"{message.text} oy")
    
    await state.set_state(CreditState.ASK_PURPOSE)
    text = (
        "🎯 **4-qadam: Kredit maqsadi**\n\n"
        "Kredit mablag'larini qanday maqsadda ishlatmoqchisiz?"
    )
    await message.answer(text, reply_markup=purpose_keyboard())

@credit_router.callback_query(CreditState.ASK_PURPOSE, F.data.startswith("purpose_"))
async def process_purpose_callback(callback: CallbackQuery, state: FSMContext):
    # Mapping for purpose
    purpose_map = {
        "purpose_1": "Mikrokredit 100 mln gacha",
        "purpose_2": "Kundalik xarajatlar uchun kredit",
        "purpose_3": "Biznesni rivojlantirish uchun kredit",
        "purpose_4": "Yangi boshlagan subyektlar uchun kredit",
        "purpose_5": "Biznes uchun avtokredit",
        "purpose_6": "Overdraft",
        "purpose_7": "Biznes uchun ipoteka/qurilish krediti",
        "purpose_8": "Yashil kredit",
        "purpose_9": "Buyurtmalarni moliyalashtirish",
        "purpose_10": "Yosh tadbirkorlar uchun kredit",
        "purpose_11": "Xotin-qizlar tadbirkorligi uchun kredit",
        "purpose_12": "Universal kredit"
    }
    purpose = purpose_map.get(callback.data, "Boshqa")
    await state.update_data(purpose=purpose)
    
    await state.set_state(CreditState.ASK_COLLATERAL)
    text = (
        "🛡 **5-qadam: Ta'minot (Garov)**\n\n"
        "Qanday ta'minot turini taqdim eta olasiz?"
    )
    await callback.message.edit_text(text, reply_markup=collateral_keyboard())
    await callback.answer()

@credit_router.callback_query(CreditState.ASK_COLLATERAL, F.data.startswith("collateral_"))
async def process_collateral_callback(callback: CallbackQuery, state: FSMContext):
    col_map = {
        "collateral_auto": "Avtomobil",
        "collateral_realestate": "Ko'chmas mulk",
        "collateral_technics": "Texnika"
    }
    collateral = col_map.get(callback.data, "Boshqa")
    await state.update_data(collateral=collateral)
    
    await state.set_state(CreditState.ASK_COLLATERAL_PHOTO)
    text = (
        f"📸 **Ta'minot rasmi**\n\n"
        f"Siz **{collateral}** turini tanladingiz. Iltimos, mulk rasmini yoki hujjatini yuklang.\n"
        "Yoki rasmsiz davom etishingiz mumkin:"
    )
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=skip_photo_keyboard())
    await callback.answer()

@credit_router.callback_query(CreditState.ASK_COLLATERAL_PHOTO, F.data == "skip_photo")
async def skip_photo_callback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(has_photo=False)
    await ask_for_banks(callback.message, state)
    await callback.answer()

@credit_router.message(CreditState.ASK_COLLATERAL_PHOTO, F.photo | F.document)
async def process_collateral_photo(message: Message, state: FSMContext):
    await state.update_data(has_photo=True)
    await ask_for_banks(message, state)

async def ask_for_banks(message: Message, state: FSMContext):
    # Select 3 random banks
    recommended_banks = random.sample(ALL_BANKS, 3)
    await state.update_data(recommended_banks=recommended_banks)
    
    await state.set_state(CreditState.SELECT_BANKS)
    text = (
        "🏦 **6-qadam: Banklarni tanlash**\n\n"
        "Sizning so'rovingizga mos keladigan banklar topildi. Qaysi bankka arizangizni yuboraylik?"
    )
    await message.answer(text, reply_markup=banks_keyboard(recommended_banks))

@credit_router.callback_query(CreditState.SELECT_BANKS, F.data.startswith("bank_"))
async def process_bank_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    recommended_banks = data.get("recommended_banks", [])
    
    if callback.data == "bank_all":
        selected_bank = "Barcha tavsiya etilgan banklar"
        banks_text = ", ".join([f"{i+1}. {b}" for i, b in enumerate(recommended_banks)])
        selected_bank_display = f"Barcha tavsiya etilgan banklar:\n{banks_text}"
    else:
        idx = int(callback.data.split("_")[1])
        selected_bank = recommended_banks[idx]
        selected_bank_display = f"{selected_bank}"
        
    await state.update_data(selected_bank=selected_bank)
    
    # Skip contact and finish directly
    user_id = callback.from_user.id
    phone = await get_user_phone(user_id)
    
    amount = data.get("amount", "Kiritilmagan")
    term = data.get("term", "Kiritilmagan")
    purpose = data.get("purpose", "Kiritilmagan")
    collateral = data.get("collateral", "Kiritilmagan")
    business = data.get("business_info", {})
    
    # Generate random ID
    req_id = f"AR-{random.randint(10000, 99999)}"
    
    db_data = {
        'request_id': req_id,
        'user_id': user_id,
        'phone': phone,
        'inn_jshshir': business.get('inn_jshshir', ''),
        'business_type': business.get('type', ''),
        'business_name': business.get('name', ''),
        'amount': amount,
        'term': term,
        'purpose': purpose,
        'collateral': collateral,
        'selected_bank': selected_bank
    }
    await save_credit_request(db_data)
    
    # Adminga xabar yuborish
    if ADMIN_CHAT_ID:
        nomalum_text = "Noma'lum"
        admin_text = (
            f"🔔 **Yangi Kredit Arizasi!**\n\n"
            f"🆔 **ID:** {req_id}\n"
            f"👤 **Mijoz (Tel):** {phone}\n"
            f"🏢 **Biznes nomi:** {business.get('name', nomalum_text)}\n"
            f"💰 **Summa:** {amount}\n"
            f"🗓 **Muddat:** {term}\n"
            f"🏦 **Tanlangan bank:** {selected_bank_display}\n"
            f"❓ **Maqsad:** {purpose}\n"
            f"🛡 **Ta'minot:** {collateral}\n"
        )
        try:
            await callback.message.bot.send_message(
                chat_id=ADMIN_CHAT_ID, 
                text=admin_text, 
                reply_markup=operator_accept_keyboard(req_id),
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Failed to send admin notification: {e}")

    text = (
        f"🎉 **Arizangiz muvaffaqiyatli qabul qilindi!**\n\n"
        f"**Kredit ariza detalizatsiyasi:**\n"
        f"🔹 **Kredit summasi:** {amount}\n"
        f"🔹 **Kredit muddati:** {term}\n"
        f"🔹 **Kredit olish maqsadi:** {purpose}\n"
        f"🔹 **Ta'minot turi:** {collateral}\n\n"
        f"✅ Sizning arizangiz 🆔 **{req_id}** raqami bilan ro'yxatga olindi.\n"
        f"🏦 **{selected_bank_display}** ga yuborildi. Bank vakillari tez orada siz bilan aloqaga chiqadi!"
    )
    
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=main_menu_reply_keyboard(), parse_mode="Markdown")
    await state.clear()
    await callback.answer()

@credit_router.callback_query(F.data == "nav_back")
async def nav_back_handler(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()
    
    if current_state == CreditState.ASK_AMOUNT.state:
        # Orqaga qaytish: ASK_INN ga
        await state.set_state(CreditState.ASK_INN)
        text = (
            "🆔 **1-qadam: Mijozni identifikatsiya qilish**\n\n"
            "Iltimos, o'zingizning INN (9 xonali) yoki JSHSHIR (14 xonali) raqamingizni kiriting:"
        )
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=ReplyKeyboardRemove())
        
    elif current_state == CreditState.ASK_TERM.state:
        # Orqaga qaytish: ASK_AMOUNT
        await state.set_state(CreditState.ASK_AMOUNT)
        business = data.get("business_info", {})
        text_info = (
            f"✅ **Mijoz ma'lumotlari topildi:**\n"
            f"🏢 {business.get('type', '')} - **{business.get('name', '')}**\n"
            f"🏦 Bank: **{business.get('bank', '')}**\n"
            f"💳 H/r: **{business.get('account', '')}**\n\n"
            "💰 **2-qadam: Kredit summasi**\n\n"
            "Sizga qancha miqdorda kredit zarur? Quyidagi variantlardan birini tanlang yoki "
            "summani raqamlar bilan kiriting (masalan: 100000000):"
        )
        await callback.message.edit_text(text_info, reply_markup=amount_keyboard(), parse_mode="Markdown")
        
    elif current_state == CreditState.ASK_PURPOSE.state:
        await state.set_state(CreditState.ASK_TERM)
        text = (
            "🗓 **3-qadam: Kredit muddati**\n\n"
            "Qarzni qancha muddatda qaytarishni rejalashtiryapsiz?"
        )
        await callback.message.edit_text(text, reply_markup=term_keyboard())
        
    elif current_state == CreditState.ASK_COLLATERAL.state:
        await state.set_state(CreditState.ASK_PURPOSE)
        text = (
            "🎯 **4-qadam: Kredit maqsadi**\n\n"
            "Kredit mablag'larini qanday maqsadda ishlatmoqchisiz?"
        )
        await callback.message.edit_text(text, reply_markup=purpose_keyboard())
        
    elif current_state == CreditState.ASK_COLLATERAL_PHOTO.state:
        await state.set_state(CreditState.ASK_COLLATERAL)
        text = (
            "🛡 **5-qadam: Ta'minot (Garov)**\n\n"
            "Qanday ta'minot turini taqdim eta olasiz?"
        )
        await callback.message.edit_text(text, reply_markup=collateral_keyboard())
        
    elif current_state == CreditState.SELECT_BANKS.state:
        await state.set_state(CreditState.ASK_COLLATERAL_PHOTO)
        collateral = data.get("collateral", "Boshqa")
        text = (
            f"📸 **Ta'minot rasmi**\n\n"
            f"Siz **{collateral}** turini tanladingiz. Iltimos, mulk rasmini yoki hujjatini yuklang.\n"
            "Yoki rasmsiz davom etishingiz mumkin:"
        )
        await callback.message.edit_text(text, reply_markup=skip_photo_keyboard())
        
    await callback.answer()

@credit_router.callback_query(F.data == "nav_next")
async def nav_next_handler(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    data = await state.get_data()
    
    if current_state == CreditState.ASK_AMOUNT.state:
        if "amount" not in data:
            return await callback.answer("⚠️ Iltimos, avval tanlovni amalga oshiring!", show_alert=True)
        await state.set_state(CreditState.ASK_TERM)
        text = "🗓 **3-qadam: Kredit muddati**\n\nQarzni qancha muddatda qaytarishni rejalashtiryapsiz?"
        await callback.message.edit_text(text, reply_markup=term_keyboard())
        
    elif current_state == CreditState.ASK_TERM.state:
        if "term" not in data:
            return await callback.answer("⚠️ Iltimos, avval tanlovni amalga oshiring!", show_alert=True)
        await state.set_state(CreditState.ASK_PURPOSE)
        text = "🎯 **4-qadam: Kredit maqsadi**\n\nKredit mablag'larini qanday maqsadda ishlatmoqchisiz?"
        await callback.message.edit_text(text, reply_markup=purpose_keyboard())
        
    elif current_state == CreditState.ASK_PURPOSE.state:
        if "purpose" not in data:
            return await callback.answer("⚠️ Iltimos, avval tanlovni amalga oshiring!", show_alert=True)
        await state.set_state(CreditState.ASK_COLLATERAL)
        text = "🛡 **5-qadam: Ta'minot (Garov)**\n\nQanday ta'minot turini taqdim eta olasiz?"
        await callback.message.edit_text(text, reply_markup=collateral_keyboard())
        
    elif current_state == CreditState.ASK_COLLATERAL.state:
        if "collateral" not in data:
            return await callback.answer("⚠️ Iltimos, avval tanlovni amalga oshiring!", show_alert=True)
        await state.set_state(CreditState.ASK_COLLATERAL_PHOTO)
        collateral = data.get("collateral", "Boshqa")
        text = f"📸 **Ta'minot rasmi**\n\nSiz **{collateral}** turini tanladingiz. Iltimos, mulk rasmini yoki hujjatini yuklang.\nYoki rasmsiz davom etishingiz mumkin:"
        await callback.message.edit_text(text, reply_markup=skip_photo_keyboard())
        
    elif current_state == CreditState.ASK_COLLATERAL_PHOTO.state:
        if "has_photo" not in data:
            return await callback.answer("⚠️ Iltimos, rasm yuklang yoki 'Rasmsiz davom etish' ni tanlang!", show_alert=True)
        recommended_banks = data.get("recommended_banks")
        if not recommended_banks:
            import random
            recommended_banks = random.sample(ALL_BANKS, 3)
            await state.update_data(recommended_banks=recommended_banks)
            
        await state.set_state(CreditState.SELECT_BANKS)
        text = "🏦 **6-qadam: Banklarni tanlash**\n\nSizning so'rovingizga mos keladigan banklar topildi. Qaysi bankka arizangizni yuboraylik?"
        await callback.message.edit_text(text, reply_markup=banks_keyboard(recommended_banks))
        
    elif current_state == CreditState.SELECT_BANKS.state:
        return await callback.answer("⚠️ Iltimos, ro'yxatdan banklardan birini tanlang!", show_alert=True)
        
    await callback.answer()
