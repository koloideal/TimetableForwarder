from logging import Logger, getLogger
from typing import Optional
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.database.database_models import User


action_logger: Logger = getLogger('action_logger')


async def get_username_for_unban_user_rout(message: Message, state: FSMContext, users_dao: UsersDAO) -> None:
    raw_input_username: str = message.text.strip()

    finished_input_username: str = (
        raw_input_username
        if raw_input_username[0] != "@"
        else raw_input_username[1:]
    )
    
    user_for_unban: Optional[User] = await users_dao.get_user_by_username(finished_input_username)

    if user_for_unban and user_for_unban.is_banned:
        await users_dao.unban_user(user_for_unban.user_id)
        await message.answer(f"User @{finished_input_username} unbanned")
        action_logger.warning(f"User $ @{finished_input_username} $ unbanned by creator")
    elif user_for_unban and not user_for_unban.is_banned:
        await message.answer(f"User not banned")
    else:
        await message.answer(f"User not found")

    await state.clear()
