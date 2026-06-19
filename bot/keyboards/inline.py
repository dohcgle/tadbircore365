from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def add_nav_buttons(keyboard: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    # Klaviaturalarga Orqaga va Oldinga tugmalarini qo'shish
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="nav_back"),
        InlineKeyboardButton(text="➡️ Oldinga", callback_data="nav_next")
    ])
    return keyboard

def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔍 Kredit tanlash", callback_data="start_credit_scenario"),
                InlineKeyboardButton(text="📞 Murojaat qoldirish", callback_data="leave_request")
            ],
            [
                InlineKeyboardButton(text="💡 AI-maslahatchi", callback_data="ai_advisor"),
                InlineKeyboardButton(text="❓ Yordam / FAQ", callback_data="help_faq")
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

def amount_keyboard() -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="50 mln gacha 💰", callback_data="amount_50m")],
            [InlineKeyboardButton(text="50 - 100 mln 💵", callback_data="amount_50-100m")],
            [InlineKeyboardButton(text="100 - 500 mln 💸", callback_data="amount_100-500m")],
            [InlineKeyboardButton(text="500 mln+ 🏦", callback_data="amount_500m_plus")]
        ]
    ))

def term_keyboard() -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="6 oy 🗓", callback_data="term_6"),
                InlineKeyboardButton(text="12 oy 🗓", callback_data="term_12")
            ],
            [
                InlineKeyboardButton(text="24 oy 🗓", callback_data="term_24"),
                InlineKeyboardButton(text="36 oy 🗓", callback_data="term_36")
            ],
            [
                InlineKeyboardButton(text="60 oy 🗓", callback_data="term_60")
            ]
        ]
    ))

def purpose_keyboard() -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏢 Mikrokredit", callback_data="purpose_1"),
                InlineKeyboardButton(text="🛒 Kundalik xarajatlar", callback_data="purpose_2")
            ],
            [
                InlineKeyboardButton(text="📈 Biznes rivoji", callback_data="purpose_3"),
                InlineKeyboardButton(text="🌱 Yangi boshlaganlar", callback_data="purpose_4")
            ],
            [
                InlineKeyboardButton(text="🚗 Avtokredit", callback_data="purpose_5"),
                InlineKeyboardButton(text="🔁 Overdraft", callback_data="purpose_6")
            ],
            [
                InlineKeyboardButton(text="🏗 Ipoteka/Qurilish", callback_data="purpose_7"),
                InlineKeyboardButton(text="♻️ Yashil kredit", callback_data="purpose_8")
            ],
            [
                InlineKeyboardButton(text="🧾 Moliyalashtirish", callback_data="purpose_9"),
                InlineKeyboardButton(text="🧑‍🎓 Yosh tadbirkorlar", callback_data="purpose_10")
            ],
            [
                InlineKeyboardButton(text="👩‍💼 Ayollar tadbirkorligi", callback_data="purpose_11"),
                InlineKeyboardButton(text="🔄 Universal kredit", callback_data="purpose_12")
            ]
        ]
    ))

def collateral_keyboard() -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚗 Avtomobil", callback_data="collateral_auto")],
            [InlineKeyboardButton(text="🏠 Ko'chmas mulk", callback_data="collateral_realestate")],
            [InlineKeyboardButton(text="🚜 Texnika", callback_data="collateral_technics")]
        ]
    ))

def skip_photo_keyboard() -> InlineKeyboardMarkup:
    return add_nav_buttons(InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭ Rasmsiz davom etish", callback_data="skip_photo")]
        ]
    ))

def banks_keyboard(bank_names: list) -> InlineKeyboardMarkup:
    buttons = []
    for i, b_name in enumerate(bank_names):
        buttons.append([InlineKeyboardButton(text=f"🏦 {b_name}", callback_data=f"bank_{i}")])
    buttons.append([InlineKeyboardButton(text="✅ Barchasiga yuborish", callback_data="bank_all")])
    
    return add_nav_buttons(InlineKeyboardMarkup(inline_keyboard=buttons))

def apply_credit_keyboard(amount: str, term: str, purpose: str, b_type: str) -> InlineKeyboardMarkup:
    # URL ni encode qilib yuboramiz. URL TadbirCore domeniga moslanadi.
    url = f"https://tadbircore.uz/apply?amount={amount}&term={term}&purpose={purpose}&type={b_type}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Ariza topshirish", url=url)],
            [InlineKeyboardButton(text="⬅️ Bosh menyuga qaytish", callback_data="back_to_main")]
        ]
    )

def calculator_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Annuitet", callback_data="calc_type_annuity")],
            [InlineKeyboardButton(text="📉 Differensial", callback_data="calc_type_diff")]
        ]
    )

def operator_accept_keyboard(request_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Qabul qildim", callback_data=f"accept_{request_id}")]
        ]
    )
