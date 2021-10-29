from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    enter_lab = State()