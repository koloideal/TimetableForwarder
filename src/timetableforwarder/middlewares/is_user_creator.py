from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from timetableforwarder.utils.get_config import Config, load_config


config: Config = load_config()
creator_id: int = config.creator_id


class RejectNotCreatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not event.text:
            return
        
        user_id: int = event.from_user.id

        creator_commands = ['/ban_user', '/unban_user', '/list_banned']

        if event.text.strip() in creator_commands:
            if user_id == creator_id:
                return await handler(event, data)
            else:
                await event.answer("Unknwon command, enter /start")
        else:
            return await handler(event, data)