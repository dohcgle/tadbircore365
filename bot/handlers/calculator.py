import math
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.states.calculator_state import CalculatorState
from bot.keyboards.inline import calculator_type_keyboard
from bot.keyboards.reply import (
    main_menu_reply_keyboard,
    calculator_rate_keyboard,
    calculator_term_keyboard
)

calculator_router = Router()

@calculator_router.message(F.text == "🧮 Kredit kalkulyatori")
async def start_calculator(message: Message, state: FSMContext):
    await state.set_state(CalculatorState.ASK_AMOUNT)
    text = (
        "🧮 **Kredit kalkulyatori**\n\n"
        "Iltimos, kredit summasini kiriting (faqat raqamlarda, masalan: 10000000):"
    )
    await message.answer(text, reply_markup=ReplyKeyboardRemove())

@calculator_router.message(CalculatorState.ASK_AMOUNT)
async def process_amount(message: Message, state: FSMContext):
    amount_str = message.text.replace(" ", "").replace(",", "")
    if not amount_str.isdigit():
        await message.answer("⚠️ Iltimos, summani faqat raqamlarda kiriting:")
        return
    
    amount = float(amount_str)
    await state.update_data(calc_amount=amount)
    
    await state.set_state(CalculatorState.ASK_RATE)
    text = "📈 Yillik foiz stavkasini kiriting (masalan: 21 dan 28):"
    await message.answer(text, reply_markup=calculator_rate_keyboard())

@calculator_router.message(CalculatorState.ASK_RATE)
async def process_rate(message: Message, state: FSMContext):
    rate_str = message.text.replace(",", ".")
    try:
        rate = float(rate_str)
        if rate <= 0 or rate > 100:
            raise ValueError
    except ValueError:
        await message.answer("⚠️ Iltimos, foiz stavkasini to'g'ri kiriting (masalan: 24):")
        return
        
    await state.update_data(calc_rate=rate)
    
    await state.set_state(CalculatorState.ASK_TERM)
    text = "🗓 Kredit muddatini oy hisobida kiriting (masalan: 36):"
    await message.answer(text, reply_markup=calculator_term_keyboard())

@calculator_router.message(CalculatorState.ASK_TERM)
async def process_term(message: Message, state: FSMContext):
    term_str = message.text.strip()
    if not term_str.isdigit() or int(term_str) <= 0:
        await message.answer("⚠️ Iltimos, muddatni to'g'ri kiriting (masalan: 36):")
        return
        
    term = int(term_str)
    await state.update_data(calc_term=term)
    
    await state.set_state(CalculatorState.ASK_TYPE)
    text = "⚙️ Hisoblash turini tanlang:\n\n**Annuitet** - Har oy bir xil summa to'lanadi.\n**Differensial** - Asosiy qarz bir xil, foizlar kamayib boradi."
    await message.answer(text, reply_markup=calculator_type_keyboard())

@calculator_router.callback_query(CalculatorState.ASK_TYPE, F.data.startswith("calc_type_"))
async def process_calc_type(callback: CallbackQuery, state: FSMContext):
    calc_type = callback.data.replace("calc_type_", "")
    data = await state.get_data()
    
    amount = data.get("calc_amount")
    rate = data.get("calc_rate")
    term = data.get("calc_term")
    
    if not all([amount, rate, term]):
        await callback.message.answer("⚠️ Xatolik yuz berdi. Iltimos, boshidan boshlang.")
        await state.clear()
        return

    # Format numbers beautifully
    def format_money(val: float) -> str:
        return f"{val:,.2f}".replace(",", " ") + " so'm"

    if calc_type == "annuity":
        # Annuitet
        monthly_rate = rate / 12 / 100
        monthly_payment = amount * (monthly_rate * math.pow(1 + monthly_rate, term)) / (math.pow(1 + monthly_rate, term) - 1)
        total_payment = monthly_payment * term
        total_interest = total_payment - amount
        
        result_text = (
            "📊 **Annuitet hisob-kitobi natijasi:**\n\n"
            f"💰 Kredit summasi: **{format_money(amount)}**\n"
            f"📈 Yillik foiz: **{rate}%**\n"
            f"🗓 Muddat: **{term} oy**\n\n"
            f"💵 Har oylik to'lov: **{format_money(monthly_payment)}**\n"
            f"📉 Jami hisoblangan foiz: **{format_money(total_interest)}**\n"
            f"💸 Jami qaytariladigan summa: **{format_money(total_payment)}**"
        )
    else:
        # Differensial
        principal_payment = amount / term
        monthly_rate = rate / 12 / 100
        
        first_month_interest = amount * monthly_rate
        first_month_payment = principal_payment + first_month_interest
        
        last_month_interest = principal_payment * monthly_rate
        last_month_payment = principal_payment + last_month_interest
        
        total_interest = 0
        current_balance = amount
        for _ in range(term):
            total_interest += current_balance * monthly_rate
            current_balance -= principal_payment
            
        total_payment = amount + total_interest
        
        result_text = (
            "📉 **Differensial hisob-kitobi natijasi:**\n\n"
            f"💰 Kredit summasi: **{format_money(amount)}**\n"
            f"📈 Yillik foiz: **{rate}%**\n"
            f"🗓 Muddat: **{term} oy**\n\n"
            f"🔼 Birinchi oy to'lovi: **{format_money(first_month_payment)}**\n"
            f"🔽 Oxirgi oy to'lovi: **{format_money(last_month_payment)}**\n"
            f"📉 Jami hisoblangan foiz: **{format_money(total_interest)}**\n"
            f"💸 Jami qaytariladigan summa: **{format_money(total_payment)}**"
        )
        
    await callback.message.delete()
    await callback.message.answer(result_text, reply_markup=main_menu_reply_keyboard(), parse_mode="Markdown")
    await state.clear()
    await callback.answer()
