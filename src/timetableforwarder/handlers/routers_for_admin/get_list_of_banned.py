from aiogram.types import Message
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.database.database_models import User


async def get_list_of_banned(message: Message, users_dao: UsersDAO) -> None:
    banned_users: list[User] = await users_dao.get_banned_users()
    if not banned_users:
        await message.answer('🐸 Заблокированных юзеров <b>нет</b>')
        return

    res_text = '💂 <b>Список заблокированных юзеров:</b>\n\n'
    for banned_user in banned_users:
        res_text += f'👮 <b><i>@{banned_user.username}</i></b>\n'

    res_text += f'\n<blockquote>Всего: <b>{len(banned_users)}</b> 🔝</blockquote>'

    await message.answer(res_text, parse_mode='HTML')

