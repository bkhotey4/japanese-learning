# -*- coding: utf-8 -*-
"""
測試直接傳送日語發音音檔到使用者 Discord 私訊 (DM)
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
        title="🔊【日語真人生動發音：實機播放】",
        description=(
            "### 『 これをお願いします。 』\n"
            "• **羅馬拼音**：*Kore o onegai shimasu.*\n"
            "• **中文意思**：請給我這個。\n\n"
            "👇 **請點擊下方音檔的【▶️ 播放鍵】聽聽看道地的東京標準發音！**"
        ),
        color=discord.Color.from_rgb(80, 200, 180)
    )
    embed.set_footer(text="支援 Discord 內建播放器，手機與電腦皆可一鍵點聽！")
    
    file = discord.File("test_voice.mp3", filename="kore_o_onegai_shimasu.mp3")
    await user.send(embed=embed, file=file)
    print("VOICE_SAMPLE_SENT")
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
