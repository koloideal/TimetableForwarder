import json
from httpx import AsyncClient
import base64
from timetableforwarder.utils.get_config import Config, load_config


class ImageToTextService:
    def __init__(self, api_key: str, api_url: str = "https://api.perplexity.ai/chat/completions"):
        self._api_key = api_key
        self._api_url = api_url

    async def converting_image_to_text(self, image_path: str) -> list[dict[str, str | list[dict[str, str | int]]]]:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        config: Config = load_config()
        all_possible_groups: list[int] = config.groups

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}"
        }

        prompt_text = f"""
            You are an expert in structured data extraction from images.
            Your task is to analyze an image of a class schedule and generate a JSON object containing information only for the specified groups.

            **Instructions:**

            1.  **Target Groups:** Process only the groups whose numbers are listed here: `{all_possible_groups}`. Completely ignore all other groups in the image.
            2.  **Data Extraction:**
                *   The group number is located in the first column of the table.
                *   For each target group, find its list of subjects in the second column (labeled "Расписание").
            3.  **JSON Formatting:**
                *   Your output must be a valid JSON object—a list of dictionaries.
                *   Each dictionary in the list corresponds to a single group.
                *   The `"group"` key must contain the group number as a string.
                *   The `"lessons"` key must contain a list of dictionaries, where each dictionary represents one lesson.
                    *   The `"position"` key must be the lesson's sequential number (1, 2, 3, etc.), as an integer.
                    *   The `"name"` key must be the subject's name, as a string.
            4.  **What to Ignore:** You are strictly forbidden from including any extraneous information in the JSON:
                *   Names of teachers or curators (e.g., "[translate:Боровик О.В.]", "[translate:куратор]").
                *   Auditorium numbers (e.g., "[translate:ауд. 43]").
                *   Any text from the columns to the right of the subject list.

            **Example of the required JSON structure:**

            [
                {{
                "group": "1125",
                "lessons": [
                {{
                "position": 1,
                "name": "Физика"
                }},
                {{
                "position": 2,
                "name": "Математика"
                }}
                ]
                }},
                {{
                "group": "2125",
                "lessons": [
                {{
                "position": 1,
                "name": "Русский язык"
                }},
                {{
                "position": 2,
                "name": "Физика"
                }}
                ]
                }}
            ]

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
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 4000
        }

        async with AsyncClient(timeout=120.0) as client:
            response = await client.post(self._api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            api_response = response.json()
            content_str = api_response["choices"][0]["message"]["content"]
            
            if content_str.startswith("```"):
                content_str = content_str[7:-3].strip()

            return json.loads(content_str)
                
