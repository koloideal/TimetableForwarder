from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    waiting_for_add_admin: State = State()
    waiting_for_del_admin: State = State()
    waiting_for_ban_user: State = State()
    waiting_for_unban_user: State = State()
