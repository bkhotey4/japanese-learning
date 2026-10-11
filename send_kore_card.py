# -*- coding: utf-8 -*-
"""
傳送柴犬拉麵「これ、ください」圖卡與音檔到 Discord 私訊
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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    card_path = os.path.join(base_dir, "cards", "card_kore_kudasai.jpg")
    audio_path = os.path.join(base_dir, "kore_kudasai.mp3")
    
    img_file = discord.File(card_path, filename="kore_kudasai.jpg")
    audio_file = discord.File(audio_path, filename="kore_kudasai.mp3")
    
    embed = discord.Embed(
        title="🍜【超萌實戰圖卡：これ、ください】",
        description=(
            "### 『 これ、ください。 』\n"
            "• **羅馬拼音**：*Kore, kudasai.*\n"
            "• **中文諧音**：**顆粒、庫達塞**\n"
            "• **意思**：This, please! (請給我這個)\n\n"
            "🐕 **情境秒記**：\n"
            "看圖卡裡的可愛柴犬小旅人！\n"
            "就像牠一樣，手拿菜單、手指著香噴噴的拉麵說：\n"
            "👉 **「これ、ください！」**，一秒輕鬆點餐！"
        ),
        color=discord.Color.from_rgb(255, 160, 80)
    )
    embed.set_image(url="attachment://kore_kudasai.jpg")
    embed.set_footer(text="每天一張生動情境圖，圖像記憶最深刻！")
    
    await user.send(embed=embed, files=[img_file, audio_file])
    print("SENT_CARD_SUCCESS")
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
