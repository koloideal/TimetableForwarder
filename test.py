from PIL import Image
import numpy as np

# Предположим, у вас есть массив NumPy 'denoised_img'
denoised_img = 255 * np.ones((500, 800), dtype=np.uint8)

# Сначала конвертируем его в объект Pillow
pil_image = Image.fromarray(denoised_img)

# Задаем координаты для обрезки (left, upper, right, lower)
crop_box = (50, 100, 250, 250) # x1, y1, x2, y2

# Выполняем нарезку
cropped_pil_image = pil_image.crop(crop_box)

# Сохраняем результат
cropped_pil_image.save('cropped_pillow.png')

print(f"Оригинальный размер: {pil_image.size}")
print(f"Размер вырезанного изображения: {cropped_pil_image.size}")
