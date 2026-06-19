from aiogram.fsm.state import State, StatesGroup

class CalculatorState(StatesGroup):
    ASK_AMOUNT = State()
    ASK_RATE = State()
    ASK_TERM = State()
    ASK_TYPE = State()
