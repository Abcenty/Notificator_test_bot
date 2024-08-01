from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    set_name = State()
    set_email = State()
    create_note = State()
    set_timestamp = State()