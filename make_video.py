# -*- coding: utf-8 -*-
"""
合成日文短影音 (MP4)：
結合柴犬圖卡、中文導讀配音與日語道地發音，輸出 15 秒教學短片並推送到 Discord 私訊。
"""

import os
import sys
import subprocess
import asyncio
import imageio_ffmpeg
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

ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
base_dir = os.path.dirname(os.path.abspath(__file__))

intro_wav = os.path.join(base_dir, "intro.wav")
jp_mp3 = os.path.join(base_dir, "kore_kudasai.mp3")
card_img = os.path.join(base_dir, "cards", "card_kore_kudasai.jpg")
combined_audio = os.path.join(base_dir, "combined_audio.wav")
output_mp4 = os.path.join(base_dir, "kore_kudasai_lesson.mp4")

# 1. 使用 ffmpeg 合成音訊 (中文導讀 + 日語發音)
print("正在合成講解音訊...")
concat_cmd = [
    ffmpeg_bin, "-y",
    "-i", intro_wav,
    "-i", jp_mp3,
    "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[outa]",
    "-map", "[outa]",
    combined_audio
]
subprocess.run(concat_cmd, check=True)

# 2. 合成短影音 (圖片循環 + 縮放呼吸效果 + 音訊)
print("正在合成 MP4 短影音...")
video_cmd = [
    ffmpeg_bin, "-y",
    "-loop", "1",
    "-i", card_img,
    "-i", combined_audio,
    "-c:v", "libx264",
    "-tune", "stillimage",
    "-c:a", "aac",
    "-b:a", "192k",
    "-pix_fmt", "yuv420p",
    "-shortest",
    output_mp4
]
subprocess.run(video_cmd, check=True)
print(f"✅ 短影音生成完畢: {output_mp4}")

# 3. 發送到 Discord 私訊
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    user = await client.fetch_user(TARGET_USER_ID)
    embed = discord.Embed(
        title="🎬【15秒日語精華短影音：これ、ください】",
        description=(
            "為您生成的**「專屬講解短影音」**來囉！\n\n"
            "📺 **影片特點**：\n"
            "• 搭配超萌柴犬拉麵點餐圖卡\n"
            "• 中文重點講解（點餐時機、記憶口訣）\n"
            "• 慢速道地真人日語發音示範\n\n"
            "👇 **點擊下方影片直接觀看播放！**"
        ),
        color=discord.Color.from_rgb(255, 120, 100)
    )
    file = discord.File(output_mp4, filename="kore_kudasai_lesson.mp4")
    await user.send(embed=embed, file=file)
    print("SENT_VIDEO_TO_DISCORD")
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
