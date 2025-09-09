import json
from html import escape
import polib

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InputMediaPhoto,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from findlybot.database.database_models import UserConfig
from findlybot.states.user_states import WaitMaxSize
from findlybot.database.dao.users_config_dao import UsersConfigDAO
from findlybot.utils.reformat_name import reformat_name
from findlybot.handlers.custom_callback_data.swipe_items_callback_data import SwipeItemsCallbackData


en_msgs = polib.pofile("locales/en/callback_query.po")
ru_msgs = polib.pofile("locales/ru/callback_query.po")


async def callback_query_swipe_items(callback: CallbackQuery,
                                     callback_data: SwipeItemsCallbackData):
    current_marketplace = callback_data.marketplace
    current_item_id = callback_data.current_item_id
    requestor_username = callback.from_user.username

    query = callback_data.query

    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=requestor_username)
    language: str = user_config.language

    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    with open(
        f"local_data/products_data/{requestor_username}/{query}.json", "r"
    ) as response:
        api_json_data: dict = json.load(response)

    current_item_link = api_json_data[current_marketplace][current_item_id]["link"]
    current_item_image_link = api_json_data[current_marketplace][current_item_id]["image"]
    current_item_price = api_json_data[current_marketplace][current_item_id]["price"]
    current_item_name = api_json_data[current_marketplace][current_item_id]["name"]
    size_of_products = len(api_json_data[current_marketplace])

    max_item_id = max([x["id"] for x in api_json_data[current_marketplace]])

    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if 0 < current_item_id < max_item_id:
        builder.add(
            InlineKeyboardButton(
                text="⬅",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace,
                    current_item_id=current_item_id - 1,
                    query=query,
                ).pack(),
            ),
        )
        builder.add(
            InlineKeyboardButton(
                text="➡",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace,
                    current_item_id=current_item_id + 1,
                    query=query,
                ).pack(),
            ),
        )

    elif current_item_id == 0:
        builder.add(
            InlineKeyboardButton(
                text="➡",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace,
                    current_item_id=1,
                    query=query,
                ).pack(),
            ),
        )

    elif current_item_id == max_item_id:
        builder.add(
            InlineKeyboardButton(
                text="⬅",
                callback_data=SwipeItemsCallbackData(
                    marketplace=current_marketplace,
                    current_item_id=max_item_id - 1,
                    query=query,
                ).pack(),
            ),
        )

    if current_item_image_link == "images/placeholder.png":
        image = FSInputFile("local_data/images/placeholder.jpg")
    else:
        image = FSInputFile(
            f"local_data/images/{requestor_username}/{query}/{current_marketplace}/{current_item_name}.jpg"
        )

    res_name = await reformat_name(current_item_name.replace("_", " "), query)

    await callback.message.edit_media(
        InputMediaPhoto(
            media=image,
            caption=msgs.find("many_cards_msg").msgstr.format(
                current_marketplace=current_marketplace,
                current_item_link=current_item_link,
                res_name=res_name,
                current_item_price=current_item_price,
                current_item_id=current_item_id + 1,
                size_of_products=size_of_products,
            ),
        ),
        reply_markup=builder.as_markup(),
    )


async def callback_query_change_config(callback: CallbackQuery):
    callback_data = callback.data
    username: str = callback.from_user.username
    user_config: UsersConfigDAO = UsersConfigDAO()
    match '_'.join(callback_data.split('_')[:-1]):
        case 'only_new':
            only_new: str = callback_data.split('_')[-1].lower()
            user_config.change_only_new_config(only_new=only_new,
                                               username=username)
        case 'lang':
            language: str = callback_data.split('_')[-1]
            user_config.change_lang_config(language=language,
                                           username=username)
        case 'name_filter':
            name_filter: str = callback_data.split('_')[-1].lower()
            user_config.change_name_filter_config(name_filter=name_filter,
                                                  username=username)
        case 'price_filter':
            price_filter: str = callback_data.split('_')[-1].lower()
            user_config.change_price_filter_config(price_filter=price_filter,
                                                   username=username)

    on_or_off: dict = {
        'ON': 'OFF',
        'OFF': 'ON'
    }
    en_or_ru: dict = {
        'EN': 'lang_RU',
        'RU': 'lang_EN'
    }

    user_config: UserConfig = user_config.get_all_configs(username=username)
    language: str = user_config.language

    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    lang_msg = msgs.find(f"lang_msg").msgstr
    lang_callback_data = en_or_ru[language]

    only_new: str = user_config.only_new
    only_new_msg = msgs.find(f"only_new_{only_new}_msg").msgstr
    only_new_callback_data = "only_new_" + on_or_off[only_new.upper()]

    name_filter: str = user_config.name_filter
    name_filter_msg = msgs.find(f"name_filter_{name_filter}_msg").msgstr
    name_filter_callback_data = "name_filter_" + on_or_off[name_filter.upper()]

    price_filter: str = user_config.price_filter
    price_filter_msg = msgs.find(f"price_filter_{price_filter}_msg").msgstr
    price_filter_callback_data = "price_filter_" + on_or_off[price_filter.upper()]

    max_size: int = user_config.max_size
    max_size_msg = msgs.find("ch_max_size_msg").msgstr

    buttons: list = [
        [
            InlineKeyboardButton(
                text=only_new_msg, callback_data=only_new_callback_data
            )
        ],
        [
            InlineKeyboardButton(
                text=name_filter_msg, callback_data=name_filter_callback_data
            )
        ],
        [
            InlineKeyboardButton(
                text=price_filter_msg, callback_data=price_filter_callback_data
            )
        ],
        [
            InlineKeyboardButton(
                text=lang_msg, callback_data=lang_callback_data
            )
        ],
        [
            InlineKeyboardButton(
                text=max_size_msg, callback_data="change_max_size",
            )
        ],
    ]

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text=msgs.find("config_msg").msgstr.format(max_size=max_size),
                                     reply_markup=keyboard)


async def callback_query_max_size(callback: CallbackQuery, state: FSMContext):
    text: str = escape("0 < max_size <= 40")
    username: str = callback.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=username)
    language: str = user_config.language

    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs
    await callback.message.answer(msgs.find("max_size_msg").msgstr.format(text=text))
    await state.set_state(WaitMaxSize.wait_max_size)
