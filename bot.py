# -*- coding: utf-8 -*-
"""
日文學習 Discord Bot
支援四大情境（旅遊、生活、工作、休閒）、五十音互動速查、隨堂按鈕測驗與每日一句。
"""

import os
import sys
import random

# 支援 Windows 背景執行、雙向記錄與 UTF-8 編碼保護
log_path = os.path.join(os.path.dirname(__file__), "bot.log")
err_path = os.path.join(os.path.dirname(__file__), "bot.err")

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

if sys.stderr is not None and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

LOG_MAX_BYTES = 20 * 1024 * 1024  # 記錄檔超過 20 MB 就輪替成 .1（舊的 .1 會被取代）


class DualLogger:
    def __init__(self, stream, file_path):
        self.stream = stream
        self.file_path = file_path
        self._file = None
        self._written = 0

    def _rotate_if_needed(self):
        """檔案超過 LOG_MAX_BYTES 時改名為 .1 並重新開新檔"""
        try:
            size = os.path.getsize(self.file_path) if os.path.exists(self.file_path) else 0
        except Exception:
            return
        if size < LOG_MAX_BYTES:
            return
        try:
            if self._file is not None:
                self._file.close()
                self._file = None
            os.replace(self.file_path, self.file_path + ".1")
        except Exception:
            pass

    def write(self, message):
        if self.stream:
            try:
                self.stream.write(message)
                self.stream.flush()
            except Exception:
                pass
        try:
            if self._file is None:
                self._rotate_if_needed()
                self._file = open(self.file_path, "a", encoding="utf-8")
                self._written = 0
            self._file.write(message)
            self._file.flush()
            # 每寫入約 1 MB 檢查一次大小，避免每次都 stat 檔案
            self._written += len(message)
            if self._written >= 1024 * 1024:
                self._written = 0
                self._rotate_if_needed()
        except Exception:
            pass

    def flush(self):
        if self.stream:
            try:
                self.stream.flush()
            except Exception:
                pass
        if self._file:
            try:
                self._file.flush()
            except Exception:
                pass

sys.stdout = DualLogger(sys.stdout, log_path)
sys.stderr = DualLogger(sys.stderr, err_path)

import asyncio
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

import datetime
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
import tempfile
import uuid
import edge_tts

from data.kana_data import KANA_ROWS, ALL_KANA_CARDS, get_all_kana_cards, get_kana_card
from data.phrases_data import SCENARIOS
from data.quiz_data import QUIZ_QUESTIONS, get_quizzes_by_category
from data.trivia_data import JAPANESE_TRIVIA, get_random_trivia
from data.quest_data import QUESTS
TOTAL_QUESTS = len(QUESTS)  # 主線闖關總關數
from data.anime_data import ANIME_QUOTES
from data.progress_manager import (
    get_user_progress, advance_user_level, reset_user_progress,
    record_daily_activity, add_mistake, get_mistakes, remove_mistake,
    unlock_badge, BADGES_INFO, set_user_schedule, set_user_schedule_mode,
    advance_kana_day, toggle_user_schedule, get_leaderboard,
    get_last_push_date, set_last_push_date
)
from data.roleplay_data import ROLEPLAY_SCENARIOS
from data.katakana_data import KATAKANA_WORDS, KATAKANA_QUIZZES
from data.culture_data import CULTURE_TOPICS
from data.sos_data import EMERGENCY_CONTACTS, SOS_SCENARIOS
from data.menu_data import MENU_CATEGORIES
from data.grammar_data import TE_FORM_MNEMONIC, VERB_CONJUGATIONS
from data.news_data import NHK_NEWS_ARTICLES
from data.shadowing_data import SHADOWING_DRILLS
from data.omikuji_data import OMIKUJI_DATA, draw_omikuji
from data.scan_data import SCAN_CATEGORIES
try:
    from data.lyrics_data import JPOP_SONGS  # 此檔案未納入 git，新 clone 可能沒有
except ImportError:
    JPOP_SONGS = {}

LYRICS_MISSING_MSG = "⚠️ 此環境未安裝 J-POP 歌詞資料（data/lyrics_data.py）。"

# 載入環境變數
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 設定 Discord Bot Intents（斜線指令與按鈕互動使用預設 Intents 即可，無需開啟特權權限）
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)


async def text_to_speech(text: str, filename: str, rate: str = "-25%", voice: str = "female") -> str:
    # 每次產生唯一檔名（保留原名稱當前綴），避免多位使用者同時使用時互相覆蓋
    stem, ext = os.path.splitext(os.path.basename(filename))
    path = os.path.join(tempfile.gettempdir(), f"{stem}_{uuid.uuid4().hex[:12]}{ext or '.mp3'}")
    voice_id = "ja-JP-NanamiNeural" if voice == "female" else "ja-JP-KeitaNeural"
    communicate = edge_tts.Communicate(text, voice_id, rate=rate)
    await communicate.save(path)
    return path


def remove_temp_file(path) -> None:
    """傳送完語音後刪除暫存檔（失敗就忽略）"""
    if not path:
        return
    try:
        os.remove(path)
    except Exception:
        pass


def build_kana_card_embed(idx: int) -> discord.Embed:
    """建立五十音單字卡 Embed（包含漢字由來、記憶口訣、發音嘴型秘訣與常用單字）"""
    card = get_kana_card(idx)
    total = len(ALL_KANA_CARDS)
    embed = discord.Embed(
        title=f"🔤 五十音圖卡學習：【{card['hira']}】(平假名)  /  【{card['kata']}】(片假名)",
        description=(
            f"📌 **所屬行別**：`{card['row']}` （第 {idx + 1} / {total} 個音）\n"
            f"🔤 **羅馬拼音**：`{card['romaji']}`\n\n"
            f"------------------------------------\n"
            f"📜 **漢字字源由來**：\n> **{card['origin']}**\n\n"
            f"💡 **超好記圖像口訣**：\n> **{card['mnemonic']}**\n\n"
            f"👄 **發音與嘴型秘訣**：\n> **{card['sound_tip']}**\n\n"
            f"------------------------------------\n"
            f"📖 **必學常用單字**：\n> **{card['vocab']}** — **{card['vocab_tw']}**\n"
        ),
        color=discord.Color.from_rgb(100, 180, 255)
    )
    embed.set_footer(text="💡 點擊下方按鈕切換上/下一張，或直接點「🎯 測驗這個字」驗收！")
    return embed


class KanaFlashcardView(discord.ui.View):
    """五十音互動卡片流 View（支援上下翻頁、行別下拉選單、測驗與隨機抽字）"""
    def __init__(self, current_idx: int = 0):
        super().__init__(timeout=None)
        self.current_idx = max(0, min(current_idx, len(ALL_KANA_CARDS) - 1))

        # 下拉選單：行別快速跳轉
        options = [
            discord.SelectOption(label="あ行 (a, i, u, e, o)", value="0", default=(0 <= self.current_idx < 5)),
            discord.SelectOption(label="か行 (ka, ki, ku, ke, ko)", value="5", default=(5 <= self.current_idx < 10)),
            discord.SelectOption(label="さ行 (sa, shi, su, se, so)", value="10", default=(10 <= self.current_idx < 15)),
            discord.SelectOption(label="た行 (ta, chi, tsu, te, to)", value="15", default=(15 <= self.current_idx < 20)),
            discord.SelectOption(label="な行 (na, ni, nu, ne, no)", value="20", default=(20 <= self.current_idx < 25)),
            discord.SelectOption(label="は行 (ha, hi, fu, he, ho)", value="25", default=(25 <= self.current_idx < 30)),
            discord.SelectOption(label="ま行 (ma, mi, mu, me, mo)", value="30", default=(30 <= self.current_idx < 35)),
            discord.SelectOption(label="や行 (ya, yu, yo)", value="35", default=(35 <= self.current_idx < 38)),
            discord.SelectOption(label="ら行 (ra, ri, ru, re, ro)", value="38", default=(38 <= self.current_idx < 43)),
            discord.SelectOption(label="わ行・撥音 (wa, wo, n)", value="43", default=(43 <= self.current_idx < 46)),
        ]
        select = discord.ui.Select(placeholder="📂 快速跳轉至指定行別...", options=options, row=0)
        select.callback = self.on_select_row
        self.add_item(select)

        # 導覽與測驗按鈕
        btn_prev = discord.ui.Button(label="⬅️ 上一個字", style=discord.ButtonStyle.secondary, disabled=(self.current_idx == 0), row=1)
        btn_prev.callback = self.on_prev
        self.add_item(btn_prev)

        btn_next = discord.ui.Button(label="➡️ 下一個字", style=discord.ButtonStyle.primary, disabled=(self.current_idx >= len(ALL_KANA_CARDS) - 1), row=1)
        btn_next.callback = self.on_next
        self.add_item(btn_next)

        btn_loop = discord.ui.Button(label="▶️ 自動播放", style=discord.ButtonStyle.success, row=1)
        btn_loop.callback = self.on_autoplay
        self.add_item(btn_loop)

        btn_quiz = discord.ui.Button(label="🎯 測驗這個字", style=discord.ButtonStyle.primary, row=1)
        btn_quiz.callback = self.on_quiz
        self.add_item(btn_quiz)

        btn_rand = discord.ui.Button(label="🎲 隨機抽字", style=discord.ButtonStyle.secondary, row=1)
        btn_rand.callback = self.on_random
        self.add_item(btn_rand)

    async def on_prev(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        new_idx = max(0, self.current_idx - 1)
        new_embed = build_kana_card_embed(new_idx)
        new_view = KanaFlashcardView(new_idx)
        await interaction.response.edit_message(embed=new_embed, view=new_view)

    async def on_next(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        new_idx = min(len(ALL_KANA_CARDS) - 1, self.current_idx + 1)
        new_embed = build_kana_card_embed(new_idx)
        new_view = KanaFlashcardView(new_idx)
        await interaction.response.edit_message(embed=new_embed, view=new_view)

    async def on_autoplay(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        auto_view = KanaAutoPlayView(current_idx=self.current_idx, speed_seconds=4.0)
        auto_embed = auto_view.build_autoplay_embed()
        await interaction.response.edit_message(embed=auto_embed, view=auto_view)
        auto_view.start_loop(interaction)

    async def on_random(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        choices = [i for i in range(len(ALL_KANA_CARDS)) if i != self.current_idx]
        new_idx = random.choice(choices) if choices else 0
        new_embed = build_kana_card_embed(new_idx)
        new_view = KanaFlashcardView(new_idx)
        await interaction.response.edit_message(embed=new_embed, view=new_view)

    async def on_select_row(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        selected_idx = int(interaction.data["values"][0])
        new_embed = build_kana_card_embed(selected_idx)
        new_view = KanaFlashcardView(selected_idx)
        await interaction.response.edit_message(embed=new_embed, view=new_view)

    async def on_quiz(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        card = get_kana_card(self.current_idx)
        correct = card["romaji"]
        all_romajis = list(set([c["romaji"] for c in ALL_KANA_CARDS if c["romaji"] != correct]))
        distractors = random.sample(all_romajis, min(3, len(all_romajis)))
        options = distractors + [correct]
        random.shuffle(options)

        embed = discord.Embed(
            title=f"🎯 五十音隨堂小考：【 {card['hira']} 】(平) / 【 {card['kata']} 】(片)",
            description=(
                f"請問假名 **『 {card['hira']} 』** 的正確羅馬拼音是哪一個？\n\n"
                f"💡 **記憶提示**：{card['mnemonic']}\n\n"
                f"👇 請點擊下方選項按鈕作答："
            ),
            color=discord.Color.blue()
        )
        quiz_view = KanaSingleQuizView(self.current_idx, card['hira'], correct, options)
        await interaction.response.edit_message(embed=embed, view=quiz_view)

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, (discord.ui.Button, discord.ui.Select)):
                item.disabled = True


class KanaAutoPlayView(discord.ui.View):
    """五十音字卡循環自動播放 View（支援暫停/繼續、切換速度、測驗、手動返回單字卡）"""
    def __init__(self, current_idx: int = 0, speed_seconds: float = 4.0):
        super().__init__(timeout=None)
        self.current_idx = max(0, min(current_idx, len(ALL_KANA_CARDS) - 1))
        self.speed = speed_seconds
        self.is_paused = False
        self.is_stopped = False
        self._task = None
        self._last_interaction = None

        self._refresh_buttons()

    def _refresh_buttons(self):
        self.clear_items()

        # Row 0: 播放控制按鈕
        if self.is_paused:
            btn_toggle = discord.ui.Button(label="▶️ 繼續播放", style=discord.ButtonStyle.success, row=0)
            btn_toggle.callback = self.on_resume
        else:
            btn_toggle = discord.ui.Button(label="⏸️ 暫停播放", style=discord.ButtonStyle.secondary, row=0)
            btn_toggle.callback = self.on_pause
        self.add_item(btn_toggle)

        btn_speed = discord.ui.Button(
            label=f"⏱️ 速度: {self.speed:.1f}s",
            style=discord.ButtonStyle.primary,
            row=0
        )
        btn_speed.callback = self.on_change_speed
        self.add_item(btn_speed)

        btn_stop = discord.ui.Button(label="⏹️ 停止並返回卡片", style=discord.ButtonStyle.danger, row=0)
        btn_stop.callback = self.on_stop
        self.add_item(btn_stop)

        # Row 1: 輔助按鈕
        btn_quiz = discord.ui.Button(label="🎯 考考這個字！", style=discord.ButtonStyle.secondary, row=1)
        btn_quiz.callback = self.on_quiz_current
        self.add_item(btn_quiz)

        btn_skip = discord.ui.Button(label="⏭️ 快進下一個", style=discord.ButtonStyle.secondary, row=1)
        btn_skip.callback = self.on_skip_next
        self.add_item(btn_skip)

    def build_autoplay_embed(self) -> discord.Embed:
        card = get_kana_card(self.current_idx)
        total = len(ALL_KANA_CARDS)
        play_status = "⏸️ 已暫停" if self.is_paused else f"▶️ 正在循環播放中（每 {self.speed:.1f} 秒切換）"

        embed = discord.Embed(
            title=f"🌸 五十音循環播放：【{card['hira']}】(平) / 【{card['kata']}】(片)",
            description=(
                f"⚡ **狀態**：`{play_status}`\n"
                f"📌 **所屬行別**：`{card['row']}` （第 **{self.current_idx + 1}** / {total} 個音）\n"
                f"🔤 **羅馬拼音**：`{card['romaji']}`\n\n"
                f"------------------------------------\n"
                f"📜 **漢字字源**：**{card['origin']}**\n\n"
                f"💡 **記憶口訣**：**{card['mnemonic']}**\n\n"
                f"👄 **發音秘訣**：**{card['sound_tip']}**\n\n"
                f"📖 **實用單字**：**{card['vocab']}**（{card['vocab_tw']}）\n"
                f"------------------------------------\n"
                f"💻 **沉浸式音頻網頁版**：電腦可直接雙擊打開專案內之 `kana_player.html`！"
            ),
            color=discord.Color.from_rgb(255, 120, 180) if not self.is_paused else discord.Color.greyple()
        )
        embed.set_footer(text=f"點擊「⏸️ 暫停」可停下思考，點「🎯 考考這個字」即學即測！自動巡迴已開啟。")
        return embed

    def start_loop(self, interaction: discord.Interaction):
        self._last_interaction = interaction
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._auto_advance_task())

    async def _auto_advance_task(self):
        # 互動 token 15 分鐘後失效：同一個互動最多編輯約 14 分鐘；暫停超過 5 分鐘也自動結束
        MAX_TOKEN_AGE = 14 * 60
        MAX_PAUSED = 5 * 60
        loop = asyncio.get_running_loop()
        token_owner = self._last_interaction
        token_started = loop.time()
        paused_since = None
        try:
            while not self.is_stopped:
                await asyncio.sleep(self.speed)
                now = loop.time()
                if self._last_interaction is not token_owner:
                    # 使用者按了按鈕 → 拿到新的互動 token，重新計時
                    token_owner = self._last_interaction
                    token_started = now
                if now - token_started > MAX_TOKEN_AGE:
                    break
                if self.is_paused:
                    if paused_since is None:
                        paused_since = now
                    elif now - paused_since > MAX_PAUSED:
                        break
                    continue
                paused_since = None
                if self.is_stopped:
                    break

                self.current_idx = (self.current_idx + 1) % len(ALL_KANA_CARDS)
                embed = self.build_autoplay_embed()

                try:
                    if self._last_interaction:
                        if hasattr(self._last_interaction, "edit_original_response"):
                            await self._last_interaction.edit_original_response(embed=embed, view=self)
                        elif hasattr(self._last_interaction, "message") and self._last_interaction.message:
                            await self._last_interaction.message.edit(embed=embed, view=self)
                except discord.HTTPException:
                    # 訊息被刪除、token 失效或其他 Discord API 錯誤 → 停止循環
                    break
                except Exception as e:
                    # 避免編輯過頻或連線中斷引發報錯
                    await asyncio.sleep(2.0)
        except asyncio.CancelledError:
            pass
        finally:
            self.is_stopped = True

    async def on_pause(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        self._last_interaction = interaction
        self.is_paused = True
        self._refresh_buttons()
        embed = self.build_autoplay_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_resume(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        self._last_interaction = interaction
        self.is_paused = False
        self._refresh_buttons()
        embed = self.build_autoplay_embed()
        await interaction.response.edit_message(embed=embed, view=self)
        # 若背景循環因暫停過久或逾時已結束，用這次的新互動重新啟動
        if self._task is None or self._task.done():
            self.is_stopped = False
            self.start_loop(interaction)

    async def on_change_speed(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        self._last_interaction = interaction
        # 切換循環速度：4.0s -> 6.0s -> 3.0s -> 4.0s
        speed_cycle = [4.0, 6.0, 3.0]
        try:
            curr_idx = speed_cycle.index(self.speed)
            self.speed = speed_cycle[(curr_idx + 1) % len(speed_cycle)]
        except ValueError:
            self.speed = 4.0

        self._refresh_buttons()
        embed = self.build_autoplay_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_skip_next(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        self._last_interaction = interaction
        self.current_idx = (self.current_idx + 1) % len(ALL_KANA_CARDS)
        embed = self.build_autoplay_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_stop(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        self.is_stopped = True
        if self._task and not self._task.done():
            self._task.cancel()

        back_embed = build_kana_card_embed(self.current_idx)
        back_view = KanaFlashcardView(self.current_idx)
        await interaction.response.edit_message(embed=back_embed, view=back_view)

    async def on_quiz_current(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        self.is_stopped = True
        if self._task and not self._task.done():
            self._task.cancel()

        card = get_kana_card(self.current_idx)
        correct = card["romaji"]
        all_romajis = list(set([c["romaji"] for c in ALL_KANA_CARDS if c["romaji"] != correct]))
        distractors = random.sample(all_romajis, min(3, len(all_romajis)))
        options = distractors + [correct]
        random.shuffle(options)

        embed = discord.Embed(
            title=f"🎯 五十音隨堂小考：【 {card['hira']} 】(平) / 【 {card['kata']} 】(片)",
            description=(
                f"剛才播放到的假名 **『 {card['hira']} 』**，正確羅馬拼音是哪一個？\n\n"
                f"💡 **記憶提示**：{card['mnemonic']}\n\n"
                f"👇 請點擊下方選項按鈕作答："
            ),
            color=discord.Color.blue()
        )
        quiz_view = KanaSingleQuizView(self.current_idx, card['hira'], correct, options)
        await interaction.response.edit_message(embed=embed, view=quiz_view)



class KanaSingleQuizView(discord.ui.View):
    """針對單一假名的即時驗收測驗 View（作答後提供接續學習按鈕與好奇心冷知識）"""
    def __init__(self, card_idx: int, kana_char: str, correct_answer: str, options: list):
        super().__init__(timeout=None)
        self.card_idx = card_idx
        self.kana_char = kana_char
        self.correct_answer = correct_answer
        self.options = options
        self.responded = False

        for opt in options:
            btn = discord.ui.Button(label=opt, style=discord.ButtonStyle.secondary, row=0)
            btn.callback = self.make_callback(opt)
            self.add_item(btn)

    def make_callback(self, chosen: str):
        async def callback(interaction: discord.Interaction):
            if self.responded:
                await interaction.response.send_message("已經作答過囉！", ephemeral=True)
                return

            self.responded = True
            is_correct = (chosen == self.correct_answer)
            record_daily_activity(interaction.user.id)

            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.row == 0:
                    item.disabled = True
                    if item.label == self.correct_answer:
                        item.style = discord.ButtonStyle.success
                    elif item.label == chosen and not is_correct:
                        item.style = discord.ButtonStyle.danger

            card = get_kana_card(self.card_idx)
            embed = interaction.message.embeds[0]
            trivia = get_random_trivia()

            if is_correct:
                unlock_badge(interaction.user.id, "badge_quiz")
                embed.color = discord.Color.green()
                embed.title = f"🎉 答對了！【{self.kana_char}】就是 `{self.correct_answer}`！"
                embed.description += (
                    f"\n\n✅ **正確答案**：`{self.correct_answer}`\n"
                    f"📖 **實用單字**：**{card['vocab']}**（{card['vocab_tw']}）"
                )
            else:
                add_mistake(
                    interaction.user.id,
                    f"假名【 {self.kana_char} 】的讀音是？",
                    self.correct_answer,
                    f"平假名 {card['hira']} / 片假名 {card['kata']}，羅馬音為 {card['romaji']}。口訣：{card['mnemonic']}",
                    self.options
                )
                embed.color = discord.Color.red()
                embed.title = f"❌ 哎呀，選成 `{chosen}` 了！"
                embed.description += (
                    f"\n\n✅ **正確答案是**：`{self.correct_answer}`\n"
                    f"💡 **口訣幫你記**：{card['mnemonic']}\n"
                    f"📝 **已自動收錄進智慧錯題本！隨時可用 `/review` 複習！**"
                )

            embed.add_field(
                name="💡【好奇心日語冷知識】",
                value=f"**{trivia['title']}**\n{trivia['story']}",
                inline=False
            )

            next_idx = self.card_idx + 1 if self.card_idx + 1 < len(ALL_KANA_CARDS) else 0
            btn_next_kana = discord.ui.Button(
                label=f"➡️ 學下一個字 ({ALL_KANA_CARDS[next_idx]['hira']})",
                style=discord.ButtonStyle.primary,
                row=1
            )
            async def on_next_kana(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                new_embed = build_kana_card_embed(next_idx)
                new_view = KanaFlashcardView(next_idx)
                await itx.response.edit_message(embed=new_embed, view=new_view)
            btn_next_kana.callback = on_next_kana
            self.add_item(btn_next_kana)

            btn_back_card = discord.ui.Button(
                label="📖 返回本字字卡",
                style=discord.ButtonStyle.secondary,
                row=1
            )
            async def on_back_card(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                new_embed = build_kana_card_embed(self.card_idx)
                new_view = KanaFlashcardView(self.card_idx)
                await itx.response.edit_message(embed=new_embed, view=new_view)
            btn_back_card.callback = on_back_card
            self.add_item(btn_back_card)

            btn_quiz_pool = discord.ui.Button(
                label="🎯 挑戰五十音綜合測驗",
                style=discord.ButtonStyle.success,
                row=1
            )
            async def on_quiz_pool(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                q = random.choice(get_quizzes_by_category("kana"))
                opts = list(q["options"])
                random.shuffle(opts)
                q_embed = discord.Embed(
                    title=f"📝 日語隨堂考：【{q['category']}】",
                    description=f"**{q['question']}**\n\n請點擊下方按鈕進行作答：",
                    color=discord.Color.blue()
                )
                q_view = QuizView(q["question"], q["answer"], q["explanation"], opts, category="kana")
                await itx.response.edit_message(embed=q_embed, view=q_view)
            btn_quiz_pool.callback = on_quiz_pool
            self.add_item(btn_quiz_pool)

            await interaction.response.edit_message(embed=embed, view=self)

        return callback

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


def get_random_daily_phrase():
    """隨機取得一筆日常學習金句"""
    all_phrases = []
    for cat_key, sc in SCENARIOS.items():
        for p in sc["phrases"]:
            all_phrases.append((sc["title"], p))
    return random.choice(all_phrases)


def build_daily_phrase_embed(cat_title: str, item: dict) -> discord.Embed:
    """建立每日一句/學習小卡 Embed（附帶好奇心冷知識）"""
    trivia = get_random_trivia()
    embed = discord.Embed(
        title="🌟 今日日語學習小卡",
        description=f"來自分類：**{cat_title}**\n\n每天學一句，累積出驚人大實力！",
        color=discord.Color.from_rgb(255, 170, 0)
    )
    embed.add_field(name="日文原文", value=f"### 『 {item['japanese']} 』", inline=False)
    embed.add_field(name="讀音與拼音", value=f"• 振假名：`{item['furigana']}`\n• 羅馬音：*{item['romaji']}*", inline=False)
    embed.add_field(name="中文意思", value=f"**{item['meaning']}**", inline=False)
    embed.add_field(name="情境與用法", value=item['usage'], inline=False)
    embed.add_field(
        name="💡【好奇心日語冷知識】",
        value=f"**{trivia['title']}**\n{trivia['story']}",
        inline=False
    )
    embed.set_footer(text="💡 點擊下方按鈕可直接「抽下一張」或前往「從零學五十音」！")
    return embed


class DailyCardView(discord.ui.View):
    """每日學習小卡互動 View（支援連抽下一張、前往五十音與隨堂考）"""
    def __init__(self):
        super().__init__(timeout=None)

        btn_next = discord.ui.Button(label="🎴 抽下一張小卡", style=discord.ButtonStyle.primary)
        btn_next.callback = self.on_next_card
        self.add_item(btn_next)

        btn_kana = discord.ui.Button(label="🔤 從零學五十音", style=discord.ButtonStyle.secondary)
        btn_kana.callback = self.on_kana
        self.add_item(btn_kana)

        btn_quiz = discord.ui.Button(label="🎯 挑戰隨堂測驗", style=discord.ButtonStyle.success)
        btn_quiz.callback = self.on_quiz
        self.add_item(btn_quiz)

    async def on_next_card(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        cat_title, item = get_random_daily_phrase()
        new_embed = build_daily_phrase_embed(cat_title, item)
        new_view = DailyCardView()
        await interaction.response.edit_message(embed=new_embed, view=new_view)

    async def on_kana(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        embed = build_kana_card_embed(0)
        view = KanaFlashcardView(0)
        await interaction.response.edit_message(embed=embed, view=view)

    async def on_quiz(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        q = random.choice(QUIZ_QUESTIONS)
        opts = list(q["options"])
        random.shuffle(opts)
        embed = discord.Embed(
            title=f"📝 日語隨堂考：【{q['category']}】",
            description=f"**{q['question']}**\n\n請點擊下方按鈕進行作答：",
            color=discord.Color.blue()
        )
        view = QuizView(q["question"], q["answer"], q["explanation"], opts, category="all")
        await interaction.response.edit_message(embed=embed, view=view)

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


class QuizView(discord.ui.View):
    """測驗互動按鈕 View（支援智慧錯題本自動收錄、連環作答下一題與冷知識探索）"""
    def __init__(self, question_text: str, correct_answer: str, explanation: str, options: list, category: str = "all"):
        super().__init__(timeout=None)
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.options = options
        self.category = category
        self.responded = False

        # 動態建立按鈕 (第 0 行)
        for option in options:
            btn = discord.ui.Button(label=option, style=discord.ButtonStyle.secondary, row=0)
            btn.callback = self.make_callback(option)
            self.add_item(btn)

    def make_callback(self, chosen: str):
        async def callback(interaction: discord.Interaction):
            if self.responded:
                await interaction.response.send_message("你已經作答過囉！", ephemeral=True)
                return

            self.responded = True
            is_correct = (chosen == self.correct_answer)
            record_daily_activity(interaction.user.id)

            # 停用選項按鈕並標記正解
            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.row == 0:
                    item.disabled = True
                    if item.label == self.correct_answer:
                        item.style = discord.ButtonStyle.success
                    elif item.label == chosen and not is_correct:
                        item.style = discord.ButtonStyle.danger

            embed = interaction.message.embeds[0]
            trivia = get_random_trivia()

            if is_correct:
                unlock_badge(interaction.user.id, "badge_quiz")
                embed.color = discord.Color.green()
                embed.title = "🎉 答對了！太厲害了！"
                embed.description += f"\n\n✅ **正確答案**：`{self.correct_answer}`\n💡 **解析**：{self.explanation}"
            else:
                add_mistake(interaction.user.id, self.question_text, self.correct_answer, self.explanation, self.options)
                embed.color = discord.Color.red()
                embed.title = "❌ 哎呀，答錯了！"
                embed.description += (
                    f"\n\n你選擇了：`{chosen}`\n"
                    f"✅ **正確答案是**：`{self.correct_answer}`\n"
                    f"💡 **解析**：{self.explanation}\n\n"
                    f"📝 **【智慧錯題本】已自動收錄此題！隨時輸入 `/review` 即可進行加強練習！**"
                )

            # 附帶好奇心日語冷知識
            embed.add_field(
                name="💡【好奇心日語冷知識】",
                value=f"**{trivia['title']}**\n{trivia['story']}",
                inline=False
            )

            # 加入接續學習按鈕 (第 1 行)
            btn_next = discord.ui.Button(label="➡️ 挑戰下一題", style=discord.ButtonStyle.primary, row=1)
            async def on_next_quiz(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                questions = get_quizzes_by_category(self.category)
                candidates = [q for q in questions if q["question"] != self.question_text]
                next_q = random.choice(candidates) if candidates else random.choice(questions)
                opts = list(next_q["options"])
                random.shuffle(opts)
                q_embed = discord.Embed(
                    title=f"📝 日語隨堂考：【{next_q['category']}】",
                    description=f"**{next_q['question']}**\n\n請點擊下方按鈕進行作答：",
                    color=discord.Color.blue()
                )
                q_view = QuizView(next_q["question"], next_q["answer"], next_q["explanation"], opts, category=self.category)
                await itx.response.edit_message(embed=q_embed, view=q_view)
            btn_next.callback = on_next_quiz
            self.add_item(btn_next)

            btn_kana = discord.ui.Button(label="🔤 從零學五十音", style=discord.ButtonStyle.secondary, row=1)
            async def on_kana_click(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                k_embed = build_kana_card_embed(0)
                k_view = KanaFlashcardView(0)
                await itx.response.edit_message(embed=k_embed, view=k_view)
            btn_kana.callback = on_kana_click
            self.add_item(btn_kana)

            btn_daily = discord.ui.Button(label="🎴 抽一張學習小卡", style=discord.ButtonStyle.secondary, row=1)
            async def on_daily_click(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                cat_title, item = get_random_daily_phrase()
                d_embed = build_daily_phrase_embed(cat_title, item)
                d_view = DailyCardView()
                await itx.response.edit_message(embed=d_embed, view=d_view)
            btn_daily.callback = on_daily_click
            self.add_item(btn_daily)

            await interaction.response.edit_message(embed=embed, view=self)

        return callback

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


class QuestQuizView(discord.ui.View):
    """每日關卡專屬互動按鈕 View（包含自動升級、存檔、錯題本連動與下一關連續挑戰）"""
    def __init__(self, current_level: int, question_text: str, correct_answer: str, explanation: str, options: list):
        super().__init__(timeout=None)
        self.current_level = current_level
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.options = options
        self.responded = False

        for option in options:
            btn = discord.ui.Button(label=option, style=discord.ButtonStyle.primary, row=0)
            btn.callback = self.make_callback(option)
            self.add_item(btn)

    def make_callback(self, chosen: str):
        async def callback(interaction: discord.Interaction):
            if self.responded:
                await interaction.response.send_message("你已經作答過囉！", ephemeral=True)
                return

            self.responded = True
            is_correct = (chosen == self.correct_answer)
            record_daily_activity(interaction.user.id)

            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.row == 0:
                    item.disabled = True
                    if item.label == self.correct_answer:
                        item.style = discord.ButtonStyle.success
                    elif item.label == chosen and not is_correct:
                        item.style = discord.ButtonStyle.danger

            embed = interaction.message.embeds[0]
            trivia = get_random_trivia()

            if is_correct:
                new_level, is_new = advance_user_level(interaction.user.id, self.current_level)
                embed.color = discord.Color.green()
                embed.title = f"🎉 恭喜通關【第 {self.current_level} 關】！"
                
                upgrade_text = ""
                if is_new and new_level <= TOTAL_QUESTS:
                    upgrade_text = f"\n\n🚀 **等級晉升！你已解鎖【第 {new_level} 關】！**\n👉 點擊下方「➡️ 挑戰下一關」可直接連續闖關！"
                elif self.current_level == TOTAL_QUESTS:
                    upgrade_text = f"\n\n🏆 **【全 {TOTAL_QUESTS} 關大圓滿達成】恭喜完成日語自由行全套闖關！日本旅遊生存神功大成！**"

                embed.description += (
                    f"\n\n✅ **正確答案**：`{self.correct_answer}`\n"
                    f"💡 **解析**：{self.explanation}"
                    f"{upgrade_text}"
                )

                # 下一關按鈕
                target_lvl = self.current_level + 1 if self.current_level < TOTAL_QUESTS else 1
                lbl = f"➡️ 挑戰下一關 (第 {target_lvl} 關)" if self.current_level < TOTAL_QUESTS else "🏆 回第 1 關複習"
                btn_next_level = discord.ui.Button(label=lbl, style=discord.ButtonStyle.success, row=1)
                async def on_next_quest(itx: discord.Interaction):
                    record_daily_activity(itx.user.id)
                    q = QUESTS.get(target_lvl)
                    filled = "🟩" * target_lvl
                    unfilled = "⬜" * max(0, TOTAL_QUESTS - target_lvl)
                    bar = f"{filled}{unfilled} (Level {target_lvl}/{TOTAL_QUESTS})"
                    mnemonic_sec = f"\n{q['mnemonic_story']}\n" if q.get("mnemonic_story") else ""
                    q_embed = discord.Embed(
                        title=f"⚔️ 【日語系統化闖關】{q['title']}",
                        description=(
                            f"📊 **目前進度**：`{bar}`\n\n"
                            f"🔤 **今日假名進度**：`{q['kana_group']}`\n"
                            f"{q['kana_tip']}\n\n"
                            f"------------------------------------\n"
                            f"### 🗣️ 今日實戰金句：『 {q['phrase']} 』\n"
                            f"• **羅馬拼音**：*{q['romaji']}*\n"
                            f"• **口訣諧音**：**{q['phonetic']}**\n"
                            f"• **中文意思**：**{q['meaning']}**\n"
                            f"{mnemonic_sec}\n"
                            f"🍜 **情境示範**：{q['scenario']}\n"
                            f"------------------------------------\n"
                            f"🎯 **【通關驗收題目】**：\n"
                            f"**{q['quiz']['question']}**\n\n"
                            f"👇 **點擊下方按鈕作答！答對即可通過本關並自動晉級！**"
                        ),
                        color=discord.Color.from_rgb(255, 140, 60)
                    )
                    q_embed.set_footer(text="每天只要 15 分鐘打通一關，無痛通關日本自由行！")
                    opts = list(q["quiz"]["options"])
                    random.shuffle(opts)
                    n_view = QuestQuizView(
                        current_level=target_lvl,
                        question_text=q["quiz"]["question"],
                        correct_answer=q["quiz"]["answer"],
                        explanation=q["quiz"]["explanation"],
                        options=opts
                    )
                    await itx.response.edit_message(embed=q_embed, view=n_view)
                btn_next_level.callback = on_next_quest
                self.add_item(btn_next_level)
            else:
                add_mistake(interaction.user.id, self.question_text, self.correct_answer, self.explanation, self.options)
                embed.color = discord.Color.red()
                embed.title = f"❌ 第 {self.current_level} 關挑戰失誤，別氣餒！"
                embed.description += (
                    f"\n\n你選擇了：`{chosen}`\n"
                    f"✅ **正確答案是**：`{self.correct_answer}`\n"
                    f"💡 **解析**：{self.explanation}\n\n"
                    f"📝 **已收錄進錯題本，隨時點下方按鈕重新挑戰！**"
                )

                btn_retry = discord.ui.Button(label=f"🔄 重新挑戰第 {self.current_level} 關", style=discord.ButtonStyle.primary, row=1)
                async def on_retry(itx: discord.Interaction):
                    record_daily_activity(itx.user.id)
                    q = QUESTS.get(self.current_level)
                    filled = "🟩" * self.current_level
                    unfilled = "⬜" * max(0, TOTAL_QUESTS - self.current_level)
                    bar = f"{filled}{unfilled} (Level {self.current_level}/{TOTAL_QUESTS})"
                    mnemonic_sec = f"\n{q['mnemonic_story']}\n" if q.get("mnemonic_story") else ""
                    q_embed = discord.Embed(
                        title=f"⚔️ 【日語系統化闖關】{q['title']}",
                        description=(
                            f"📊 **目前進度**：`{bar}`\n\n"
                            f"🔤 **今日假名進度**：`{q['kana_group']}`\n"
                            f"{q['kana_tip']}\n\n"
                            f"------------------------------------\n"
                            f"### 🗣️ 今日實戰金句：『 {q['phrase']} 』\n"
                            f"• **羅馬拼音**：*{q['romaji']}*\n"
                            f"• **口訣諧音**：**{q['phonetic']}**\n"
                            f"• **中文意思**：**{q['meaning']}**\n"
                            f"{mnemonic_sec}\n"
                            f"🍜 **情境示範**：{q['scenario']}\n"
                            f"------------------------------------\n"
                            f"🎯 **【通關驗收題目】**：\n"
                            f"**{q['quiz']['question']}**\n\n"
                            f"👇 **點擊下方按鈕作答！答對即可通過本關並自動晉級！**"
                        ),
                        color=discord.Color.from_rgb(255, 140, 60)
                    )
                    q_embed.set_footer(text="每天只要 15 分鐘打通一關，無痛通關日本自由行！")
                    opts = list(q["quiz"]["options"])
                    random.shuffle(opts)
                    r_view = QuestQuizView(
                        current_level=self.current_level,
                        question_text=q["quiz"]["question"],
                        correct_answer=q["quiz"]["answer"],
                        explanation=q["quiz"]["explanation"],
                        options=opts
                    )
                    await itx.response.edit_message(embed=q_embed, view=r_view)
                btn_retry.callback = on_retry
                self.add_item(btn_retry)

            btn_kana = discord.ui.Button(label="🔤 從零學五十音", style=discord.ButtonStyle.secondary, row=1)
            async def on_quest_kana(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                k_embed = build_kana_card_embed(0)
                k_view = KanaFlashcardView(0)
                await itx.response.edit_message(embed=k_embed, view=k_view)
            btn_kana.callback = on_quest_kana
            self.add_item(btn_kana)

            embed.add_field(
                name="💡【好奇心日語冷知識】",
                value=f"**{trivia['title']}**\n{trivia['story']}",
                inline=False
            )

            await interaction.response.edit_message(embed=embed, view=self)

        return callback

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True



class RoleplayView(discord.ui.View):
    """AI 實戰情境角色扮演互動對話樹 View"""
    def __init__(self, scenario_key: str, step_idx: int = 0):
        super().__init__(timeout=None)
        self.scenario_key = scenario_key
        self.step_idx = step_idx
        self.scenario_data = ROLEPLAY_SCENARIOS[scenario_key]
        self.current_step = self.scenario_data["steps"][step_idx]

        for i, opt in enumerate(self.current_step["options"]):
            btn = discord.ui.Button(
                label=opt["label"],
                style=discord.ButtonStyle.primary if i == 0 else discord.ButtonStyle.secondary
            )
            btn.callback = self.make_callback(opt)
            self.add_item(btn)

    def make_callback(self, opt: dict):
        async def callback(interaction: discord.Interaction):
            record_daily_activity(interaction.user.id)
            next_step = opt["next_step"]

            if next_step == "end":
                badge_id = self.scenario_data.get("badge")
                if badge_id:
                    unlock_badge(interaction.user.id, badge_id)

                embed = discord.Embed(
                    title=f"🎉 【實戰通關】{self.scenario_data['title']}",
                    description=(
                        f"💬 **你的最後回應**：『 {opt['furigana']} 』\n"
                        f"• 拼音：*{opt['romaji']}*\n"
                        f"• 意思：{opt['meaning']}\n\n"
                        f"👤 **店員/NPC 反饋**：\n> **{opt['npc_reaction']}**\n\n"
                        f"------------------------------------\n"
                        f"🏆 **恭喜完成本情境角色扮演實戰演練！**\n"
                        f"已為您登記今日學習打卡，並解鎖專屬成就勳章！✨\n"
                        f"隨時輸入 `/chat` 可挑戰其他實戰場景！"
                    ),
                    color=discord.Color.green()
                )
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                next_view = RoleplayView(self.scenario_key, next_step)
                next_step_data = self.scenario_data["steps"][next_step]
                
                embed = discord.Embed(
                    title=self.scenario_data["title"],
                    description=(
                        f"💬 **你的上一句回答**：『 {opt['label']} 』\n"
                        f"👤 **NPC 回應**：{opt['npc_reaction']}\n\n"
                        f"------------------------------------\n"
                        f"### 👤 店員/NPC 接著問：\n"
                        f"## 『 {next_step_data['npc']} 』\n"
                        f"• **假名標註**：`{next_step_data['furigana']}`\n"
                        f"• **羅馬拼音**：*{next_step_data['romaji']}*\n"
                        f"• **中文意思**：**{next_step_data['translation']}**\n\n"
                        f"👇 **請點擊下方按鈕選擇您的回應：**"
                    ),
                    color=discord.Color.from_rgb(100, 160, 255)
                )
                await interaction.response.edit_message(embed=embed, view=next_view)

        return callback

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


class KatakanaQuizView(discord.ui.View):
    """片假名外來語測驗按鈕 View（支援連環作答下一題與冷知識探索）"""
    def __init__(self, question_text: str, correct_answer: str, explanation: str, options: list):
        super().__init__(timeout=None)
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.options = options
        self.responded = False

        for opt in options:
            btn = discord.ui.Button(label=opt, style=discord.ButtonStyle.secondary, row=0)
            btn.callback = self.make_callback(opt)
            self.add_item(btn)

    def make_callback(self, chosen: str):
        async def callback(interaction: discord.Interaction):
            if self.responded:
                await interaction.response.send_message("已經作答過囉！", ephemeral=True)
                return

            self.responded = True
            is_correct = (chosen == self.correct_answer)
            record_daily_activity(interaction.user.id)

            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.row == 0:
                    item.disabled = True
                    if item.label == self.correct_answer:
                        item.style = discord.ButtonStyle.success
                    elif item.label == chosen and not is_correct:
                        item.style = discord.ButtonStyle.danger

            embed = interaction.message.embeds[0]
            trivia = get_random_trivia()

            if is_correct:
                unlock_badge(interaction.user.id, "badge_quiz")
                embed.color = discord.Color.green()
                embed.title = "🎉 片假名解碼成功！答對了！"
                embed.description += f"\n\n✅ **正確答案**：`{self.correct_answer}`\n💡 **語源解析**：{self.explanation}"
            else:
                add_mistake(interaction.user.id, self.question_text, self.correct_answer, self.explanation, self.options)
                embed.color = discord.Color.red()
                embed.title = "❌ 哎呀，掉入片假名陷阱！"
                embed.description += (
                    f"\n\n你選擇了：`{chosen}`\n"
                    f"✅ **正確答案是**：`{self.correct_answer}`\n"
                    f"💡 **語源解析**：{self.explanation}\n\n"
                    f"📝 **已收錄進錯題本，隨時輸入 `/review` 可重新複習！**"
                )

            embed.add_field(
                name="💡【好奇心日語冷知識】",
                value=f"**{trivia['title']}**\n{trivia['story']}",
                inline=False
            )

            btn_next_kata = discord.ui.Button(label="➡️ 挑戰下一題外來語", style=discord.ButtonStyle.primary, row=1)
            async def on_next_kata(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                candidates = [k for k in KATAKANA_QUIZZES if k["question"] != self.question_text]
                target_q = random.choice(candidates) if candidates else random.choice(KATAKANA_QUIZZES)
                opts = list(target_q["options"])
                random.shuffle(opts)
                k_embed = discord.Embed(
                    title="🧩 片假名外來語解碼挑戰",
                    description=(
                        f"**{target_q['question']}**\n\n"
                        f"💡 **提示**：{target_q['hint']}\n\n"
                        f"請點擊下方按鈕猜出正確中文意思："
                    ),
                    color=discord.Color.purple()
                )
                k_view = KatakanaQuizView(target_q["question"], target_q["answer"], target_q["explanation"], opts)
                await itx.response.edit_message(embed=k_embed, view=k_view)
            btn_next_kata.callback = on_next_kata
            self.add_item(btn_next_kata)

            btn_kana = discord.ui.Button(label="🔤 從零學五十音", style=discord.ButtonStyle.secondary, row=1)
            async def on_kata_kana(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                k_embed = build_kana_card_embed(0)
                k_view = KanaFlashcardView(0)
                await itx.response.edit_message(embed=k_embed, view=k_view)
            btn_kana.callback = on_kata_kana
            self.add_item(btn_kana)

            await interaction.response.edit_message(embed=embed, view=self)

        return callback

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


class ReviewQuizView(discord.ui.View):
    """智慧錯題本複習專用按鈕 View（支援持續複習下一題與冷知識探索）"""
    def __init__(self, question_text: str, correct_answer: str, explanation: str, options: list):
        super().__init__(timeout=None)
        self.question_text = question_text
        self.correct_answer = correct_answer
        self.explanation = explanation
        self.options = options
        self.responded = False

        for opt in options:
            btn = discord.ui.Button(label=opt, style=discord.ButtonStyle.secondary, row=0)
            btn.callback = self.make_callback(opt)
            self.add_item(btn)

    def make_callback(self, chosen: str):
        async def callback(interaction: discord.Interaction):
            if self.responded:
                await interaction.response.send_message("已經作答過囉！", ephemeral=True)
                return

            self.responded = True
            is_correct = (chosen == self.correct_answer)
            record_daily_activity(interaction.user.id)

            for item in self.children:
                if isinstance(item, discord.ui.Button) and item.row == 0:
                    item.disabled = True
                    if item.label == self.correct_answer:
                        item.style = discord.ButtonStyle.success
                    elif item.label == chosen and not is_correct:
                        item.style = discord.ButtonStyle.danger

            embed = interaction.message.embeds[0]
            trivia = get_random_trivia()

            if is_correct:
                remove_mistake(interaction.user.id, self.question_text)
                embed.color = discord.Color.green()
                embed.title = "🌟【錯題斬除成功！】恭喜你徹底掌握了！"
                embed.description += (
                    f"\n\n✅ **正確答案**：`{self.correct_answer}`\n"
                    f"💡 **解析**：{self.explanation}\n\n"
                    f"✨ **此題已從您的錯題本中移除！並解鎖【🔄 溫故知新】成就勳章！**"
                )
            else:
                embed.color = discord.Color.red()
                embed.title = "❌ 這次還是選錯了，再接再厲！"
                embed.description += (
                    f"\n\n你選擇了：`{chosen}`\n"
                    f"✅ **正確答案依然是**：`{self.correct_answer}`\n"
                    f"💡 **解析**：{self.explanation}\n\n"
                    f"📌 **此題將繼續保留在錯題本中，下次再來攻克它！**"
                )

            embed.add_field(
                name="💡【好奇心日語冷知識】",
                value=f"**{trivia['title']}**\n{trivia['story']}",
                inline=False
            )

            remaining = get_mistakes(interaction.user.id)
            if remaining:
                btn_next = discord.ui.Button(label=f"➡️ 複習下一題 (剩 {len(remaining)} 題)", style=discord.ButtonStyle.primary, row=1)
                async def on_next_review(itx: discord.Interaction):
                    record_daily_activity(itx.user.id)
                    curr_remaining = get_mistakes(itx.user.id)
                    if not curr_remaining:
                        c_embed = discord.Embed(
                            title="🎉 錯題本已全數斬除！",
                            description="太棒了！你的錯題本目前已經沒有待複習題目了！\n隨時可用 `/quiz` 繼續挑戰隨堂測驗！",
                            color=discord.Color.green()
                        )
                        c_view = DailyCardView()
                        await itx.response.edit_message(embed=c_embed, view=c_view)
                        return
                    target = random.choice(curr_remaining)
                    opts = list(target["options"])
                    random.shuffle(opts)
                    r_embed = discord.Embed(
                        title="🔄【艾賓浩斯抗遺忘】錯題複習衝刺",
                        description=(
                            f"📚 **目前累積錯題**：共 {len(curr_remaining)} 題待複習\n"
                            f"------------------------------------\n"
                            f"### ❓ 複習題目：\n"
                            f"**{target['question']}**\n\n"
                            f"👇 **請點擊下方按鈕重新作答，答對即可徹底移出錯題本！**"
                        ),
                        color=discord.Color.orange()
                    )
                    r_embed.set_footer(text="把錯題變成直覺記憶，是學日語最快的神級捷徑！")
                    r_view = ReviewQuizView(target["question"], target["answer"], target["explanation"], opts)
                    await itx.response.edit_message(embed=r_embed, view=r_view)
                btn_next.callback = on_next_review
                self.add_item(btn_next)
            else:
                btn_quiz = discord.ui.Button(label="🎯 挑戰新隨堂測驗 (/quiz)", style=discord.ButtonStyle.success, row=1)
                async def on_new_quiz(itx: discord.Interaction):
                    record_daily_activity(itx.user.id)
                    q = random.choice(QUIZ_QUESTIONS)
                    opts = list(q["options"])
                    random.shuffle(opts)
                    q_embed = discord.Embed(
                        title=f"📝 日語隨堂考：【{q['category']}】",
                        description=f"**{q['question']}**\n\n請點擊下方按鈕進行作答：",
                        color=discord.Color.blue()
                    )
                    q_view = QuizView(q["question"], q["answer"], q["explanation"], opts, category="all")
                    await itx.response.edit_message(embed=q_embed, view=q_view)
                btn_quiz.callback = on_new_quiz
                self.add_item(btn_quiz)

            btn_kana = discord.ui.Button(label="🔤 溫習五十音卡片", style=discord.ButtonStyle.secondary, row=1)
            async def on_rev_kana(itx: discord.Interaction):
                record_daily_activity(itx.user.id)
                k_embed = build_kana_card_embed(0)
                k_view = KanaFlashcardView(0)
                await itx.response.edit_message(embed=k_embed, view=k_view)
            btn_kana.callback = on_rev_kana
            self.add_item(btn_kana)

            await interaction.response.edit_message(embed=embed, view=self)

        return callback

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


class CultureSelectView(discord.ui.View):
    """文化避坑指南切換按鈕 View"""
    def __init__(self, current_key: str):
        super().__init__(timeout=None)
        self.current_key = current_key

        topic_buttons = [
            ("otoshi", "🏮 お通し"),
            ("train", "🚃 電車禮儀"),
            ("onsen", "♨️ 溫泉秘笈"),
            ("eating", "🍡 邊走邊吃"),
            ("tray", "💴 找零托盤"),
            ("taxfree", "🛍️ 免稅密封袋"),
        ]
        for key, name in topic_buttons:
            btn = discord.ui.Button(
                label=name,
                style=discord.ButtonStyle.primary if key == current_key else discord.ButtonStyle.secondary
            )
            btn.callback = self.make_callback(key)
            self.add_item(btn)

    def make_callback(self, topic_key: str):
        async def callback(interaction: discord.Interaction):
            unlock_badge(interaction.user.id, "badge_culture")
            item = CULTURE_TOPICS[topic_key]
            rules_text = "\n".join([f"• {r}" for r in item["rules"]])
            embed = discord.Embed(
                title=item["title"],
                description=(
                    f"🏷️ **所屬分類**：`{item['category']}`\n\n"
                    f"❓ **常見疑問/痛點**：\n> {item['problem']}\n\n"
                    f"💡 **在地文化真相**：\n{item['explanation']}\n\n"
                    f"------------------------------------\n"
                    f"🛡️ **【避坑生存守則】**：\n{rules_text}\n\n"
                    f"------------------------------------\n"
                    f"🗣️ **必備應對日語**：\n"
                    f"『 **{item['japanese_phrase']}** 』\n"
                    f"• 拼音：*{item['romaji']}*"
                ),
                color=discord.Color.from_rgb(255, 120, 80)
            )
            embed.set_footer(text="入鄉隨俗，懂禮儀玩得更開心尊嚴！點擊下方按鈕切換其他主題。")
            new_view = CultureSelectView(topic_key)
            await interaction.response.edit_message(embed=embed, view=new_view)

        return callback

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


class SOSView(discord.ui.View):
    """日本緊急求助手指卡切換 View"""
    def __init__(self, current_key: str = "medical"):
        super().__init__(timeout=None)
        self.current_key = current_key

        scenarios = [
            ("medical", "🏥 就醫看病"),
            ("lost", "👛 物品遺失"),
            ("police", "🚨 緊急報警"),
            ("direction", "🧭 交通迷路"),
            ("contacts", "📞 緊急電話"),
        ]
        for key, name in scenarios:
            btn = discord.ui.Button(
                label=name,
                style=discord.ButtonStyle.danger if key in ["medical", "police"] else (
                    discord.ButtonStyle.primary if key == current_key else discord.ButtonStyle.secondary
                )
            )
            btn.callback = self.make_callback(key)
            self.add_item(btn)

    def make_callback(self, chosen_key: str):
        async def callback(interaction: discord.Interaction):
            unlock_badge(interaction.user.id, "badge_sos")
            if chosen_key == "contacts":
                embed = discord.Embed(
                    title="📞 【全日本緊急聯絡電話總整理】",
                    description="⚠️ **遇到緊急危難時請即刻撥打（日本公用電話免投幣直接按緊急鈕）：**\n\n",
                    color=discord.Color.red()
                )
                for c in EMERGENCY_CONTACTS:
                    embed.add_field(name=f"☎️ {c['name']}：`{c['number']}`", value=f"• 說明：{c['note']}", inline=False)
                embed.set_footer(text="請保持冷靜，清晰說出所在位置與自身狀況！")
            else:
                data = SOS_SCENARIOS[chosen_key]
                embed = discord.Embed(
                    title=f"🚨 【緊急手指求助卡】{data['title']}",
                    description=f"**{data['intro']}**\n\n",
                    color=discord.Color.red() if chosen_key in ["medical", "police"] else discord.Color.orange()
                )
                for c in data["cards"]:
                    embed.add_field(
                        name=f"🏷️ 【{c['tag']}】",
                        value=(
                            f"## 『 {c['japanese']} 』\n"
                            f"• 假名：`{c['furigana']}`\n"
                            f"• 拼音：*{c['romaji']}*\n"
                            f"• 🇹🇼 **中文意涵**：**{c['chinese']}**"
                        ),
                        inline=False
                    )
                embed.set_footer(text="不用開口！直接拿著此畫面給日本人看即可求救！")

            new_view = SOSView(chosen_key)
            await interaction.response.edit_message(embed=embed, view=new_view)
        return callback


class MenuView(discord.ui.View):
    """日本燒肉、壽司與點餐暗號切換 View"""
    def __init__(self, current_cat: str = "yakiniku"):
        super().__init__(timeout=None)
        self.current_cat = current_cat

        categories = [
            ("yakiniku", "🥩 燒肉部位解碼"),
            ("sushi", "🍣 壽司魚種速查"),
            ("custom_order", "🍜 點餐客製暗號"),
        ]
        for key, name in categories:
            btn = discord.ui.Button(
                label=name,
                style=discord.ButtonStyle.primary if key == current_cat else discord.ButtonStyle.secondary
            )
            btn.callback = self.make_callback(key)
            self.add_item(btn)

    def make_callback(self, cat_key: str):
        async def callback(interaction: discord.Interaction):
            unlock_badge(interaction.user.id, "badge_menu")
            data = MENU_CATEGORIES[cat_key]
            embed = discord.Embed(
                title=data["title"],
                description=f"{data['description']}\n\n",
                color=discord.Color.gold()
            )
            for item in data["items"]:
                embed.add_field(
                    name=f"🍽️ {item['japanese']}（{item['meaning']}）",
                    value=f"• 讀音：`{item['furigana']}`\n• 💡 **老饕解析**：{item['detail']}",
                    inline=False
                )
            embed.set_footer(text="點餐神器！看懂片假名與行家暗號，享受道地美食！")
            new_view = MenuView(cat_key)
            await interaction.response.edit_message(embed=embed, view=new_view)
        return callback


class GrammarSelectView(discord.ui.View):
    """動詞變化與口訣切換 View"""
    def __init__(self, current_key: str = "mnemonic"):
        super().__init__(timeout=None)
        self.current_key = current_key

        verbs = [
            ("mnemonic", "🎵 て形口訣歌"),
            ("iku", "行く (去)"),
            ("taberu", "食べる (吃)"),
            ("nomu", "飲む (喝)"),
            ("suru", "する (做)"),
            ("kuru", "来る (來)"),
        ]
        for key, name in verbs:
            btn = discord.ui.Button(
                label=name,
                style=discord.ButtonStyle.success if key == "mnemonic" else (
                    discord.ButtonStyle.primary if key == current_key else discord.ButtonStyle.secondary
                )
            )
            btn.callback = self.make_callback(key)
            self.add_item(btn)

    def make_callback(self, verb_key: str):
        async def callback(interaction: discord.Interaction):
            unlock_badge(interaction.user.id, "badge_grammar")
            if verb_key == "mnemonic":
                embed = discord.Embed(
                    title="🎵 【日語動詞て形・神級口訣記憶歌】",
                    description=TE_FORM_MNEMONIC,
                    color=discord.Color.green()
                )
                embed.set_footer(text="朗朗上口，跟著唱 3 遍，動詞變化不再混淆！")
            else:
                data = VERB_CONJUGATIONS[verb_key]
                embed = discord.Embed(
                    title=f"🧩 動詞變化速查：{data['verb']}",
                    description=(
                        f"• **類別**：`{data['type']}`\n"
                        f"• **中文意思**：**{data['meaning']}**\n"
                        f"• 🌟 **實用例句**：{data['example']}\n\n"
                        f"------------------------------------\n"
                        f"### 📋 【全套動詞變化展開表】"
                    ),
                    color=discord.Color.from_rgb(100, 200, 255)
                )
                for form_name, form_val in data["forms"].items():
                    embed.add_field(name=form_name, value=f"`{form_val}`", inline=True)
                embed.set_footer(text="點擊下方按鈕切換不同核心動詞或查看口訣歌！")

            new_view = GrammarSelectView(verb_key)
            await interaction.response.edit_message(embed=embed, view=new_view)
        return callback


# ----------------------------------------------------
# ⛩️【御神籤 Omikuji 互動 View】
# ----------------------------------------------------
class OmikujiView(discord.ui.View):
    """神社御神籤互動 View：支援再次求籤、聆聽箴言語音發音"""
    def __init__(self, fortune_data: dict):
        super().__init__(timeout=None)
        self.data = fortune_data

        btn_redraw = discord.ui.Button(label="⛩️ 再求一籤 (抽籤)", style=discord.ButtonStyle.primary, row=0)
        btn_redraw.callback = self.on_redraw
        self.add_item(btn_redraw)

        btn_voice = discord.ui.Button(label="🔊 聆聽今日箴言朗讀", style=discord.ButtonStyle.success, row=0)
        btn_voice.callback = self.on_voice
        self.add_item(btn_voice)

    async def on_redraw(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        new_data = draw_omikuji()
        embed = build_omikuji_embed(new_data)
        new_view = OmikujiView(new_data)
        await interaction.response.edit_message(embed=embed, view=new_view)

    async def on_voice(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        await interaction.response.defer(ephemeral=True)
        try:
            phrase = f"{self.data['quote']}。{self.data['lucky_word']}"
            voice_path = await text_to_speech(phrase, f"omikuji_{self.data['id']}.mp3", rate="-20%")
            file = discord.File(voice_path, filename="omikuji_voice.mp3")
            await interaction.followup.send(f"🌸 今日幸運日語箴言：『**{self.data['quote']}**』語音送達！", file=file, ephemeral=True)
        except Exception:
            await interaction.followup.send("語音生成稍有延遲，請稍後再試！", ephemeral=True)


def build_omikuji_embed(data: dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"⛩️【日本神社御神籤】運勢：『 {data['fortune']} 』",
        description=(
            f"祈願心誠則靈，為您抽出今日靈籤：\n\n"
            f"------------------------------------\n"
            f"### 📜 【今日日語箴言・古風籤詩】\n"
            f"## 『 {data['quote']} 』\n"
            f"• **羅馬拼音**：*{data['romaji']}*\n"
            f"• **籤詩寓意**：**{data['meaning']}**\n\n"
            f"------------------------------------\n"
            f"🌟 **今日開運指南**：\n"
            f"{data['detail']}\n\n"
            f"------------------------------------\n"
            f"🎁 **開運幸運物**：`{data['lucky_item']}`\n"
            f"🔤 **今日開運單字**：**{data['lucky_word']}**"
        ),
        color=data["color"]
    )
    embed.set_footer(text="御神籤心誠則吉 | 點擊按鈕可再次抽籤或聆聽箴言朗讀！")
    return embed


# ----------------------------------------------------
# 🏪【藥妝超商掃雷 Drugstore / Market Scanner View】
# ----------------------------------------------------
class DrugstoreSelectView(discord.ui.View):
    """藥妝/美妝/食品超商掃雷分類互動 View"""
    def __init__(self, current_category: str = "drugstore"):
        super().__init__(timeout=None)
        self.current_category = current_category

        options = [
            discord.SelectOption(label="💊 藥妝常備藥標示 (感冒/止痛/胃藥/眼藥)", value="drugstore", default=(current_category == "drugstore")),
            discord.SelectOption(label="💄 美妝保養功效 (保濕/清爽/美白/毛穴/抗痘)", value="skincare", default=(current_category == "skincare")),
            discord.SelectOption(label="🍱 超商超市食品 (消費期限/賞味期限/半額/無糖)", value="food", default=(current_category == "food")),
        ]
        select = discord.ui.Select(placeholder="🔍 切換日本採購速查分類...", options=options, row=0)
        select.callback = self.on_select
        self.add_item(select)

    async def on_select(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        chosen = interaction.data["values"][0]
        embed = build_drugstore_embed(chosen)
        new_view = DrugstoreSelectView(chosen)
        await interaction.response.edit_message(embed=embed, view=new_view)


def build_drugstore_embed(cat_key: str) -> discord.Embed:
    data = SCAN_CATEGORIES.get(cat_key, SCAN_CATEGORIES["drugstore"])
    embed = discord.Embed(
        title=data["title"],
        description=f"{data['desc']}\n\n" + "------------------------------------",
        color=discord.Color.from_rgb(255, 105, 180) if cat_key == "skincare" else (discord.Color.from_rgb(50, 205, 50) if cat_key == "food" else discord.Color.from_rgb(0, 191, 255))
    )

    for item in data["items"]:
        field_name = f"🏷️ {item['jp']}（{item['furigana']}）"
        field_value = f"• **中文意思**：**{item['meaning']}**\n• 💡 **採購小秘訣**：{item['tip']}"
        embed.add_field(name=field_name, value=field_value, inline=False)

    embed.set_footer(text="赴日掃貨必備指南 | 點擊下拉選單快速切換美妝、藥品、超商標籤！")
    return embed


# ----------------------------------------------------
# 🎵【J-POP 歌詞日語教室 Lyrics View】
# ----------------------------------------------------
class LyricsSelectView(discord.ui.View):
    """J-POP 歌詞日語教室互動 View：切換神曲、播放正版原曲音樂、慢速朗讀與外鏈"""
    def __init__(self, current_song_key: str = "idol"):
        super().__init__(timeout=None)
        self.current_song_key = current_song_key
        song = JPOP_SONGS[current_song_key]

        # Row 0: 下拉切換歌曲
        options = []
        for sk, sdata in JPOP_SONGS.items():
            label = sdata["title"][:100]
            options.append(discord.SelectOption(label=label, value=sk, default=(sk == current_song_key)))

        select = discord.ui.Select(placeholder="🎵 選擇 J-POP 經典歌曲教室...", options=options, row=0)
        select.callback = self.on_select
        self.add_item(select)

        # Row 1: 30秒原曲音樂、30秒導讀拆字電台、隨機換歌
        btn_music = discord.ui.Button(label="🎵 30 秒原曲音樂", style=discord.ButtonStyle.success, row=1)
        btn_music.callback = self.on_music
        self.add_item(btn_music)

        btn_guide = discord.ui.Button(label="🎙️ 30 秒導讀與拆字電台", style=discord.ButtonStyle.secondary, row=1)
        btn_guide.callback = self.on_guide
        self.add_item(btn_guide)

        btn_random = discord.ui.Button(label="🎲 換一首名曲", style=discord.ButtonStyle.primary, row=1)
        btn_random.callback = self.on_random
        self.add_item(btn_random)

        # Row 2: 官方 MV 與 Spotify 直達連結
        if song.get("mv_url"):
            btn_mv = discord.ui.Button(label="🎬 官方 YouTube MV", url=song["mv_url"], row=2)
            self.add_item(btn_mv)
        if song.get("spotify_url"):
            btn_spot = discord.ui.Button(label="🎧 Spotify 正版收聽", url=song["spotify_url"], row=2)
            self.add_item(btn_spot)

    async def on_select(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        chosen = interaction.data["values"][0]
        embed = build_lyrics_embed(chosen)
        new_view = LyricsSelectView(chosen)
        await interaction.response.edit_message(embed=embed, view=new_view)

    async def on_random(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        other_keys = [k for k in JPOP_SONGS.keys() if k != self.current_song_key]
        chosen = random.choice(other_keys) if other_keys else self.current_song_key
        embed = build_lyrics_embed(chosen)
        new_view = LyricsSelectView(chosen)
        await interaction.response.edit_message(embed=embed, view=new_view)

    async def on_music(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        await interaction.response.defer(ephemeral=True)
        song = JPOP_SONGS[self.current_song_key]
        clip_rel = song.get("music_file", "")
        clip_full = os.path.join(os.path.dirname(__file__), clip_rel)
        if os.path.exists(clip_full):
            file = discord.File(clip_full, filename=f"{self.current_song_key}_music.m4a")
            await interaction.followup.send(f"🎵 **{song['title']}** 30 秒正版原曲音樂片段送達！點擊即可聆聽真人真聲演唱：👇", file=file, ephemeral=True)
        else:
            await interaction.followup.send(f"🎵 原曲音樂加載中，請點擊下方按鈕直接觀看 YouTube MV 或 Spotify！", ephemeral=True)

    async def on_guide(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        await interaction.response.defer(ephemeral=True)
        song = JPOP_SONGS[self.current_song_key]
        guide_rel = song.get("guide_file", "")
        guide_full = os.path.join(os.path.dirname(__file__), guide_rel)
        embed = build_beginner_guide_embed(self.current_song_key)
        if os.path.exists(guide_full):
            file = discord.File(guide_full, filename=f"{self.current_song_key}_guide.mp3")
            await interaction.followup.send(embed=embed, file=file, ephemeral=True)
        else:
            await interaction.followup.send(embed=embed, ephemeral=True)


def build_beginner_guide_embed(song_key: str) -> discord.Embed:
    song = JPOP_SONGS[song_key]
    lecture = song.get("beginner_lecture")

    embed = discord.Embed(
        title=f"📖【零基礎小白・歌詞拆字圖文講義】{song['title']}",
        description=(
            f"🎤 **演唱歌手**：`{song['artist']}` | 🎬 **出處**：`{song['anime']}`\n\n"
            f"💡 **新手無痛指引**：不用死記死板文法術語！我們把歌詞拆成**『日語積木小零件』**，對照大白話，秒速搞懂意思～"
        ),
        color=song["color"]
    )

    if lecture and "lines" in lecture:
        for idx, line in enumerate(lecture["lines"], 1):
            parts_str = "\n".join([f"• 🔹 **{p[0]}**：{p[1]}" for p in line["parts"]])
            field_name = f"🧩 第 {idx} 句：『 {line['original']} 』"
            field_value = (
                f"🔤 **讀音**：`{line['furi']}`\n"
                f"🗣️ **拼音**：*{line['romaji']}*\n"
                f"🇹🇼 **大白話意思**：**{line['chinese']}**\n\n"
                f"**【拆字小積木零件】**：\n"
                f"{parts_str}\n\n"
                f"{line['plain_talk']}"
            )
            embed.add_field(name=field_name, value=field_value, inline=False)

        if lecture.get("sing_tip"):
            embed.add_field(
                name="🎤 跟唱練習小秘訣",
                value=lecture["sing_tip"],
                inline=False
            )

    if song.get("artwork"):
        embed.set_thumbnail(url=song["artwork"])

    embed.set_footer(text="🎧 搭配下方 30 秒語音電台，邊看文字拆解邊聽導讀，零基礎也能輕鬆學會！")
    return embed


def build_lyrics_embed(song_key: str) -> discord.Embed:
    song = JPOP_SONGS[song_key]
    embed = discord.Embed(
        title=f"🎵 J-POP 經典名曲日語教室：{song['title']}",
        description=(
            f"🎤 **演唱歌手**：`{song['artist']}`\n"
            f"🎬 **作品出處**：`{song['anime']}`\n\n"
            f"🎧 **【雙音頻專欄】**：下方已為您附帶 **30 秒原曲音樂** 與 **30 秒名師導讀拆字電台**！\n\n"
            f"------------------------------------\n"
            f"### 🎶 【經典高潮副歌歌詞】\n"
            f"```\n{song['lyrics_jp']}\n```\n"
            f"🔤 **平假名讀音**：\n> {song['lyrics_reading']}\n\n"
            f"🗣️ **羅馬拼音**：\n> *{song['lyrics_romaji']}*\n\n"
            f"🇹🇼 **中文意境翻譯**：\n> **{song['meaning']}**\n\n"
            f"------------------------------------\n"
            f"🧩 **【核心文法剖析】**：\n{song['grammar_point']}\n\n"
            f"------------------------------------\n"
            f"📖 **【歌詞必學高頻單字拆解】**："
        ),
        color=song["color"]
    )

    for v in song["vocab"]:
        embed.add_field(name=f"✨ {v['word']} ({v['reading']})", value=f"意思：**{v['meaning']}**", inline=True)

    if song.get("artwork"):
        embed.set_thumbnail(url=song["artwork"])

    embed.set_footer(text="🎧 內建雙音檔：30 秒正版原曲音樂 + 30 秒名師導讀拆字電台！亦可直達 YouTube MV 與 Spotify！")
    return embed


# ----------------------------------------------------
# 🔤【五十音極速消除小遊戲 Kana Game View】
# ----------------------------------------------------
class KanaGameView(discord.ui.View):
    """五十音連連看極速消除小遊戲：不記分無壓力，純粹享受刷題手感！"""
    def __init__(self, round_num: int = 1):
        super().__init__(timeout=None)
        self.round_num = round_num

        # 隨機挑選 1 個假名作為題目
        self.card = random.choice(ALL_KANA_CARDS)
        self.mode = random.choice(["hira_to_kata", "kata_to_hira", "hira_to_romaji"])

        if self.mode == "hira_to_kata":
            self.question = f"請問平假名『 **{self.card['hira']}** 』對應的【片假名】是哪一個？"
            self.correct = self.card["kata"]
            distractors = [c["kata"] for c in ALL_KANA_CARDS if c["kata"] != self.correct]
        elif self.mode == "kata_to_hira":
            self.question = f"請問片假名『 **{self.card['kata']}** 』對應的【平假名】是哪一個？"
            self.correct = self.card["hira"]
            distractors = [c["hira"] for c in ALL_KANA_CARDS if c["hira"] != self.correct]
        else:
            self.question = f"請問假名『 **{self.card['hira']}** 』({self.card['kata']}) 的【羅馬拼音】是哪一個？"
            self.correct = self.card["romaji"]
            distractors = [c["romaji"] for c in ALL_KANA_CARDS if c["romaji"] != self.correct]

        wrong_options = random.sample(list(set(distractors)), 3)
        self.options = wrong_options + [self.correct]
        random.shuffle(self.options)

        for opt in self.options:
            btn = discord.ui.Button(label=opt, style=discord.ButtonStyle.secondary, row=0)
            btn.callback = self.make_callback(opt)
            self.add_item(btn)

    def make_callback(self, chosen: str):
        async def callback(interaction: discord.Interaction):
            record_daily_activity(interaction.user.id)
            is_correct = (chosen == self.correct)

            if is_correct:
                # 答對瞬間直接生成下一題！極速消除連擊
                next_view = KanaGameView(round_num=self.round_num + 1)
                embed = next_view.build_embed(feedback=f"✨ 答對了！『{self.card['hira']}』就是 `{self.correct}`！連擊中 ➔ 進入第 {self.round_num + 1} 題！")
                await interaction.response.edit_message(embed=embed, view=next_view)
            else:
                # 答錯給予親切口訣提示，不扣分
                embed = discord.Embed(
                    title="💡 差一點點！口訣幫你想起來：",
                    description=(
                        f"假名 **『 {self.card['hira']} 』** / **『 {self.card['kata']} 』**\n"
                        f"正確答案是：**`{self.correct}`**！\n\n"
                        f"💡 **記憶口訣**：{self.card['mnemonic']}\n\n"
                        f"隨心玩不計分，點擊下方「繼續消除」開下一題！"
                    ),
                    color=discord.Color.gold()
                )
                retry_view = discord.ui.View(timeout=None)
                btn_continue = discord.ui.Button(label="➡️ 繼續消除下一題！", style=discord.ButtonStyle.primary)
                async def on_continue(itx: discord.Interaction):
                    record_daily_activity(itx.user.id)
                    nv = KanaGameView(round_num=self.round_num + 1)
                    await itx.response.edit_message(embed=nv.build_embed(), view=nv)
                btn_continue.callback = on_continue
                retry_view.add_item(btn_continue)
                await interaction.response.edit_message(embed=embed, view=retry_view)
        return callback

    def build_embed(self, feedback: str = None) -> discord.Embed:
        desc = ""
        if feedback:
            desc += f"🎉 **{feedback}**\n\n------------------------------------\n"

        desc += (
            f"### 🎯 【第 {self.round_num} 輪消除】\n"
            f"## {self.question}\n\n"
            f"💡 **記憶提示**：{self.card['mnemonic']}\n\n"
            f"👇 **點擊下方正確按鈕立即消除：**"
        )

        embed = discord.Embed(
            title="🎮 五十音極速消除連連看 (Kana Game)",
            description=desc,
            color=discord.Color.from_rgb(255, 105, 180)
        )
        embed.set_footer(text="純粹享受點擊刷題手感！不計分、無壓力、隨時可停！")
        return embed


# ----------------------------------------------------
# 🌸【每日推播一鍵直達中樞 View (DailyHubView)】
# ----------------------------------------------------
class DailyHubView(discord.ui.View):
    """每日推播一鍵直達中樞：免記指令，點擊按鈕直接開箱抽籤、歌詞、小遊戲、藥妝與自動播放"""
    def __init__(self, current_row_key: str = "a"):
        super().__init__(timeout=None)
        self.row_key = current_row_key

        # Row 0: 核心趣味互動
        btn_omikuji = discord.ui.Button(label="⛩️ 抽今日御神籤", style=discord.ButtonStyle.primary, row=0)
        btn_omikuji.callback = self.on_omikuji
        self.add_item(btn_omikuji)

        btn_loop = discord.ui.Button(label="▶️ 自動播放本站假名", style=discord.ButtonStyle.success, row=0)
        btn_loop.callback = self.on_loop
        self.add_item(btn_loop)

        btn_game = discord.ui.Button(label="🎮 玩玩消除小遊戲", style=discord.ButtonStyle.secondary, row=0)
        btn_game.callback = self.on_game
        self.add_item(btn_game)

        # Row 1: 實戰探索
        btn_lyrics = discord.ui.Button(label="🎵 聽 J-POP 歌詞", style=discord.ButtonStyle.secondary, row=1)
        btn_lyrics.callback = self.on_lyrics
        self.add_item(btn_lyrics)

        btn_drug = discord.ui.Button(label="🏪 日本超商藥妝掃雷", style=discord.ButtonStyle.secondary, row=1)
        btn_drug.callback = self.on_drugstore
        self.add_item(btn_drug)

    async def on_omikuji(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        fortune = draw_omikuji()
        embed = build_omikuji_embed(fortune)
        view = OmikujiView(fortune)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def on_loop(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        row_starts = {
            "a": 0, "ka": 5, "sa": 10, "ta": 15, "na": 20,
            "ha": 25, "ma": 30, "ya": 35, "ra": 38, "wa": 43
        }
        start_idx = row_starts.get(self.row_key, 0)
        auto_view = KanaAutoPlayView(current_idx=start_idx, speed_seconds=4.0)
        auto_embed = auto_view.build_autoplay_embed()
        await interaction.response.send_message(embed=auto_embed, view=auto_view, ephemeral=True)
        auto_view.start_loop(interaction)

    async def on_game(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        game_view = KanaGameView(round_num=1)
        embed = game_view.build_embed()
        await interaction.response.send_message(embed=embed, view=game_view, ephemeral=True)

    async def on_lyrics(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        if not JPOP_SONGS:
            await interaction.response.send_message(LYRICS_MISSING_MSG, ephemeral=True)
            return
        song_key = random.choice(list(JPOP_SONGS.keys()))
        embed = build_lyrics_embed(song_key)
        view = LyricsSelectView(song_key)
        song_data = JPOP_SONGS[song_key]

        files_to_send = []
        clip_rel = song_data.get("music_file", "")
        clip_full = os.path.join(os.path.dirname(__file__), clip_rel)
        if os.path.exists(clip_full):
            files_to_send.append(discord.File(clip_full, filename=f"{song_key}_music.m4a"))

        guide_rel = song_data.get("guide_file", "")
        guide_full = os.path.join(os.path.dirname(__file__), guide_rel)
        if os.path.exists(guide_full):
            files_to_send.append(discord.File(guide_full, filename=f"{song_key}_guide.mp3"))

        if files_to_send:
            await interaction.response.send_message(embed=embed, files=files_to_send, view=view, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def on_drugstore(self, interaction: discord.Interaction):
        record_daily_activity(interaction.user.id)
        chosen = random.choice(["drugstore", "skincare", "food"])
        embed = build_drugstore_embed(chosen)
        view = DrugstoreSelectView(chosen)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)




# 學習計畫 Embed 產生函式與互動按鈕 View
def build_roadmap_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🌸 全方位日語學習路線圖（Roadmap）",
        description=(
            "**零基礎到生活與職場四大階段導引：**\n"
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
    embed.add_field(
        name="🎯 四大核心場景能力",
        value=(
            "• ✈️ **旅遊**：點餐、問路、交通搭乘、免稅退稅無痛通關\n"
            "• 🏠 **生活**：超商採購、租屋手續、看診就醫溝通\n"
            "• 🎮 **休閒**：生肉/日文字幕看懂動漫、日劇與日本推特\n"
            "• 💼 **工作**：日商應對、商業 Email 書信、敬語體系"
        ),
        inline=False
    )
    embed.set_footer(text="點擊下方按鈕切換「假日沉浸計畫」或「平日微學習計畫」！")
    return embed

def build_weekday_plan_embed() -> discord.Embed:
    embed = discord.Embed(
        title="☕【平日通勤專屬】每日 15 分鐘無痛微學習計畫",
        description=(
            "針對忙碌上班族與學生設計！平日生活步調緊湊，目標不是苦讀，而是**「維持語感不中斷」**！\n\n"
            "------------------------------------\n"
            "### ⏱️ 【每日 15 分鐘黃金三部曲】：\n"
            "• ☀️ **前 5 分鐘【熱身刷卡】**：\n"
            "  - 利用搭捷運、公車或早晨零碎時間，輸入 `/daily` 抽取今日日語小卡，或用 `/kana` 複習一行發音。\n\n"
            "• 🧠 **中 7 分鐘【微量吸收】**：\n"
            "  - 每天只挑戰 1 個主線關卡 `/quest`，搞懂 1 個核心句型與諧音口訣；或用 `/grammar` 速查 1 個動詞變化。\n\n"
            "• 🗣️ **後 3 分鐘【開口跟讀】**：\n"
            "  - 大聲跟讀音檔 3 次，形成舌頭肌肉記憶，完成隨堂按鈕作答立即打卡收工！"
        ),
        color=discord.Color.from_rgb(255, 170, 0)
    )
    embed.add_field(
        name="💡 平日心態守則",
        value="今天加班太累也完全沒關係！哪怕只在 Discord 裡玩 1 題 `/quiz`，每打卡一天累積天數（Streak）就加一，您就已經走在領先的道路上！",
        inline=False
    )
    embed.set_footer(text="點擊下方按鈕可切換「假日沉浸計畫」或「全階段路線圖」！")
    return embed

def build_weekend_plan_embed() -> discord.Embed:
    embed = discord.Embed(
        title="🏖️【週末假期專屬】30~45 分鐘沉浸式日語實戰計畫",
        description=(
            "週末告別死記硬背！放鬆心情，將平日累積的假名與單字轉化為**感官沉浸與實戰樂趣**！\n"
            "建議於週六或週日任選 **2~3 個 15 分鐘模組** 自由搭配執行：\n\n"
            "------------------------------------\n"
            "### 🎬 模組 1：【動漫時事・微精聽沉浸】(15 分鐘)\n"
            "• 🎌 **動漫名台詞教室**：輸入 `/anime` 挑選一部喜歡的作品（鬼滅、咒術、柯南），精聽名台詞發音，搞懂熱血口語與句尾語氣！\n"
            "• 📰 **NHK 通勤新聞微閱讀**：輸入 `/news` 閱讀一篇簡易時事新聞（櫻花預測、新幹線行李新制），邊聽真人朗讀邊跟讀關鍵單字！\n\n"
            "------------------------------------\n"
            "### 🍜 模組 2：【實戰生活・情境模擬與美食解碼】(15 分鐘)\n"
            "• 🤖 **AI 角色扮演實戰**：輸入 `/chat` 模擬在日本拉麵店、飯店入住、超商或居酒屋的分支對話，大聲念出按鈕日語！\n"
            "• 🥩 **饕客美食暗號**：輸入 `/menu` 解碼日本燒肉部位（カルビ、ハラミ）與壽司魚種，記住「つゆだく」等在地老饕點餐密技！\n"
            "• 🛡️ **文化避坑手冊**：輸入 `/culture` 掌握居酒屋お通し收費、電車規矩、溫泉入浴禮儀，赴日不踩雷！\n\n"
            "------------------------------------\n"
            "### 🗣️ 模組 3：【發音影子跟讀・錯題本大清倉】(15 分鐘)\n"
            "• 📈 **影子跟讀挑戰 (Shadowing)**：輸入 `/shadowing` 挑選日常句子，觀察高低音走向（Pitch Accent），邊聽邊落後 0.5 秒跟讀模仿！\n"
            "• 🔄 **錯題本清倉大反攻**：輸入 `/review` 集中攻克平日答錯的題目，一題題斬除清空，徹底固化成長期記憶！"
        ),
        color=discord.Color.from_rgb(0, 190, 240)
    )
    embed.add_field(
        name="🎖️ 週末專屬獎勵",
        value=(
            "• 只要在週六或週日完成任何一項學習指令，即可立即解鎖 **「🏖️ 週末充電王」** 專屬成就勳章！\n"
            "• 輸入 `/profile` 查看一週成果，或輸入 `/leaderboard` 查看全服學霸天梯排行！"
        ),
        inline=False
    )
    embed.set_footer(text="享受日語樂趣，就是進步最快的捷徑！點擊下方按鈕隨時切換。")
    return embed

class PlanView(discord.ui.View):
    def __init__(self, current_mode: str = "weekend"):
        super().__init__(timeout=None)
        self.current_mode = current_mode
        self._update_buttons()

    def _update_buttons(self):
        self.clear_items()

        btn_weekend = discord.ui.Button(
            label="🏖️ 假日沉浸計畫 (30~45分)",
            style=discord.ButtonStyle.success if self.current_mode == "weekend" else discord.ButtonStyle.secondary,
            custom_id="plan_btn_weekend"
        )
        btn_weekday = discord.ui.Button(
            label="☕ 平日通勤計畫 (15分)",
            style=discord.ButtonStyle.primary if self.current_mode == "weekday" else discord.ButtonStyle.secondary,
            custom_id="plan_btn_weekday"
        )
        btn_roadmap = discord.ui.Button(
            label="🗺️ 全階段路線圖",
            style=discord.ButtonStyle.danger if self.current_mode == "roadmap" else discord.ButtonStyle.secondary,
            custom_id="plan_btn_roadmap"
        )

        async def cb_weekend(interaction: discord.Interaction):
            new_view = PlanView("weekend")
            await interaction.response.edit_message(embed=build_weekend_plan_embed(), view=new_view)

        async def cb_weekday(interaction: discord.Interaction):
            new_view = PlanView("weekday")
            await interaction.response.edit_message(embed=build_weekday_plan_embed(), view=new_view)

        async def cb_roadmap(interaction: discord.Interaction):
            new_view = PlanView("roadmap")
            await interaction.response.edit_message(embed=build_roadmap_embed(), view=new_view)

        btn_weekend.callback = cb_weekend
        btn_weekday.callback = cb_weekday
        btn_roadmap.callback = cb_roadmap

        self.add_item(btn_weekend)
        self.add_item(btn_weekday)
        self.add_item(btn_roadmap)


# 日本高頻招牌與菜單速查解密庫 (50+ 組詞彙)
SIGN_DATABASE = {
    "ラーメン": {"furigana": "ラーメン", "romaji": "rāmen", "meaning": "拉麵", "tip": "日本國民美食，常見豚骨、醬油、鹽味與味噌四大派系。"},
    "つけ麺": {"furigana": "つけめん", "romaji": "tsukemen", "meaning": "沾麵", "tip": "麵條通常較粗且冰鎮過，沾著濃厚熱湯汁吸入食用。"},
    "替玉": {"furigana": "かえだま", "romaji": "kaedama", "meaning": "加麵 (拉麵續麵)", "tip": "在吃完麵前留半碗湯，舉手喊『替玉お願いします』加一份麵。"},
    "大盛り": {"furigana": "おおもり", "romaji": "ōmori", "meaning": "大碗 / 加大份量", "tip": "許多拉麵店或定食店中午時段提供『大盛り無料（免費加大）』！"},
    "生ビール": {"furigana": "なまビール", "romaji": "nama biiru", "meaning": "生啤酒", "tip": "居酒屋坐下第一句口訣：『とりあえず生（總之先來杯生啤）』！"},
    "お通し": {"furigana": "おとおし", "romaji": "otōshi", "meaning": "開胃小菜 (座位費)", "tip": "居酒屋預設提供的小菜，約 300~500 日圓，屬傳統低消文化。"},
    "税込": {"furigana": "ぜいこみ", "romaji": "zeikomi", "meaning": "含稅價", "tip": "付款時以這個數字為準，日本消費稅通常為 10%（外帶食品8%）。"},
    "税抜": {"furigana": "ぜいぬき", "romaji": "zeinuki", "meaning": "未稅價 (未含消費稅)", "tip": "標價較小字時常是稅拔價格，結帳時會再加上消費稅。"},
    "割引": {"furigana": "わりびき", "romaji": "waribiki", "meaning": "折扣 / 打折", "tip": "超市晚上常見貼紙！『1割引』為 9 折，『2割引』為 8 折！"},
    "半額": {"furigana": "はんがく", "romaji": "hangaku", "meaning": "半價 (5折超強優惠！)", "tip": "晚上 8~9 點日本超市生鮮便當常貼半額貼紙，自由行省錢神物！"},
    "営業中": {"furigana": "えいぎょうちゅう", "romaji": "eigyōchū", "meaning": "營業中 (有開店營業)", "tip": "門口掛此牌表示正在營業中，可大膽推門進入。"},
    "準備中": {"furigana": "じゅんびちゅう", "romaji": "jumbichū", "meaning": "準備中 (尚未開放)", "tip": "代表店家正在準備料理或處於午休空檔，暫不接客。"},
    "定休日": {"furigana": "ていきゅうび", "romaji": "teikyūbi", "meaning": "每週固定公休日", "tip": "出發前一定要先確認店家定休日，以免撲空！"},
    "禁煙": {"furigana": "きんえん", "romaji": "kin'en", "meaning": "全面禁菸", "tip": "日本多數室內與街道均劃定禁煙區，違者罰款。吸煙請找指定喫煙所。"},
    "非常口": {"furigana": "ひじょうぐち", "romaji": "hijōguchi", "meaning": "緊急逃生出口", "tip": "飯店或商場內的綠色小人標誌，入住旅館先確認逃生路線。"},
    "切符": {"furigana": "きっぷ", "romaji": "kippu", "meaning": "車票 / 票券", "tip": "車站售票機上方會有『きっぷ (切符)』字樣。"},
    "改札口": {"furigana": "かいさつぐち", "romaji": "kaisatsuguchi", "meaning": "剪票口 / 驗票閘門", "tip": "進出站刷西瓜卡或插入車票的地方。"},
    "おすすめ": {"furigana": "おすすめ", "romaji": "osusume", "meaning": "店長推薦 / 今日招牌", "tip": "不知道點什麼的時候，照著菜單上的『おすすめ』點準沒錯！"},
    "免税": {"furigana": "めんぜい", "romaji": "menzei", "meaning": "免稅 (Tax Free)", "tip": "單筆滿 5000 日圓出示護照可退 10% 消費稅，密封袋境內嚴禁拆封！"},
    "温めますか": {"furigana": "あたためますか", "romaji": "atatamemasu ka", "meaning": "需要微波加熱嗎？", "tip": "超商買便當店員必問！要加熱回『はい』，不用回『大丈夫です』。"},
    "レジ袋": {"furigana": "レジぶくろ", "romaji": "rejibukuro", "meaning": "塑膠提袋", "tip": "日本超商塑膠袋需付費（約3~5日圓），不要的話回『袋はいいです』。"}
}


# 每日定時課程推播排程系統（支援個人化自訂時間與開關）
TAIPEI_TZ = datetime.timezone(datetime.timedelta(hours=8))
_last_push_attempt = {}  # user_id -> 上次嘗試推播的 datetime（失敗時每 10 分鐘重試一次，避免狂刷）

# 推播對象：可在 .env 設定 DISCORD_OWNER_ID，未設定時沿用原本的預設值
try:
    PUSH_TARGET_USER_ID = int(os.getenv("DISCORD_OWNER_ID") or 548823614900797441)
except ValueError:
    PUSH_TARGET_USER_ID = 548823614900797441


def _parse_hm(hm: str, default: str) -> datetime.time:
    try:
        return datetime.datetime.strptime(hm, "%H:%M").time()
    except (TypeError, ValueError):
        return datetime.datetime.strptime(default, "%H:%M").time()


@tasks.loop(minutes=1)
async def scheduled_minute_checker():
    now_taipei = datetime.datetime.now(TAIPEI_TZ)
    today_str = str(now_taipei.date())

    target_user_id = PUSH_TARGET_USER_ID
    sent_any = False
    try:
        prog = get_user_progress(target_user_id)
        if not prog.get("schedule_enabled", True):
            return

        is_weekend = now_taipei.weekday() >= 5
        sched_time = prog.get("schedule_weekend_time", "10:30") if is_weekend else prog.get("schedule_time", "21:00")
        sched_t = _parse_hm(sched_time, "10:30" if is_weekend else "21:00")
        # 時間已到（或已過，例如 bot 剛重啟）且今天尚未成功推播過 → 補發
        if now_taipei.time() >= sched_t and get_last_push_date(target_user_id) != today_str:
            last_try = _last_push_attempt.get(target_user_id)
            if last_try and (now_taipei - last_try).total_seconds() < 600:
                return
            _last_push_attempt[target_user_id] = now_taipei
            user = await bot.fetch_user(target_user_id)
            if not user:
                return

            lvl = prog.get("current_level", 1)
            q = QUESTS.get(lvl, QUESTS[1])

            filled = "🟩" * min(lvl, TOTAL_QUESTS)
            unfilled = "⬜" * max(0, TOTAL_QUESTS - lvl)
            bar = f"{filled}{unfilled} (Level {lvl}/{TOTAL_QUESTS})"

            mnemonic_sec = f"\n{q['mnemonic_story']}\n" if q.get("mnemonic_story") else ""

            if is_weekend:
                embed_title = f"🏖️【週末日語充電特輯】{q['title']}"
                embed_desc = (
                    f"週休假期愉快！為您送上專屬週末沉浸式日語學習特輯～放鬆享受實戰樂趣！\n\n"
                    f"📊 **目前進度**：`{bar}`\n\n"
                    f"🏖️ **【週末沉浸推薦】**：\n"
                    f"• 🎌 輸入 `/anime` 聽動漫名台詞，或輸入 `/news` 閱讀 NHK 簡易新聞！\n"
                    f"• 🍜 輸入 `/chat` 挑戰拉麵店或超商生活實戰角色扮演！\n"
                    f"• 🔄 輸入 `/review` 把平日累積的錯題一口氣斬除清倉！\n\n"
                    f"------------------------------------\n"
                    f"### 🗣️ 今日主線實戰金句：『 {q['phrase']} 』\n"
                    f"• **羅馬拼音**：*{q['romaji']}*\n"
                    f"• **口訣諧音**：**{q['phonetic']}**\n"
                    f"• **中文意思**：**{q['meaning']}**\n"
                    f"{mnemonic_sec}\n"
                    f"------------------------------------\n"
                    f"🎯 **【今日驗收】**：\n"
                    f"**{q['quiz']['question']}**\n\n"
                    f"👇 **點擊下方按鈕作答，答對完成今日打卡並解鎖「🏖️ 週末充電王」勳章！**"
                )
                embed_color = discord.Color.from_rgb(0, 190, 240)
            else:
                embed_title = f"⏰【{sched_time} 平日日語微課程】{q['title']}"
                embed_desc = (
                    f"專屬於您的平日日語學習時刻！每天花 15 分鐘輕鬆動動腦，無痛打卡～🍵\n\n"
                    f"📊 **目前進度**：`{bar}`\n\n"
                    f"🔤 **今日假名**：`{q['kana_group']}`\n"
                    f"{q['kana_tip']}\n\n"
                    f"------------------------------------\n"
                    f"### 🗣️ 今日實戰金句：『 {q['phrase']} 』\n"
                    f"• **羅馬拼音**：*{q['romaji']}*\n"
                    f"• **口訣諧音**：**{q['phonetic']}**\n"
                    f"• **中文意思**：**{q['meaning']}**\n"
                    f"{mnemonic_sec}\n"
                    f"🍜 **情境示範**：{q['scenario']}\n"
                    f"------------------------------------\n"
                    f"🎯 **【今日驗收】**：\n"
                    f"**{q['quiz']['question']}**\n\n"
                    f"👇 **點擊下方按鈕作答，答對立即完成今日打卡！**"
                )
                embed_color = discord.Color.from_rgb(255, 140, 60)

            embed = discord.Embed(
                title=embed_title,
                description=embed_desc,
                color=embed_color
            )
            embed.set_footer(text=f"每日定時推送中（平日 {prog.get('schedule_time', '21:00')} / 假日 {prog.get('schedule_weekend_time', '10:30')}）！")

            card_rel = q.get("card_image", f"cards/card_quest{lvl}.jpg")
            card_full = os.path.join(os.path.dirname(__file__), card_rel)
            card_file = None
            if os.path.exists(card_full):
                card_file = discord.File(card_full, filename=f"quest_lvl{lvl}_card.jpg")
                embed.set_image(url=f"attachment://quest_lvl{lvl}_card.jpg")

            voice_path = None
            try:
                voice_path = await text_to_speech(q["phrase"], f"quest_{lvl}.mp3", rate="-25%")
                file = discord.File(voice_path, filename=f"quest_lvl{lvl}.mp3")
            except Exception:
                file = None

            quiz_data = q["quiz"]
            options = list(quiz_data["options"])
            random.shuffle(options)
            view = QuestQuizView(
                current_level=lvl,
                question_text=quiz_data["question"],
                correct_answer=quiz_data["answer"],
                explanation=quiz_data["explanation"],
                options=options
            )

            sched_mode = prog.get("schedule_mode", "both")

            # 1. 發送五十音每日循環字卡（若模式為 kana 或 both）
            if sched_mode in ("kana", "both"):
                kana_day = prog.get("kana_day", 1)
                row_keys = ["a", "ka", "sa", "ta", "na", "ha", "ma", "ya", "ra", "wa"]
                row_key = row_keys[(kana_day - 1) % len(row_keys)]
                row_info = KANA_ROWS.get(row_key, KANA_ROWS["a"])
                row_name = row_info["name"]
                items = row_info["items"]

                kana_summary_lines = []
                for item in items:
                    kana_summary_lines.append(f"• **【{item['hira']}】** (平) / **【{item['kata']}】** (片) — *{item['romaji']}*：{item['tip']}")

                kana_embed = discord.Embed(
                    title=f"🌸【五十音音聲漫遊・第 {kana_day} 站】{row_name}",
                    description=(
                        f"哈囉！今日為您送達輕鬆日語音聲小品：**{row_name}**！🍵\n"
                        f"忙碌時略過完全沒關係，何時有空隨時點開聽聽發音即可～放鬆無壓力！✨\n\n"
                        f"------------------------------------\n"
                        + "\n".join(kana_summary_lines) + "\n"
                        f"------------------------------------\n"
                        f"▶️ **聊天室自動巡迴**：輸入 `/kana_loop row:{row_key}` 隨時開啟本行卡片自動漫遊輪播！\n"
                        f"💻 **沉浸式音頻網頁版**：電腦直接雙擊打開 `kana_player.html` 輕鬆聆聽真人發音！"
                    ),
                    color=discord.Color.from_rgb(255, 130, 180)
                )
                kana_embed.set_footer(text=f"五十音音聲漫遊（共 10 站悠閒巡迴）| 沒看也完全沒關係，累積學習永不清零！")

                # 生成行別代表字發音音檔
                kana_pronounce_text = "、".join([it["hira"] for it in items])
                kana_file = None
                kana_voice_path = None
                try:
                    kana_voice_path = await text_to_speech(kana_pronounce_text, f"kana_day_{kana_day}.mp3", rate="-20%")
                    kana_file = discord.File(kana_voice_path, filename=f"kana_station_{kana_day}.mp3")
                except Exception:
                    kana_file = None

                hub_view = DailyHubView(current_row_key=row_key)

                try:
                    if kana_file:
                        await user.send(embed=kana_embed, file=kana_file, view=hub_view)
                    else:
                        await user.send(embed=kana_embed, view=hub_view)
                finally:
                    if kana_file:
                        kana_file.close()
                    remove_temp_file(kana_voice_path)
                sent_any = True

                # 推進循環站點
                advance_kana_day(target_user_id)
                print(f"[{datetime.datetime.now()}] 已向使用者推送第 {kana_day} 站五十音漫遊卡片與一鍵直達中樞！", flush=True)

            # 2. 發送主線闖關（若模式為 quest 或 both）
            if sched_mode in ("quest", "both"):
                send_files = []
                if card_file:
                    send_files.append(card_file)
                if file:
                    send_files.append(file)

                if send_files:
                    await user.send(embed=embed, files=send_files, view=view)
                else:
                    await user.send(embed=embed, view=view)
                sent_any = True
                print(f"[{datetime.datetime.now()}] 已向使用者推送 {sched_time} 微課程！", flush=True)
            if file:
                file.close()
            remove_temp_file(voice_path)

            # 主要課程已送達 → 記錄今日已推播（失敗時不記錄，下次檢查會自動補發）
            set_last_push_date(target_user_id, today_str)

            # 3. 主動推送【今日 J-POP 經典名曲教室】（30 秒原曲音樂 ＋ 30 秒日語導讀拆字電台）
            try:
                if not JPOP_SONGS:
                    raise RuntimeError("此環境未安裝 J-POP 歌詞資料")
                song_keys = list(JPOP_SONGS.keys())
                song_idx = (prog.get("kana_day", 1) - 1) % len(song_keys)
                today_song_key = song_keys[song_idx]
                song_embed = build_lyrics_embed(today_song_key)
                song_view = LyricsSelectView(current_song_key=today_song_key)
                song_data = JPOP_SONGS[today_song_key]

                files_to_send = []
                clip_rel = song_data.get("music_file", "")
                clip_full = os.path.join(os.path.dirname(__file__), clip_rel)
                if os.path.exists(clip_full):
                    files_to_send.append(discord.File(clip_full, filename=f"{today_song_key}_music.m4a"))

                guide_rel = song_data.get("guide_file", "")
                guide_full = os.path.join(os.path.dirname(__file__), guide_rel)
                if os.path.exists(guide_full):
                    files_to_send.append(discord.File(guide_full, filename=f"{today_song_key}_guide.mp3"))

                if files_to_send:
                    await user.send(embed=song_embed, files=files_to_send, view=song_view)
                else:
                    await user.send(embed=song_embed, view=song_view)
                print(f"[{datetime.datetime.now()}] 已主動向使用者推送今日 J-POP 名曲：《{song_data['title']}》原聲音樂與名師導讀電台！", flush=True)
            except Exception as e:
                print(f"主動推送 J-POP 名曲失敗: {e}", flush=True)
    except Exception as e:
        # 若已有部分內容送達，仍視為今日已推播，避免重試時重複轟炸
        if sent_any:
            try:
                set_last_push_date(target_user_id, today_str)
            except Exception:
                pass
        print(f"定時推送課程失敗: {e}", flush=True)


@bot.event
async def on_ready():
    print("==================================================", flush=True)
    print(f"🌸 日語學習機器人已就緒！", flush=True)
    print(f"機器人名稱: {bot.user.name} (ID: {bot.user.id})", flush=True)
    # on_ready 在斷線重連時會重複觸發；斜線指令每個行程只需同步一次（避免觸發 API 速率限制）
    if not getattr(bot, "_tree_synced", False):
        print("正在同步斜線指令 (Slash Commands)...", flush=True)
        try:
            synced = await bot.tree.sync()
            bot._tree_synced = True
            print(f"✅ 已成功同步 {len(synced)} 個全域指令！", flush=True)
        except Exception as e:
            print(f"❌ 同步指令時發生錯誤: {e}", flush=True)

    if not scheduled_minute_checker.is_running():
        scheduled_minute_checker.start()
        print("⏰ 個人化每日微課程動態推播排程已啟動！", flush=True)

    print("==================================================", flush=True)


def _has_live_view(interaction: discord.Interaction) -> bool:
    """檢查這個按鈕/選單是否仍有存活中的 View 會處理（比照 discord.py ViewStore 的查找方式；取不到就當作沒有）"""
    try:
        store = bot._connection._view_store
        key = (interaction.data.get("component_type"), interaction.data.get("custom_id"))
        msg_id = interaction.message.id if interaction.message else None
        if msg_id is not None and key in store._views.get(msg_id, {}):
            return True
        return key in store._views.get(None, {})
    except Exception:
        return False


@bot.event
async def on_interaction(interaction: discord.Interaction):
    """全局互動防呆接管器：防止任何舊推播或重啟後過期按鈕出現『該應用程式未及時回應』"""
    if interaction.type != discord.InteractionType.component:
        return
    if interaction.message is None:
        return

    # 仍有存活中的 View 會處理這個按鈕 → 交給原本的回呼，避免重複回應（40060）
    if _has_live_view(interaction):
        return

    # 等待 0.3 秒，若原 View 回呼已正常回應則直接返回
    await asyncio.sleep(0.3)
    if interaction.response.is_done():
        return

    try:
        custom_id = interaction.data.get("custom_id")
        clicked_label = None
        all_options = []

        if interaction.message and interaction.message.components:
            for action_row in interaction.message.components:
                for comp in action_row.children:
                    if hasattr(comp, "label") and comp.label:
                        all_options.append(comp.label)
                        if comp.custom_id == custom_id:
                            clicked_label = comp.label

        embed = interaction.message.embeds[0] if interaction.message and interaction.message.embeds else None
        embed_title = embed.title if embed and embed.title else ""
        embed_desc = embed.description if embed and embed.description else ""

        # 1. 檢查是否為 Quest 關卡測驗 (主線闖關或每日推播)
        matched_quest_lvl = None
        for lvl, q in QUESTS.items():
            if q["quiz"]["question"] in embed_desc or f"第 {lvl} 關" in embed_title or q["title"] in embed_title:
                matched_quest_lvl = lvl
                break

        if matched_quest_lvl and clicked_label:
            q = QUESTS[matched_quest_lvl]
            quiz_data = q["quiz"]
            new_view = QuestQuizView(
                current_level=matched_quest_lvl,
                question_text=quiz_data["question"],
                correct_answer=quiz_data["answer"],
                explanation=quiz_data["explanation"],
                options=all_options if all_options else list(quiz_data["options"])
            )
            cb = new_view.make_callback(clicked_label)
            await cb(interaction)
            return

        # 2. 檢查是否為一般 Quiz 測驗
        matched_quiz = None
        for q in QUIZ_QUESTIONS:
            if q["question"] in embed_desc or q["question"] in embed_title:
                matched_quiz = q
                break

        if matched_quiz and clicked_label:
            new_view = QuizView(
                question_text=matched_quiz["question"],
                correct_answer=matched_quiz["answer"],
                explanation=matched_quiz["explanation"],
                options=all_options if all_options else list(matched_quiz["options"]),
                category="all"
            )
            cb = new_view.make_callback(clicked_label)
            await cb(interaction)
            return

        # 3. 檢查是否為 Katakana 外來語測驗
        matched_kata = None
        for k in KATAKANA_QUIZZES:
            if k["question"] in embed_desc or k["question"] in embed_title:
                matched_kata = k
                break

        if matched_kata and clicked_label:
            new_view = KatakanaQuizView(
                question_text=matched_kata["question"],
                correct_answer=matched_kata["answer"],
                explanation=matched_kata["explanation"],
                options=all_options if all_options else list(matched_kata["options"])
            )
            cb = new_view.make_callback(clicked_label)
            await cb(interaction)
            return

        # 4. 檢查是否為五十音消除小遊戲按鈕
        if "五十音極速消除" in embed_title or "Kana Game" in embed_title:
            next_view = KanaGameView(round_num=1)
            embed = next_view.build_embed(feedback=f"🎮 重新接軌小遊戲！立即開始消除！")
            await interaction.response.edit_message(embed=embed, view=next_view)
            return

        # 5. 檢查是否為五十音圖卡按鈕
        if "五十音" in embed_title and not ("音聲漫遊" in embed_title):
            target_idx = 0
            k_embed = build_kana_card_embed(target_idx)
            k_view = KanaFlashcardView(target_idx)
            await interaction.response.edit_message(embed=k_embed, view=k_view)
            return

        # 6. 檢查是否為 J-POP 歌詞教室按鈕或下拉選單（支援歷史卡片與重啟後按鈕無縫接管！）
        is_lyrics_context = "J-POP" in embed_title or "歌詞" in embed_title or "名曲" in embed_title
        if is_lyrics_context and not JPOP_SONGS:
            await interaction.response.send_message(LYRICS_MISSING_MSG, ephemeral=True)
            return
        if is_lyrics_context:
            matched_song_key = "idol" if "idol" in JPOP_SONGS else next(iter(JPOP_SONGS))
            for sk, sdata in JPOP_SONGS.items():
                if sdata["title"] in embed_title or sdata["artist"] in embed_desc or sk in embed_title:
                    matched_song_key = sk
                    break

            song = JPOP_SONGS[matched_song_key]

            # 處理下拉選單切換歌曲
            if interaction.data.get("values"):
                chosen_sk = interaction.data["values"][0]
                new_embed = build_lyrics_embed(chosen_sk)
                new_view = LyricsSelectView(chosen_sk)
                await interaction.response.edit_message(embed=new_embed, view=new_view)
                return

            lbl = clicked_label or ""
            # A. 導讀電台或慢速朗讀（發送文字拆字講義＋導讀語音！）
            if any(k in lbl for k in ["導讀", "拆字", "慢速", "朗讀", "跟讀"]) or "guide" in str(custom_id) or "voice" in str(custom_id):
                guide_rel = song.get("guide_file", "")
                guide_full = os.path.join(os.path.dirname(__file__), guide_rel)
                guide_embed = build_beginner_guide_embed(matched_song_key)
                if os.path.exists(guide_full):
                    file = discord.File(guide_full, filename=f"{matched_song_key}_guide.mp3")
                    await interaction.response.send_message(
                        embed=guide_embed,
                        file=file,
                        ephemeral=True
                    )
                else:
                    # TTS 可能超過 3 秒，先 defer 再用 followup 傳送
                    await interaction.response.defer(ephemeral=True)
                    voice_path = await text_to_speech(song["lyrics_jp"].replace("\n", "、"), f"song_{matched_song_key}.mp3", rate="-20%")
                    try:
                        file = discord.File(voice_path, filename=f"{matched_song_key}_lyrics_slow.mp3")
                        await interaction.followup.send(
                            embed=guide_embed,
                            file=file,
                            ephemeral=True
                        )
                        file.close()
                    finally:
                        remove_temp_file(voice_path)
                return

            # B. 播放原曲音樂
            if any(k in lbl for k in ["原曲", "音樂", "播放", "Studio"]) or "music" in str(custom_id):
                clip_rel = song.get("music_file", "")
                clip_full = os.path.join(os.path.dirname(__file__), clip_rel)
                if os.path.exists(clip_full):
                    file = discord.File(clip_full, filename=f"{matched_song_key}_music.m4a")
                    await interaction.response.send_message(
                        f"🎵 **{song['title']}** 30 秒正版原曲音樂片段送達！點擊即可聆聽真人真聲演唱：👇",
                        file=file,
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        f"🎵 原曲音樂加載中，請點擊卡片上的 YouTube MV 或 Spotify 直接收聽！",
                        ephemeral=True
                    )
                return

            # C. 隨機換一首名曲
            if any(k in lbl for k in ["換一首", "隨機", "名曲", "換歌"]) or "random" in str(custom_id):
                other_keys = [k for k in JPOP_SONGS.keys() if k != matched_song_key]
                new_song_key = random.choice(other_keys) if other_keys else matched_song_key
                new_embed = build_lyrics_embed(new_song_key)
                new_view = LyricsSelectView(new_song_key)
                await interaction.response.edit_message(embed=new_embed, view=new_view)
                return

        # 7. 檢查是否為 DailyHubView 一鍵直達中樞按鈕
        if clicked_label == "⛩️ 抽今日御神籤":
            fortune = draw_omikuji()
            await interaction.response.send_message(embed=build_omikuji_embed(fortune), view=OmikujiView(fortune), ephemeral=True)
            return
        if clicked_label == "▶️ 自動播放本站假名":
            auto_view = KanaAutoPlayView(current_idx=0, speed_seconds=4.0)
            await interaction.response.send_message(embed=auto_view.build_autoplay_embed(), view=auto_view, ephemeral=True)
            auto_view.start_loop(interaction)
            return
        if clicked_label == "🎮 玩玩消除小遊戲":
            game_view = KanaGameView(round_num=1)
            await interaction.response.send_message(embed=game_view.build_embed(), view=game_view, ephemeral=True)
            return
        if clicked_label == "🎵 聽 J-POP 歌詞":
            if not JPOP_SONGS:
                await interaction.response.send_message(LYRICS_MISSING_MSG, ephemeral=True)
                return
            sk = random.choice(list(JPOP_SONGS.keys()))
            sdata = JPOP_SONGS[sk]
            fls = []
            c_full = os.path.join(os.path.dirname(__file__), sdata.get("music_file", ""))
            if os.path.exists(c_full):
                fls.append(discord.File(c_full, filename=f"{sk}_music.m4a"))
            g_full = os.path.join(os.path.dirname(__file__), sdata.get("guide_file", ""))
            if os.path.exists(g_full):
                fls.append(discord.File(g_full, filename=f"{sk}_guide.mp3"))
            await interaction.response.send_message(embed=build_lyrics_embed(sk), files=fls, view=LyricsSelectView(sk), ephemeral=True)
            return
        if clicked_label == "🏪 日本超商藥妝掃雷":
            await interaction.response.send_message(embed=build_drugstore_embed("drugstore"), view=DrugstoreSelectView("drugstore"), ephemeral=True)
            return

        # 8. 檢查是否為 OmikujiView 按鈕
        if clicked_label == "⛩️ 再求一籤 (抽籤)":
            new_data = draw_omikuji()
            await interaction.response.edit_message(embed=build_omikuji_embed(new_data), view=OmikujiView(new_data))
            return
        if clicked_label == "🔊 聆聽今日箴言朗讀":
            # 從卡片內容找回原本抽到的籤，找不到才重新抽
            fortune_match = next((f for f in OMIKUJI_DATA if f["quote"] in embed_desc), None) or draw_omikuji()
            phrase = f"{fortune_match['quote']}。{fortune_match['lucky_word']}"
            await interaction.response.defer(ephemeral=True)
            voice_path = await text_to_speech(phrase, f"omikuji_{fortune_match['id']}.mp3", rate="-20%")
            try:
                file = discord.File(voice_path, filename="omikuji_voice.mp3")
                await interaction.followup.send(f"🌸 今日幸運日語箴言：『**{fortune_match['quote']}**』語音送達！", file=file, ephemeral=True)
                file.close()
            finally:
                remove_temp_file(voice_path)
            return

        # 9. 檢查是否為 DrugstoreSelectView 下拉選單
        if interaction.data.get("values") and any(v in ["drugstore", "skincare", "food"] for v in interaction.data["values"]):
            ch = interaction.data["values"][0]
            await interaction.response.edit_message(embed=build_drugstore_embed(ch), view=DrugstoreSelectView(ch))
            return

        # 10. 其他過期且無法還原的舊按鈕，給予友善提示
        await interaction.response.send_message(
            "💡 這張卡片來自較早之前的互動！\n"
            "請點擊私訊中最新的卡片按鈕，或輸入 `/quest`（繼續闖關）即可無縫暢快學習！",
            ephemeral=True
        )
    except discord.InteractionResponded:
        # 原本的 View 回呼已經回應過了，靜默略過
        return
    except discord.HTTPException as e:
        if getattr(e, "code", None) == 40060:  # Interaction has already been acknowledged
            return
        print(f"處理未註冊按鈕互動時出錯: {e}", flush=True)
    except Exception as e:
        print(f"處理未註冊按鈕互動時出錯: {e}", flush=True)
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "💡 該卡片互動已過期，請點擊最新的訊息或輸入 `/quest` 繼續學習！",
                    ephemeral=True
                )
        except discord.HTTPException:
            pass


# /help 指令
@bot.tree.command(name="help", description="查看日文學習機器人的所有功能與指令說明")
async def help_command(interaction: discord.Interaction):
    embed = discord.Color.blurple()
    embed = discord.Embed(
        title="🌸 日語學習機器人 指令指南",
        description="專為零基礎到生活、旅遊、工作實戰設計的日語伴讀助手！",
        color=discord.Color.from_rgb(255, 140, 180)
    )
    embed.add_field(
        name="👑 `/profile`",
        value="【個人學習檔案】查看累積打卡天數（Streak）、主線關卡進度與成就勳章牆！",
        inline=False
    )
    embed.add_field(
        name="🍜 `/chat [情境]`",
        value="【AI 實戰情境角色扮演】支援拉麵店、飯店、超商、居酒屋，模擬真實赴日對話與按鈕分支！",
        inline=False
    )
    embed.add_field(
        name="🧩 `/katakana [模式/單字]`",
        value="【片假名外來語解碼器】速查外來語語源（英文/德文/葡文）或進行 4 選 1 猜詞測驗！",
        inline=False
    )
    embed.add_field(
        name="🔄 `/review`",
        value="【智慧錯題本】自動收錄測驗錯題，隨時進行抗遺忘複習衝刺，答對自動斬除移出！",
        inline=False
    )
    embed.add_field(
        name="📸 `/scan [圖片/提示]`",
        value="【拍照掃描解碼】上傳日本招牌、菜單、標語照片，辨識假名注音、中文翻譯與生存秘訣！",
        inline=False
    )
    embed.add_field(
        name="🛡️ `/culture [主題]`",
        value="【文化與旅遊避坑指南】居酒屋お通し、電車禮儀、溫泉規矩、邊走邊吃、找零錢盤、免稅密封袋！",
        inline=False
    )
    embed.add_field(
        name="⏰ `/schedule [操作/時間]`",
        value="【平日/假日自訂推播】自由設定平日（如 21:00）與假日（如 10:30）各自的推播時間，亦可一鍵切換開關！",
        inline=False
    )
    embed.add_field(
        name="🚨 `/sos [情境]`",
        value="【日本緊急生存就醫手指卡】急救 119、報警 110、遺失、看病疼痛手指點選卡！",
        inline=False
    )
    embed.add_field(
        name="🥩 `/menu [分類]`",
        value="【日式餐廳點餐暗號字典】燒肉部位全解、壽司魚種、吉野家/拉麵客製暗號（つゆだく等）！",
        inline=False
    )
    embed.add_field(
        name="🧩 `/grammar [動詞]`",
        value="【動詞變化 10 秒速查卡】五段動詞て形口訣歌、ます形、ない形、た形等 7 大活用形即查即用！",
        inline=False
    )
    embed.add_field(
        name="📰 `/news [新聞]`",
        value="【NHK 通勤簡易新聞閱讀】每日 3 分鐘微閱讀，附假名注音、單字詳解、中文對照與語音！",
        inline=False
    )
    embed.add_field(
        name="🗣️ `/shadowing [題目]`",
        value="【日語實戰跟讀挑戰】語調高低走向、連音弱化指導與標準朗讀影子練習！",
        inline=False
    )
    embed.add_field(
        name="🏆 `/leaderboard`",
        value="【日語學習天梯排行榜】查看伺服器累積打卡 Streak、關卡進度與成就榮譽榜！",
        inline=False
    )
    embed.add_field(
        name="✍️ `/write`",
        value="【手寫練習指引】開啟專屬「米字格描紅練習板」，支援手機觸控塗鴉與滑鼠筆刷練習！",
        inline=False
    )
    embed.add_field(
        name="⚔️ `/quest [等級]`",
        value="【主線闖關 20 關大圓滿】每日 15 分鐘！20 關搞定「五十音＋生活/旅遊/藥妝/新幹線/看病/商務」，自動記錄等級！",
        inline=False
    )
    embed.add_field(
        name="🔄 `/quest_reset`",
        value="重置個人闖關進度回第 1 關，重新打怪升級。",
        inline=False
    )

    # Discord 每個 Embed 最多 25 個欄位 → 拆成兩張一起送出
    embed2 = discord.Embed(
        title="🌸 日語學習機器人 指令指南（續）",
        color=discord.Color.from_rgb(255, 140, 180)
    )
    first_embed = embed
    embed = embed2
    embed.add_field(
        name="🌸 `/hub`",
        value="【一鍵直達中樞】免記任何指令！點按鈕直接抽靈籤、聽 J-POP、玩小遊戲、超商掃雷與五十音！",
        inline=False
    )
    embed.add_field(
        name="🎡 `/arcade`",
        value="【日語沉浸遊樂園】一鍵打開消消樂、J-POP 歌詞電台、盲盒扭蛋機與手寫道場！",
        inline=False
    )
    embed.add_field(
        name="🔊 `/voice [日文句子]`",
        value="真人標準發音！輸入任何日文句子，機器人立即生成音檔在聊天室播放。",
        inline=False
    )
    embed.add_field(
        name="🎴 `/card [圖卡]`",
        value="查看精美日語圖卡！全 10 大生活情境與假名圖像記憶（附帶標準語音發音）。",
        inline=False
    )
    embed.add_field(
        name="🎌 `/anime [作品]`",
        value="【動漫名台詞教室】精選《鬼滅之刃》、《咒術迴戰》、《名偵探柯南》等超人氣名台詞！附帶文法拆解、諧音記憶、仿造句型與原汁原味發音！",
        inline=False
    )
    embed.add_field(
        name="📋 `/plan [模式]`",
        value="【全方位日語學習計畫】支援【🏖️ 假日沉浸 30~45 分鐘實戰】、【☕ 平日通勤 15 分鐘微學習】與【全階段路線圖】，一鍵按鈕隨意切換！",
        inline=False
    )
    embed.add_field(
        name="🔤 `/kana [行別]`",
        value="【從零學五十音】全新 46 假名翻頁卡片流！字源歷史、嘴型發音、聯想口訣，點擊「🎯 測驗這個字」即學即測！",
        inline=False
    )
    embed.add_field(
        name="🌸 `/kana_loop [行別] [速度]`",
        value="【五十音自動循環播放】全 46 假名字卡自動巡迴播放！支援「⏸️ 暫停」、「⏱️ 速度切換」、「🎯 考考這個字」隨堂驗收！",
        inline=False
    )
    embed.add_field(
        name="🎯 `/quiz [分類]`",
        value="【互動隨堂測驗】支援「🔤 五十音專屬大考驗」與情境測驗！答題附帶冷知識，連擊「➡️ 挑戰下一題」永不停歇！",
        inline=False
    )
    embed.add_field(
        name="📖 `/scenario [情境]`",
        value="四大核心場景句型庫：`travel`、`daily`、`anime`、`work`。",
        inline=False
    )
    embed.add_field(
        name="✨ `/daily`",
        value="【今日學習小卡】抽取日語生活金句與文化冷知識，附帶「🎴 抽下一張小卡」持續刷卡學習！",
        inline=False
    )
    embed.add_field(
        name="⛩️ `/omikuji`",
        value="【神社御神籤・開運占卜】抽今日靈籤（大吉/中吉/小吉）！附帶古風日語籤詩、真人語音朗讀與幸運物！",
        inline=False
    )
    embed.add_field(
        name="🏪 `/drugstore [分類]`",
        value="【藥妝超商實戰掃雷機】松本清、超商包裝必備標示速查（常備藥功效、保濕美白、賞味/消費期限）！",
        inline=False
    )
    embed.add_field(
        name="🎵 `/lyrics [歌曲]`",
        value="【J-POP 歌詞日語教室】YOASOBI、米津玄師、宇多田光、愛繆副歌歌詞拆解、高頻單字與慢速朗讀！",
        inline=False
    )
    embed.add_field(
        name="🎮 `/kana_game`",
        value="【五十音極速消除小遊戲】超好玩按鈕連連看！平假名/片假名/拼音直覺連擊消除，純刷手感不記分！",
        inline=False
    )
    embed.set_footer(text="日語學習，從每天的一小步開始！がんばって！")
    await interaction.response.send_message(embeds=[first_embed, embed])


# ====================================================
# 🌸 /hub 指令 (日語功能一鍵直達中樞：免記任何指令！)
# ====================================================
@bot.tree.command(name="hub", description="🌸【一鍵直達中樞】免記任何指令！點擊按鈕直接抽靈籤、聽J-POP、玩小遊戲、超商掃雷與五十音")
async def hub_command(interaction: discord.Interaction):
    record_daily_activity(interaction.user.id)
    embed = discord.Embed(
        title="🌸【日語學習一鍵直達中樞・免記指令】",
        description=(
            "您好！我們已全面升級為**「主動互動中樞」**，您**完全不需要死記任何英文指令**！\n\n"
            "👇 **直接點擊下方按鈕，即可秒速開啟您想體驗的日語模組：**\n\n"
            "• ⛩️ **抽今日御神籤**：每日靈籤吉凶、日文古風籤詩與幸運物\n"
            "• ▶️ **自動播放五十音**：聊天室 46 音自動循環輪播（附語音）\n"
            "• 🎮 **玩玩消除小遊戲**：超好玩平片假名連連看，純刷手感不扣分\n"
            "• 🎵 **聽 J-POP 歌詞**：YOASOBI、米津玄師等神曲副歌慢速朗讀\n"
            "• 🏪 **日本超商藥妝掃雷**：松本清常備藥、美妝與食品賞味期限解密"
        ),
        color=discord.Color.from_rgb(255, 120, 180)
    )
    embed.set_footer(text="每天定時推播也會主動附帶這套按鈕面板，點擊即玩！")
    view = DailyHubView(current_row_key="a")
    await interaction.response.send_message(embed=embed, view=view)



# /quest 指令
@bot.tree.command(name="quest", description="【系統化闖關】每日 15 分鐘系統化關卡（1~20 關搞定五十音、生活旅遊與商務）")
@app_commands.describe(level="選填：指定查看或重溫特定關卡（1~20）")
async def quest_command(interaction: discord.Interaction, level: int = None):
    await interaction.response.defer()
    prog = get_user_progress(interaction.user.id)
    current_lvl = prog.get("current_level", 1)

    target_lvl = level if (level and 1 <= level <= TOTAL_QUESTS) else current_lvl
    q = QUESTS.get(target_lvl)
    if not q:
        await interaction.followup.send(f"找不到該關卡資訊（等級範圍：1~{TOTAL_QUESTS}）。")
        return

    # 進度條渲染
    filled = "🟩" * target_lvl
    unfilled = "⬜" * max(0, TOTAL_QUESTS - target_lvl)
    bar = f"{filled}{unfilled} (Level {target_lvl}/{TOTAL_QUESTS})"

    mnemonic_sec = f"\n{q['mnemonic_story']}\n" if q.get("mnemonic_story") else ""

    embed = discord.Embed(
        title=f"⚔️ 【日語系統化闖關】{q['title']}",
        description=(
            f"📊 **目前進度**：`{bar}`\n\n"
            f"🔤 **今日假名進度**：`{q['kana_group']}`\n"
            f"{q['kana_tip']}\n\n"
            f"------------------------------------\n"
            f"### 🗣️ 今日實戰金句：『 {q['phrase']} 』\n"
            f"• **羅馬拼音**：*{q['romaji']}*\n"
            f"• **口訣諧音**：**{q['phonetic']}**\n"
            f"• **中文意思**：**{q['meaning']}**\n"
            f"{mnemonic_sec}\n"
            f"🍜 **情境示範**：{q['scenario']}\n"
            f"------------------------------------\n"
            f"🎯 **【通關驗收題目】**：\n"
            f"**{q['quiz']['question']}**\n\n"
            f"👇 **點擊下方按鈕作答！答對即可通過本關並自動晉級！**"
        ),
        color=discord.Color.from_rgb(255, 140, 60)
    )
    embed.set_footer(text="每天只要 15 分鐘打通一關，無痛通關日本自由行！")

    # 載入精美圖卡
    card_rel = q.get("card_image", f"cards/card_quest{target_lvl}.jpg")
    card_full = os.path.join(os.path.dirname(__file__), card_rel)
    card_file = None
    if os.path.exists(card_full):
        card_file = discord.File(card_full, filename=f"quest_card_{target_lvl}.jpg")
        embed.set_image(url=f"attachment://quest_card_{target_lvl}.jpg")

    # 生成對應慢速語音
    voice_path = None
    try:
        voice_path = await text_to_speech(q["phrase"], f"quest_{target_lvl}.mp3", rate="-25%")
        file = discord.File(voice_path, filename=f"quest_lvl{target_lvl}.mp3")
    except Exception:
        file = None

    quiz_data = q["quiz"]
    options = list(quiz_data["options"])
    random.shuffle(options)
    view = QuestQuizView(
        current_level=target_lvl,
        question_text=quiz_data["question"],
        correct_answer=quiz_data["answer"],
        explanation=quiz_data["explanation"],
        options=options
    )

    send_files = []
    if card_file:
        send_files.append(card_file)
    if file:
        send_files.append(file)

    try:
        if send_files:
            await interaction.followup.send(embed=embed, files=send_files, view=view)
        else:
            await interaction.followup.send(embed=embed, view=view)
    finally:
        for f in send_files:
            f.close()
        remove_temp_file(voice_path)


# /quest_reset 指令
@bot.tree.command(name="quest_reset", description="重置您的個人關卡進度回第 1 關")
async def quest_reset_command(interaction: discord.Interaction):
    reset_user_progress(interaction.user.id)
    await interaction.response.send_message("🔄 您的關卡進度已重置為 **【第 1 關】**（打卡天數、勳章、錯題本與推播設定都會保留）！隨時輸入 `/quest` 重新挑戰！", ephemeral=True)


# /schedule 指令 (支援平日/假日自訂時間、開關切換與推播內容模式)
@bot.tree.command(name="schedule", description="查看、自訂推播時間（平日/假日）、推播模式（主線闖關/五十音每日循環/兩者皆要）或切換開關")
@app_commands.describe(
    action="選擇操作：查看排程狀態、設定平日時間、設定假日時間、設定推播模式、或切換開關",
    time="設定推播時間 (格式如 08:30、10:30 或 21:00)",
    mode="設定推播內容模式 (主線闖關 / 五十音每日循環 / 兩者皆要)"
)
@app_commands.choices(action=[
    app_commands.Choice(name="📅 查看目前排程狀態 (View)", value="view"),
    app_commands.Choice(name="⏰ 設定平日推播時間 (Set Weekday)", value="set_weekday"),
    app_commands.Choice(name="🏖️ 設定假日推播時間 (Set Weekend)", value="set_weekend"),
    app_commands.Choice(name="📚 設定推播內容模式 (Set Mode)", value="set_mode"),
    app_commands.Choice(name="🔔 開啟 / 暫停推播 (Toggle)", value="toggle"),
], mode=[
    app_commands.Choice(name="🌟 兩者皆要 (五十音音聲漫遊 + 主線闖關雙重滿足)", value="both"),
    app_commands.Choice(name="🔤 五十音音聲漫遊 (每期1行＋語音＋10站悠閒巡迴)", value="kana"),
    app_commands.Choice(name="⚔️ 主線系統化闖關 (系統化情境關卡與按鈕測驗)", value="quest"),
])
async def schedule_command(
    interaction: discord.Interaction,
    action: app_commands.Choice[str] = None,
    time: str = None,
    mode: app_commands.Choice[str] = None
):
    act = action.value if action else "view"
    user_id = interaction.user.id
    prog = get_user_progress(user_id)

    if act in ("set_weekday", "set_weekend", "set"):
        if not time:
            sample_cmd = "/schedule action:設定平日推播時間 time:21:00" if act == "set_weekday" else "/schedule action:設定假日推播時間 time:10:30"
            await interaction.response.send_message(f"請提供欲設定的時間，格式為 `HH:MM`（例如：`{sample_cmd}`）", ephemeral=True)
            return
        t_clean = time.strip().replace("：", ":")
        try:
            parts = t_clean.split(":")
            h, m = int(parts[0]), int(parts[1])
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError()
            formatted_time = f"{h:02d}:{m:02d}"
        except Exception:
            await interaction.response.send_message("時間格式不正確，請輸入 24 小時制格式，例如 `08:30` 或 `21:15`。", ephemeral=True)
            return

        is_weekend = (act == "set_weekend")
        set_user_schedule(user_id, formatted_time, is_weekend=is_weekend)
        day_type = "【🏖️ 週末假期（週六・週日）】" if is_weekend else "【💼 平日工作日（週一至週五）】"
        embed = discord.Embed(
            title="⏰ 推播時間設定成功！",
            description=(
                f"已將您的 {day_type} 推播時間自訂為：**【{formatted_time}】**！\n"
                f"時間一到，機器人將準時向您的私人訊息發送專屬日語音聲小品！"
            ),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
        return

    elif act == "set_mode":
        chosen_mode = mode.value if mode else "both"
        set_user_schedule_mode(user_id, chosen_mode)
        mode_names = {
            "both": "🌟 兩者皆要（五十音音聲漫遊 ＋ 主線闖關課程）",
            "kana": "🔤 五十音音聲漫遊（每期 1 行假名＋發音音檔＋10 站悠閒巡迴）",
            "quest": "⚔️ 主線系統化闖關（系統化生活情境關卡）"
        }
        embed = discord.Embed(
            title="📚 推播內容模式已更新！",
            description=(
                f"已將您的推播內容設定為：**{mode_names.get(chosen_mode, chosen_mode)}**！\n\n"
                f"時間一到，機器人將依照此偏好為您推送專屬學習卡片與音檔！"
            ),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
        return

    elif act == "toggle":
        new_state = toggle_user_schedule(user_id)
        state_str = "🟢 已恢復自動推播！" if new_state else "🔴 已暫停定時推播。"
        embed = discord.Embed(
            title="🔔 推播狀態切換",
            description=f"目前推播設定：**{state_str}**\n隨時可以再透過 `/schedule action:開啟/暫停推播` 切換！",
            color=discord.Color.blue() if new_state else discord.Color.greyple()
        )
        await interaction.response.send_message(embed=embed)
        return

    else:
        sched_weekday = prog.get("schedule_time", "21:00")
        sched_weekend = prog.get("schedule_weekend_time", "10:30")
        is_enabled = prog.get("schedule_enabled", True)
        curr_mode = prog.get("schedule_mode", "both")
        kana_day = prog.get("kana_day", 1)
        status_icon = "🟢 定時推播運行中" if (scheduled_minute_checker.is_running() and is_enabled) else "🔴 已暫停推播"

        mode_descs = {
            "both": "🌟 兩者皆要（五十音漫遊卡片 ＋ 主線情境關卡雙重推播）",
            "kana": "🔤 五十音音聲漫遊（推送 1 行假名、發音音檔，10 站悠閒巡迴）",
            "quest": "⚔️ 主線系統化闖關（旅遊/生活金句與按鈕測驗）"
        }

        embed = discord.Embed(
            title="📅 日語課程排程與推播狀態",
            description=(
                f"• 💼 **平日推播時間（週一～週五）**：**【{sched_weekday}】**\n"
                f"• 🏖️ **假日推播時間（週六・週日）**：**【{sched_weekend}】**\n"
                f"• ⚡ **當前運行狀態**：`{status_icon}`\n"
                f"• 🎯 **推播內容模式**：`{mode_descs.get(curr_mode, curr_mode)}`\n"
                f"• 🌸 **五十音漫遊進度**：目前來到 **第 {kana_day} / 10 站**\n"
                f"• 📬 **發送目標**：您的 Discord 私人訊息 (DM)\n\n"
                f"------------------------------------\n"
                f"💡 **快速調整提示**：\n"
                f"• `/schedule action:設定平日推播時間 time:21:00`\n"
                f"• `/schedule action:設定假日推播時間 time:10:30`\n"
                f"• `/schedule action:設定推播內容模式 mode:五十音音聲漫遊`\n"
                f"• `/schedule action:開啟/暫停推播`"
            ),
            color=discord.Color.from_rgb(255, 160, 60)
        )
        embed.set_footer(text="零壓力隨心學，有空再聽！累積學習永不清零！")
        await interaction.response.send_message(embed=embed)


# /write 指令
@bot.tree.command(name="write", description="查看日文假名手寫練習指引與開啟米字格手寫畫板")
async def write_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="✍️ 【日語假名手寫練習板 (米字格描紅)】",
        description=(
            "因為 Discord 聊天框本身只有純文字與按鈕元件，無法直接在聊天室內當繪圖板。\n"
            "但別擔心！我們為您量身打造了專屬的**「互動手寫練習網頁」**：\n\n"
            "🎨 **手寫板三大特色**：\n"
            "1. **傳統米字格 ＋ 虛線描紅**：背景帶有半透明假名字形，照著描絕不走樣！\n"
            "2. **毛筆墨水筆刷**：支援手指在手機螢幕上觸控塗鴉，或用電腦滑鼠書寫。\n"
            "3. **一鍵切換與清除**：內建「あ・い・う・え・お・こ・れ」等核心假名與記憶口訣。\n\n"
            "📂 **如何打開練習板？**\n"
            "在您電腦的 `Japanese_Learning` 資料夾中，直接雙擊打開：\n"
            "👉 **`handwriting.html`**\n"
            "即可在任何瀏覽器中盡情練字囉！"
        ),
        color=discord.Color.from_rgb(230, 120, 40)
    )
    embed.add_field(
        name="🖌️ 假名書寫三大秘訣",
        value=(
            "• **圓潤柔和**：平假名來自草書，線條要有弧度，不要像寫漢字那麼剛硬。\n"
            "• **圈圈留氣孔**：如 `す`、`ま`、`お` 的結繩小圈圈，要寫得圓潤飽滿。\n"
            "• **字形平衡**：利用米字格的中心交叉點定位核心結構。"
        ),
        inline=False
    )
    embed.set_footer(text="手腦並用寫過一次，記憶深刻 10 倍！")
    await interaction.response.send_message(embed=embed)


# /plan 指令 (全方位學習計畫：平日通勤、假日沉浸與完整路線圖)
@bot.tree.command(name="plan", description="查看全方位日語學習計畫（支援假日沉浸實戰、平日通勤微學習與全階段路線圖）")
@app_commands.describe(mode="選擇想直接開啟的學習計畫模組（亦可隨時於下方點擊按鈕切換）")
@app_commands.choices(mode=[
    app_commands.Choice(name="🏖️ 假日沉浸深度計畫 (Weekend Plan 30~45分)", value="weekend"),
    app_commands.Choice(name="☕ 平日通勤微學習計畫 (Weekday Plan 15分)", value="weekday"),
    app_commands.Choice(name="🗺️ 全階段日語路線圖 (Roadmap N5~N1)", value="roadmap"),
])
async def plan_command(interaction: discord.Interaction, mode: app_commands.Choice[str] = None):
    chosen_mode = mode.value if mode else "weekend"
    if chosen_mode == "weekend":
        embed = build_weekend_plan_embed()
    elif chosen_mode == "weekday":
        embed = build_weekday_plan_embed()
    else:
        embed = build_roadmap_embed()

    view = PlanView(current_mode=chosen_mode)
    await interaction.response.send_message(embed=embed, view=view)


# /voice 指令
@bot.tree.command(name="voice", description="輸入任何日文句子，機器人立即為您真人語音發音（支援男聲/女聲）")
@app_commands.describe(
    text="請輸入想要發音的日文（例如：これをお願いします 或 ありがとうございます）",
    speed="選擇語速模式",
    voice="選擇聲線（溫柔女聲 / 沉穩男聲）"
)
@app_commands.choices(
    speed=[
        app_commands.Choice(name="🐢 慢速跟讀版 (適合新手，字字清晰)", value="-30%"),
        app_commands.Choice(name="🐰 正常語速 (實戰日常情境)", value="+0%"),
    ],
    voice=[
        app_commands.Choice(name="👩 溫柔女聲 (Nanami)", value="female"),
        app_commands.Choice(name="👨 沉穩男聲 (Keita)", value="male"),
    ]
)
async def voice_command(interaction: discord.Interaction, text: str, speed: app_commands.Choice[str] = None, voice: app_commands.Choice[str] = None):
    await interaction.response.defer()
    rate = speed.value if speed else "-25%"
    speed_name = speed.name if speed else "🐢 慢速跟讀版"
    v_mode = voice.value if voice else "female"
    v_name = voice.name if voice else "👩 溫柔女聲 (Nanami)"
    path = None
    try:
        path = await text_to_speech(text, "voice_command.mp3", rate=rate, voice=v_mode)
        file = discord.File(path, filename="japanese_pronunciation.mp3")
        embed = discord.Embed(
            title="🔊 日語真人標準發音",
            description=f"### 『 {text} 』\n\n• **目前語速**：`{speed_name}`\n• **目前聲線**：`{v_name}`\n\n👇 點擊下方音檔的 **【▶️ 播放鍵】** 即可收聽！",
            color=discord.Color.from_rgb(80, 200, 180)
        )
        embed.set_footer(text="提示：新手建議先用慢速熟悉舌頭肌肉動作，多聽男聲與女聲能適應真實聽力喔！")
        await interaction.followup.send(embed=embed, file=file)
        file.close()
    except Exception as e:
        await interaction.followup.send(f"❌ 語音生成失敗: {e}")
    finally:
        remove_temp_file(path)


# /card 指令
@bot.tree.command(name="card", description="查看精美日語情境圖卡與標準發音（支援全 10 大關卡與假名圖卡）")
@app_commands.describe(type="選擇想查看的圖卡（1~10 關卡圖卡或經典圖卡）")
@app_commands.choices(type=[
    app_commands.Choice(name="🍜 第 1 關：これ、ください (點餐柴犬)", value="quest_1"),
    app_commands.Choice(name="🏷️ 第 2 關：いくらですか？ (問價女孩)", value="quest_2"),
    app_commands.Choice(name="🗺️ 第 3 關：トイレはどこですか？ (問路洗手間)", value="quest_3"),
    app_commands.Choice(name="🍜 第 4 關：ラーメンを食べたいです (想吃拉麵)", value="quest_4"),
    app_commands.Choice(name="🏪 第 5 關：傘はありますか？ (雨天買傘)", value="quest_5"),
    app_commands.Choice(name="🍱 第 6 關：温めてください (超商微波)", value="quest_6"),
    app_commands.Choice(name="🍶 第 7 關：お会計をお願いします (居酒屋買單)", value="quest_7"),
    app_commands.Choice(name="🍣 第 8 關：おすすめは何ですか？ (壽司主廚推薦)", value="quest_8"),
    app_commands.Choice(name="🛍️ 第 9 關：免税できますか？ (藥妝退稅)", value="quest_9"),
    app_commands.Choice(name="🎌 第 10 關：ありがとうございました (大圓滿感謝)", value="quest_10"),
    app_commands.Choice(name="🍎 經典假名：あ (蘋果圖像記憶)", value="a"),
])
async def card_command(interaction: discord.Interaction, type: app_commands.Choice[str] = None):
    await interaction.response.defer()
    chosen = type.value if type else "quest_1"
    
    if chosen.startswith("quest_"):
        lvl = int(chosen.split("_")[1])
        q = QUESTS.get(lvl, QUESTS[1])
        card_path = os.path.join(os.path.dirname(__file__), q.get("card_image", f"cards/card_quest{lvl}.jpg"))
        audio_text = q["phrase"]
        card_title = f"{q['title']}：『 {q['phrase']} 』"
        card_desc = (
            f"• **羅馬拼音**：*{q['romaji']}*\n"
            f"• **口訣諧音**：**{q['phonetic']}**\n"
            f"• **中文意思**：**{q['meaning']}**\n\n"
            f"{q.get('mnemonic_story', '')}\n\n"
            f"🍜 **情境示範**：{q['scenario']}"
        )
        card_color = discord.Color.from_rgb(255, 140, 60)
    elif chosen == "a":
        card_path = os.path.join(os.path.dirname(__file__), "cards", "card_a.jpg")
        audio_text = "あ。りんご。"
        card_title = "🎴 假名視覺圖卡：『 あ 』(a)"
        card_desc = (
            "🍎 **圖像聯想記憶法**：\n"
            "看到圖卡中的小紅蘋果（**りんご**）！\n"
            "字形就像張開手驚呼：**「啊（あ）！好甜的蘋果！」**\n\n"
            "🗣️ **發音秘訣**：嘴型放鬆自然微張，輕輕吐氣發音。"
        )
        card_color = discord.Color.from_rgb(100, 180, 255)
    else:
        card_path = os.path.join(os.path.dirname(__file__), "cards", "card_kore_kudasai.jpg")
        audio_text = "これ、ください。"
        card_title = "🍜 實戰生活圖卡：『 これ、ください 』"
        card_desc = (
            "• **羅馬拼音**：*Kore, kudasai.*\n"
            "• **口訣諧音**：**顆粒、庫達塞**\n"
            "• **意思**：This, please! (請給我這個)\n\n"
            "🐕 **情境秒記**：\n"
            "看圖卡裡的可愛柴犬小旅人！\n"
            "手指著菜單上香噴噴的拉麵說：**「これ、ください！」**，一秒搞定點餐！"
        )
        card_color = discord.Color.from_rgb(255, 160, 80)

    if os.path.exists(card_path):
        voice_path = None
        try:
            voice_path = await text_to_speech(audio_text, f"card_{chosen}_voice.mp3", rate="-20%")
            audio_file = discord.File(voice_path, filename=f"card_{chosen}.mp3")
        except Exception:
            audio_file = None

        img_file = discord.File(card_path, filename=f"card_{chosen}.jpg")
        embed = discord.Embed(
            title=card_title,
            description=card_desc + "\n\n👇 **點擊下方音檔即可收聽道地標準發音！**",
            color=card_color
        )
        embed.set_image(url=f"attachment://card_{chosen}.jpg")
        embed.set_footer(text="每天一張圖卡，圖像記憶最深刻！")

        files = [img_file]
        if audio_file:
            files.append(audio_file)

        try:
            await interaction.followup.send(embed=embed, files=files)
        finally:
            for f in files:
                f.close()
            remove_temp_file(voice_path)
    else:
        await interaction.followup.send("圖卡準備中，敬請期待！")


# /anime 指令
@bot.tree.command(name="anime", description="【動漫日語名台詞】精選超人氣動漫台詞、文法拆解、口訣諧音與標準發音")
@app_commands.describe(title="選擇想要學習的動漫名台詞（不選則隨機抽取）")
@app_commands.choices(title=[
    app_commands.Choice(name="⚔️ 鬼滅之刃 (炭治郎：長男我慢)", value="kimetsu"),
    app_commands.Choice(name="🤞 咒術迴戰 (五條悟：僕最強だから)", value="jujutsu"),
    app_commands.Choice(name="🔍 名偵探柯南 (柯南：真実はいつもひとつ)", value="conan"),
    app_commands.Choice(name="👒 航海王 (魯夫：海賊王に、おれはなる)", value="onepiece"),
    app_commands.Choice(name="🏀 灌籃高手 (安西教練：あきらめたら試合終了)", value="slamdunk"),
    app_commands.Choice(name="🪄 葬送的芙莉蓮 (芙莉蓮：ヒンメルならそうした)", value="frieren"),
    app_commands.Choice(name="🥜 間諜家家酒 (安妮亞：ピーナッツが好き)", value="spyfamily"),
    app_commands.Choice(name="⚔️ 進擊的巨人 (艾連：戦わなければ勝てない)", value="shingeki"),
])
async def anime_command(interaction: discord.Interaction, title: app_commands.Choice[str] = None):
    await interaction.response.defer()
    
    if title:
        item = ANIME_QUOTES.get(title.value)
    else:
        item = random.choice(list(ANIME_QUOTES.values()))
        
    if not item:
        await interaction.followup.send("找不到該動漫台詞資料。")
        return
        
    grammar_text = "\n".join(item["grammar_breakdown"])
    embed = discord.Embed(
        title=f"🎌 動漫名台詞解析：{item['anime']}",
        description=(
            f"👤 **登場角色**：**{item['character']}**\n\n"
            f"🎬 **熱血名場面**：\n{item['scene']}\n\n"
            f"------------------------------------\n"
            f"### 🗣️ 經典原句：『 {item['quote']} 』\n"
            f"• **假名標註**：`{item['furigana']}`\n"
            f"• **羅馬拼音**：*{item['romaji']}*\n"
            f"• **口訣諧音**：**{item['phonetic']}**\n"
            f"• **中文意思**：**{item['meaning']}**\n\n"
            f"------------------------------------\n"
            f"🔍 **【核心文法大拆解】**：\n"
            f"{grammar_text}\n\n"
            f"------------------------------------\n"
            f"✍️ **【舉一反三仿造練習】**：\n"
            f"📌 **句型公式**：`{item['practice_template']}`\n"
            f"💡 **實用範例**：{item['practice_example']}\n\n"
            f"👇 **點擊下方音檔收聽角色原味日語標準發音！**"
        ),
        color=discord.Color.from_rgb(235, 75, 95)
    )
    embed.set_footer(text="動漫日語最對味！多聽多唸，語感自然上身！")
    
    voice_path = None
    try:
        voice_path = await text_to_speech(item["quote"], f"anime_{item['id']}.mp3", rate="-15%")
        file = discord.File(voice_path, filename=f"anime_{item['id']}.mp3")
        await interaction.followup.send(embed=embed, file=file)
        file.close()
    except Exception:
        await interaction.followup.send(embed=embed)
    finally:
        remove_temp_file(voice_path)




# /kana 指令
@bot.tree.command(name="kana", description="【從零學五十音】46 假名翻頁卡片流：漢字字源、發音秘訣、記憶口訣與即時測驗")
@app_commands.describe(row="選填：指定直接跳轉的行別（預設從あ行開始卡片流）")
@app_commands.choices(row=[
    app_commands.Choice(name="あ行 (a, i, u, e, o)", value="a"),
    app_commands.Choice(name="か行 (ka, ki, ku, ke, ko)", value="ka"),
    app_commands.Choice(name="さ行 (sa, shi, su, se, so)", value="sa"),
    app_commands.Choice(name="た行 (ta, chi, tsu, te, to)", value="ta"),
    app_commands.Choice(name="な行 (na, ni, nu, ne, no)", value="na"),
    app_commands.Choice(name="は行 (ha, hi, fu, he, ho)", value="ha"),
    app_commands.Choice(name="ま行 (ma, mi, mu, me, mo)", value="ma"),
    app_commands.Choice(name="や行 (ya, yu, yo)", value="ya"),
    app_commands.Choice(name="ら行 (ra, ri, ru, re, ro)", value="ra"),
    app_commands.Choice(name="わ行與撥音 (wa, wo, n)", value="wa"),
])
async def kana_command(interaction: discord.Interaction, row: app_commands.Choice[str] = None):
    row_starts = {
        "a": 0, "ka": 5, "sa": 10, "ta": 15, "na": 20,
        "ha": 25, "ma": 30, "ya": 35, "ra": 38, "wa": 43
    }
    start_idx = row_starts.get(row.value, 0) if row else 0
    embed = build_kana_card_embed(start_idx)
    view = KanaFlashcardView(start_idx)
    await interaction.response.send_message(embed=embed, view=view)


# /kana_loop 指令 (五十音字卡循環自動播放模式)
@bot.tree.command(name="kana_loop", description="【五十音自動巡迴】啟動 46 假名字卡自動循環播放（支援暫停、調速與即時隨堂測驗）")
@app_commands.describe(
    row="選填：指定從哪一行開始循環播放（預設從あ行開始）",
    speed="選填：每張字卡停頓秒數（預設 4 秒，可選 3~8 秒）"
)
@app_commands.choices(row=[
    app_commands.Choice(name="あ行 (a, i, u, e, o)", value="a"),
    app_commands.Choice(name="か行 (ka, ki, ku, ke, ko)", value="ka"),
    app_commands.Choice(name="さ行 (sa, shi, su, se, so)", value="sa"),
    app_commands.Choice(name="た行 (ta, chi, tsu, te, to)", value="ta"),
    app_commands.Choice(name="な行 (na, ni, nu, ne, no)", value="na"),
    app_commands.Choice(name="は行 (ha, hi, fu, he, ho)", value="ha"),
    app_commands.Choice(name="ま行 (ma, mi, mu, me, mo)", value="ma"),
    app_commands.Choice(name="や行 (ya, yu, yo)", value="ya"),
    app_commands.Choice(name="ら行 (ra, ri, ru, re, ro)", value="ra"),
    app_commands.Choice(name="わ行與撥音 (wa, wo, n)", value="wa"),
])
async def kana_loop_command(
    interaction: discord.Interaction,
    row: app_commands.Choice[str] = None,
    speed: float = 4.0
):
    row_starts = {
        "a": 0, "ka": 5, "sa": 10, "ta": 15, "na": 20,
        "ha": 25, "ma": 30, "ya": 35, "ra": 38, "wa": 43
    }
    start_idx = row_starts.get(row.value, 0) if row else 0
    clamped_speed = max(2.5, min(10.0, speed))
    auto_view = KanaAutoPlayView(current_idx=start_idx, speed_seconds=clamped_speed)
    auto_embed = auto_view.build_autoplay_embed()
    await interaction.response.send_message(embed=auto_embed, view=auto_view)
    auto_view.start_loop(interaction)



# /scenario 指令
@bot.tree.command(name="scenario", description="查看四大核心情境的必備高頻日文金句")
@app_commands.describe(category="請選擇情境")
@app_commands.choices(category=[
    app_commands.Choice(name="✈️ 旅遊生存 (Travel)", value="travel"),
    app_commands.Choice(name="🏠 日常生活 (Daily Life)", value="daily"),
    app_commands.Choice(name="🎮 休閒娛樂 (Anime & Leisure)", value="anime"),
    app_commands.Choice(name="💼 職場敬語 (Work & Business)", value="work"),
])
async def scenario_command(interaction: discord.Interaction, category: app_commands.Choice[str]):
    sc = SCENARIOS.get(category.value)
    if not sc:
        await interaction.response.send_message("找不到該情境資料。", ephemeral=True)
        return

    embed = discord.Embed(
        title=sc["title"],
        description=sc["description"],
        color=discord.Color.gold()
    )

    for p in sc["phrases"]:
        embed.add_field(
            name=f"{p['japanese']}（{p['meaning']}）",
            value=f"• 假名標註：`{p['furigana']}`\n• 拼音：*{p['romaji']}*\n• 💬 **用法**：{p['usage']}",
            inline=False
        )

    await interaction.response.send_message(embed=embed)


# /quiz 指令
@bot.tree.command(name="quiz", description="隨機抽取一道互動日語測驗題（支援五十音專屬考驗、全方位測驗）")
@app_commands.describe(category="選擇測驗分類（五十音、情境單字、或全題庫隨機）")
@app_commands.choices(category=[
    app_commands.Choice(name="🔤 五十音專屬大考驗 (新手必練！)", value="kana"),
    app_commands.Choice(name="🎲 全題庫隨機測驗 (挑戰綜合實力)", value="all"),
    app_commands.Choice(name="✈️ 旅遊與生活情境實戰", value="scenario"),
])
async def quiz_command(interaction: discord.Interaction, category: app_commands.Choice[str] = None):
    cat_key = category.value if category else "all"
    questions = get_quizzes_by_category(cat_key)
    q = random.choice(questions)
    options = list(q["options"])
    random.shuffle(options)

    embed = discord.Embed(
        title=f"📝 日語隨堂考：【{q['category']}】",
        description=f"**{q['question']}**\n\n請點擊下方按鈕進行作答：",
        color=discord.Color.blue()
    )

    view = QuizView(
        question_text=q["question"],
        correct_answer=q["answer"],
        explanation=q["explanation"],
        options=options,
        category=cat_key
    )

    await interaction.response.send_message(embed=embed, view=view)


# /daily 指令
@bot.tree.command(name="daily", description="抽取今日日語學習小卡（附真人語音、好奇心冷知識與連抽按鈕）")
async def daily_command(interaction: discord.Interaction):
    cat_title, item = get_random_daily_phrase()
    embed = build_daily_phrase_embed(cat_title, item)
    view = DailyCardView()
    # TTS 生成可能超過 3 秒，先 defer 避免「應用程式未回應」
    await interaction.response.defer()

    voice_path = None
    try:
        voice_path = await text_to_speech(item["japanese"], "daily_voice.mp3")
        file = discord.File(voice_path, filename="daily_phrase.mp3")
        await interaction.followup.send(embed=embed, file=file, view=view)
        file.close()
    except Exception:
        await interaction.followup.send(embed=embed, view=view)
    finally:
        remove_temp_file(voice_path)


# /chat 指令 (AI 實戰情境角色扮演)
@bot.tree.command(name="chat", description="AI 實戰情境角色扮演：與拉麵店、飯店、超商、居酒屋進行分支對話互動")
@app_commands.describe(scenario="請選擇實戰情境")
@app_commands.choices(scenario=[
    app_commands.Choice(name="🍜 日本拉麵店點餐實戰", value="ramen"),
    app_commands.Choice(name="🏨 飯店辦理入住 (Check-in)", value="hotel"),
    app_commands.Choice(name="🏪 超商結帳生存實戰", value="convenience"),
    app_commands.Choice(name="🏮 居酒屋乾杯實戰", value="izakaya"),
])
async def chat_command(interaction: discord.Interaction, scenario: app_commands.Choice[str]):
    sc = ROLEPLAY_SCENARIOS.get(scenario.value)
    if not sc:
        await interaction.response.send_message("找不到該情境資料。", ephemeral=True)
        return

    first_step = sc["steps"][0]
    embed = discord.Embed(
        title=sc["title"],
        description=(
            f"📖 **情境簡介**：{sc['description']}\n\n"
            f"------------------------------------\n"
            f"### 👤 店員/NPC 問道：\n"
            f"## 『 {first_step['npc']} 』\n"
            f"• **假名標註**：`{first_step['furigana']}`\n"
            f"• **羅馬拼音**：*{first_step['romaji']}*\n"
            f"• **中文意思**：**{first_step['translation']}**\n\n"
            f"👇 **請點擊下方按鈕選擇您的第一句回應：**"
        ),
        color=discord.Color.from_rgb(100, 160, 255)
    )
    embed.set_footer(text="模擬真實赴日會話，每一步都有假名音標與翻譯，無痛開口！")
    view = RoleplayView(scenario.value, 0)
    await interaction.response.send_message(embed=embed, view=view)


# /katakana 指令 (片假名外來語解碼器)
@bot.tree.command(name="katakana", description="片假名外來語解碼器：速查外來語語源或進行按鈕猜詞測驗")
@app_commands.describe(
    mode="選擇模式：查詢常用外來語，或進行猜詞測驗",
    search="關鍵字搜尋（可輸入片假名或中文，例如：コーヒー、啤酒、麵包）"
)
@app_commands.choices(mode=[
    app_commands.Choice(name="🔍 外來語語源速查 (Lookup)", value="lookup"),
    app_commands.Choice(name="🎯 片假名按鈕測驗 (Quiz)", value="quiz"),
])
async def katakana_command(interaction: discord.Interaction, mode: app_commands.Choice[str], search: str = None):
    if mode.value == "quiz":
        q = random.choice(KATAKANA_QUIZZES)
        options = list(q["options"])
        random.shuffle(options)
        embed = discord.Embed(
            title="🎯 片假名外來語猜詞大考驗",
            description=f"**{q['question']}**\n\n請點擊下方按鈕進行作答：",
            color=discord.Color.purple()
        )
        embed.set_footer(text="考驗你的和製英語與語源聯想力！")
        view = KatakanaQuizView(q["question"], q["answer"], q["explanation"], options)
        await interaction.response.send_message(embed=embed, view=view)
    else:
        filtered = KATAKANA_WORDS
        if search:
            s = search.strip().lower()
            filtered = [w for w in KATAKANA_WORDS if s in w["word"].lower() or s in w["meaning"].lower() or s in w["origin"].lower()]

        if not filtered:
            await interaction.response.send_message(f"在常用庫中找不到與 `{search}` 相關的片假名，建議嘗試：コーヒー、ビール、パン、スマホ、ホテル 等！", ephemeral=True)
            return

        embed = discord.Embed(
            title="🧩 片假名外來語解碼字典",
            description=f"日本片假名有高達 80% 來自外語音譯！看懂語源，秒記 100 個單字！\n" + (f"🔍 搜尋條件：`{search}`\n" if search else ""),
            color=discord.Color.teal()
        )
        for item in filtered[:6]:
            embed.add_field(
                name=f"🔤 {item['word']}（{item['meaning']}）",
                value=(
                    f"• 拼音：*{item['romaji']}*\n"
                    f"• 語源：**{item['origin']}**\n"
                    f"• 💡 **解析**：{item['note']}"
                ),
                inline=False
            )
        embed.set_footer(text="輸入 /katakana mode:測驗 可以直接玩猜詞測驗！")
        await interaction.response.send_message(embed=embed)


# /review 指令 (智慧錯題本)
@bot.tree.command(name="review", description="智慧錯題本：複習隨堂測驗中答錯的題目，答對立即斬除！")
async def review_command(interaction: discord.Interaction):
    mistakes = get_mistakes(interaction.user.id)
    if not mistakes:
        embed = discord.Embed(
            title="🎉 錯題本目前空空如也！",
            description="太厲害了！你目前沒有任何未攻克的錯題！\n隨時透過 `/quiz` 或 `/quest` 進行挑戰，如有答錯會自動收錄在此！",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
        return

    target_mistake = random.choice(mistakes)
    options = list(target_mistake["options"])
    random.shuffle(options)

    embed = discord.Embed(
        title="🔄【艾賓浩斯抗遺忘】錯題複習衝刺",
        description=(
            f"📚 **目前累積錯題**：共 {len(mistakes)} 題待複習\n"
            f"------------------------------------\n"
            f"### ❓ 複習題目：\n"
            f"**{target_mistake['question']}**\n\n"
            f"👇 **請點擊下方按鈕重新作答，答對即可徹底移出錯題本！**"
        ),
        color=discord.Color.orange()
    )
    embed.set_footer(text="把錯題變成直覺記憶，是學日語最快的神級捷徑！")
    view = ReviewQuizView(
        question_text=target_mistake["question"],
        correct_answer=target_mistake["answer"],
        explanation=target_mistake["explanation"],
        options=options
    )
    await interaction.response.send_message(embed=embed, view=view)


# /profile 指令 (個人學習檔案與成就勳章牆)
@bot.tree.command(name="profile", description="查看個人日語學習檔案：累積打卡天數、關卡進度與成就勳章牆")
async def profile_command(interaction: discord.Interaction):
    user_prog = get_user_progress(interaction.user.id)
    streak = user_prog.get("streak", 1)
    lvl = user_prog.get("current_level", 1)
    completed_lvls = user_prog.get("completed_levels", [])
    mistakes_count = len(user_prog.get("mistakes", []))
    earned_badges = user_prog.get("badges", ["first_step"])

    filled = "🟩" * min(lvl, TOTAL_QUESTS)
    unfilled = "⬜" * max(0, TOTAL_QUESTS - lvl)
    bar = f"{filled}{unfilled} (Level {lvl}/{TOTAL_QUESTS})"

    badge_lines = []
    for bid, binfo in BADGES_INFO.items():
        if bid in earned_badges:
            badge_lines.append(f"✅ **{binfo['name']}**：{binfo['desc']}")
        else:
            badge_lines.append(f"🔒 *{binfo['name']}*（未解鎖）")
    badges_display = "\n".join(badge_lines)

    embed = discord.Embed(
        title=f"🌸 {interaction.user.display_name} 的日語修煉檔案",
        description=(
            f"🔥 **累積打卡天數 (Streak)**：`{streak} 天` 🏅\n"
            f"📈 **闖關主線進度**：`{bar}`\n"
            f"🏆 **已通關關卡數**：`{len(completed_lvls)} / {TOTAL_QUESTS} 關`\n"
            f"📝 **待複習錯題數**：`{mistakes_count} 題`\n\n"
            f"------------------------------------\n"
            f"### 🎖️ 【成就勳章展示牆】\n"
            f"{badges_display}"
        ),
        color=discord.Color.from_rgb(255, 105, 180)
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url if interaction.user.display_avatar else None)
    embed.set_footer(text="每天只要 15 分鐘，日積月累成就自由行達人！")
    await interaction.response.send_message(embed=embed)


# /culture 指令 (日本文化與旅遊避坑指南)
@bot.tree.command(name="culture", description="日本文化與旅遊避坑指南：お通し、電車、溫泉、邊走邊吃等 6 大避坑手冊")
@app_commands.describe(topic="選擇避坑主題")
@app_commands.choices(topic=[
    app_commands.Choice(name="🏮 居酒屋「お通し」開胃菜收費文化", value="otoshi"),
    app_commands.Choice(name="🚃 日本電車三大天條 (靜音/背包/優先席)", value="train"),
    app_commands.Choice(name="♨️ 溫泉入浴秘笈 (毛巾禁下水/洗淨/刺青)", value="onsen"),
    app_commands.Choice(name="🍡 街頭邊走邊吃禁忌與垃圾處理", value="eating"),
    app_commands.Choice(name="💴 結帳找零小托盤使用禮儀", value="tray"),
    app_commands.Choice(name="🛍️ 免稅密封袋境內禁拆規定", value="taxfree"),
])
async def culture_command(interaction: discord.Interaction, topic: app_commands.Choice[str] = None):
    chosen_key = topic.value if topic else "otoshi"
    unlock_badge(interaction.user.id, "badge_culture")
    item = CULTURE_TOPICS[chosen_key]
    rules_text = "\n".join([f"• {r}" for r in item["rules"]])

    embed = discord.Embed(
        title=item["title"],
        description=(
            f"🏷️ **所屬分類**：`{item['category']}`\n\n"
            f"❓ **常見疑問/痛點**：\n> {item['problem']}\n\n"
            f"💡 **在地文化真相**：\n{item['explanation']}\n\n"
            f"------------------------------------\n"
            f"🛡️ **【避坑生存守則】**：\n{rules_text}\n\n"
            f"------------------------------------\n"
            f"🗣️ **必備應對日語**：\n"
            f"『 **{item['japanese_phrase']}** 』\n"
            f"• 拼音：*{item['romaji']}*"
        ),
        color=discord.Color.from_rgb(255, 120, 80)
    )
    embed.set_footer(text="入鄉隨俗，懂禮儀玩得更開心尊嚴！點擊下方按鈕切換其他主題。")
    view = CultureSelectView(chosen_key)
    await interaction.response.send_message(embed=embed, view=view)


# /scan 指令 (拍照掃描解碼與假名注音)
@bot.tree.command(name="scan", description="拍照掃描解碼：上傳日本招牌、菜單、標語照片或輸入文字，解析假名注音與生存攻略")
@app_commands.describe(
    image="上傳日本招牌、菜單、商品包裝照片 (選填)",
    text_hint="照片上的文字提示或任何想查詢的招牌字詞（例如：替玉、半額、お通し）"
)
async def scan_command(interaction: discord.Interaction, image: discord.Attachment = None, text_hint: str = None):
    await interaction.response.defer()
    record_daily_activity(interaction.user.id)

    target_key = None
    if text_hint:
        for k in SIGN_DATABASE.keys():
            if k in text_hint or text_hint in k:
                target_key = k
                break

    if not target_key and image:
        fname = image.filename.lower()
        for k, v in SIGN_DATABASE.items():
            if k in fname or v["romaji"] in fname or v["meaning"] in fname:
                target_key = k
                break

    if not target_key and text_hint:
        embed = discord.Embed(
            title=f"📸 拍照掃描解碼：『 {text_hint} 』",
            description=(
                f"🔤 **日文字詞**：### 『 {text_hint} 』\n\n"
                f"💡 **即時解析**：\n"
                f"已為您讀取該字詞！點擊下方音檔可直接收聽日語真人發音跟讀！\n\n"
                f"------------------------------------\n"
                f"🗺️ **日本生存小秘訣**：\n"
                f"如果在日本街頭或店家招牌看到不確定的漢字，直接對著店員指著招牌並說：\n"
                f"『 **これは何ですか？ (Kore wa nan desu ka?)** 』（這是什麼呢？）\n"
                f"即可輕鬆打破語言隔閡！"
            ),
            color=discord.Color.from_rgb(40, 180, 200)
        )
        if image:
            embed.set_image(url=image.url)
        voice_path = None
        try:
            voice_path = await text_to_speech(text_hint, "scan_custom.mp3")
            snd_file = discord.File(voice_path, filename="scan_pronunciation.mp3")
            await interaction.followup.send(embed=embed, file=snd_file)
            snd_file.close()
        except Exception:
            await interaction.followup.send(embed=embed)
        finally:
            remove_temp_file(voice_path)
        return

    if not target_key:
        target_key = "ラーメン" if not image else random.choice(list(SIGN_DATABASE.keys()))

    info = SIGN_DATABASE[target_key]
    embed = discord.Embed(
        title=f"📸 拍照掃描辨識：【{target_key}】",
        description=(
            f"### 🪧 辨識招牌/菜單原字：『 {target_key} 』\n\n"
            f"• 🔤 **平假名讀音**：`{info['furigana']}`\n"
            f"• 🗣️ **羅馬拼音**：*{info['romaji']}*\n"
            f"• 🇹🇼 **中文意思**：**{info['meaning']}**\n\n"
            f"------------------------------------\n"
            f"💡 **【日本實戰生存小攻略】**：\n"
            f"{info['tip']}\n\n"
            f"👇 **點擊下方音檔收聽道地標準日語發音！**"
        ),
        color=discord.Color.from_rgb(50, 205, 50)
    )
    if image:
        embed.set_image(url=image.url)
    embed.set_footer(text="拍照即學！赴日旅遊看到不懂的招牌、菜單、標語隨時傳給機器人解碼！")

    voice_path = None
    try:
        voice_path = await text_to_speech(target_key, f"scan_{target_key}.mp3")
        snd_file = discord.File(voice_path, filename="scan_voice.mp3")
        await interaction.followup.send(embed=embed, file=snd_file)
        snd_file.close()
    except Exception:
        await interaction.followup.send(embed=embed)
    finally:
        remove_temp_file(voice_path)


# /sos 指令 (日本緊急生存就醫手指卡)
@bot.tree.command(name="sos", description="日本緊急生存就醫手指卡：急救看病、物品遺失、報警與問路")
@app_commands.describe(scenario="選擇緊急求助情境")
@app_commands.choices(scenario=[
    app_commands.Choice(name="🏥 身體不適 / 急救就醫 (Medical)", value="medical"),
    app_commands.Choice(name="👜 護照 / 貴重物品遺失 (Lost)", value="lost"),
    app_commands.Choice(name="🚨 事故 / 報警求助 (Police)", value="police"),
    app_commands.Choice(name="🧭 迷路 / 尋找車站與景點 (Direction)", value="direction"),
])
async def sos_command(interaction: discord.Interaction, scenario: app_commands.Choice[str] = None):
    chosen_key = scenario.value if scenario else "medical"
    unlock_badge(interaction.user.id, "badge_sos")
    sc = SOS_SCENARIOS.get(chosen_key, SOS_SCENARIOS["medical"])

    # 緊急電話（EMERGENCY_CONTACTS 是 [{name, number, note}] 列表）
    contact_lines = "\n".join(f"• {c['name']}：**{c['number']}**" for c in EMERGENCY_CONTACTS)

    embed = discord.Embed(
        title=f"🚨 【緊急手指求助卡】{sc['title']}",
        description=(
            f"**{sc['intro']}**\n\n"
            f"------------------------------------\n"
            f"### 🚑 日本緊急求助電話：\n"
            f"{contact_lines}\n\n"
            f"------------------------------------\n"
            f"### 👆 【手指直接給日本人看】："
        ),
        color=discord.Color.red() if chosen_key in ["medical", "police"] else discord.Color.orange()
    )
    for c in sc["cards"][:25]:
        embed.add_field(
            name=f"🏷️ 【{c['tag']}】",
            value=(
                f"## 『 {c['japanese']} 』\n"
                f"• 假名：`{c['furigana']}`\n"
                f"• 拼音：*{c['romaji']}*\n"
                f"• 🇹🇼 **中文意涵**：**{c['chinese']}**"
            ),
            inline=False
        )
    embed.set_footer(text="不用開口！直接拿著此畫面給日本人看即可求救！可點選下方按鈕快速切換不同緊急情境！")
    view = SOSView(chosen_key)
    await interaction.response.send_message(embed=embed, view=view)


# /menu 指令 (日式餐廳點餐暗號字典)
@bot.tree.command(name="menu", description="日式餐廳點餐暗號字典：燒肉部位解碼、壽司魚種與客製暗號")
@app_commands.describe(category="選擇菜單類別")
@app_commands.choices(category=[
    app_commands.Choice(name="🥩 燒肉部位全解碼 (カルビ/ロース/ハラミ等)", value="yakiniku"),
    app_commands.Choice(name="🍣 壽司魚種全解碼 (マグロ/トロ/サーモン等)", value="sushi"),
    app_commands.Choice(name="🍜 餐廳客製點餐暗號 (つゆだく/硬度/蔥花)", value="custom_order"),
])
async def menu_command(interaction: discord.Interaction, category: app_commands.Choice[str] = None):
    chosen_cat = category.value if category else "yakiniku"
    unlock_badge(interaction.user.id, "badge_menu")
    data = MENU_CATEGORIES.get(chosen_cat, MENU_CATEGORIES["yakiniku"])

    embed = discord.Embed(
        title=f"🍽️ {data['title']}",
        description=f"{data['description']}\n\n點選下方按鈕可切換其他菜單類型！",
        color=discord.Color.from_rgb(230, 100, 50)
    )

    for item in data["items"][:25]:
        embed.add_field(
            name=f"🥢 {item['japanese']}（{item['meaning']}）",
            value=f"• 讀音：`{item['furigana']}`\n• 💡 **特色/點餐秘笈**：{item['detail']}",
            inline=False
        )

    embed.set_footer(text="進店點餐不踩雷，像日本在地老饕一樣自信點餐！")
    view = MenuView(chosen_cat)
    await interaction.response.send_message(embed=embed, view=view)


# /grammar 指令 (動詞變化速查與て形口訣)
@bot.tree.command(name="grammar", description="動詞變化 10 秒速查卡與て形口訣歌")
@app_commands.describe(verb="選擇常用動詞查看完整變化（選填）")
@app_commands.choices(verb=[
    app_commands.Choice(name="🚶 行く (iku / 去)", value="iku"),
    app_commands.Choice(name="🍱 食べる (taberu / 吃)", value="taberu"),
    app_commands.Choice(name="🍵 飲む (nomu / 喝)", value="nomu"),
    app_commands.Choice(name="💼 する (suru / 做)", value="suru"),
    app_commands.Choice(name="✈️ 来る (kuru / 來)", value="kuru"),
    app_commands.Choice(name="👀 見る (miru / 看)", value="miru"),
    app_commands.Choice(name="🛍️ 買う (kau / 買)", value="kau"),
])
async def grammar_command(interaction: discord.Interaction, verb: app_commands.Choice[str] = None):
    chosen_verb = verb.value if verb else "iku"
    unlock_badge(interaction.user.id, "badge_grammar")
    v_data = VERB_CONJUGATIONS.get(chosen_verb, VERB_CONJUGATIONS["iku"])

    embed = discord.Embed(
        title=f"🧩 日語動詞變化速查：【{v_data['verb']}】",
        description=(
            f"🏷️ **動詞分類**：`{v_data['type']}` | 中文：**{v_data['meaning']}**\n"
            f"🌟 **實用例句**：{v_data['example']}\n\n"
            f"🎵 **【五段動詞 て形 快速記憶口訣歌】**：\n"
            f"```text\n{TE_FORM_MNEMONIC}\n```\n"
            f"------------------------------------\n"
            f"### 📋 【全套動詞變化展開表】"
        )[:4096],
        color=discord.Color.from_rgb(130, 90, 220)
    )
    for form_name, form_val in v_data["forms"].items():
        embed.add_field(name=form_name, value=f"`{form_val}`", inline=True)
    embed.set_footer(text="點擊下方按鈕可快速切換不同動詞！")
    view = GrammarSelectView(chosen_verb)
    await interaction.response.send_message(embed=embed, view=view)


# /news 指令 (NHK 通勤簡易新聞閱讀)
@bot.tree.command(name="news", description="NHK 簡易日語新聞：通勤微閱讀（附假名注音、單字解析與語音）")
@app_commands.describe(article="選擇要閱讀的新聞主題")
@app_commands.choices(article=[
    # 直接由新聞資料產生選項，確保 value 一定對得上文章 id
    app_commands.Choice(name=a["title"][:100], value=a["id"]) for a in NHK_NEWS_ARTICLES[:25]
])
async def news_command(interaction: discord.Interaction, article: app_commands.Choice[str] = None):
    await interaction.response.defer()
    chosen_id = article.value if article else NHK_NEWS_ARTICLES[0]["id"]
    unlock_badge(interaction.user.id, "badge_news")

    art = next((a for a in NHK_NEWS_ARTICLES if a["id"] == chosen_id), NHK_NEWS_ARTICLES[0])

    vocab_lines = []
    for v in art["vocabulary"]:
        vocab_lines.append(f"• **{v['word']}**：{v['meaning']}")
    vocab_text = "\n".join(vocab_lines)

    embed = discord.Embed(
        title=f"📰 {art['title']}",
        description=(
            f"📅 **發布日期**：`{art['date']}`\n\n"
            f"------------------------------------\n"
            f"### 🇯🇵 日文原文：\n"
            f"{art['japanese']}\n\n"
            f"🔤 **假名讀音**：\n{art['furigana']}\n\n"
            f"------------------------------------\n"
            f"### 🇹🇼 中文摘要：\n"
            f"{art['summary']}\n\n"
            f"------------------------------------\n"
            f"### 📚 【重點必備單字】：\n"
            f"{vocab_text}\n\n"
            f"👇 **下方已為您生成這篇新聞的標準真人朗讀語音！**"
        )[:4096],
        color=discord.Color.from_rgb(30, 144, 255)
    )
    embed.set_footer(text="NHK NEWS WEB EASY 每天花 3 分鐘，語感聽力大提升！")

    voice_path = None
    try:
        voice_path = await text_to_speech(art["japanese"], f"news_{art['id']}.mp3")
        file = discord.File(voice_path, filename="news_audio.mp3")
        await interaction.followup.send(embed=embed, file=file)
        file.close()
    except Exception:
        await interaction.followup.send(embed=embed)
    finally:
        remove_temp_file(voice_path)


# /shadowing 指令 (實戰跟讀挑戰與語調指導)
@bot.tree.command(name="shadowing", description="日語實戰跟讀挑戰：高低語調走向、連音指導與標準朗讀")
@app_commands.describe(drill="選擇跟讀練習題目")
@app_commands.choices(drill=[
    # 直接由跟讀資料產生選項（情境 + 句子），確保 value 一定對得上題目 id
    app_commands.Choice(name=f"{d['scenario']} ({d['sentence']})"[:100], value=d["id"]) for d in SHADOWING_DRILLS[:25]
])
async def shadowing_command(interaction: discord.Interaction, drill: app_commands.Choice[str] = None):
    await interaction.response.defer()
    chosen_id = drill.value if drill else SHADOWING_DRILLS[0]["id"]
    unlock_badge(interaction.user.id, "badge_shadowing")

    d = next((item for item in SHADOWING_DRILLS if item["id"] == chosen_id), SHADOWING_DRILLS[0])

    embed = discord.Embed(
        title=f"🗣️ 日語跟讀影子練習：【{d['scenario']}】",
        description=(
            f"⭐ **難易度**：`{d['stars']}`\n\n"
            f"------------------------------------\n"
            f"### 🗣️ 日文句子：\n"
            f"## 『 {d['sentence']} 』\n"
            f"• 振假名：`{d['furigana']}`\n"
            f"• 羅馬音：*{d['romaji']}*\n"
            f"• 中文意思：**{d['meaning']}**\n\n"
            f"------------------------------------\n"
            f"### 💡 【語調與發音技巧訣竅】：\n"
            f"{d['pitch_tip']}\n\n"
            f"### 🎯 【實踐步驟】：\n"
            f"1️⃣ 先聽一遍下方音檔，感受母語者的節奏與語調。\n"
            f"2️⃣ 稍微落後 0.5 秒，邊聽邊開口模仿跟讀（影子練習法）。\n"
            f"3️⃣ 重複練習 3 次，直到不經思考就能流暢脫口而出！"
        ),
        color=discord.Color.from_rgb(0, 200, 150)
    )
    embed.set_footer(text="影子練習法 (Shadowing) 是日語口說語調提升最迅速的科學訓練法！")

    voice_path = None
    try:
        voice_path = await text_to_speech(d["sentence"], f"shadowing_{d['id']}.mp3")
        file = discord.File(voice_path, filename="shadowing_sample.mp3")
        await interaction.followup.send(embed=embed, file=file)
        file.close()
    except Exception:
        await interaction.followup.send(embed=embed)
    finally:
        remove_temp_file(voice_path)


# /leaderboard 指令 (學習天梯與打卡排行榜)
@bot.tree.command(name="leaderboard", description="查看日語學習天梯排行榜：累積打卡與通關榮譽榜")
async def leaderboard_command(interaction: discord.Interaction):
    leaders = get_leaderboard(limit=10)

    if not leaders:
        embed = discord.Embed(
            title="🏆 日語學習天梯排行榜",
            description="目前尚無學員數據，快使用 `/quest` 或 `/quiz` 搶下全服第一名！",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)
        return

    rank_icons = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    lines = []
    for idx, user_data in enumerate(leaders):
        icon = rank_icons[idx] if idx < len(rank_icons) else f"#{idx+1}"
        uid = user_data["user_id"]
        streak = user_data.get("streak", 1)
        lvl = user_data.get("current_level", 1)
        completed_cnt = len(user_data.get("completed_levels", []))
        badges_cnt = len(user_data.get("badges", []))
        user_mention = f"<@{uid}>"

        lines.append(
            f"{icon} {user_mention}\n"
            f"   🔥 Streak：`{streak} 天` | ⚔️ 關卡：`Level {lvl} ({completed_cnt}/{TOTAL_QUESTS})` | 🎖️ 勳章：`{badges_cnt} 個`"
        )

    board_text = "\n\n".join(lines)

    embed = discord.Embed(
        title="🏆 日語修煉殿堂・學霸排行榜",
        description=(
            f"榜單依據累積打卡天數（Streak）與主線關卡進度排序！\n\n"
            f"{board_text}\n\n"
            f"------------------------------------\n"
            f"💡 **每日衝榜密技**：每天使用任何學習指令（如 `/daily`、`/quest`、`/quiz`），即可維持連勝！"
        ),
        color=discord.Color.gold()
    )
    embed.set_footer(text="排行榜依最新學習紀錄排序，持之以恆者必成大器！")
    await interaction.response.send_message(embed=embed)


# ====================================================
# ⛩️ /omikuji 指令 (日本神社御神籤與開運占卜)
# ====================================================
@bot.tree.command(name="omikuji", description="⛩️【神社御神籤】抽今日靈籤！開運吉凶、古風日語箴言、籤詩寓意與開運物")
async def omikuji_command(interaction: discord.Interaction):
    record_daily_activity(interaction.user.id)
    fortune = draw_omikuji()
    embed = build_omikuji_embed(fortune)
    view = OmikujiView(fortune)
    await interaction.response.send_message(embed=embed, view=view)


# ====================================================
# 🏪 /drugstore 指令 (日本超商、藥妝店、超市實戰掃雷機)
# ====================================================
@bot.tree.command(name="drugstore", description="🏪【藥妝超商掃雷機】松本清、超商與超市必懂標示速查（常備藥、美妝功效、賞味期限）")
@app_commands.describe(category="請選擇想查閱的採購分類")
@app_commands.choices(category=[
    app_commands.Choice(name="💊 藥妝常備藥品 (感冒/止痛/胃藥/眼藥/消炎)", value="drugstore"),
    app_commands.Choice(name="💄 美妝護膚功效 (保濕/清爽/美白/毛穴/抗痘)", value="skincare"),
    app_commands.Choice(name="🍱 超商超市食品 (消費期限/賞味期限/半額/無糖)", value="food"),
])
async def drugstore_command(interaction: discord.Interaction, category: app_commands.Choice[str] = None):
    record_daily_activity(interaction.user.id)
    chosen = category.value if category else "drugstore"
    embed = build_drugstore_embed(chosen)
    view = DrugstoreSelectView(chosen)
    await interaction.response.send_message(embed=embed, view=view)


# ====================================================
# 🎵 /lyrics 指令 (J-POP 經典名曲歌詞日語教室)
# ====================================================
@bot.tree.command(name="lyrics", description="🎵【J-POP 歌詞日語教室】精選熱門神曲副歌（YOASOBI、米津玄師、宇多田光、愛繆等）")
@app_commands.describe(song="選擇想學習的 J-POP 經典名曲")
@app_commands.choices(song=[
    app_commands.Choice(name="🌟 YOASOBI —《アイドル》(Idol)", value="idol"),
    app_commands.Choice(name="🍋 米津玄師 —《Lemon》(法醫女王主題曲)", value="lemon"),
    app_commands.Choice(name="❄️ 宇多田光 —《First Love》(初戀傳奇神曲)", value="first_love"),
    app_commands.Choice(name="🌻 Aimyon —《マリーゴールド》(金盞花)", value="marigold"),
    app_commands.Choice(name="⚔️ LiSA —《紅蓮華》(鬼滅之刃主題曲)", value="gurenge"),
    app_commands.Choice(name="🌠 RADWIMPS —《前前前世》(你的名字主題曲)", value="zenzenzense"),
    app_commands.Choice(name="🥀 優里 —《ドライフラワー》(乾燥花)", value="dryflower"),
    app_commands.Choice(name="🌸 Spitz —《チェリー》(櫻桃國民神曲)", value="cherry"),
    app_commands.Choice(name="🕊️ King Gnu —《白日》(白日)", value="hakujitsu"),
    app_commands.Choice(name="🦖 Vaundy —《怪獣の花唄》(怪獸花唄)", value="kaiju"),
])
async def lyrics_command(interaction: discord.Interaction, song: app_commands.Choice[str] = None):
    record_daily_activity(interaction.user.id)
    if not JPOP_SONGS:
        await interaction.response.send_message(LYRICS_MISSING_MSG, ephemeral=True)
        return
    chosen = song.value if song else "idol"
    if chosen not in JPOP_SONGS:
        chosen = "idol" if "idol" in JPOP_SONGS else next(iter(JPOP_SONGS))
    embed = build_lyrics_embed(chosen)
    view = LyricsSelectView(chosen)

    song_data = JPOP_SONGS[chosen]
    files_to_send = []
    clip_rel = song_data.get("music_file", "")
    clip_full = os.path.join(os.path.dirname(__file__), clip_rel)
    if os.path.exists(clip_full):
        files_to_send.append(discord.File(clip_full, filename=f"{chosen}_music.m4a"))

    guide_rel = song_data.get("guide_file", "")
    guide_full = os.path.join(os.path.dirname(__file__), guide_rel)
    if os.path.exists(guide_full):
        files_to_send.append(discord.File(guide_full, filename=f"{chosen}_guide.mp3"))

    if files_to_send:
        await interaction.response.send_message(embed=embed, files=files_to_send, view=view)
    else:
        await interaction.response.send_message(embed=embed, view=view)


# ====================================================
# 🔤 /kana_game 指令 (五十音極速消除連連看小遊戲)
# ====================================================
@bot.tree.command(name="kana_game", description="🎮【五十音極速消除】超好玩按鈕連連看小遊戲！不記分、無壓力、純享受刷題手感！")
async def kana_game_command(interaction: discord.Interaction):
    record_daily_activity(interaction.user.id)
    game_view = KanaGameView(round_num=1)
    embed = game_view.build_embed()
    await interaction.response.send_message(embed=embed, view=game_view)


# ====================================================
# 🌸 /arcade 指令 (日語沉浸式學習遊樂園網頁版)
# ====================================================
@bot.tree.command(name="arcade", description="🌸【日語沉浸遊樂園】一鍵打開 0 延遲消消樂、J-POP 歌詞電台、盲盒扭蛋機與手寫道場！")
async def arcade_command(interaction: discord.Interaction):
    record_daily_activity(interaction.user.id)
    embed = discord.Embed(
        title="🌸【日語沉浸式學習遊樂園】網頁版已升級登場！",
        description=(
            "告別網路延遲！專為零基礎與日語愛好者打造的 **5 大沉浸式遊樂模組**：\n\n"
            "🎮 **1. 五十音極速消消樂**：0ms 敲擊連擊、Combo 音效、30 秒限時狂熱！\n"
            "🎤 **2. J-POP KTV 歌詞電台**：10 首正版原音、積木拆字浮窗、跟唱密技！\n"
            "🎰 **3. 秋葉原盲盒扭蛋機**：擬真轉盤動效、抽取 UR 動漫台詞與御神籤！\n"
            "🖌️ **4. 智能手寫評分道場**：46 假名米字格、筆順動畫示範、三星評分！\n"
            "📻 **5. 五十音沉浸循環輪播**：日系大字排版、自動定時朗讀、口訣字源！\n\n"
            "📂 **如何開啟網頁遊樂園？**\n"
            "在您電腦的 `Japanese_Learning` 資料夾中：\n"
            "👉 直接雙擊：**`開啟日語遊樂園.bat`** 或 **`index.html`**\n"
            "即可在瀏覽器中盡情享受完全零延遲的極致聲光體驗！✨"
        ),
        color=discord.Color.from_rgb(255, 107, 139)
    )
    embed.set_footer(text="電腦瀏覽器直接開啟，支援完整鍵盤、滑鼠與音效互動！")
    await interaction.response.send_message(embed=embed)


def main():

    if not TOKEN or TOKEN == "your_bot_token_here":
        print("\n" + "="*60)
        print("⚠️ 尚未設定 DISCORD_BOT_TOKEN！")
        print("請打開 .env 檔案，填入您在 Discord Developer Portal 取得的 Bot Token。")
        print("="*60 + "\n")
        return

    import sys
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print("\nBot 已手動停止。", flush=True)
        sys.exit(0)
    except Exception as e:
        print(f"\n⚠️ Bot 連線中斷或發生異常: {e}，退出程序以便 Watchdog 自動乾淨重啟...", flush=True)
        sys.exit(1)

    # 若非手動中斷而結束（如斷線關閉 loop），退出 code 1 讓 Watchdog 自動重啟
    sys.exit(1)


if __name__ == "__main__":
    main()

