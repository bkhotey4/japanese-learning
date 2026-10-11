# -*- coding: utf-8 -*-
"""
用戶學習進度與成就管理模組 (Progress Manager)
使用 JSON 檔案持久化記錄：
1. 主線闖關關卡 (Level 1~20 雙季全開)
2. 每日連續打卡記錄 (Streak & Last Active Date)
3. 智慧錯題本 (Mistakes Notebook)
4. 成就勳章系統 (Badges Showcase)
5. 個人化推播時間與開關 (Schedule Preferences)
6. 伺服器學習天梯排行榜 (Leaderboard)
"""

import os
import json
import datetime

PROGRESS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "user_progress.json")

# 成就徽章定義庫
BADGES_INFO = {
    "first_step": {
        "name": "🐣 假名初探",
        "desc": "完成首次日語學習互動或五十音速查"
    },
    "badge_quiz": {
        "name": "🎯 隨堂考勇者",
        "desc": "完成隨機隨堂測驗並獲得答題記錄"
    },
    "badge_review": {
        "name": "🔄 溫故知新",
        "desc": "成功在錯題本中複習並斬除錯題"
    },
    "master_ramen": {
        "name": "🍜 拉麵達人",
        "desc": "成功完成拉麵店點餐實戰角色扮演"
    },
    "master_hotel": {
        "name": "🏨 暢行無阻",
        "desc": "順利完成飯店退房/入住角色扮演"
    },
    "master_convenience": {
        "name": "🏪 超商生存家",
        "desc": "聽懂便當加熱與塑膠袋詢問並完成超商結帳"
    },
    "master_izakaya": {
        "name": "🏮 乾杯酒豪",
        "desc": "掌握居酒屋點酒、烤雞串與お通し文化"
    },
    "badge_culture": {
        "name": "🛡️ 避坑大師",
        "desc": "閱讀日本文化與旅遊避坑指南"
    },
    "badge_sos": {
        "name": "🚨 急難避險王",
        "desc": "查閱日本緊急生存就醫手指卡"
    },
    "badge_menu": {
        "name": "🥩 美食老饕",
        "desc": "解鎖日本燒肉部位與餐廳客製點餐暗號"
    },
    "badge_grammar": {
        "name": "🧩 文法小神童",
        "desc": "掌握動詞變化公式與て形口訣歌"
    },
    "badge_news": {
        "name": "📰 通勤時事通",
        "desc": "閱讀 NHK 簡易日語短篇新聞"
    },
    "badge_shadowing": {
        "name": "🗣️ 口說挑戰者",
        "desc": "完成實戰跟讀挑戰與發音練習"
    },
    "badge_streak_3": {
        "name": "🔥 三日堅持",
        "desc": "連續打卡學習達到 3 天"
    },
    "badge_streak_7": {
        "name": "👑 七日不輟",
        "desc": "連續打卡學習達到 7 天"
    },
    "badge_quest_master": {
        "name": "🏆 旅遊通關王",
        "desc": "全破第 1 季 (1~10關) 日本自由行生存關卡"
    },
    "badge_quest_20": {
        "name": "🎓 日語大圓滿",
        "desc": "達成全 20 關終極通關！融入道地日本生活"
    },
    "badge_weekend": {
        "name": "🏖️ 週末充電王",
        "desc": "在週末假期完成日語學習打卡"
    }
}

def load_progress() -> dict:
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_progress(data: dict):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_progress(user_id: int) -> dict:
    data = load_progress()
    uid = str(user_id)
    if uid not in data:
        data[uid] = {
            "current_level": 1,
            "completed_levels": [],
            "streak": 1,
            "last_active_date": str(datetime.date.today()),
            "mistakes": [],
            "badges": ["first_step"],
            "schedule_time": "21:00",
            "schedule_weekend_time": "10:30",
            "schedule_enabled": True,
            "schedule_mode": "both",
            "kana_day": 1
        }
        save_progress(data)
    else:
        updated = False
        if "streak" not in data[uid]:
            data[uid]["streak"] = 1
            updated = True
        if "last_active_date" not in data[uid]:
            data[uid]["last_active_date"] = str(datetime.date.today())
            updated = True
        if "mistakes" not in data[uid]:
            data[uid]["mistakes"] = []
            updated = True
        if "badges" not in data[uid]:
            data[uid]["badges"] = ["first_step"]
            updated = True
        if "schedule_time" not in data[uid]:
            data[uid]["schedule_time"] = "21:00"
            updated = True
        if "schedule_weekend_time" not in data[uid]:
            data[uid]["schedule_weekend_time"] = "10:30"
            updated = True
        if "schedule_enabled" not in data[uid]:
            data[uid]["schedule_enabled"] = True
            updated = True
        if "schedule_mode" not in data[uid]:
            data[uid]["schedule_mode"] = "both"
            updated = True
        if "kana_day" not in data[uid]:
            data[uid]["kana_day"] = 1
            updated = True
        if updated:
            save_progress(data)
    return data[uid]

def record_daily_activity(user_id: int) -> tuple[int, bool]:
    data = load_progress()
    uid = str(user_id)
    user_info = get_user_progress(user_id)
    today = datetime.date.today()
    last_date_str = user_info.get("last_active_date")
    
    is_first_today = False
    if last_date_str:
        try:
            last_date = datetime.datetime.strptime(last_date_str, "%Y-%m-%d").date()
        except Exception:
            last_date = today
        diff = (today - last_date).days
        if diff == 0:
            is_first_today = False
        else:
            # 不論間隔幾天沒看，累積次數永遠只增不減，絕不清零！
            user_info["streak"] = user_info.get("streak", 1) + 1
            user_info["last_active_date"] = str(today)
            is_first_today = True
    else:
        user_info["streak"] = 1
        user_info["last_active_date"] = str(today)
        is_first_today = True

    current_streak = user_info.get("streak", 1)
    if current_streak >= 3 and "badge_streak_3" not in user_info.get("badges", []):
        user_info["badges"].append("badge_streak_3")
    if current_streak >= 7 and "badge_streak_7" not in user_info.get("badges", []):
        user_info["badges"].append("badge_streak_7")

    # 週末學習打卡專屬勳章 (週六=5, 週日=6)
    if today.weekday() >= 5 and "badge_weekend" not in user_info.get("badges", []):
        user_info["badges"].append("badge_weekend")

    data[uid] = user_info
    save_progress(data)
    return current_streak, is_first_today

def advance_user_level(user_id: int, finished_level: int) -> tuple[int, bool]:
    data = load_progress()
    uid = str(user_id)
    user_info = get_user_progress(user_id)
    
    is_new_level = False
    completed = user_info.get("completed_levels", [])
    if finished_level not in completed:
        completed.append(finished_level)
        user_info["completed_levels"] = completed
    
    if user_info.get("current_level", 1) == finished_level and finished_level < 20:
        user_info["current_level"] = finished_level + 1
        is_new_level = True
    
    # 檢查第 1 季通關 (10 關)
    if len(user_info.get("completed_levels", [])) >= 10:
        if "badge_quest_master" not in user_info.get("badges", []):
            user_info["badges"].append("badge_quest_master")

    # 檢查第 2 季大圓滿通關 (20 關)
    if len(user_info.get("completed_levels", [])) >= 20:
        if "badge_quest_20" not in user_info.get("badges", []):
            user_info["badges"].append("badge_quest_20")

    data[uid] = user_info
    save_progress(data)
    return user_info["current_level"], is_new_level

def unlock_badge(user_id: int, badge_id: str) -> bool:
    data = load_progress()
    uid = str(user_id)
    user_info = get_user_progress(user_id)
    badges = user_info.get("badges", [])
    if badge_id not in badges and badge_id in BADGES_INFO:
        badges.append(badge_id)
        user_info["badges"] = badges
        data[uid] = user_info
        save_progress(data)
        return True
    return False

def add_mistake(user_id: int, question: str, answer: str, explanation: str, options: list):
    data = load_progress()
    uid = str(user_id)
    user_info = get_user_progress(user_id)
    mistakes = user_info.get("mistakes", [])
    
    for m in mistakes:
        if m.get("question") == question:
            return
            
    mistakes.append({
        "question": question,
        "answer": answer,
        "explanation": explanation,
        "options": options,
        "date": str(datetime.date.today())
    })
    user_info["mistakes"] = mistakes
    data[uid] = user_info
    save_progress(data)

def get_mistakes(user_id: int) -> list:
    user_info = get_user_progress(user_id)
    return user_info.get("mistakes", [])

def remove_mistake(user_id: int, question: str) -> bool:
    data = load_progress()
    uid = str(user_id)
    user_info = get_user_progress(user_id)
    mistakes = user_info.get("mistakes", [])
    new_mistakes = [m for m in mistakes if m.get("question") != question]
    if len(new_mistakes) != len(mistakes):
        user_info["mistakes"] = new_mistakes
        data[uid] = user_info
        save_progress(data)
        unlock_badge(user_id, "badge_review")
        return True
    return False

def set_user_schedule(user_id: int, time_str: str, is_weekend: bool = False) -> bool:
    """設定使用者的平日或假日推播時間（格式 HH:MM）"""
    data = load_progress()
    uid = str(user_id)
    user_info = get_user_progress(user_id)
    if is_weekend:
        user_info["schedule_weekend_time"] = time_str
    else:
        user_info["schedule_time"] = time_str
    user_info["schedule_enabled"] = True
    data[uid] = user_info
    save_progress(data)
    return True

def set_user_schedule_mode(user_id: int, mode: str) -> str:
    """設定推播內容模式：'quest' (主線闖關), 'kana' (五十音每日循環), 'both' (兩者皆要)"""
    data = load_progress()
    uid = str(user_id)
    user_info = get_user_progress(user_id)
    valid_modes = ["quest", "kana", "both"]
    if mode in valid_modes:
        user_info["schedule_mode"] = mode
        data[uid] = user_info
        save_progress(data)
    return user_info.get("schedule_mode", "both")

def advance_kana_day(user_id: int) -> int:
    """將使用者的五十音循環推進到下一天（1~10天循環）"""
    data = load_progress()
    uid = str(user_id)
    user_info = get_user_progress(user_id)
    current = user_info.get("kana_day", 1)
    next_day = 1 if current >= 10 else current + 1
    user_info["kana_day"] = next_day
    data[uid] = user_info
    save_progress(data)
    return next_day

def toggle_user_schedule(user_id: int) -> bool:
    """切換使用者的推播開關，回傳切換後的新狀態"""
    data = load_progress()
    uid = str(user_id)
    user_info = get_user_progress(user_id)
    current_state = user_info.get("schedule_enabled", True)
    new_state = not current_state
    user_info["schedule_enabled"] = new_state
    data[uid] = user_info
    save_progress(data)
    return new_state

def get_leaderboard(limit: int = 10) -> list:
    """取得所有使用者的天梯排行榜資料（依連續天數與通關關卡排序）"""
    data = load_progress()
    leaderboard = []
    for uid, info in data.items():
        leaderboard.append({
            "user_id": uid,
            "streak": info.get("streak", 1),
            "current_level": info.get("current_level", 1),
            "completed_levels": info.get("completed_levels", []),
            "badges": info.get("badges", [])
        })
    # 優先依 streak 排序，次依 completed_levels 數量與徽章數排序
    leaderboard.sort(key=lambda x: (x["streak"], len(x["completed_levels"]), len(x["badges"])), reverse=True)
    return leaderboard[:limit]

def reset_user_progress(user_id: int):
    data = load_progress()
    uid = str(user_id)
    data[uid] = {
        "current_level": 1,
        "completed_levels": [],
        "streak": 1,
        "last_active_date": str(datetime.date.today()),
        "mistakes": [],
        "badges": ["first_step"],
        "schedule_time": "21:00",
        "schedule_weekend_time": "10:30",
        "schedule_enabled": True
    }
    save_progress(data)
