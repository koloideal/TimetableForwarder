from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from timetableforwarder.services.image_to_text import ImageToTextService
from timetableforwarder.utils.get_config import Config
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.database.dao.subscribed_groups_dao import SubscribedGroupsDAO


def build_group_message(group: str, lessons: list[dict], date: str) -> str:
    header = (
        f"<b>📅 Расписание на <u>{date}</u></b>\n"
        f"<b>Группа: <u>{group}</u></b>\n\n"
    )
    if not lessons:
        return header + "<blockquote><i>Нет занятий</i></blockquote>"
    lines = []
    for item in sorted(lessons, key=lambda x: x.get("position", 0)):
        name = item.get("name", "—")
        pos = item.get("position", 0)
        lines.append(f"{pos}. <b>{name}</b>\n")
    return header + f"<blockquote>{'\n'.join(lines)}</blockquote>\n"


async def handle_channel_photo(
    message: Message,
    config: Config,
    users_dao: UsersDAO,
    subscribed_groups_dao: SubscribedGroupsDAO,
) -> None:
    if message.caption:
        return

    # image_to_text_service = ImageToTextService(api_key=config.plpx_key)
    # response = image_to_text_service.converting_image_to_text("test.jpg")
    response = {
        "date": "03.05.2025",
        "timetable": [
            {
                "group": "1125",
                "lessons": [
                    {"name": "Физика", "position": 1},
                    {"name": "Физическая культура и здоровье, 1 уч.ч", "position": 2},
                    {"name": "Русский язык", "position": 3},
                    {"name": "Кураторский час", "position": 4},
                ],
            },
            {
                "group": "1124",
                "lessons": [
                    {"name": "Физическая культура и здоровье, 1 уч.ч", "position": 1},
                    {"name": "Кураторский час", "position": 2},
                    {"name": "Защита населения и территорий от ЧС", "position": 3},
                    {"name": "Охрана труда", "position": 4},
                ],
            },
            {
                "group": "1123",
                "lessons": [
                    {"name": "Бухгалтерский учет", "position": 1},
                    {"name": "Анализ хозяйственной деятельности", "position": 2},
                    {"name": "Информационные технологии", "position": 3},
                ],
            },
            {
                "group": "1225",
                "lessons": [
                    {"name": "Физика", "position": 1},
                    {"name": "Кураторский час", "position": 2},
                    {"name": "История Беларуси и государственности", "position": 3},
                ],
            },
            {
                "group": "1224",
                "lessons": [
                    {"name": "Бухгалтерский учет", "position": 1},
                    {
                        "name": "Иностранный язык (профессиональная лексика)",
                        "position": 2,
                    },
                    {"name": "Основы маркетинга", "position": 3},
                ],
            },
            {
                "group": "2125",
                "lessons": [
                    {"name": "Кураторский час", "position": 1},
                    {"name": "Информатика", "position": 2},
                    {"name": "Физическая культура и здоровье, 1 уч.ч", "position": 3},
                    {"name": "Допризывная (медицинская) подготовка", "position": 4},
                ],
            },
            {
                "group": "2124",
                "lessons": [
                    {
                        "name": "История Беларуси в контексте всемирной истории",
                        "position": 1,
                    },
                    {"name": "Охрана труда", "position": 2},
                    {
                        "name": "Математика и профессиональная деятельность",
                        "position": 3,
                    },
                    {"name": "Кураторский час", "position": 4},
                ],
            },
            {
                "group": "2123",
                "lessons": [
                    {
                        "name": "Алгебра и элементы математической статистики",
                        "position": 1,
                    },
                    {"name": "Информатика", "position": 2},
                    {"name": "Программное обеспечение", "position": 3},
                    {"name": "Кураторский час", "position": 4},
                ],
            },
            {
                "group": "2122",
                "lessons": [
                    {
                        "name": "История мировой и древнейшей деятельности отраслей",
                        "position": 1,
                    },
                    {
                        "name": "Основы проектирования создания информационных систем и "
                        "СУБД",
                        "position": 2,
                    },
                    {"name": "Кураторский час", "position": 3},
                ],
            },
            {
                "group": "3125",
                "lessons": [
                    {"name": "Химия", "position": 1},
                    {"name": "Русский язык", "position": 2},
                    {"name": "Физическая культура и здоровье, 1 уч.ч", "position": 3},
                    {"name": "Кураторский час", "position": 4},
                ],
            },
            {
                "group": "3124",
                "lessons": [
                    {"name": "Иностранный язык", "position": 1},
                    {"name": "Стилистика б.я.", "position": 2},
                    {
                        "name": "История Беларуси в контексте всемирной истории",
                        "position": 3,
                    },
                    {"name": "Кураторский час", "position": 4},
                    {"name": "Физическая культура и здоровье, 1 уч.ч", "position": 5},
                ],
            },
            {
                "group": "3123",
                "lessons": [
                    {"name": "Медицинская подготовка", "position": 1},
                    {"name": "История мировой государственности", "position": 2},
                    {"name": "Физическая культура и здоровье, 1 уч.ч", "position": 3},
                    {"name": "Кураторский час", "position": 4},
                ],
            },
            {
                "group": "4125",
                "lessons": [
                    {"name": "Основы гостиничных услуг", "position": 1},
                    {
                        "name": "История Беларуси в контексте всемирной истории",
                        "position": 2,
                    },
                    {"name": "Экономика гостиничного хозяйства", "position": 3},
                ],
            },
            {
                "group": "4124",
                "lessons": [
                    {"name": "Практикум по устной и письменной речи", "position": 1},
                    {"name": "Основы гостиничных услуг", "position": 2},
                    {"name": "Информационные технологии", "position": 3},
                ],
            },
            {
                "group": "4123",
                "lessons": [
                    {"name": "Физическая культура и здоровье, 1 уч.ч", "position": 1},
                    {"name": "Основы гостиничных услуг", "position": 2},
                    {"name": "Кураторский час", "position": 3},
                ],
            },
            {
                "group": "5125",
                "lessons": [
                    {"name": "Физическая культура и здоровье, 1 уч.ч", "position": 1},
                    {"name": "Кураторский час", "position": 2},
                ],
            },
        ],
    }

    date_str: str = response.get("date", "—")
    timetable = response.get("timetable", [])
    group_to_text: dict[str, str] = {
        entry["group"]: build_group_message(entry["group"], entry.get("lessons", []), date_str)
        for entry in timetable
    }

    users = await users_dao.get_all_users()

    for user in users:
        subs_str = user.subscribed_groups
        if not subs_str:
            continue
        groups = [g for g in subs_str.split(":") if g]
        texts = [group_to_text[g] for g in groups if g in group_to_text]
        if not texts:
            continue
        if len(texts) == 1:
            line_separate = '\n'
        else:
            line_separate = '\n\n'
        final_text = "\n\n".join(texts) + f"{line_separate}<b><i>made by kolo</i></b>"
        try:
            await message.bot.send_message(
                chat_id=user.user_id, text=final_text, parse_mode="HTML"
            )
        except (TelegramForbiddenError, TelegramBadRequest):
            continue

    subscribed_groups = await subscribed_groups_dao.get_all_groups()

    for rec in subscribed_groups:
        target_group = str(rec.subscribed_group)
        chat_id = rec.group_id
        if not target_group:
            continue
        text = group_to_text.get(target_group)
        text += "\n<b><i>made by kolo</i></b>"
        try:
            sent = await message.bot.send_message(
                chat_id=chat_id, text=text, parse_mode="HTML"
            )
            await message.bot.pin_chat_message(
                chat_id=chat_id, message_id=sent.message_id, disable_notification=True
            )
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
