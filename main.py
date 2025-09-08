import httpx
import asyncio
import json
import base64
import os

async def get_schedule_from_perplexity(image_path: str, api_key: str):
    api_url = "https://api.perplexity.ai/chat/completions"

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt_text = """
    Analyze the attached image, which contains a class schedule written in Russian.
    Extract all information and return it as a single, minified JSON array. Do not include any text outside of the JSON.
    Each object in the array should represent a single group's schedule and must follow this structure:
    {
      "group_info": "Group number and classroom (e.g., '1125, ауд. 43')",
      "lessons": [
        {
          "subject": "The name of the subject",
          "teacher1": "The first teacher from the middle column, including any numbers",
          "teacher2": "The second teacher from the far-right column (if present, otherwise empty string)"
        }
      ]
    }
    Ensure all text values are extracted exactly as they appear in Russian.
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

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            api_response = response.json()
            content_str = api_response["choices"][0]["message"]["content"]
            
            if content_str.startswith("```"):
                content_str = content_str[7:-3].strip()

            return json.loads(content_str)
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Failed to parse API response. Raw content: {api_response['choices']['message']['content']}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    return None

async def main():
    api_key = os.getenv("PPLX_API_KEY")
    if not api_key:
        print("Error: Perplexity API key not found. Set the PPLX_API_KEY environment variable.")
        return

    structured_schedule = await get_schedule_from_perplexity("test.jpg", api_key)
    
    if structured_schedule:
        print(json.dumps(structured_schedule, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
