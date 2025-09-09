from aiogram.types import Message
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.database.database_models import User


async def get_list_of_all_users(message: Message, users_dao: UsersDAO) -> None:
    all_users: list[User] = await users_dao.get_all_users()
    if not all_users:
        await message.answer('🐸 Юзеров <b>нет</b>')
        return

    res_text = '👥 <b>Список всех юзеров:</b>\n\n'
    for user in all_users:
        if user.is_banned:
            res_text += f'👮 <b><i>@{user.username}</i></b> <i>(заблокирован)</i>\n'
        else:
            res_text += f'👤 <b><i>@{user.username}</i></b>\n'

    res_text += f'\n<blockquote>Всего: <b>{len(all_users)}</b> 🔝</blockquote>'

    await message.answer(res_text, parse_mode='HTML')
