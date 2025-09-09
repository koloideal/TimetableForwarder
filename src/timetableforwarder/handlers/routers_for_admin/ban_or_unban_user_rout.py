from aiogram import types
from timetableforwarder.states.admin_states import AdminState
from aiogram.fsm.context import FSMContext

async def ban_or_unban_user_rout(
    message: types.Message, ban_or_unban: str, state: FSMContext
) -> None:
    match ban_or_unban:
        case "ban":
            await message.answer("Enter username for ban user")
            await state.set_state(AdminState.waiting_for_ban_user)
        case "unban":
            await message.answer("Enter username for unban user")
            await state.set_state(AdminState.waiting_for_unban_user)
