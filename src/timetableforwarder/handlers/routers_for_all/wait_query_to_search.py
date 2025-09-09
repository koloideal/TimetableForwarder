from logging import Logger, getLogger
import os
import re
import time
import typing
import polib
from findlybot.database.database_models import UserConfig
from findlybot.exceptions.request_exceptions import TooLongQueryForSearchError
from findlybot.handlers.search_command_funcs.api_data_to_dump import api_data_to_dump
from findlybot.handlers.search_command_funcs.forming_response import forming_response
from aiogram.types import Message
from findlybot.database.dao.users_config_dao import UsersConfigDAO
from aiogram.fsm.context import FSMContext
from httpx import Response, HTTPError
from findlybot.get_api_data.get_api_data import get_api_data
import json
if typing.TYPE_CHECKING:
    from _typeshed import SupportsWrite


en_msgs = polib.pofile("locales/en/wait_query_to_search.po")
ru_msgs = polib.pofile("locales/ru/wait_query_to_search.po")

main_logger: Logger = getLogger('root')
action_logger: Logger = getLogger('action_logger')


async def get_query_to_search_rout(message: Message, state: FSMContext) -> None:
    query: str = message.text.strip()
    requestor_username: str = message.from_user.username
    try:
        if len(query) > 25:
            raise TooLongQueryForSearchError(len(query))
        query_with_plus: str = re.sub(r" ", "+", query)
        user_config: UserConfig = UsersConfigDAO().get_all_configs(requestor_username)
        language: str = user_config.language

        match language:
            case "RU":
                msgs = ru_msgs
            case "EN":
                msgs = en_msgs
            case _:
                msgs = en_msgs
        wait_message: Message = await message.answer(msgs.find("search_in_progress").msgstr)

        os.makedirs(f"local_data/products_data/{requestor_username}", exist_ok=True)
        os.makedirs(f"local_data/images/{requestor_username}", exist_ok=True)

        max_size: int = user_config.max_size
        only_new: str = user_config.only_new
        price_filter: str = user_config.price_filter
        name_filter: str = user_config.name_filter


        api_data: Response = await get_api_data(
            query_with_plus,
            max_size=max_size,
            only_new=only_new,
            price_filter=price_filter,
            name_filter=name_filter
        )
        if not api_data:
            action_logger.error(f"Unsuccessful /search request from a user with username $ @{requestor_username} $")
            main_logger.error(f"Unsuccessful /search request from a user with username $ @{requestor_username} $")

            await message.answer("Unsuccessful request, please wait or contact @kolo_id")

        response_data = api_data.json()

        products_data: dict[str, dict] = response_data["products_data"]
        metadata: dict[str | dict] = response_data["request_metadata"]
        escaping_query: str = re.sub(r"[ /\\]", "_", metadata["request_args"]["query"])

        action_logger.warning(f"Request from $ @{requestor_username} $ with $ {metadata['size_of_products']['all']} $ products")

        if not products_data:
            await message.answer(msgs.find("empty_response").msgstr)
            await state.clear()
            return
        else:
            current_response = {"name": escaping_query, "date": time.time()}
            if os.path.exists(f"local_data/images/{requestor_username}/responses.json"):
                data = json.load(open(f"local_data/images/{requestor_username}/responses.json"))
                data["responses"].append(current_response)
                with open(
                    f"local_data/images/{requestor_username}/responses.json", "w"
                ) as file: # type: SupportsWrite[str]
                    json.dump(data, file, indent=4)
            else:
                with open(
                    f"local_data/images/{requestor_username}/responses.json", "w"
                ) as file: # type: SupportsWrite[str]
                    data = {"responses": [current_response]}
                    json.dump(data, file, indent=4)

            to_dump_data: dict = await api_data_to_dump(
                products_data, requestor_username, escaping_query
            )

            with open(
                f"local_data/products_data/{requestor_username}/{escaping_query}.json", "w"
            ) as file: # type: SupportsWrite[str]
                json.dump(to_dump_data, file, indent=4, ensure_ascii=False)

    except HTTPError as e:
        main_logger.error(e)
    except TooLongQueryForSearchError as e:
        action_logger.error(f"{e} from user {requestor_username}")
        await message.answer(str(e))
    else:
        await forming_response(
            message=message,
            query=escaping_query,
            wait_message=wait_message,
        )
    finally:
        await state.clear()
