import json
import re
import base64
from httpx import AsyncClient
import cv2
import numpy as np

from timetableforwarder.utils.get_config import Config, load_config


def _find_table_rows(image_bytes: bytes) -> list[tuple[int, int, int, int]]:
    image_np = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_GRAYSCALE)
    
    # 1. Инвертируем изображение, чтобы линии стали белыми, а фон черным
    # Используем более мягкие параметры adaptiveThreshold
    binary_inv = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 7
    )
    # --- ОТЛАДКА ---
    # Раскомментируйте, чтобы увидеть результат бинаризации.
    # Текст и линии должны быть белыми.
    # cv2.imwrite('debug_binary.png', binary_inv)

    # 2. Ищем горизонтальные линии. Делаем ядро чуть шире.
    # Ширина ядра зависит от ширины изображения, что делает его более гибким.
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (img.shape[1] // 30, 1))
    detected_horizontal = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    # --- ОТЛАДКА ---
    # Раскомментируйте, чтобы увидеть найденные линии.
    # В этом файле вы должны увидеть только белые горизонтальные линии таблицы.
    # cv2.imwrite('debug_lines.png', detected_horizontal)

    contours, _ = cv2.findContours(detected_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return []

    sorted_contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
    
    row_boxes = []
    # Определяем границы строк по промежуткам между найденными линиями
    for i in range(len(sorted_contours) - 1):
        y1_box = cv2.boundingRect(sorted_contours[i])
        y2_box = cv2.boundingRect(sorted_contours[i+1])
        
        row_y = y1_box[1] + y1_box[3] # y-координата начала строки
        row_h = y2_box[1] - row_y      # высота строки
        
        # Фильтруем слишком маленькие промежутки (шум)
        if row_h > 15: 
            row_boxes.append((0, row_y, img.shape[1], row_h))

    return row_boxes

class ImageToTextService:
    def __init__(self, api_key: str, api_url: str = "https://api.perplexity.ai/chat/completions"):
        self._api_key = api_key
        self._api_url = api_url
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }

    async def _recognize_text_from_cell(self, cell_image: np.ndarray, client: AsyncClient) -> str:
        _, buffer = cv2.imencode('.png', cell_image)
        image_base64 = base64.b64encode(buffer).decode("utf-8")

        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text from this image as accurately as possible. Provide only the text."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_base64}"},
                        },
                    ],
                }
            ],
            "max_tokens": 500,
        }

        response = await client.post(self._api_url, json=payload, headers=self._headers)
        response.raise_for_status()
        api_response = response.json()
        return api_response["choices"][0]["message"]["content"].strip()

    async def converting_image_to_text(self, image_bytes: bytes) -> dict:
        config: Config = load_config()
        all_possible_groups = config.groups

        full_image_np = np.frombuffer(image_bytes, np.uint8)
        full_image = cv2.imdecode(full_image_np, cv2.IMREAD_COLOR)

        row_boxes = _find_table_rows(image_bytes)
        print(row_boxes)
        exit(1)
        final_json = {"date": "not found", "timetable": []}

        async with AsyncClient(timeout=120.0) as client:
            header_img = full_image[0:50, :]
            header_text = await self._recognize_text_from_cell(header_img, client)
            date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', header_text)
            if date_match:
                final_json["date"] = date_match.group(0)

            for x, y, w, h in row_boxes:
                row_img = full_image[y:y+h, x:x+w]
                
                group_cell = row_img[:, 0:int(w*0.20)]
                schedule_cell = row_img[:, int(w*0.20):int(w*0.60)]
                rooms_cell = row_img[:, int(w*0.60):]

                group_text = await self._recognize_text_from_cell(group_cell, client)
                group_match = re.search(r'\b(\d{4})\b', group_text)

                if not group_match or int(group_match.group(1)) not in all_possible_groups:
                    continue

                group_number = group_match.group(1)
                schedule_text = await self._recognize_text_from_cell(schedule_cell, client)
                rooms_text = await self._recognize_text_from_cell(rooms_cell, client)

                found_audiences = re.findall(r'\b(\d{2,3})\b', rooms_text)
                
                lessons = []
                lesson_lines = re.findall(r'(\d+)\.\s*(.+)', schedule_text)

                for i, (pos, name) in enumerate(lesson_lines):
                    audience = found_audiences[i] if i < len(found_audiences) else "not found"
                    lessons.append({
                        "position": int(pos),
                        "name": name.strip(),
                        "audience": audience
                    })

                if lessons:
                    final_json["timetable"].append({
                        "group": group_number,
                        "lessons": lessons
                    })

        return final_json
