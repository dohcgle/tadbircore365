from aiogram.fsm.state import State, StatesGroup

class CreditState(StatesGroup):
    ASK_INN = State()
    ASK_AMOUNT = State()
    ASK_TERM = State()
    ASK_PURPOSE = State()
    ASK_COLLATERAL = State()
    ASK_COLLATERAL_PHOTO = State()
    SELECT_BANKS = State()

class ContactState(StatesGroup):
    WAITING_FOR_CONTACT = State()
    WAITING_FOR_TEXT = State()

class RegistrationState(StatesGroup):
    WAITING_FOR_CONTACT = State()

class MurojaatState(StatesGroup):
    WAITING_FOR_TEXT = State()
