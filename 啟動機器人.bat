@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
title 🌸 日文學習 Discord 機器人
echo 正在啟動日文學習 Discord 機器人...
cd /d "%~dp0"

if not exist venv (
    echo 找不到虛擬環境，正在自動建立...
    python -m venv venv
    call .\venv\Scripts\pip install -r requirements.txt
)

.\venv\Scripts\python.exe bot.py
pause
