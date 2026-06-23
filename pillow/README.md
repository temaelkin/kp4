Лабораторная работа 10. Генерация изображения веб-сервером по запросу
Елькин А.О.
___
# Часть 1
Начнем с создания токена на huggingface.
Далее настроим виртуальное окружение для тестового проекта по генерации изображения, установим библиотеки PIL и huggingface_hub.
По данному в задании промпту попросим GigaCode в режиме агента написать код для генерации тестового изображения.
![[prompt_request.png]]
Выполняем написанный код и получаем изображение.
![[generated_image.png]]
# Часть 2
На руках у нас есть формулировка основного задания и требования к выполнению. Просим ChatGPT написать промпт по тексту задания:
```
напиши мне максимально точный промпт для ии агента для решения следующей задачи. должны быть учтены все нюансы, которые требует задание и общая логика. придерживайся лучших практик python кода. ии агент должен получить пошаговый путь выполнения задания.
```

Полученный промпт:
```Ты — senior Python backend разработчик. Твоя задача — реализовать полностью рабочее веб-приложение на Flask строго по техническому заданию ниже. Не отклоняйся от требований. Не добавляй лишние фреймворки или архитектуры.
---
# 📌 ОБЩАЯ ЦЕЛЬ
Создать Flask веб-приложение с двумя маршрутами:
* `/login` → JSON ответ
* `/makeimage` → генерация изображения через Hugging Face FLUX.1-schnell
---
# 🧱 ТЕХНОЛОГИИ (ОБЯЗАТЕЛЬНО)
Используй только:
* Python 3.10+
* Flask
* Pillow
* huggingface_hub
* python-dotenv
* стандартная библиотека Python
---
# 📁 СТРУКТУРА ПРОЕКТА (ОЖИДАЕМАЯ)
project/
│── app.py
│── templates/
│     └── makeimage.html
│── .env
│── requirements.txt
---
# 🔐 .env
API токен Hugging Face должен храниться здесь:
HF_TOKEN=your_token_here
Нельзя хардкодить токен в коде.
---
# 📦 requirements.txt
Flask
Pillow
huggingface-hub
python-dotenv
---
# 🌐 ROUTES
## 1. GET /login
### Требования:
* возвращает JSON
```
```json
{"author": "1155281"}
```
```
---
## 2. GET /makeimage
### Требования:
* возвращает HTML форму
* форма содержит:
  * width (number)
  * height (number)
  * text (text prompt)
* форма отправляется POST методом
* enctype: `application/x-www-form-urlencoded`
### HTML:
* если есть `message`, показать его над формой красным цветом
* message приходит из backend
---
## 3. POST /makeimage
### Входные данные:
* width
* height
* text
---
# 🧪 ВАЛИДАЦИЯ (СТРОГАЯ)
## 1. Проверка чисел
width и height должны быть int и больше 0
❌ если нет:
* вернуть template
* message = `"Invalid image size"`
---
## 2. Проверка кратности 32
width % 32 == 0 AND height % 32 == 0
❌ если нет:
* вернуть template
* message = `"Width and height must be multiples of 32"`
---
## 3. (опционально, но желательно)
ограничить диапазон:
256 <= width <= 1024
256 <= height <= 1024
иначе → ошибка через message
---
# 🤖 ГЕНЕРАЦИЯ ИЗОБРАЖЕНИЯ
Использовать:
```
```python
from huggingface_hub import InferenceClient
```
```
## Инициализация:
* токен берётся из .env
* обязательно использовать dotenv
---
## Модель:
black-forest-labs/FLUX.1-schnell
---
## Запрос:
```
```python
client.text_to_image(
    prompt=text,
    width=width,
    height=height,
    timeout=30
)
```
```
---
## Обработка результата:
* ответ обычно bytes (PNG/JPEG)
* открыть через Pillow:
```
```python
Image.open(io.BytesIO(data))
```
```
---
## Постобработка:
* convert("RGB")
* resize до (width, height) если нужно
* сохранить в JPEG:
  * quality=85–90
---
## Ответ сервера:
* Content-Type: image/jpeg
* return bytes JPEG
---
# ❗ ОШИБКИ HUGGINGFACE
Любая ошибка:
* timeout
* quota
* model failure
* network error
→ перехватить try/except
→ вернуть template:
message = "Model generation failed: <error>"
---
# 🧾 TEMPLATE (makeimage.html)
Обязательные элементы:
* форма
* поля width, height, text
* submit POST
* вывод message красным
---
# 🧠 ЛОГИКА BACKEND
В POST /makeimage:
1. прочитать form data
2. validate width/height
3. validate multiples of 32
4. try:
   * call HF model
   * convert image
   * return JPEG response
5. except:
   * render template with error message
---
# ⚙️ BEST PRACTICES (ОБЯЗАТЕЛЬНО)
* использовать app factory не обязательно, но код должен быть чистым
* отделить генерацию изображения в функцию generate_image()
* все проверки вынести в validate_size()
* не дублировать код ошибок
* использовать явные return ранним выходом
* не оставлять “магические числа” без объяснения (32, 1024)
---
# 🚀 КРИТЕРИЙ УСПЕХА
Приложение считается корректным если:
* /login возвращает JSON
* /makeimage GET показывает форму
* POST генерирует изображение
* все ошибки корректно отображаются
* HF токен берётся из .env
* изображение возвращается как JPEG
* Pillow используется корректно
* нет хардкода секретов
---
# ⚠️ ЗАПРЕТЫ
* нельзя использовать другие ML API
* нельзя Streamlit / FastAPI
* нельзя хранить токен в коде
* нельзя возвращать base64 вместо image/jpeg
```

Отдаем промпт GigaCode. Через некоторое время он создает структуру и файлы и пишет вывод в чат:

```
Веб-приложение полностью реализовано. Создана следующая структура:
Созданные файлы:

app.py — основной файл Flask приложения с:

/login — возвращает JSON {"author": "1155281"}
/makeimage GET — возвращает HTML форму
/makeimage POST — генерирует изображение через Hugging Face FLUX.1-schnell
Функция validate_size() — строгая валидация размеров
Функция generate_image() — генерация и постобработка изображения через Pillow
Обработка всех ошибок Hugging Face в одном блоке

templates/makeimage.html — HTML форма с:

Полями width, height, text
Отображением ошибок красным цветом
Запросом POST с enctype="application/x-www-form-urlencoded"

requirements.txt — зависимости (Flask, Pillow, huggingface-hub, python-dotenv)

.env — файл для хранения токена Hugging Face (HF_TOKEN)

Валидация:

width/height должны быть int и > 0
width и height должны быть кратны 32
Размеры в диапазоне 256-1024
Запуск: python app.py

Примечание: Перед первым запуском необходимо добавить реальный токен Hugging Face в файл .env.
```
# Часть 3
Установим через pip библиотеки flask и dotenv.
Добавим наш токен в .env файл и запустим приложение в первый раз.
![[app_front_page.png]]
Находим первую проблему сгенерированного кода.
![[error_one.png]]
Это очевидно, так как GigaCode придумал аргумент.
![[unknown_parameter.png]]
Просим его исправить, но чтобы ничего не сломалось, проверим самостоятельно документацию huggingface на использование таймаутов. Правильный синтаксис отправим GigaCode.
![[fix_request.png]]
```
Ошибки исправлены:

- Убрал timeout=30 из вызова client.text_to_image() — этот параметр не поддерживается этим методом
- Добавил InferenceTimeoutError в импорт из huggingface_hub
- Инициализировал client с timeout=30 как параметром конструктора
- Обернул вызов client.text_to_image() в блок try/except для перехвата InferenceTimeoutError
- При таймауте raising исключение с понятным сообщением

Теперь приложение должно работать корректно.
```

Проверим работу приложения.
Получаем новую ошибку.
![[error_two.png]]
Тут еще проще - такая же ошибка возникала при первой итерации генерации тестового кода в начале лабораторной работы. ИИ обращается к устаревшей модели FLUX.1-dev, которую нужно заменить на актуальную FLUX.1-schnell. Попросим исправить.
```
Исправлено! Добавил параметр model="black-forest-labs/FLUX.1-schnell" в вызов client.text_to_image(). Теперь приложение будет использовать правильную модель вместо устаревшей FLUX.1-dev.
```

Новая ошибка.
 ![[error_three.png]]
Просим исправить.
```
Проблема в том, что client.text_to_image() может возвращать не bytes, а уже объект PIL.Image.Image. Проверю документацию и исправлю код:
Исправлено! Добавил проверку типа в функцию generate_image():

# Если image уже является PIL Image объектом, используем его напрямую
if isinstance(image, Image.Image):
    img = image
else:
    # Иначе открываем как bytes
    img = Image.open(io.BytesIO(image))

Теперь код будет работать как с bytes, так и с объектом PIL.Image.Image, который возвращает text_to_image() в вашем случае.
```

Запустим приложение снова.
Успех.
![[final_image.png]]

