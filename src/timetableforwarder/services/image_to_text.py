import json
from httpx import AsyncClient
import base64


class ImageToTextService:
    def __init__(self, api_key: str, api_url: str = "https://api.perplexity.ai/chat/completions"):
        self._api_key = api_key
        self._api_url = api_url

    async def converting_image_to_text(self, image_path: str):
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}"
        }

        prompt_text = """
            First, analyze the attached image to determine if it is a class schedule. The schedule is written in Russian.

            If the image is NOT a class schedule, you MUST return only the following JSON object:
            {"error": "Image does not contain a valid class schedule."}

            If the image IS a class schedule, extract all its information and return it as a single, minified JSON array.
            Each object in the array should represent one group's schedule and must follow this exact structure:
            {
            "group_info": "Group number and classroom (e.g., '1125, ауд. 43')",
            "lessons": [
                {
                "subject": "The name of the subject",
                "teacher1": "The first teacher from the middle column, including any numbers",
                "teacher2": "The second teacher from the far-right column (if present, otherwise an empty string)"
                }
            ]
            }
            
            CRITICAL: Your entire response must be only the raw JSON, with no additional text, explanations, or markdown formatting like ```
        """

        payload = {
            "model": "sonar",
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
                
