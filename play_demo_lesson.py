# -*- coding: utf-8 -*-
"""
播放一次 15 分鐘完整日語圖卡體驗課（發送到使用者的 Discord DM）
包含：
1. 視覺圖卡（圖片附件）+ 記憶聯想法
2. 旅遊核心句微量吸收
3. 口語跟讀與小驗收按鈕
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

class DemoLessonQuizView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300.0)
        self.responded = False

    @discord.ui.button(label="これをお願いします", style=discord.ButtonStyle.primary)
    async def opt1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_answer(interaction, button, True)

    @discord.ui.button(label="トイレはどこですか", style=discord.ButtonStyle.secondary)
    async def opt2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_answer(interaction, button, False)

    @discord.ui.button(label="お先に失礼します", style=discord.ButtonStyle.secondary)
    async def opt3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_answer(interaction, button, False)

    async def handle_answer(self, interaction: discord.Interaction, chosen_button: discord.ui.Button, is_correct: bool):
        if self.responded:
            await interaction.response.send_message("你已經完成今天的驗收囉！", ephemeral=True)
            return

        self.responded = True
        for child in self.children:
            child.disabled = True

        if is_correct:
            chosen_button.style = discord.ButtonStyle.success
            msg = "🎉 **太棒了！完全正確！**\n👉 「これをお願いします」就是『請給我這個』！\n恭喜你完成了今天的 15 分鐘體驗課，可以安心收工打道回府囉！✨"
        else:
            chosen_button.style = discord.ButtonStyle.danger
            msg = "❌ 差一點點！\n正解是「これをお願いします」（請給我這個）。\n「トイレはどこですか」是問廁所在哪；「お先に失礼します」是下班先走喔！"

        await interaction.response.edit_message(view=self)
        await interaction.followup.send(msg)


@client.event
async def on_ready():
    user = await client.fetch_user(TARGET_USER_ID)
    
    # 1. 歡迎與整體流程引導
    intro_embed = discord.Embed(
        title="🎬【15 分鐘日語體驗課：Day 1 實機播放】",
        description=(
            "哈囉！這就是未來我們**每天 15 分鐘**的實際學習流程！\n"
            "沒有死板背書，只有 3 個輕鬆無負擔的階段：\n\n"
            "• **Step 1（5 分鐘）**：視覺圖卡記假名\n"
            "• **Step 2（7 分鐘）**：吸收 1 句旅遊/生活神句\n"
            "• **Step 3（3 分鐘）**：開口念出聲 + 1 題按鈕隨堂驗收"
        ),
        color=discord.Color.from_rgb(255, 120, 150)
    )
    await user.send(embed=intro_embed)
    await asyncio.sleep(1)

    # 2. Step 1: 發送圖卡
    card_path = os.path.join(os.path.dirname(__file__), "cards", "card_a.jpg")
    file = discord.File(card_path, filename="card_a.jpg")
    
    step1_embed = discord.Embed(
        title="🎴 Step 1: 視覺圖卡記憶（今日進度：あ）",
        description=(
            "### 平假名：『 あ 』 (發音: a)\n\n"
            "🍎 **圖像聯想法**：\n"
            "請看右邊圖卡中的小蘋果（**りんご**）！\n"
            "字形就像一個人張開雙手，看到紅通通的蘋果驚呼：**「啊（あ）！好甜的蘋果！」**\n\n"
            "🗣️ **發音嘴型秘訣**：\n"
            "嘴型放鬆自然微張（不要像中文『阿』張得太大），輕輕吐氣發音。"
        ),
        color=discord.Color.from_rgb(100, 180, 255)
    )
    step1_embed.set_image(url="attachment://card_a.jpg")
    step1_embed.set_footer(text="只要腦中浮現這個字形與蘋果，你就記住了第 1 個平假名！")
    await user.send(file=file, embed=step1_embed)
    await asyncio.sleep(1.5)

    # 3. Step 2: 核心旅遊生存句
    step2_embed = discord.Embed(
        title="✈️ Step 2: 實用旅遊神句（日本自由行必備！）",
        description=(
            "### 『 これをお願いします。 』\n"
            "• **平假名**：これを おねがいします。\n"
            "• **羅馬拼音**：*Kore o onegai shimasu.*\n"
            "• **中文意思**：**請給我這個。**\n\n"
            "💡 **拆解超級簡單**：\n"
            "1. `これ (kore)` = 這個\n"
            "2. `を (o)` = 助詞（把動作連到「這個」上）\n"
            "3. `お願いします (onegai shimasu)` = 拜託了 / 請給我\n\n"
            "🍜 **實戰情境**：\n"
            "在東京拉麵店或超商，看不懂菜單沒關係！\n"
            "**只要伸出食指指著菜單圖片或商品，微笑著說：『これをお願いします』**，店員立刻秒懂為你準備！"
        ),
        color=discord.Color.from_rgb(255, 180, 50)
    )
    await user.send(embed=step2_embed)
    await asyncio.sleep(1.5)

    # 4. Step 3: 口語跟讀與小驗收
    step3_embed = discord.Embed(
        title="🎙️ Step 3: 口語肌肉記憶 + 3 秒小驗收",
        description=(
            "請跟著羅馬音在心裡或開口念 **3 遍**：\n"
            "> **「Ko-re o o-ne-gai shi-ma-su」**\n"
            "> **「Ko-re o o-ne-gai shi-ma-su」**\n"
            "> **「Ko-re o o-ne-gai shi-ma-su」**\n\n"
            "------------------------------------\n"
            "🎯 **【今日下課驗收題】**：\n"
            "走進居酒屋想點這道人氣串燒，指著菜單你應該說哪一句？\n"
            "（請點選下方按鈕直接作答）"
        ),
        color=discord.Color.green()
    )
    view = DemoLessonQuizView()
    await user.send(embed=step3_embed, view=view)

    print("SUCCESS_DEMO_SENT")
    await client.close()

if __name__ == "__main__":
    client.run(TOKEN)
