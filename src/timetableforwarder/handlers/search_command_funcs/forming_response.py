import json
import polib
from aiogram.types import Message, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from findlybot.database.database_models import UserConfig
from findlybot.database.dao.users_config_dao import UsersConfigDAO
from findlybot.utils.reformat_name import reformat_name
from findlybot.handlers.custom_callback_data.swipe_items_callback_data import SwipeItemsCallbackData

en_msgs = polib.pofile("locales/en/forming_response.po")
ru_msgs = polib.pofile("locales/ru/forming_response.po")


async def forming_response(message: Message, query: str, wait_message: Message):
    requestor_username: str = message.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=requestor_username)
    language: str = user_config.language

    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    with open(f"local_data/products_data/{requestor_username}/{query}.json", "r") as response:
        api_json_data: dict = json.load(response)

    await wait_message.delete()

    for marketplace in api_json_data:
        item = api_json_data[marketplace][0]
        link = item["link"]
        image_link = item["image"]
        name = item["name"]
        price = item["price"]
        ids = item["id"]

        res_name = await reformat_name(name.replace("_", " "), query.replace("_", " "))

        if image_link == "images/placeholder.png":
            image = FSInputFile("local_data/images/placeholder.jpg")
        else:
            image = FSInputFile(
                f"local_data/images/{requestor_username}/{query}/{marketplace}/{name}.jpg"
            )

        size_of_products = len(api_json_data[marketplace])

        if size_of_products > 1:
            builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
            builder.add(
                InlineKeyboardButton(
                    text="➡",
                    callback_data=SwipeItemsCallbackData(
                        marketplace=marketplace,
                        current_item_id=int(ids) + 1,
                        query=query,
                    ).pack(),
                ),
            )
            await message.answer_photo(
                image,
                caption=msgs.find("many_cards_msg").msgstr.format(
                    marketplace=marketplace,
                    link=link,
                    res_name=res_name,
                    price=price,
                    ids=str(int(ids) + 1),
                    size_of_products=size_of_products,
                ),
                reply_markup=builder.as_markup(),
            )

        else:
            await message.answer_photo(
                image,
                caption=msgs.find("one_card_msg").msgstr.format(
                    marketplace=marketplace,
                    link=link,
                    res_name=res_name,
                    price=price,
                    ids=ids,
                ),
            )
