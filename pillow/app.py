import io
import os
from flask import Flask, request, render_template, make_response
from dotenv import load_dotenv
from PIL import Image
from huggingface_hub import InferenceClient, InferenceTimeoutError

# Загрузка переменных из .env
load_dotenv()

# Константы для валидации
MIN_SIZE = 256
MAX_SIZE = 1024
MULTIPLE_OF = 32

# Инициализация Flask приложения
app = Flask(__name__)

# Инициализация Hugging Face клиента
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables")
client = InferenceClient(token=HF_TOKEN, timeout=30)


def validate_size(width, height):
    """
    Валидация размеров изображения.
    Возвращает None если все ок, или строку с сообщением об ошибке.
    """
    # Проверка: должны быть целыми числами и больше 0
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        return "Invalid image size"
    
    # Проверка: кратность 32
    if width % MULTIPLE_OF != 0 or height % MULTIPLE_OF != 0:
        return "Width and height must be multiples of 32"
    
    # Проверка: диапазон
    if width < MIN_SIZE or width > MAX_SIZE or height < MIN_SIZE or height > MAX_SIZE:
        return f"Size must be between {MIN_SIZE} and {MAX_SIZE}"
    
    return None


def generate_image(prompt, width, height):
    """
    Генерация изображения через Hugging Face FLUX.1-schnell.
    Возвращает bytes в формате JPEG или вызывает исключение.
    """
    try:
        # Вызов модели с указанием модели
        image = client.text_to_image(
            prompt=prompt,
            width=width,
            height=height,
            model="black-forest-labs/FLUX.1-schnell"
        )
    except InferenceTimeoutError:
        raise Exception("Inference timed out after 30s")
    
    # Если image уже является PIL Image объектом, используем его напрямую
    if isinstance(image, Image.Image):
        img = image
    else:
        # Иначе открываем как bytes
        img = Image.open(io.BytesIO(image))
    
    # Конвертация в RGB (если RGBA или другой режим)
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # Ресайз до точных размеров (на всякий случай)
    if img.size != (width, height):
        img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    # Сохранение в JPEG
    output = io.BytesIO()
    img.save(output, format="JPEG", quality=85)
    
    return output.getvalue()


@app.route("/login", methods=["GET"])
def login():
    """Возвращает JSON с автором."""
    return {"author": "1155281"}


@app.route("/makeimage", methods=["GET"])
def makeimage_get():
    """Возвращает форму для генерации изображения."""
    return render_template("makeimage.html", message=None)


@app.route("/makeimage", methods=["POST"])
def makeimage_post():
    """Обрабатывает POST запрос на генерацию изображения."""
    # Чтение данных из формы
    width_str = request.form.get("width", "")
    height_str = request.form.get("height", "")
    text = request.form.get("text", "").strip()
    
    # Попытка конвертации в int
    try:
        width = int(width_str)
        height = int(height_str)
    except (ValueError, TypeError):
        return render_template("makeimage.html", message="Invalid image size")
    
    # Валидация размеров
    error = validate_size(width, height)
    if error:
        return render_template("makeimage.html", message=error)
    
    # Генерация изображения
    try:
        image_data = generate_image(text, width, height)
        
        # Возврат изображения как JPEG
        response = make_response(image_data)
        response.headers.set("Content-Type", "image/jpeg")
        response.headers.set("Content-Disposition", "inline", filename="generated_image.jpg")
        return response
        
    except Exception as e:
        return render_template("makeimage.html", message=f"Model generation failed: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
