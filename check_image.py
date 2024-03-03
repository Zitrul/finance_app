import base64
from io import BytesIO
from PIL import Image

# Получаем base64 строку из вашего кода Node.js
base64_data = ""

# Декодируем base64 строку в байты
bytes_data = base64.b64decode(base64_data)

# Создаем объект BytesIO из байтов
image_bytes = BytesIO(bytes_data)

# Читаем изображение из BytesIO
image = Image.open(image_bytes)

# Сохраняем изображение
image.save("output_image.png")
