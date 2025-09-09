from aiogram.fsm.state import StatesGroup, State


class WaitQuery(StatesGroup):
    wait_query = State()


class WaitMaxSize(StatesGroup):
    wait_max_size = State()
