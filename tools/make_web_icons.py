"""產生網頁 App 圖示與分享預覽圖（docs/icons/）。用法：python tools/make_web_icons.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "docs" / "icons"
OUT.mkdir(parents=True, exist_ok=True)
PINK, DEEP, WHITE = (214, 69, 107), (150, 30, 70), (255, 255, 255)
JP = "C:/Windows/Fonts/YuGothB.ttc"
TC = "C:/Windows/Fonts/msjhbd.ttc"


def gradient(w, h):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(PINK[i] * (1 - t) + DEEP[i] * t) for i in range(3)))
    return img


def petal(d, cx, cy, r, fill):
    # 簡單的五瓣櫻花
    import math
    for k in range(5):
        a = math.radians(k * 72 - 90)
        x, y = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
        d.ellipse([x - r * 0.45, y - r * 0.45, x + r * 0.45, y + r * 0.45], fill=fill)
    d.ellipse([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2], fill=(255, 220, 230))


def icon(size, maskable=False):
    img = gradient(size, size)
    d = ImageDraw.Draw(img)
    scale = 0.62 if maskable else 0.78
    font = ImageFont.truetype(JP, int(size * scale * 0.72))
    d.text((size / 2, size * 0.53), "あ", font=font, fill=WHITE, anchor="mm")
    petal(d, size * 0.74, size * 0.27, size * (0.11 if maskable else 0.14), (255, 183, 205))
    if not maskable:
        m = Image.new("L", (size, size), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, size, size], radius=size // 5, fill=255)
        img.putalpha(m)
    return img


for s in (192, 512):
    icon(s).save(OUT / f"icon-{s}.png")
icon(512, maskable=True).save(OUT / "icon-maskable-512.png")
icon(180, maskable=True).save(OUT / "apple-touch-icon.png")

og = gradient(1200, 630)
d = ImageDraw.Draw(og)
for x, y, r in [(1040, 120, 70), (1130, 260, 40), (960, 520, 55)]:
    petal(d, x, y, r, (255, 183, 205))
d.text((90, 170), "日語學習道場", font=ImageFont.truetype(TC, 104), fill=WHITE)
d.text((94, 320), "每天 15 分鐘・從五十音到日本自由行", font=ImageFont.truetype(TC, 44), fill=(255, 225, 235))
d.text((94, 400), "闖關・每日挑戰・發音評分・角色扮演", font=ImageFont.truetype(TC, 38), fill=(255, 225, 235))
d.text((94, 500), "これ、ください。", font=ImageFont.truetype(JP, 48), fill=WHITE)
og.save(OUT / "og.png", optimize=True)
print("icons written to", OUT)
