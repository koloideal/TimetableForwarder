from aiogram.types import Message
from timetableforwarder.database.database_models import User
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.utils.get_config import Config, load_config

config: Config = load_config()
creator_id: str = config.creator_id


async def start_rout(message: Message, users_dao: UsersDAO) -> None:
    username: str = message.from_user.username
    user_id: int = message.from_user.id

    creator_case: bool = user_id == creator_id
    user_case: bool = user_id != creator_id

    if creator_case:
        await message.answer("Hello creator")

    elif user_case:
        await message.answer(
            "Hello loh",
            disable_web_page_preview=True,
        )

    await users_dao.create_user(
        user_id=user_id,
        username=username
    )
