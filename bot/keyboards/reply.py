from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏢 Kredit tanlash"), KeyboardButton(text="🧮 Kredit kalkulyatori")],
            [KeyboardButton(text="💬 Jonli chat"), KeyboardButton(text="📝 Murojaat qoldirish")],
            [KeyboardButton(text="🤖 AI-maslahatchi"), KeyboardButton(text="ℹ️ Yordam / FAQ")],
            [KeyboardButton(text="👤 Shaxsiy kabinet")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Quyidagilardan birini tanlang..."
    )

def request_contact_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📲 Kontaktni yuborish", request_contact=True)],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )

def end_chat_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Chatni yakunlash")]
        ],
        resize_keyboard=True
    )

def calculator_rate_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="21"), KeyboardButton(text="22")],
            [KeyboardButton(text="24"), KeyboardButton(text="26")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Foizni tanlang yoki qo'lda kiriting..."
    )

def calculator_term_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="12"), KeyboardButton(text="24"), KeyboardButton(text="36")],
            [KeyboardButton(text="48"), KeyboardButton(text="60")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Muddatni tanlang yoki qo'lda kiriting..."
    )
