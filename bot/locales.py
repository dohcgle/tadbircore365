from bot.database import get_user_lang, update_user_lang

TEXTS = {
    "uz": {
        "welcome": "🇺🇿 Iltimos, tilni tanlang:\n🇷🇺 Пожалуйста, выберите язык:\n🇬🇧 Please choose language:",
        "oferta_info": "👋 **Assalomu alaykum, Tadbirkor! TadbirCore'ga xush kelibsiz!**\n\nBotdan to'liq foydalanish va arizalarni qoldirish uchun qoidalarimiz bilan tanishib chiqing:\n👉 [Ommaviy oferta](https://tadbircore.uz/public-offer)\n\nIltimos, pastdagi **«📲 Kontaktni yuborish»** tugmasini bosish orqali raqamingizni tasdiqlang. Ushbu tugmani bosish orqali siz avtomatik ravishda Ofertaga o'z roziligingizni bildirasiz.",
        "oferta_accepted": "✅ **Ofertaga rozilik bildirildi va raqamingiz qabul qilindi!**\n\n🚀 **TadbirCore** — bu kredit olishga mo‘ljallangan noyob onlayn platforma bo'lib, bank kreditlariga bitta ariza orqali topshirish va ularni o'zaro taqqoslash imkonini beradi.\n\n**Nima uchun TadbirCore?**\n⏱ **Vaqtingizni tejaydi:** Bir marta ariza to'ldirasiz (taxminan 25 daqiqa) va o'zingiz xohlagan banklarni tanlaysiz.\n📊 **Qulay taqqoslash:** Banklarning takliflari (foiz, muddat, oylik to'lov) shaxsiy kabinetingizda bir sahifada chiqadi. Siz faqat eng yaxshisini tanlaysiz!\n🎯 **Missiyamiz:** Banklar eng yaxshi takliflar bilan mijoz uchun kurashadigan raqobatbardosh bozorni yaratish.\n\n👇 Iltimos, quyidagi menyudan kerakli bo'limni tanlang:",
        "contact_invalid": "⚠️ Iltimos, raqamingizni yuborish uchun pastdagi **«📲 Kontaktni yuborish»** tugmasidan foydalaning.\n\nBu orqali siz [Ommaviy oferta](https://tadbircore.uz/public-offer) shartlariga rozilik bildirasiz.",
        "main_menu": "🏠 **Asosiy menyu**\n\n👇 Iltimos, quyidagi menyudan kerakli bo'limni tanlang:",
        "ai_advisor": "💡 AI-maslahatchi: Tez orada ishga tushadi!",
        "help_faq": "❓ **Yordam / FAQ**\n\nBu bot orqali siz o'z biznesingiz uchun eng qulay kredit mahsulotlarini osongina topishingiz va ariza berishingiz mumkin.\nSavollaringiz bo'lsa, /start buyrug'i orqali qaytadan boshlashingiz mumkin.",
        "live_chat_start": "👨‍💻 **Operator bilan bog'lanish**\n\nSiz jonli chatga ulandingiz. Barcha savol va takliflaringizni shu yerda yozishingiz mumkin. Operatorlarimiz tez orada sizga shu yerning o'zida javob qaytarishadi.\n\nSuhbatni tugatish uchun pastdagi **❌ Chatni yakunlash** tugmasini bosing.",
        "chat_ended": "Suhbat yakunlandi. Asosiy menyudasiz:",
        "murojaat_start": "📝 **Murojaat qoldirish**\n\nO'z taklif, shikoyat yoki savolingizni shu yerda yozib qoldirishingiz mumkin. Operatorlarimiz uni ko'rib chiqib, siz bilan bog'lanishadi.\n\nBekor qilish va orqaga qaytish uchun quyidagi tugmani bosing.",
        "murojaat_cancelled": "Murojaat yuborish bekor qilindi.",
        "murojaat_sent": "✅ Murojaatingiz muvaffaqiyatli yuborildi! Tez orada mutaxassislarimiz aloqaga chiqishadi.",
        
        "credit_step1": "🆔 **1-qadam: Mijozni identifikatsiya qilish**\n\nIltimos, o'zingizning INN (9 xonali) yoki JSHSHIR (14 xonali) raqamingizni kiriting:",
        "credit_invalid_inn": "Siz noto'g'ri kiritdingiz, iltimos to'g'ri kiriting",
        "credit_step2_base": "✅ **Mijoz ma'lumotlari topildi:**\n🏢 {type} - **{name}**\n🏦 Bank: **{bank}**\n💳 H/r: **{account}**\n\n💰 **2-qadam: Kredit summasi**\n\nSizga qancha miqdorda kredit zarur? Quyidagi variantlardan birini tanlang yoki summani raqamlar bilan kiriting (masalan: 120 000 000):",
        "credit_step3": "🗓 **3-qadam: Kredit muddati**\n\nQarzni qancha muddatda qaytarishni rejalashtiryapsiz?",
        "credit_step4": "🎯 **4-qadam: Kredit olish maqsadi**\n\nKredit qanday maqsadlar uchun ishlatiladi? Quyidagi variantlardan birini tanlang yoki o'z maqsadingizni yozib yuboring:",
        "credit_step5": "🛡 **5-qadam: Ta'minot turi**\n\nKredit uchun qanday ta'minot turini taqdim eta olasiz? Variantlardan birini tanlang yoki o'z turingizni yozing:",
        "credit_step_photo1": "📸 **Kredit olinayotgan obyekt yoki garov rasmini yuboring**\n\nRasmni jo'nating yoki ushbu bosqichni o'tkazib yuborish uchun tugmani bosing.",
        "credit_step_photo2": "Siz {count} ta rasm yubordingiz. Yana rasm yuborishingiz yoki keyingi qadamga o'tish uchun quyidagi tugmalardan birini bosishingiz mumkin:",
        "credit_step6": "🏦 **6-qadam: Banklarni tanlash**\n\nQuyida sizning arizangizga mos keladigan banklar keltirilgan. Kerakli bankni tanlang yoki barchasiga yuboring:",
        "credit_success": "🎉 **Arizangiz muvaffaqiyatli qabul qilindi!**\n\n**Kredit ariza detalizatsiyasi:**\n🔹 **Kredit summasi:** {amount}\n🔹 **Kredit muddati:** {term}\n🔹 **Kredit olish maqsadi:** {purpose}\n🔹 **Ta'minot turi:** {collateral}\n\n✅ Sizning arizangiz 🆔 **{req_id}** raqami bilan ro'yxatga olindi.\n\n📤 **Arizangiz quyidagi bank(lar)ga yuborildi:**\n{selected_bank_display}\n\nBank vakillari tez orada siz bilan aloqaga chiqadi!",
        "banks_all_display": "Barcha tavsiya etilgan banklar:\n{banks_text}",
        "all_banks_text": "Barcha tavsiya etilgan banklar",
        
        "calc_type": "🧮 **Kredit Kalkulyatori**\n\nIltimos, kredit to'lash turini tanlang:",
        "calc_amount": "💰 **Kredit summasi**\n\nQancha miqdorda kredit olmoqchisiz? (raqamlar bilan kiriting, masalan: 100 000 000)",
        "calc_invalid_amount": "Noto'g'ri qiymat. Iltimos faqat raqamlar ishlating.",
        "calc_rate": "📈 **Yillik foiz stavkasi**\n\nFoizni tanlang yoki qo'lda kiriting (masalan: 24):",
        "calc_term": "🗓 **Kredit muddati (oylarda)**\n\nMuddatni tanlang yoki qo'lda kiriting (masalan: 36):",
        "calc_result": "📊 **Kalkulyator natijasi** ({type})\n\n💰 Summa: {amount} so'm\n📈 Foiz stavkasi: {rate}%\n🗓 Muddat: {term} oy\n\n💳 Umumiy to'lov: {total} so'm\n💸 Jami foizlar: {overpay} so'm\n\n📅 **Oylik to'lov grafik:**\n{schedule}",
        "alert_select_first": "⚠️ Iltimos, avval tanlovni amalga oshiring!",
        "alert_upload_photo": "⚠️ Iltimos, rasm yuklang yoki 'Rasmsiz davom etish' ni tanlang!",
        "alert_select_bank": "⚠️ Iltimos, ro'yxatdan banklardan birini tanlang!"
    },
    "ru": {
        "welcome": "🇺🇿 Iltimos, tilni tanlang:\n🇷🇺 Пожалуйста, выберите язык:\n🇬🇧 Please choose language:",
        "oferta_info": "👋 **Здравствуйте, Предприниматель! Добро пожаловать в TadbirCore!**\n\nДля полного использования бота и подачи заявок ознакомьтесь с нашими правилами:\n👉 [Публичная оферта](https://tadbircore.uz/public-offer)\n\nПожалуйста, подтвердите ваш номер, нажав кнопку **«📲 Отправить контакт»** ниже. Нажав эту кнопку, вы автоматически соглашаетесь с условиями Оферты.",
        "oferta_accepted": "✅ **Вы согласились с офертой, ваш номер принят!**\n\n🚀 **TadbirCore** — это уникальная онлайн платформа для получения кредитов, позволяющая подать единую заявку в разные банки и сравнить их предложения.\n\n**Почему TadbirCore?**\n⏱ **Экономит время:** Вы заполняете заявку один раз (около 25 минут) и выбираете нужные банки.\n📊 **Удобное сравнение:** Предложения банков (ставка, срок, платеж) отображаются в личном кабинете на одной странице. Выбирайте лучшее!\n🎯 **Наша миссия:** Создать конкурентный рынок, где банки борются за клиента.\n\n👇 Пожалуйста, выберите нужный раздел из меню ниже:",
        "contact_invalid": "⚠️ Пожалуйста, используйте кнопку **«📲 Отправить контакт»** ниже для отправки номера.\n\nЭтим вы соглашаетесь с условиями [Публичной оферты](https://tadbircore.uz/public-offer).",
        "main_menu": "🏠 **Главное меню**\n\n👇 Пожалуйста, выберите нужный раздел из меню ниже:",
        "ai_advisor": "💡 AI-консультант: Скоро будет запущен!",
        "help_faq": "❓ **Помощь / FAQ**\n\nС помощью этого бота вы можете легко найти и подать заявку на самые подходящие кредитные продукты для вашего бизнеса.\nЕсли у вас есть вопросы, вы можете начать заново с помощью команды /start.",
        "live_chat_start": "👨‍💻 **Связь с оператором**\n\nВы подключились к живому чату. Вы можете задать все свои вопросы здесь. Операторы скоро ответят вам.\n\nДля завершения чата нажмите кнопку **❌ Завершить чат**.",
        "chat_ended": "Чат завершен. Вы в главном меню:",
        "murojaat_start": "📝 **Оставить обращение**\n\nЗдесь вы можете оставить свое предложение, жалобу или вопрос. Операторы рассмотрят его и свяжутся с вами.\n\nДля отмены нажмите кнопку ниже.",
        "murojaat_cancelled": "Отправка обращения отменена.",
        "murojaat_sent": "✅ Ваше обращение успешно отправлено! Специалисты скоро свяжутся с вами.",
        
        "credit_step1": "🆔 **Шаг 1: Идентификация клиента**\n\nПожалуйста, введите ваш ИНН (9 цифр) или ПИНФЛ (14 цифр):",
        "credit_invalid_inn": "Вы ввели неверно, пожалуйста, введите правильно",
        "credit_step2_base": "✅ **Данные клиента найдены:**\n🏢 {type} - **{name}**\n🏦 Банк: **{bank}**\n💳 Р/с: **{account}**\n\n💰 **Шаг 2: Сумма кредита**\n\nКакая сумма вам нужна? Выберите один из вариантов или введите сумму цифрами (например: 120 000 000):",
        "credit_step3": "🗓 **Шаг 3: Срок кредита**\n\nНа какой срок вы планируете взять кредит?",
        "credit_step4": "🎯 **Шаг 4: Цель кредита**\n\nДля каких целей будет использован кредит? Выберите один из вариантов или напишите свою цель:",
        "credit_step5": "🛡 **Шаг 5: Тип обеспечения**\n\nКакой тип обеспечения вы можете предоставить? Выберите один из вариантов или напишите свой:",
        "credit_step_photo1": "📸 **Отправьте фото объекта или залога**\n\nОтправьте фото или нажмите кнопку, чтобы пропустить этот шаг.",
        "credit_step_photo2": "Вы отправили {count} фото. Вы можете отправить еще или перейти к следующему шагу, нажав одну из кнопок ниже:",
        "credit_step6": "🏦 **Шаг 6: Выбор банков**\n\nНиже представлены банки, подходящие для вашей заявки. Выберите нужный банк или отправьте всем:",
        "credit_success": "🎉 **Ваша заявка успешно принята!**\n\n**Детали заявки:**\n🔹 **Сумма:** {amount}\n🔹 **Срок:** {term}\n🔹 **Цель:** {purpose}\n🔹 **Обеспечение:** {collateral}\n\n✅ Ваша заявка зарегистрирована под номером 🆔 **{req_id}**.\n\n📤 **Отправлено в следующие банки:**\n{selected_bank_display}\n\nПредставители банка скоро свяжутся с вами!",
        "banks_all_display": "Все рекомендованные банки:\n{banks_text}",
        "all_banks_text": "Все рекомендованные банки",
        
        "calc_type": "🧮 **Кредитный калькулятор**\n\nПожалуйста, выберите тип погашения:",
        "calc_amount": "💰 **Сумма кредита**\n\nСколько вы хотите взять? (введите цифрами, например: 100 000 000)",
        "calc_invalid_amount": "Неверное значение. Пожалуйста, используйте только цифры.",
        "calc_rate": "📈 **Годовая процентная ставка**\n\nВыберите процент или введите вручную (например: 24):",
        "calc_term": "🗓 **Срок кредита (в месяцах)**\n\nВыберите срок или введите вручную (например: 36):",
        "calc_result": "📊 **Результат калькулятора** ({type})\n\n💰 Сумма: {amount} сум\n📈 Процентная ставка: {rate}%\n🗓 Срок: {term} мес\n\n💳 Общий платеж: {total} сум\n💸 Итого проценты: {overpay} сум\n\n📅 **График платежей:**\n{schedule}",
        "alert_select_first": "⚠️ Пожалуйста, сначала сделайте выбор!",
        "alert_upload_photo": "⚠️ Пожалуйста, загрузите фото или выберите 'Продолжить без фото'!",
        "alert_select_bank": "⚠️ Пожалуйста, выберите один из банков из списка!"
    }
}

BTNS = {
    "uz": {
        "credit": "🏢 Kredit tanlash",
        "calc": "🧮 Kredit kalkulyatori",
        "live_chat": "💬 Jonli chat",
        "murojaat": "📝 Murojaat qoldirish",
        "ai": "🤖 AI-maslahatchi",
        "faq": "ℹ️ Yordam / FAQ",
        "cabinet": "👤 Shaxsiy kabinet",
        "contact": "📲 Kontaktni yuborish",
        "cancel": "❌ Bekor qilish",
        "end_chat": "❌ Chatni yakunlash",
        "back_main": "🏠 Bosh menyuga qaytish",
        "nav_back": "⬅️ Orqaga",
        "nav_next": "➡️ Oldinga",
        "btn_amount_1": "50 mln gacha 💰",
        "btn_amount_2": "50 - 100 mln 💵",
        "btn_amount_3": "100 - 500 mln 💸",
        "btn_amount_4": "500 mln+ 🏦",
        "btn_term_1": "6 oy 🗓",
        "btn_term_2": "12 oy 🗓",
        "btn_term_3": "24 oy 🗓",
        "btn_term_4": "36 oy 🗓",
        "btn_term_5": "60 oy 🗓",
        "btn_purp_1": "🏢 Mikrokredit",
        "btn_purp_2": "🛒 Kundalik xarajatlar",
        "btn_purp_3": "📈 Biznes rivoji",
        "btn_purp_4": "🌱 Yangi boshlaganlar",
        "btn_purp_5": "🚗 Avtokredit",
        "btn_purp_6": "🔁 Overdraft",
        "btn_purp_7": "🏗 Ipoteka/Qurilish",
        "btn_purp_8": "♻️ Yashil kredit",
        "btn_purp_9": "🧾 Moliyalashtirish",
        "btn_purp_10": "🧑‍🎓 Yosh tadbirkorlar",
        "btn_purp_11": "👩‍💼 Ayollar tadbirkorligi",
        "btn_purp_12": "🔄 Universal kredit",
        "btn_col_1": "🚗 Avtomobil",
        "btn_col_2": "🏠 Ko'chmas mulk",
        "btn_col_3": "🚜 Texnika",
        "btn_skip_photo": "⏭ Rasmsiz davom etish",
        "btn_bank_all": "✅ Barchasiga yuborish",
        "btn_apply": "🚀 Ariza topshirish",
        "btn_back_main_inline": "⬅️ Bosh menyuga qaytish",
        "calc_ann": "📊 Annuitet",
        "calc_diff": "📉 Differensial"
    },
    "ru": {
        "credit": "🏢 Выбрать кредит",
        "calc": "🧮 Кредитный калькулятор",
        "live_chat": "💬 Живой чат",
        "murojaat": "📝 Оставить обращение",
        "ai": "🤖 AI-консультант",
        "faq": "ℹ️ Помощь / FAQ",
        "cabinet": "👤 Личный кабинет",
        "contact": "📲 Отправить контакт",
        "cancel": "❌ Отмена",
        "end_chat": "❌ Завершить чат",
        "back_main": "🏠 Вернуться в главное меню",
        "nav_back": "⬅️ Назад",
        "nav_next": "➡️ Вперед",
        "btn_amount_1": "До 50 млн 💰",
        "btn_amount_2": "50 - 100 млн 💵",
        "btn_amount_3": "100 - 500 млн 💸",
        "btn_amount_4": "500 млн+ 🏦",
        "btn_term_1": "6 мес 🗓",
        "btn_term_2": "12 мес 🗓",
        "btn_term_3": "24 мес 🗓",
        "btn_term_4": "36 мес 🗓",
        "btn_term_5": "60 мес 🗓",
        "btn_purp_1": "🏢 Микрокредит",
        "btn_purp_2": "🛒 Текущие расходы",
        "btn_purp_3": "📈 Развитие бизнеса",
        "btn_purp_4": "🌱 Начинающие",
        "btn_purp_5": "🚗 Автокредит",
        "btn_purp_6": "🔁 Овердрафт",
        "btn_purp_7": "🏗 Ипотека/Стройка",
        "btn_purp_8": "♻️ Зеленый кредит",
        "btn_purp_9": "🧾 Финансирование",
        "btn_purp_10": "🧑‍🎓 Молодые предприниматели",
        "btn_purp_11": "👩‍💼 Женское предпринимательство",
        "btn_purp_12": "🔄 Универсальный кредит",
        "btn_col_1": "🚗 Автомобиль",
        "btn_col_2": "🏠 Недвижимость",
        "btn_col_3": "🚜 Техника",
        "btn_skip_photo": "⏭ Продолжить без фото",
        "btn_bank_all": "✅ Отправить всем",
        "btn_apply": "🚀 Подать заявку",
        "btn_back_main_inline": "⬅️ В главное меню",
        "calc_ann": "📊 Аннуитетный",
        "calc_diff": "📉 Дифференцированный"
    }
}

USER_LANGS = {}

async def get_lang(user_id: int) -> str:
    if user_id not in USER_LANGS:
        lang = await get_user_lang(user_id)
        USER_LANGS[user_id] = lang or 'uz'
    return USER_LANGS[user_id]

async def set_lang(user_id: int, lang: str):
    USER_LANGS[user_id] = lang
    await update_user_lang(user_id, lang)

def _(key: str, lang: str = 'uz') -> str:
    return TEXTS.get(lang, TEXTS['uz']).get(key, key)

def _btn(key: str, lang: str = 'uz') -> str:
    return BTNS.get(lang, BTNS['uz']).get(key, key)
