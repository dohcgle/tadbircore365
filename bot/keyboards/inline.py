from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales import _btn

def add_nav_buttons(keyboard: InlineKeyboardMarkup, lang: str = 'uz') -> InlineKeyboardMarkup:
    # Klaviaturalarga Orqaga va Oldinga tugmalarini qo'shish
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=_btn("nav_back", lang), callback_data="nav_back"),
        InlineKeyboardButton(text=_btn("nav_next", lang), callback_data="nav_next")
    ])
    return keyboard

def main_menu_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_btn("credit", lang), callback_data="start_credit_scenario"),
                InlineKeyboardButton(text=_btn("murojaat", lang), callback_data="leave_request")
            ],
            [
                InlineKeyboardButton(text=_btn("ai", lang), callback_data="ai_advisor"),
                InlineKeyboardButton(text=_btn("faq", lang), callback_data="help_faq")
            ]
        ]
    )

def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
            ]
        ]
    )

def amount_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_btn("btn_amount_1", lang), callback_data="amount_50m")],
            [InlineKeyboardButton(text=_btn("btn_amount_2", lang), callback_data="amount_50-100m")],
            [InlineKeyboardButton(text=_btn("btn_amount_3", lang), callback_data="amount_100-500m")],
            [InlineKeyboardButton(text=_btn("btn_amount_4", lang), callback_data="amount_500m_plus")]
        ]
    ), lang)

def term_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_btn("btn_term_1", lang), callback_data="term_6"),
                InlineKeyboardButton(text=_btn("btn_term_2", lang), callback_data="term_12")
            ],
            [
                InlineKeyboardButton(text=_btn("btn_term_3", lang), callback_data="term_24"),
                InlineKeyboardButton(text=_btn("btn_term_4", lang), callback_data="term_36")
            ],
            [
                InlineKeyboardButton(text=_btn("btn_term_5", lang), callback_data="term_60")
            ]
        ]
    ), lang)

def purpose_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_btn("btn_purp_1", lang), callback_data="purpose_1"),
                InlineKeyboardButton(text=_btn("btn_purp_2", lang), callback_data="purpose_2")
            ],
            [
                InlineKeyboardButton(text=_btn("btn_purp_3", lang), callback_data="purpose_3"),
                InlineKeyboardButton(text=_btn("btn_purp_4", lang), callback_data="purpose_4")
            ],
            [
                InlineKeyboardButton(text=_btn("btn_purp_5", lang), callback_data="purpose_5"),
                InlineKeyboardButton(text=_btn("btn_purp_6", lang), callback_data="purpose_6")
            ],
            [
                InlineKeyboardButton(text=_btn("btn_purp_7", lang), callback_data="purpose_7"),
                InlineKeyboardButton(text=_btn("btn_purp_8", lang), callback_data="purpose_8")
            ],
            [
                InlineKeyboardButton(text=_btn("btn_purp_9", lang), callback_data="purpose_9"),
                InlineKeyboardButton(text=_btn("btn_purp_10", lang), callback_data="purpose_10")
            ],
            [
                InlineKeyboardButton(text=_btn("btn_purp_11", lang), callback_data="purpose_11"),
                InlineKeyboardButton(text=_btn("btn_purp_12", lang), callback_data="purpose_12")
            ]
        ]
    ), lang)

def collateral_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_btn("btn_col_1", lang), callback_data="collateral_auto")],
            [InlineKeyboardButton(text=_btn("btn_col_2", lang), callback_data="collateral_realestate")],
            [InlineKeyboardButton(text=_btn("btn_col_3", lang), callback_data="collateral_technics")]
        ]
    ), lang)

def skip_photo_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_btn("btn_skip_photo", lang), callback_data="skip_photo")]
        ]
    ), lang)

def banks_keyboard(bank_names: list, lang: str = 'uz') -> InlineKeyboardMarkup:
    buttons = []
    for i, b_name in enumerate(bank_names):
        buttons.append([InlineKeyboardButton(text=f"🏦 {b_name}", callback_data=f"bank_{i}")])
    buttons.append([InlineKeyboardButton(text=_btn("btn_bank_all", lang), callback_data="bank_all")])
    
    return add_nav_buttons(InlineKeyboardMarkup(inline_keyboard=buttons), lang)

def apply_credit_keyboard(amount: str, term: str, purpose: str, b_type: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    url = f"https://tadbircore.uz/apply?amount={amount}&term={term}&purpose={purpose}&type={b_type}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_btn("btn_apply", lang), url=url)],
            [InlineKeyboardButton(text=_btn("btn_back_main_inline", lang), callback_data="back_to_main")]
        ]
    )

def calculator_type_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_btn("calc_ann", lang), callback_data="calc_type_annuity")],
            [InlineKeyboardButton(text=_btn("calc_diff", lang), callback_data="calc_type_diff")]
        ]
    )

def operator_accept_keyboard(request_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Qabul qildim", callback_data=f"accept_{request_id}")]
        ]
    )
