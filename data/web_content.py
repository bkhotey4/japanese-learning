"""網站專用的內容與設定（只給 docs/ 網頁用，bot 不會讀）。

由 tools/export_web_data.py 匯出到 docs/data.js 的 `site` 欄位。
連結一律寫成網站內部路由 `#/...`；說明文字可用 **粗體** 與 [文字](#/路由) 連結。
"""

# 首頁新手引導：依學習目標推薦三步路線
WEB_GOALS = {
    "travel": {
        "icon": "✈️", "name": "日本自由行", "desc": "點餐、購物、問路、退稅",
        "steps": [
            {"href": "#/quest/1", "title": "⚔️ 第 1 關：これ、ください", "desc": "最萬用的點餐神句"},
            {"href": "#/talk/ramen", "title": "🍜 拉麵店角色扮演", "desc": "實際走一遍點餐流程"},
            {"href": "#/travel/sos", "title": "🚨 SOS 手指卡", "desc": "出發前一定要存"},
        ],
    },
    "anime": {
        "icon": "🎌", "name": "看懂動漫日劇", "desc": "聽懂台詞、不靠字幕",
        "steps": [
            {"href": "#/anime", "title": "🎌 動漫名台詞教室", "desc": "鬼滅、咒術、柯南…"},
            {"href": "#/kana/game", "title": "🎮 五十音消除遊戲", "desc": "先把假名練成反射"},
            {"href": "#/talk/anime", "title": "💬 動漫常用口語", "desc": "すごい、やばい、まじで"},
        ],
    },
    "life": {
        "icon": "🏠", "name": "日本生活", "desc": "超商、看醫生、租屋",
        "steps": [
            {"href": "#/talk/daily", "title": "🏠 日常生活會話", "desc": "每天都用得到"},
            {"href": "#/talk/convenience", "title": "🏪 超商結帳角色扮演", "desc": "要加熱嗎？要袋子嗎？"},
            {"href": "#/travel/culture", "title": "🛡️ 文化避坑指南", "desc": "居酒屋、電車、溫泉禮儀"},
        ],
    },
    "work": {
        "icon": "💼", "name": "職場工作", "desc": "敬語、商務應對",
        "steps": [
            {"href": "#/talk/work", "title": "💼 職場敬語入門", "desc": "かしこまりました"},
            {"href": "#/grammar", "title": "🧩 動詞變化", "desc": "て形口訣歌一次搞懂"},
            {"href": "#/news", "title": "📰 NHK 簡易新聞", "desc": "練商務閱讀"},
        ],
    },
}

# 學習計畫頁（#/plan/<id>）。blocks 是一格一格的方塊；stages 會畫成由上而下的路線圖
WEB_PLANS = {
    "intro": "上班族專屬：能長久堅持，遠比一次讀很久更重要。",
    "tabs": [
        {
            "id": "weekday", "label": "☕ 平日 15 分",
            "title": "☕ 平日通勤：每日 15 分鐘微學習",
            "intro": "目標不是苦讀，而是**維持語感不中斷**。",
            "blocks": [
                {"title": "☀️ 前 5 分鐘【熱身刷卡】", "body": "首頁看 [今日一句](#/)，或用 [五十音](#/kana) 複習一行發音。"},
                {"title": "🧠 中 7 分鐘【微量吸收】", "body": "挑戰 1 個 [主線關卡](#/quest)，或在 [文法](#/grammar) 速查 1 個動詞變化。"},
                {"title": "🗣️ 後 3 分鐘【開口跟讀】", "body": "大聲跟讀 3 次，完成隨堂測驗就打卡收工！"},
            ],
            "tip": "💡 今天太累也沒關係，哪怕只做 1 題 [測驗](#/quiz)，累積天數就會 +1。",
        },
        {
            "id": "weekend", "label": "🏖️ 假日沉浸",
            "title": "🏖️ 週末：30～45 分鐘沉浸實戰",
            "intro": "任選 2～3 個 15 分鐘模組自由搭配：",
            "blocks": [
                {"title": "🎬 模組 1【動漫時事精聽】", "body": "[動漫名台詞](#/anime)、[NHK 簡易新聞](#/news)、[童謡跟唱](#/songs)"},
                {"title": "🍜 模組 2【情境模擬與美食解碼】", "body": "[角色扮演](#/talk)、[燒肉壽司菜單](#/travel/menu)、[文化避坑](#/travel/culture)"},
                {"title": "🗣️ 模組 3【影子跟讀與錯題清倉】", "body": "[影子跟讀](#/speak)、[錯題本](#/review)"},
            ],
            "tip": "🎖️ 週六日學習即可解鎖「🏖️ 週末充電王」成就！",
        },
        {
            "id": "roadmap", "label": "🗺️ 路線圖",
            "title": "🗺️ 全階段日語路線圖",
            "intro": "",
            "stages": [
                {"title": "階段 0：發音與五十音", "time": "2～4 週", "goal": "假名直覺反射"},
                {"title": "階段 1：旅遊生存與基礎會話", "time": "JLPT N5｜2～3 個月", "goal": "自由行通關 ✈️"},
                {"title": "階段 2：生活溝通與休閒娛樂", "time": "JLPT N4～N3｜4～6 個月", "goal": "獨立生活 🏠 + 娛樂沉浸 🎮"},
                {"title": "階段 3：職場入門與流暢交流", "time": "JLPT N2｜6～9 個月", "goal": "日商求職、商務書信 💼"},
                {"title": "階段 4：專業商務與深度融入", "time": "JLPT N1 / BJT", "goal": "深度談判與商務協作"},
            ],
            "tip": "**🎯 四大核心場景**\n✈️ 旅遊：點餐、問路、交通、退稅\n🏠 生活：超商、租屋、看診\n🎮 休閒：動漫、日劇、日本社群\n💼 工作：日商應對、商業 Email、敬語",
        },
    ],
}

# 網站規則的數字（改這裡就好，不用改 app.js）
WEB_SETTINGS = {
    # 連續學習 N 天解鎖的成就
    "streak_badges": {"badge_streak_3": 3, "badge_streak_7": 7},
    # 「旅遊通關王」需要通過的關卡數（第 1 季）
    "quest_master_levels": 10,
    # 單字卡（間隔重複）
    "srs_new_per_day": 10,
    "srs_new_per_day_choices": [5, 10, 15, 20, 30],
    "srs_default_decks": ["kana", "quest", "phrase"],
    "srs_mature_days": 21,
}
