"""把 Discord bot 的學習資料匯出成網頁用的 docs/data.js（GitHub Pages）。

用法：python tools/export_web_data.py
修改 data/*.py 後重新執行一次即可同步網頁內容。
"""
import ast
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT))

from data.anime_data import ANIME_QUOTES
from data.culture_data import CULTURE_TOPICS
from data.doyo_data import DOYO_SONGS
from data.grammar_data import TE_FORM_MNEMONIC, VERB_CONJUGATIONS
from data.kana_data import KANA_ROWS, ALL_KANA_CARDS
from data.katakana_data import KATAKANA_WORDS, KATAKANA_QUIZZES
from data.menu_data import MENU_CATEGORIES
from data.news_data import NHK_NEWS_ARTICLES
from data.omikuji_data import OMIKUJI_DATA
from data.phrases_data import SCENARIOS
from data.progress_manager import BADGES_INFO
from data.quest_data import QUESTS
from data.quiz_data import QUIZ_QUESTIONS
from data.roleplay_data import ROLEPLAY_SCENARIOS
from data.scan_data import SCAN_CATEGORIES
from data.shadowing_data import SHADOWING_DRILLS
from data.sos_data import EMERGENCY_CONTACTS, SOS_SCENARIOS
from data.trivia_data import JAPANESE_TRIVIA


def literal_from_bot(name: str):
    """從 bot.py 取出純資料常數（不 import discord）。"""
    tree = ast.parse((ROOT / "bot.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def copy_asset(src_rel: str, dest_dir: str) -> str:
    """複製素材到 docs/assets，回傳網頁相對路徑；檔案不存在則回傳空字串。"""
    if not src_rel:
        return ""
    src = ROOT / src_rel
    if not src.exists():
        return ""
    dest = DOCS / "assets" / dest_dir / src.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return f"assets/{dest_dir}/{src.name}"


def main():
    quests = {}
    for k, q in QUESTS.items():
        q = dict(q)
        q["card_image"] = copy_asset(q.get("card_image", ""), "cards")
        quests[str(k)] = q

    data = {
        "anime": ANIME_QUOTES,
        "culture": CULTURE_TOPICS,
        "teForm": TE_FORM_MNEMONIC,
        "verbs": VERB_CONJUGATIONS,
        "kanaRows": KANA_ROWS,
        "kanaCards": ALL_KANA_CARDS,
        "katakanaWords": KATAKANA_WORDS,
        "katakanaQuizzes": KATAKANA_QUIZZES,
        "doyo": DOYO_SONGS,
        "menu": MENU_CATEGORIES,
        "news": NHK_NEWS_ARTICLES,
        "omikuji": OMIKUJI_DATA,
        "scenarios": SCENARIOS,
        "badges": BADGES_INFO,
        "quests": quests,
        "quiz": QUIZ_QUESTIONS,
        "roleplay": ROLEPLAY_SCENARIOS,
        "scan": SCAN_CATEGORIES,
        "signs": literal_from_bot("SIGN_DATABASE"),
        "shadowing": SHADOWING_DRILLS,
        "sosContacts": EMERGENCY_CONTACTS,
        "sos": SOS_SCENARIOS,
        "trivia": JAPANESE_TRIVIA,
    }
    out = DOCS / "data.js"
    out.write_text("window.JP_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
