# -*- coding: utf-8 -*-
"""
將完整的日文學習計畫直接推送到 Discord 頻道中
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
TARGET_CHANNEL_ID = 1505956373639463005

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def build_plan_embeds():
    # Embed 1: 總覽
    embed1 = discord.Embed(
        title="🌸 全方位日文學習計畫：從 0 開始到生活與職場",
        description=(
            "歡迎開啟日文學習之旅！本計畫為零基礎學習者量身規劃，\n"
            "以**「旅遊 ✈️、生活 🏠、休閒 🎮、工作 💼」**四大核心實戰為導向。\n\n"
            "**🗺️ 學習路線圖（Roadmap）**\n"
            "```\n"
            "【階段 0：發音與五十音】(2~4 週) ➔ 假名直覺反射\n"
            "   ↓\n"
            "【階段 1：旅遊生存與基礎會話】(JLPT N5 | 2~3 個月) ➔ 自由行通關 ✈️\n"
            "   ↓\n"
            "【階段 2：生活溝通與休閒娛樂】(JLPT N4~N3 | 4~6 個月) ➔ 獨立生活 🏠 + 娛樂沉浸 🎮\n"
            "   ↓\n"
            "【階段 3：職場入門與流暢交流】(JLPT N2 | 6~9 個月) ➔ 日商求職/商務書信 💼\n"
            "   ↓\n"
            "【階段 4：專業商務與深度融入】(JLPT N1 / BJT) ➔ 深度談判與商務協作\n"
            "```"
        ),
        color=discord.Color.from_rgb(255, 140, 180)
    )

    # Embed 2: 各階段里程碑
    embed2 = discord.Embed(
        title="🎯 各階段具體目標與規劃",
        color=discord.Color.from_rgb(100, 180, 255)
    )
    embed2.add_field(
        name="🌱 階段 0：發音與五十音奠基（約 2～4 週）",
        value=(
            "• **重點**：平假名、片假名、濁音、拗音、促音、長音\n"
            "• **關鍵**：**片假名一定要熟記！** 日本旅遊時菜單、飲料、外來語招牌全都是片假名。\n"
            "• **推薦**：搭配手寫與發音音檔，培養直覺反射。"
        ),
        inline=False
    )
    embed2.add_field(
        name="✈️ 階段 1：旅遊生存與日常會話（N5 水準，約 2～3 個月）",
        value=(
            "• **核心語法**：`です/ます` 禮貌體、核心助詞（は、が、を、に、で）、動詞四大基本變形（ます形、て形、ない形、辭書形）\n"
            "• **實戰應用**：餐廳點餐、問路求助、交通買票、免稅退稅。\n"
            "• **推薦教材**：《大家的日本語 初級 I & II》或《出口日語》基礎單元。"
        ),
        inline=False
    )
    embed2.add_field(
        name="🏠 階段 2：獨立生活與休閒娛樂（N4～N3 水準，約 4～6 個月）",
        value=(
            "• **核心語法**：動詞進階（可能形、假定形、意向形、被動/使役）、授受動詞（人際互助表達）\n"
            "• **實戰應用**：超商/超市採購、租屋手續、診所就醫；看懂日文字幕動漫、日劇與推特。\n"
            "• **推薦教材**：《大家的日本語 進階 I & II》+《TRY！日本語 N3 達標！》。"
        ),
        inline=False
    )
    embed2.add_field(
        name="💼 階段 3：職場敲門磚與流暢交流（N2 水準，約 6～9 個月）",
        value=(
            "• **核心語法**：**敬語三大體系**（丁寧語、尊敬語、謙讓語）、商務 Email 結構\n"
            "• **實戰應用**：日文履歷與自傳、面試自我介紹、職場電話應答、公文與合約閱讀。\n"
            "• **推薦教材**：《新日檢完勝 500 題 N3~N2》、《TRY！日本語 N2》。"
        ),
        inline=False
    )

    # Embed 3: 每日時間表與工具推薦
    embed3 = discord.Embed(
        title="⏰ 每日高效學習安排 & 推薦神器",
        description="每天維持 60～90 分鐘規律學習，持之以恆效果最顯著！",
        color=discord.Color.from_rgb(255, 200, 50)
    )
    embed3.add_field(
        name="⏳ 每日時間分配建議",
        value=(
            "• **15 分鐘【單字與發音】**：利用通勤碎片時間用 Anki / MOJI 辭書 刷單字卡\n"
            "• **35 分鐘【文法與句型】**：讀課本 1 課或看教學影片，動手造句與做練習\n"
            "• **15 分鐘【影子跟讀 (Shadowing)】**：聽音檔同步大聲跟讀，訓練口腔肌肉記憶\n"
            "• **20 分鐘【興趣休閒沉浸】**：聽日文歌、看動漫/日劇（搭配 Language Reactor 雙語字幕）"
        ),
        inline=False
    )
    embed3.add_field(
        name="🛠️ 推薦工具箱",
        value=(
            "• **查字典**：`MOJI 辭書`（重音標註、詞性完整）、`Weblio 日中中日`\n"
            "• **記單字**：`Anki`（艾賓浩斯間隔複習）\n"
            "• **練聽讀**：`NHK NEWS WEB EASY`（帶注音假名的簡單日文新聞）\n"
            "• **本機器人指令**：在聊天框輸入 `/quiz` 隨堂測驗、`/scenario` 查實用語句！"
        ),
        inline=False
    )
    embed3.set_footer(text="🌸 Japanese_Learn 伴你輕鬆學日文，がんばってください！")

    return [embed1, embed2, embed3]

@client.event
async def on_ready():
    print(f"登入機器人成功：{client.user}")
    channel = client.get_channel(TARGET_CHANNEL_ID)
    if not channel:
        try:
            channel = await client.fetch_channel(TARGET_CHANNEL_ID)
        except Exception as e:
            print(f"無法取得頻道: {e}")
            await client.close()
            return

    embeds = build_plan_embeds()
    print(f"正在向頻道 #{channel.name} 發送學習計畫...")
    for embed in embeds:
        await channel.send(embed=embed)
        await asyncio.sleep(1)
    
    print("✅ 學習計畫已成功發送到 Discord 頻道！")
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
