from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline import language_keyboard
from bot.keyboards.reply import main_menu_reply_keyboard, request_contact_keyboard
from bot.states.credit_state import RegistrationState
from bot.database import save_request

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "🇺🇿 Iltimos, tilni tanlang:\n"
        "🇷🇺 Пожалуйста, выберите язык:\n"
        "🇬🇧 Please choose language:"
    )
    await message.answer(text, reply_markup=language_keyboard())

@start_router.callback_query(F.data.startswith("lang_"))
async def language_selected_callback(callback: CallbackQuery, state: FSMContext):
    # Bu joyda tanlangan tilni bazaga saqlash ham mumkin.
    text = (
        "👋 **Assalomu alaykum, Tadbirkor! TadbirCore'ga xush kelibsiz!**\n\n"
        "Botdan to'liq foydalanish va arizalarni qoldirish uchun qoidalarimiz bilan tanishib chiqing:\n"
        "👉 [Ommaviy oferta](https://tadbircore.uz/public-offer)\n\n"
        "Iltimos, pastdagi **«📲 Kontaktni yuborish»** tugmasini bosish orqali raqamingizni tasdiqlang. "
        "Ushbu tugmani bosish orqali siz avtomatik ravishda Ofertaga o'z roziligingizni bildirasiz."
    )
    await state.set_state(RegistrationState.WAITING_FOR_CONTACT)
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=request_contact_keyboard(), parse_mode="Markdown", disable_web_page_preview=True)
    await callback.answer()

@start_router.message(RegistrationState.WAITING_FOR_CONTACT, F.contact)
async def process_registration_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    
    await save_request(user_id, phone)
    await state.clear()
    
    text = (
        "✅ **Ofertaga rozilik bildirildi va raqamingiz qabul qilindi!**\n\n"
        "🚀 **TadbirCore** — bu kredit olishga mo‘ljallangan noyob onlayn platforma bo'lib, "
        "bank kreditlariga bitta ariza orqali topshirish va ularni o'zaro taqqoslash imkonini beradi.\n\n"
        "**Nima uchun TadbirCore?**\n"
        "⏱ **Vaqtingizni tejaydi:** Bir marta ariza to'ldirasiz (taxminan 25 daqiqa) va o'zingiz xohlagan banklarni tanlaysiz.\n"
        "📊 **Qulay taqqoslash:** Banklarning takliflari (foiz, muddat, oylik to'lov) shaxsiy kabinetingizda bir sahifada chiqadi. Siz faqat eng yaxshisini tanlaysiz!\n"
        "🎯 **Missiyamiz:** Banklar eng yaxshi takliflar bilan mijoz uchun kurashadigan raqobatbardosh bozorni yaratish.\n\n"
        "👇 Iltimos, quyidagi menyudan kerakli bo'limni tanlang:"
    )
    await message.answer(text, reply_markup=main_menu_reply_keyboard(), parse_mode="Markdown")

@start_router.message(RegistrationState.WAITING_FOR_CONTACT)
async def process_registration_contact_invalid(message: Message):
    text = (
        "⚠️ Iltimos, raqamingizni yuborish uchun pastdagi **«📲 Kontaktni yuborish»** tugmasidan foydalaning.\n\n"
        "Bu orqali siz [Ommaviy oferta](https://tadbircore.uz/public-offer) shartlariga rozilik bildirasiz."
    )
    await message.answer(text, reply_markup=request_contact_keyboard(), parse_mode="Markdown", disable_web_page_preview=True)

@start_router.message(F.text == "🏠 Bosh menyuga qaytish")
async def back_to_main_message(message: Message):
    text = (
        "🏠 **Asosiy menyu**\n\n"
        "👇 Iltimos, quyidagi menyudan kerakli bo'limni tanlang:"
    )
    await message.answer(text, reply_markup=main_menu_reply_keyboard(), parse_mode="Markdown")

@start_router.message(F.text == "🤖 AI-maslahatchi")
async def ai_advisor_message(message: Message):
    await message.answer("💡 AI-maslahatchi: Tez orada ishga tushadi!")

@start_router.message(F.text == "ℹ️ Yordam / FAQ")
async def help_faq_message(message: Message):
    text = (
        "❓ **Yordam / FAQ**\n\n"
        "Bu bot orqali siz o'z biznesingiz uchun eng qulay kredit mahsulotlarini "
        "osongina topishingiz va ariza berishingiz mumkin.\n"
        "Savollaringiz bo'lsa, /start buyrug'i orqali qaytadan boshlashingiz mumkin."
    )
    await message.answer(text)
