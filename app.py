import os
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="skin.pay - Apple Pay Skins UZ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка безопасной папки для загрузок
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Чистая база данных (начинается с нуля)
# Автоматическая загрузка карточек из папки static/cards
CARDS_DB = []
CARDS_DIR = "static/cards"

if os.path.exists(CARDS_DIR):
    for filename in os.listdir(CARDS_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            CARDS_DB.append({
                "title": filename.rsplit('.', 1)[0],
                "author": "skin.pay",
                "image": f"/static/cards/{filename}",
                "likes": 0,
                "downloads": 0
            })

# Разрешенные расширения файлов для безопасности
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Информация о проекте
CREATOR_INFO = {
    "title": "skin.pay 💳",
    "subtitle": "Первый бренд по изменению обложки в Узбекистане!",
    "instagram": "skin.pay",
    "telegram": "apple_pay_changer",
    "telegram_link": "https://t.me/apple_pay_changer"
}

@app.get("/", response_class=HTMLResponse)
def home(tab: str = "community"):
    cards_html = ""
    if len(CARDS_DB) == 0:
        cards_html = """
        <div style="grid-column: span 2; text-align: center; color: #a1a1aa; padding: 60px 20px;">
            <p style="font-size: 16px; margin-bottom: 10px;">Здесь пока пусто 💳</p>
            <p style="font-size: 13px;">Нажмите на вкладку <b>Создать</b> вверху, чтобы добавить первый дизайн!</p>
        </div>
        """
    else:
        for card in CARDS_DB:
            cards_html += f"""
            <div class="card-item">
                <div class="card-preview" style="background-image: url('{card['image']}');"></div>
                <div class="card-info">
                    <div class="card-title">{card['title']}</div>
                    <div class="card-author"><span class="avatar"></span> {card['author']}</div>
                    <div class="card-actions">
                        <span class="action-btn">🔖</span>
                        <span class="action-btn">❤️ {card['likes']}</span>
                        <span class="action-btn">📥 {card['downloads']}</span>
                    </div>
                </div>
            </div>
            """

    if tab == "create":
        content = """
        <div class="form-container">
            <h2>Добавить скин карты</h2>
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <div class="input-group">
                    <label>Название дизайна:</label>
                    <input type="text" name="title" required placeholder="Например: Black Card">
                </div>
                <div class="input-group">
                    <label>Автор (Ваш ник):</label>
                    <input type="text" name="author" required placeholder="Ваше имя">
                </div>
                <div class="input-group">
                    <label>Выберите фото скина:</label>
                    <input type="file" name="file" accept="image/*" required>
                </div>
                <button type="submit" class="submit-btn">Опубликовать</button>
            </form>
        </div>
        """
    else:
        content = f"""
        <div class="main-container">
            <!-- Блок информации о бренде -->
            <div class="info-block">
                <h3>{CREATOR_INFO['title']}</h3>
                <p><b>{CREATOR_INFO['subtitle']}</b></p>
                <div class="social-links">
                    <a href="https://instagram.com/{CREATOR_INFO['instagram']}" target="_blank">Instagram: @{CREATOR_INFO['instagram']}</a>
                    <a href="{CREATOR_INFO['telegram_link']}" target="_blank">Telegram: @{CREATOR_INFO['telegram']}</a>
                </div>
            </div>

            <div class="cards-grid">
                {cards_html}
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>skin.pay - Apple Pay Skins UZ</title>
        <style>
            :root {{
                --bg: #09090b;
                --card-bg: #18181b;
                --text: #ffffff;
                --text-muted: #a1a1aa;
                --border: #27272a;
                --accent: #3b82f6;
                --link-color: #60a5fa;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 0;
            }}
            header {{
                position: sticky;
                top: 0;
                background: rgba(9, 9, 11, 0.85);
                backdrop-filter: blur(12px);
                border-bottom: 1px solid var(--border);
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 20px;
                z-index: 100;
            }}
            .logo {{ font-size: 20px; font-weight: 800; color: var(--text); }}
            .nav-tabs {{ display: flex; gap: 15px; font-size: 14px; color: var(--text-muted); }}
            .nav-tabs a {{ text-decoration: none; color: var(--text-muted); cursor: pointer; }}
            .nav-tabs a.active, .nav-tabs a:hover {{ color: var(--text); font-weight: 600; border-bottom: 2px solid var(--text); padding-bottom: 2px; }}
            
            .main-container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            
            /* Стили для блока информации */
            .info-block {{
                background-color: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                text-align: center;
            }}
            .info-block h3 {{ margin-top: 0; font-size: 20px; color: #ffffff; }}
            .info-block p {{ color: var(--text-muted); font-size: 14px; margin-bottom: 15px; }}
            .social-links {{ display: flex; flex-direction: column; gap: 8px; font-size: 14px; }}
            .social-links a {{ text-decoration: none; color: var(--link-color); font-weight: 500; }}
            .social-links a:hover {{ text-decoration: underline; }}
            
            .cards-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
            
            .card-item {{ display: flex; flex-direction: column; gap: 8px; }}
            .card-preview {{
                width: 100%;
                aspect-ratio: 1.586 / 1;
                border-radius: 12px;
                background-size: cover;
                background-position: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            .card-info {{ display: flex; flex-direction: column; gap: 2px; }}
            .card-title {{ font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            .card-author {{ font-size: 12px; color: var(--text-muted); display: flex; align-items: center; gap: 5px; }}
            .avatar {{ width: 14px; height: 14px; border-radius: 50%; background: #3b82f6; display: inline-block; }}
            .card-actions {{ display: flex; gap: 12px; align-items: center; font-size: 12px; color: var(--text-muted); margin-top: 4px; }}
            
            .form-container {{
                max-width: 400px;
                margin: 40px auto;
                background: var(--card-bg);
                padding: 24px;
                border-radius: 16px;
                border: 1px solid var(--border);
            }}
            .input-group {{ margin-bottom: 15px; display: flex; flex-direction: column; gap: 6px; }}
            .input-group label {{ font-size: 13px; color: var(--text-muted); }}
            .input-group input {{
                background: #09090b;
                border: 1px solid var(--border);
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
            }}
            .submit-btn {{
                background: var(--accent);
                color: white;
                border: none;
                width: 100%;
                padding: 12px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
            }}
            .submit-btn:hover {{ background: #2563eb; }}
        </style>
    </head>
    <body>
        <header>
            <div class="logo">💳 skin.pay</div>
            <div class="nav-tabs">
                <a href="/?tab=community" class="{'active' if tab == 'community' else ''}">Сообщество</a>
                <a href="/?tab=create" class="{'active' if tab == 'create' else ''}">Создать</a>
            </div>
        </header>

        {content}
    </body>
    </html>
    """

@app.post("/upload")
async def upload_card(title: str = Form(...), author: str = Form(...), file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Только изображения (jpg, png, webp) разрешены!")

    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    image_url = f"/static/uploads/{safe_filename}"
    CARDS_DB.insert(0, {
        "title": title,
        "author": author,
        "image": image_url,
        "likes": 0,
        "downloads": 0
    })

    return RedirectResponse(url="/?tab=community", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)