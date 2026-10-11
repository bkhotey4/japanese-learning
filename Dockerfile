FROM python:3.10-slim

WORKDIR /app

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼與資源
COPY . .

# 啟動 Discord 機器人
CMD ["python", "bot.py"]
