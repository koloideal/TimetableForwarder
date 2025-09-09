import polib
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from timetableforwarder.database.database_models import UserConfig
from timetableforwarder.database.dao.users_config_dao import UsersConfigDAO

en_msgs = polib.pofile("locales/en/rout_config.po")
ru_msgs = polib.pofile("locales/ru/rout_config.po")


async def config_rout(message: types.Message) -> None:
    username: str = message.from_user.username
    user_config: UserConfig = UsersConfigDAO().get_all_configs(username=username)
    language: str = user_config.language

    on_or_off: dict = {
        'ON': 'OFF',
        'OFF': 'ON'
    }
    en_or_ru: dict = {
        'EN': 'lang_RU',
        'RU': 'lang_EN'
    }

    match language:
        case "RU":
            msgs = ru_msgs
        case "EN":
            msgs = en_msgs
        case _:
            msgs = en_msgs

    lang_msg = msgs.find("lang_msg").msgstr
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

    await message.answer(
        msgs.find("config_msg").msgstr.format(max_size=max_size),
        reply_markup=keyboard,
    )
