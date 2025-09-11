import json
from httpx import AsyncClient
import base64
from timetableforwarder.utils.get_config import Config, load_config


class ImageToTextService:
    def __init__(
        self, api_key: str, api_url: str = "https://api.perplexity.ai/chat/completions"
    ):
        self._api_key = api_key
        self._api_url = api_url

    async def converting_image_to_text(
        self, image_path: str
    ) -> list[dict[str, str | list[dict[str, str | int]]]]:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        config: Config = load_config()
        all_possible_groups: list[int] = config.groups

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }

        prompt_text = f"""
            You are an expert in structured data extraction from images.
            Your task is to analyze an image of a class schedule and generate a single, valid JSON object that strictly follows the specified structure.

            **Instructions:**

            1.  **Extract the Date:** Find the date in the image's main header (e.g., "НА 06.09.2025") and format it as "DD.MM.YYYY".
            2.  **Target Groups:** Process only the groups whose numbers are listed here: `{all_possible_groups}`. Completely ignore all other groups in the image.
            3.  **Data Extraction for Each Group:**
                *   The **group number** is in the first column.
                *   The **list of subjects** is in the second column (labeled "Расписание").
                *   The **audience number** is a two-digit number typically found in the columns to the right of the subject list. It might be next to a teacher's name. If a two-digit audience number for a lesson cannot be found, you must use the string value `"not found"`.
            4.  **JSON Formatting:**
                *   Your entire output must be a single JSON object.
                *   This object must have a root key `"date"` containing the extracted date string.
                *   The second root key must be `"timetable"`, containing a list of dictionaries. Each dictionary in this list corresponds to a single group.
                *   Each group dictionary must contain:
                    *   `"group"`: The group number as a string.
                    *   `"lessons"`: A list of lesson dictionaries.
                *   Each lesson dictionary must contain:
                    *   `"position"`: The lesson's sequential number (1, 2, etc.) as an integer.
                    *   `"name"`: The subject's name as a string.
                    *   `"audience"`: The two-digit audience number as a string, or `"not found"` if it's missing.
            5.  **What to Ignore:** You are strictly forbidden from including any extraneous information in the JSON, such as names of teachers or curators (e.g., "[translate:Боровик О.В.]", "[translate:куратор]").

            **Example of the required JSON structure:**

            {
                "date": "06.09.2025",
                "timetable": [
                {
                "group": "1125",
                "lessons": [
                {
                "position": 1,
                "name": "Физика",
                "audience": "not found"
                },
                {
                "position": 2,
                "name": "Математика",
                "audience": "37"
                }
                ]
                },
                {
                "group": "2125",
                "lessons": [
                {
                "position": 1,
                "name": "Русский язык",
                "audience": "not found"
                },
                {
                "position": 2,
                "name": "Физика",
                "audience": "43"
                }
                ]
                }
                ]
            }

            text

            **Final Output:**
            Provide **only** the JSON object as your response, without any comments, explanations, or introductory text.
        """

        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 4000,
        }

        async with AsyncClient(timeout=120.0) as client:
            response = await client.post(self._api_url, json=payload, headers=headers)
            response.raise_for_status()

            api_response = response.json()
            content_str = api_response["choices"][0]["message"]["content"]

            if content_str.startswith("```"):
                content_str = content_str[7:-3].strip()

            return json.loads(content_str)
