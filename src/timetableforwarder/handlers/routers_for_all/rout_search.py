from aiogram.types import Message
from findlybot.database.database_models import UserConfig
from findlybot.database.dao.users_config_dao import UsersConfigDAO
from aiogram.fsm.context import FSMContext
from findlybot.states.user_states import WaitQuery
from findlybot.utils.check_responses import check_responses
import polib

en_msgs = polib.pofile("locales/en/rout_search.po")
ru_msgs = polib.pofile("locales/ru/rout_search.po")


async def search_rout(message: Message, state: FSMContext) -> None:
    username: str = message.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=username)
    language: str = user_config.language

    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    is_full_responses = await check_responses(username)
    if is_full_responses:
        await message.answer(msgs.find("full_responses_msg").msgstr)
    await message.answer(msgs.find("enter_query_msg").msgstr)
    await state.set_state(WaitQuery.wait_query)
