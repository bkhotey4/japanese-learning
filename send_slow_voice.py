# -*- coding: utf-8 -*-
"""
傳送「慢速跟讀版 (0.7x)」與「音節拆解發音法」到使用者的 Discord DM
"""

import os
import sys
import asyncio
import discord
from dotenv import load_dotenv

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TARGET_USER_ID = 548823614900797441

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    user = await client.fetch_user(TARGET_USER_ID)
    
    embed = discord.Embed(
        title="🐢【貼心降速：慢速 0.7x 拆解跟讀版】",
        description=(
            "剛學日語覺得常速太快非常正常！別擔心，我們換這個**「慢速 0.7x」**來聽：\n\n"
            "### 🧩 音節拆解練習法（不要一口氣念）：\n"
            "請試著像拍手打節拍一樣，分 4 段念：\n\n"
            "1️⃣ **Ko-re**（こ・れ）➔ 這個\n"
            "2️⃣ **o**（を）➔ 連接詞\n"
            "3️⃣ **o-ne-ga-i**（お・ね・が・い）➔ 拜託\n"
            "4️⃣ **shi-ma-su**（し・ま・す）➔ 做\n\n"
            "合體：**Ko-re** ⋯ **o** ⋯ **o-ne-ga-i** ⋯ **shi-ma-su**！\n\n"
            "👇 **點擊下方音檔，聽聽看降速 30% 的清楚發音：**"
        ),
        color=discord.Color.from_rgb(120, 210, 160)
    )
    embed.set_footer(text="慢速版把每個假名音拍都放慢，舌頭更容易跟上喔！")

    file = discord.File("slow_voice.mp3", filename="slow_kore_o_onegai_shimasu.mp3")
    await user.send(embed=embed, file=file)
    print("SLOW_VOICE_SENT")
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
