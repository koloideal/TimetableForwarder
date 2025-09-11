from aiogram.types import Message
from timetableforwarder.services.image_to_text import ImageToTextService
from timetableforwarder.utils.get_config import Config


async def handle_channel_photo(message: Message, config: Config) -> None:
    if message.caption:
        return

    # image_to_text_service = ImageToTextService(api_key=config.plpx_key)
    # response = image_to_text_service.converting_image_to_text("test.jpg")
    response = [
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
                {"name": "Иностранный язык (профессиональная лексика)", "position": 2},
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
                {"name": "Математика и профессиональная деятельность", "position": 3},
                {"name": "Кураторский час", "position": 4},
            ],
        },
        {
            "group": "2123",
            "lessons": [
                {"name": "Алгебра и элементы математической статистики", "position": 1},
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
    ]
