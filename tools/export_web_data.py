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
from data.hobi_course import HOBI_COURSE
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
from data.web_content import WEB_GOALS, WEB_PLANS, WEB_SETTINGS


def literal_from_bot(name: str):
    """從 bot.py 取出純資料常數（不 import discord）。"""
    tree = ast.parse((ROOT / "bot.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit(f"找不到 bot.py 裡的 {name}，請確認資料還在（網頁的對應功能會變空白）")


def copy_asset(src_rel: str, dest_dir: str) -> str:
    """複製素材到 docs/assets，回傳網頁相對路徑；沒有指定素材回傳空字串，指定了卻找不到就中止。"""
    if not src_rel:
        return ""
    src = ROOT / src_rel
    if not src.exists():
        raise SystemExit(f"找不到素材 {src_rel}（資料有引用，但檔案不存在）")
    dest = DOCS / "assets" / dest_dir / src.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return f"assets/{dest_dir}/{src.name}"


DRILL_FIELDS = {
    "choice": ("question", "options", "answer"),
    "listen": ("prompt", "pairs"),
    "say": ("prompt", "items"),
    "order": ("prompt", "sequence"),
    "write": ("prompt", "kana"),
    "recall": ("prompt", "items"),
}


def validate(data):
    """網頁會直接用到的欄位做基本檢查：缺資料就讓匯出失敗，而不是網站上默默變空白或卡住。"""
    errs = []

    def need(cond, msg):
        if not cond:
            errs.append(msg)

    def text(v):
        return isinstance(v, str) and v.strip() != ""

    def quiz(q, where):
        opts = q.get("options") or []
        need(text(q.get("question")), f"{where}: 缺 question")
        need(len(opts) >= 2, f"{where}: 選項少於 2 個")
        need(q.get("answer") in opts, f"{where}: 答案 {q.get('answer')!r} 不在選項裡")
        need(len(set(opts)) == len(opts), f"{where}: 選項重複 {opts}")
        need(all(text(o) for o in opts), f"{where}: 有空白選項")

    for key, val in data.items():
        need(bool(val), f"{key}: 是空的")
    for i, q in enumerate(data["quiz"]):
        quiz(q, f"quiz[{i}]")
    for i, q in enumerate(data["katakanaQuizzes"]):
        quiz(q, f"katakanaQuizzes[{i}]")
    levels = sorted(q["level"] for q in data["quests"].values())
    need(levels == list(range(1, len(levels) + 1)), f"quests: 關卡編號要從 1 連號，目前是 {levels}")
    for k, q in data["quests"].items():
        quiz(q.get("quiz") or {}, f"quests[{k}].quiz")
        for f in ("title", "phrase", "meaning"):
            need(text(q.get(f)), f"quests[{k}]: 缺 {f}")
    for k, r in data["roleplay"].items():
        need(r.get("badge") in data["badges"], f"roleplay[{k}]: 成就 {r.get('badge')} 不存在")
        n = len(r["steps"])
        for i, s in enumerate(r["steps"]):
            need(text(s.get("npc")) and s.get("options"), f"roleplay[{k}].steps[{i}]: 缺 npc 或選項")
            for o in s.get("options", []):
                ns = o.get("next_step")
                need(ns == "end" or (isinstance(ns, int) and i < ns < n), f"roleplay[{k}].steps[{i}]: next_step {ns!r} 無效")
    row_kana = [it["hira"] for row in data["kanaRows"].values() for it in row["items"]]
    need(row_kana == [c["hira"] for c in data["kanaCards"]], "kanaRows 與 kanaCards 的假名順序不一致")
    hobi = data["hobi"]
    ids = [l.get("id") for l in hobi.get("lessons", [])]
    need(ids and len(set(ids)) == len(ids), "hobi: 課程 id 重複或沒有課程")
    for l in hobi.get("lessons", []):
        need(l.get("points") and l.get("drills"), f"hobi[{l.get('id')}]: 缺重點或練習")
        for j, d in enumerate(l.get("drills", [])):
            where = f"hobi[{l.get('id')}].drills[{j}]"
            fields = DRILL_FIELDS.get(d.get("type"))
            if fields is None:
                errs.append(f"{where}: 未知的練習類型 {d.get('type')!r}")
                continue
            for f in fields:
                need(d.get(f), f"{where}: 缺 {f}")
            if d["type"] == "choice":
                quiz(d, where)
            if d["type"] == "order":
                need(len(set(d.get("sequence", []))) >= 4, f"{where}: sequence 至少要 4 個不同的字")
    site = data["site"]
    for k, g in site["goals"].items():
        need(g.get("steps"), f"site.goals[{k}]: 沒有步驟")
        for s in g.get("steps", []):
            need(str(s.get("href", "")).startswith("#/"), f"site.goals[{k}]: 連結要用 #/ 開頭")
    need(all(b in data["badges"] for b in site["settings"]["streak_badges"]), "site.settings.streak_badges: 有不存在的成就")
    need(site["settings"]["srs_new_per_day"] in site["settings"]["srs_new_per_day_choices"], "site.settings: srs_new_per_day 不在選項中")
    return errs


def main():
    # 清掉舊素材，避免刪除或改名的圖卡殘留在網站上
    shutil.rmtree(DOCS / "assets" / "cards", ignore_errors=True)

    # 同一張圖卡被多關共用時（例如 11～20 關暫用第 1 關圖卡），只保留給檔名對得上的那一關，
    # 其他關不顯示，避免出現跟內容無關的圖卡
    usage = {}
    for q in QUESTS.values():
        usage.setdefault(q.get("card_image", ""), []).append(q["level"])
    quests = {}
    for k, q in QUESTS.items():
        q = dict(q)
        img = q.get("card_image", "")
        if len(usage.get(img, [])) > 1 and f"quest{q['level']}_" not in img:
            img = ""
        q["card_image"] = copy_asset(img, "cards")
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
        "hobi": HOBI_COURSE,
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
        "site": {"goals": WEB_GOALS, "plans": WEB_PLANS, "settings": WEB_SETTINGS},
    }
    problems = validate(data)
    if problems:
        raise SystemExit("資料檢查失敗，沒有寫出 data.js：\n  - " + "\n  - ".join(problems))
    out = DOCS / "data.js"
    out.write_text("window.JP_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
