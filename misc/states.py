from aiogram.fsm.state import State, StatesGroup

class Convertor(StatesGroup):
    convert_to = State()
    text = State()