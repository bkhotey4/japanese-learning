# -*- coding: utf-8 -*-
"""
生成真正的逐幀動態動畫短影音 (MP4)：
具有文字彈入、圖卡積木拼裝、發光高亮、縮放呼吸動畫、進度條與字音同步動態。
"""

import os
import sys
import math
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

base_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
audio_file = os.path.join(base_dir, "combined_audio.wav")
output_mp4 = os.path.join(base_dir, "kore_animated_lesson.mp4")

# 字體載入
font_path = "C:/Windows/Fonts/msjh.ttc"
title_font = ImageFont.truetype(font_path, 36)
big_font = ImageFont.truetype(font_path, 52)
jp_font = ImageFont.truetype(font_path, 42)
sub_font = ImageFont.truetype(font_path, 24)
hint_font = ImageFont.truetype(font_path, 20)

WIDTH, HEIGHT = 800, 800
FPS = 25
DURATION = 24.8  # 秒
TOTAL_FRAMES = int(FPS * DURATION)

# 載入柴犬圖片作為動畫素材
shiba_path = os.path.join(base_dir, "cards", "card_kore_kudasai.jpg")
shiba_img = Image.open(shiba_path).convert("RGBA").resize((240, 240))

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def render_frame(frame_idx):
    t = frame_idx / FPS
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(250, 246, 238))
    draw = ImageDraw.Draw(img)

    # 頂部導航裝飾條
    draw.rectangle([0, 0, WIDTH, 70], fill=(255, 120, 100))
    draw.text((WIDTH // 2, 35), "🌸 日本語 15 秒動態拆解課", font=title_font, fill=(255, 255, 255), anchor="mm")

    # 階段 1: 0s ~ 13s -> 4 塊日文積木依序彈入、發光、講解
    if t < 13.0:
        draw.text((WIDTH // 2, 110), "【四大日文積木拆解】", font=jp_font, fill=(60, 60, 60), anchor="mm")
        draw.text((WIDTH // 2, 145), "日文句子像拼樂高，每個零件都有功能！", font=hint_font, fill=(120, 120, 120), anchor="mm")

        blocks = [
            {"jp": "これ", "ro": "Kore", "mean": "這個東西", "tip": "手指摸得到的近處目標", "color": (100, 180, 255), "start": 0.5},
            {"jp": "を", "ro": "o", "mean": "🎯 箭頭鎖定", "tip": "標籤貼紙：動作衝著它來", "color": (255, 170, 60), "start": 3.0},
            {"jp": "お願い", "ro": "o-negai", "mean": "⛩️ 禮貌請求", "tip": "願望(願い)+禮貌帽子(お)", "color": (120, 210, 140), "start": 5.5},
            {"jp": "します", "ro": "shimasu", "mean": "🛡️ 我來進行", "tip": "禮貌動詞：客氣的進行動作", "color": (255, 130, 160), "start": 8.0},
        ]

        y_positions = [180, 310, 440, 570]

        for i, b in enumerate(blocks):
            by = y_positions[i]
            # 進場動畫
            if t >= b["start"]:
                progress = min(1.0, (t - b["start"]) / 0.5)
                # 彈跳插值
                scale = 1.0 + 0.15 * math.sin(progress * math.pi) if progress < 1.0 else 1.0
                bx = int(WIDTH // 2)
                bw = int(700 * scale)
                bh = int(105 * scale)

                # 發光高亮
                is_active = (b["start"] <= t < b["start"] + 2.5)
                border_col = (255, 60, 60) if is_active else b["color"]
                border_w = 4 if is_active else 2

                card_box = [bx - bw//2, by - bh//2, bx + bw//2, by + bh//2]
                draw_rounded_rect(draw, card_box, radius=16, fill=(255, 255, 255), outline=border_col, width=border_w)

                # 標籤色塊
                tag_w = 170
                tag_box = [bx - bw//2, by - bh//2, bx - bw//2 + tag_w, by + bh//2]
                draw_rounded_rect(draw, tag_box, radius=16, fill=b["color"])
                draw.text((bx - bw//2 + tag_w//2, by - 12), b["jp"], font=jp_font, fill=(255, 255, 255), anchor="mm")
                draw.text((bx - bw//2 + tag_w//2, by + 22), b["ro"], font=hint_font, fill=(255, 255, 255), anchor="mm")

                # 右側解說
                draw.text((bx - bw//2 + tag_w + 30, by - 12), b["mean"], font=jp_font, fill=(40, 40, 40), anchor="lm")
                draw.text((bx - bw//2 + tag_w + 30, by + 22), b["tip"], font=sub_font, fill=(100, 100, 100), anchor="lm")

    # 階段 2: 13s ~ 結束 -> 合體神句登場！
    else:
        # 背景變為溫暖拉麵店主題
        draw.text((WIDTH // 2, 110), "🌟 實戰無腦神句合體！", font=title_font, fill=(230, 80, 50), anchor="mm")
        
        # 柴犬小旅人上下浮動呼吸動畫
        float_y = int(8 * math.sin(t * 4))
        img.paste(shiba_img, (WIDTH // 2 - 120, 145 + float_y), shiba_img)

        # 核心字卡放大彈跳
        pulse = 1.0 + 0.05 * math.sin(t * 5)
        pw = int(720 * pulse)
        ph = int(140 * pulse)
        p_box = [WIDTH // 2 - pw//2, 430 - ph//2, WIDTH // 2 + pw//2, 430 + ph//2]
        draw_rounded_rect(draw, p_box, radius=24, fill=(255, 255, 255), outline=(255, 120, 80), width=5)

        draw.text((WIDTH // 2, 405), "『 これ、ください 』", font=big_font, fill=(230, 60, 30), anchor="mm")
        draw.text((WIDTH // 2, 460), "Kore, kudasai (This, please!)", font=sub_font, fill=(100, 100, 100), anchor="mm")

        # 口訣氣泡
        draw_rounded_rect(draw, [100, 530, 700, 620], radius=16, fill=(255, 245, 200), outline=(230, 180, 50), width=3)
        draw.text((WIDTH // 2, 560), "🗣️ 四字無腦口訣：【 顆 粒、庫 達 塞 】", font=jp_font, fill=(180, 80, 0), anchor="mm")
        draw.text((WIDTH // 2, 595), "手指戳菜單照片 ➔ 說這句 ➔ 點餐全通關！", font=sub_font, fill=(100, 70, 0), anchor="mm")

    # 底部進度條動畫
    draw.rectangle([0, HEIGHT - 18, WIDTH, HEIGHT], fill=(220, 220, 220))
    prog_w = int(WIDTH * (t / DURATION))
    draw.rectangle([0, HEIGHT - 18, prog_w, HEIGHT], fill=(255, 100, 80))

    # 底部提示文字
    draw.text((WIDTH // 2, HEIGHT - 45), "🎧 跟著節拍大聲念 3 遍：Ko-re, ku-da-sai!", font=hint_font, fill=(120, 120, 120), anchor="mm")

    return img

print("開始渲染 25fps 動畫畫面...")
pipe = subprocess.Popen([
    ffmpeg_bin, "-y",
    "-f", "image2pipe",
    "-vcodec", "mjpeg",
    "-r", str(FPS),
    "-i", "-",
    "-i", audio_file,
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_mp4
], stdin=subprocess.PIPE)

for f in range(TOTAL_FRAMES):
    frame_img = render_frame(f)
    frame_img.save(pipe.stdin, "JPEG", quality=85)

pipe.stdin.close()
pipe.wait()
print(f"✅ 真・動態短影音渲染完成: {output_mp4}")
