FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

WORKDIR /app

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼與資料（.env、venv、日誌、user_progress*.json 已由 .dockerignore 排除）
COPY . .

# Token 請用環境變數傳入：docker run -e DISCORD_BOT_TOKEN=... -e DISCORD_OWNER_ID=...
# 學習進度要保存請掛載檔案：-v /path/user_progress.json:/app/user_progress.json
CMD ["python", "bot.py"]
