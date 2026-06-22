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
from bot.locales import _, _btn, get_lang, BTNS

calculator_router = Router()

@calculator_router.message(F.text.in_([BTNS['uz']['calc'], BTNS['ru']['calc']]))
async def start_calculator(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    await state.set_state(CalculatorState.ASK_AMOUNT)
    await message.answer(_("calc_amount", lang), reply_markup=ReplyKeyboardRemove())

@calculator_router.message(CalculatorState.ASK_AMOUNT)
async def process_amount(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    amount_str = message.text.replace(" ", "").replace(",", "")
    if not amount_str.isdigit():
        await message.answer(_("calc_invalid_amount", lang))
        return
    
    amount = float(amount_str)
    await state.update_data(calc_amount=amount)
    
    await state.set_state(CalculatorState.ASK_RATE)
    await message.answer(_("calc_rate", lang), reply_markup=calculator_rate_keyboard(lang))

@calculator_router.message(CalculatorState.ASK_RATE)
async def process_rate(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    rate_str = message.text.replace(",", ".")
    try:
        rate = float(rate_str)
        if rate <= 0 or rate > 100:
            raise ValueError
    except ValueError:
        await message.answer(_("calc_invalid_amount", lang) + " (rate)")
        return
        
    await state.update_data(calc_rate=rate)
    
    await state.set_state(CalculatorState.ASK_TERM)
    await message.answer(_("calc_term", lang), reply_markup=calculator_term_keyboard(lang))

@calculator_router.message(CalculatorState.ASK_TERM)
async def process_term(message: Message, state: FSMContext):
    lang = await get_lang(message.from_user.id)
    term_str = message.text.strip()
    if not term_str.isdigit() or int(term_str) <= 0:
        await message.answer(_("calc_invalid_amount", lang) + " (term)")
        return
        
    term = int(term_str)
    await state.update_data(calc_term=term)
    
    await state.set_state(CalculatorState.ASK_TYPE)
    await message.answer(_("calc_type", lang), reply_markup=calculator_type_keyboard(lang))

@calculator_router.callback_query(CalculatorState.ASK_TYPE, F.data.startswith("calc_type_"))
async def process_calc_type(callback: CallbackQuery, state: FSMContext):
    lang = await get_lang(callback.from_user.id)
    calc_type = callback.data.replace("calc_type_", "")
    data = await state.get_data()
    
    amount = data.get("calc_amount")
    rate = data.get("calc_rate")
    term = data.get("calc_term")
    
    if not all([amount, rate, term]):
        await callback.message.answer("⚠️ Error.")
        await state.clear()
        return

    if calc_type == "annuity":
        calc_type_name = "Annuitet" if lang == 'uz' else "Аннуитетный"
        monthly_rate = rate / 12 / 100
        monthly_payment = amount * (monthly_rate * math.pow(1 + monthly_rate, term)) / (math.pow(1 + monthly_rate, term) - 1)
        total_payment = monthly_payment * term
        total_interest = total_payment - amount
        
        schedule_str = f"💵 1-{term} oy: {monthly_payment:,.0f} so'm".replace(",", " ")
    else:
        calc_type_name = "Differensial" if lang == 'uz' else "Дифференцированный"
        principal_payment = amount / term
        monthly_rate = rate / 12 / 100
        
        first_month_interest = amount * monthly_rate
        first_month_payment = principal_payment + first_month_interest
        
        last_month_interest = principal_payment * monthly_rate
        last_month_payment = principal_payment + last_month_interest
        
        total_interest = 0
        current_balance = amount
        for month in range(term):
            total_interest += current_balance * monthly_rate
            current_balance -= principal_payment
            
        total_payment = amount + total_interest
        schedule_str = f"🔽 1-oy: {first_month_payment:,.0f} ... {term}-oy: {last_month_payment:,.0f} so'm".replace(",", " ")

    text = _("calc_result", lang).format(
        type=calc_type_name,
        amount=f"{amount:,.0f}".replace(",", " "),
        rate=rate,
        term=term,
        total=f"{total_payment:,.0f}".replace(",", " "),
        overpay=f"{total_interest:,.0f}".replace(",", " "),
        schedule=schedule_str
    )
    
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=main_menu_reply_keyboard(lang), parse_mode="Markdown")
    await state.clear()
    await callback.answer()
