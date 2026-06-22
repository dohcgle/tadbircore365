from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline import language_keyboard
from bot.keyboards.reply import main_menu_reply_keyboard, request_contact_keyboard
from bot.states.credit_state import RegistrationState
from bot.database import save_request
from bot.locales import _, _btn, get_lang, set_lang, BTNS

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    text = _("welcome")
    await message.answer(text, reply_markup=language_keyboard())

@start_router.callback_query(F.data.startswith("lang_"))
async def language_selected_callback(callback: CallbackQuery, state: FSMContext):
    lang_code = callback.data.split("_")[1]
    user_id = callback.from_user.id
    if lang_code in ['uz', 'ru']:
        await set_lang(user_id, lang_code)
    else:
        lang_code = 'uz'
        
    text = _("oferta_info", lang_code)
    await state.set_state(RegistrationState.WAITING_FOR_CONTACT)
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=request_contact_keyboard(lang_code), parse_mode="Markdown", disable_web_page_preview=True)
    await callback.answer()

@start_router.message(RegistrationState.WAITING_FOR_CONTACT, F.contact)
async def process_registration_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    
    await save_request(user_id, phone, first_name, last_name, username)
    await state.clear()
    
    lang = await get_lang(user_id)
    text = _("oferta_accepted", lang)
    await message.answer(text, reply_markup=main_menu_reply_keyboard(lang), parse_mode="Markdown")

@start_router.message(RegistrationState.WAITING_FOR_CONTACT)
async def process_registration_contact_invalid(message: Message):
    lang = await get_lang(message.from_user.id)
    text = _("contact_invalid", lang)
    await message.answer(text, reply_markup=request_contact_keyboard(lang), parse_mode="Markdown", disable_web_page_preview=True)

@start_router.message(F.text.in_([BTNS['uz']['back_main'], BTNS['ru']['back_main']]))
async def back_to_main_message(message: Message):
    lang = await get_lang(message.from_user.id)
    text = _("main_menu", lang)
    await message.answer(text, reply_markup=main_menu_reply_keyboard(lang), parse_mode="Markdown")

@start_router.message(F.text.in_([BTNS['uz']['ai'], BTNS['ru']['ai']]))
async def ai_advisor_message(message: Message):
    lang = await get_lang(message.from_user.id)
    await message.answer(_("ai_advisor", lang))

@start_router.message(F.text.in_([BTNS['uz']['faq'], BTNS['ru']['faq']]))
async def help_faq_message(message: Message):
    lang = await get_lang(message.from_user.id)
    text = _("help_faq", lang)
    await message.answer(text)
