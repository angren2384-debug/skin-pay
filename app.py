import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="skin.pay - Apple Pay Skins UZ")

# Абсолютный путь к корню проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Настройка безопасной папки для загрузок
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Проверяем и создаем папку static
STATIC_DIR = os.path.join(BASE_DIR, "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)

# Подключаем статику через абсолютный путь
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Автоматическая загрузка карточек из папки static/cards с абсолютным путем
CARDS_DB = []
CARDS_DIR = os.path.join(BASE_DIR, "static", "cards")

if os.path.exists(CARDS_DIR):
    print(f"INFO: Папка найдена: {CARDS_DIR}")
    for filename in os.listdir(CARDS_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            CARDS_DB.append({
                "title": filename.rsplit('.', 1)[0],
                "author": "skin.pay",
                "image": f"/static/cards/{filename}",
                "likes": 0,
                "downloads": 0
            })
else:
    print(f"DEBUG: Папка static/cards не найдена по пути: {CARDS_DIR}!")
    os.makedirs(CARDS_DIR, exist_ok=True)

# Разрешенные расширения файлов для безопасности
ALLOWED_EXCEPTIONS = {"jpg", "jpeg", "png", "webp"}

# Информация о проекте
CREATOR_INFO = {
    "title": "skin.pay",
    "subtitle": "Первый бренд по изменению обложки в Узбекистане!",
    "instagram": "skin.pay",
    "telegram": "apple_pay_changer",
    "telegram_link": "https://t.me/apple_pay_changer"
}

@app.get("/", response_class=HTMLResponse)
def read_root():
    return f"<h1>Добро пожаловать в skin.pay! Загружено карточек: {len(CARDS_DB)}</h1>"