from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.database.database_models import User


class RejectBlockedUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not event.text:
            return
        
        users_dao = await data["dishka_container"].get(UsersDAO)
        banned_users: list[User] = await users_dao.get_banned_users()

        banned_users_ids: list[int] = [banned_user.user_id for banned_user in banned_users]
        user_id: str = event.from_user.id

        if user_id in banned_users_ids:
            await event.answer(
                "🚫 <b>Вы заблокированы</b>\n\n"
                "Ваш доступ к боту ограничен. Для разблокировки обратитесь к создателю @kolo_id\n\n"
                "<i>made by kolo</i>",
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
        else:
            return await handler(event, data)