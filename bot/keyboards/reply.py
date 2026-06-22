from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.locales import _btn

def main_menu_reply_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_btn("credit", lang)), KeyboardButton(text=_btn("calc", lang))],
            [KeyboardButton(text=_btn("live_chat", lang)), KeyboardButton(text=_btn("murojaat", lang))],
            [KeyboardButton(text=_btn("ai", lang)), KeyboardButton(text=_btn("faq", lang))],
            [KeyboardButton(text=_btn("cabinet", lang))]
        ],
        resize_keyboard=True,
        input_field_placeholder="Quyidagilardan birini tanlang..." if lang == 'uz' else "Выберите один из вариантов..."
    )

def request_contact_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_btn("contact", lang), request_contact=True)],
            [KeyboardButton(text=_btn("cancel", lang))]
        ],
        resize_keyboard=True
    )

def end_chat_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_btn("end_chat", lang))]
        ],
        resize_keyboard=True
    )

def calculator_rate_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="21"), KeyboardButton(text="22")],
            [KeyboardButton(text="24"), KeyboardButton(text="26")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Foizni tanlang..." if lang == 'uz' else "Выберите процент..."
    )

def calculator_term_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="12"), KeyboardButton(text="24"), KeyboardButton(text="36")],
            [KeyboardButton(text="48"), KeyboardButton(text="60")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Muddatni tanlang..." if lang == 'uz' else "Выберите срок..."
    )
