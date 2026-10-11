# -*- coding: utf-8 -*-
"""
片假名外來語解碼字典與測驗題庫 (Katakana Data)
收錄高頻片假名單字、語源出處（英文/德文/葡文）與生活避坑冷知識。
"""

KATAKANA_WORDS = [
    {
        "word": "コーヒー",
        "romaji": "kōhī",
        "origin": "Coffee (荷蘭語/英語)",
        "meaning": "咖啡",
        "category": "飲食",
        "note": "日本喫茶店必備！熱咖啡通常稱『ホット』，冰咖啡稱『アイス』。"
    },
    {
        "word": "ビール",
        "romaji": "bīru",
        "origin": "Bier (荷蘭語)",
        "meaning": "啤酒",
        "category": "飲食",
        "note": "注意長音！若念成『ビル (biru)』會變成大樓。"
    },
    {
        "word": "パン",
        "romaji": "pan",
        "origin": "Pão (葡萄牙語)",
        "meaning": "麵包",
        "category": "飲食",
        "note": "源自16世紀葡萄牙傳教士傳入日本，不是源自英文 Bread！"
    },
    {
        "word": "アルバイト",
        "romaji": "arubaito",
        "origin": "Arbeit (德語：工作)",
        "meaning": "打工兼職 (簡稱バイト Baito)",
        "category": "職場",
        "note": "原本在德語是『工作/勞動』，日語中特指學生或副業打工。"
    },
    {
        "word": "ホテル",
        "romaji": "hoteru",
        "origin": "Hotel (英語)",
        "meaning": "飯店 / 旅館",
        "category": "旅遊",
        "note": "『ビジネスホテル』即商務旅館，自由行CP值首選。"
    },
    {
        "word": "コンビニ",
        "romaji": "kombini",
        "origin": "Convenience Store (英語簡稱)",
        "meaning": "便利超商 (如 7-11, Lawson, FamilyMart)",
        "category": "生活",
        "note": "日式和製英語精髓，將 Convenience 縮減為コンビニ。"
    },
    {
        "word": "スマホ",
        "romaji": "sumaho",
        "origin": "Smart Phone (英語簡稱)",
        "meaning": "智慧型手機",
        "category": "科技",
        "note": "Smartphone 的前綴 Smart (スマ) + Phone (ホ)。"
    },
    {
        "word": "エアコン",
        "romaji": "eakon",
        "origin": "Air Conditioner (英語簡稱)",
        "meaning": "冷暖氣空調",
        "category": "生活",
        "note": "飯店遙控器上：『冷房 (Reibō)』是冷氣，『暖房 (Danbō)』是暖氣。"
    },
    {
        "word": "パスポート",
        "romaji": "pasupōto",
        "origin": "Passport (英語)",
        "meaning": "護照",
        "category": "旅遊",
        "note": "在日本免稅購物時，店員常說『パスポートを見せてください』。"
    },
    {
        "word": "コンセント",
        "romaji": "konsento",
        "origin": "Concentric Plug (和製英語)",
        "meaning": "室內電源插座 (⚠️不是同意/同意書！)",
        "category": "生活",
        "note": "常見誤區！英文的 Consent 是同意，但在日本コンセント指牆壁上的電源插座。"
    },
    {
        "word": "テンション",
        "romaji": "tenshon",
        "origin": "Tension (和製英語)",
        "meaning": "情緒亢奮度 / High 度 (⚠️不是緊張緊張壓力！)",
        "category": "日常",
        "note": "『テンションが高い』表示心情非常亢奮嗨翻天，並非壓力很大！"
    },
    {
        "word": "フライドポテト",
        "romaji": "furaido poteto",
        "origin": "Fried Potato (和製英語)",
        "meaning": "炸薯條 (美式英文為 French Fries)",
        "category": "飲食",
        "note": "麥當勞點薯條請說『ポテト (poteto)』，不要說 French Fries！"
    },
    {
        "word": "マンション",
        "romaji": "manshon",
        "origin": "Mansion (和製英語)",
        "meaning": "集合式高級公寓 (⚠️不是獨棟豪宅！)",
        "category": "生活",
        "note": "英文 Mansion 是億萬豪宅莊園，日文中指一般鋼筋混凝土的集合式公寓。"
    },
    {
        "word": "サービス",
        "romaji": "sābisu",
        "origin": "Service (英語)",
        "meaning": "招待 / 免費贈送 (或服務)",
        "category": "飲食/商業",
        "note": "老闆說『これサービスね！』意思是『這個免費請你吃！』"
    },
    {
        "word": "チェックアウト",
        "romaji": "chekkuauto",
        "origin": "Check-out (英語)",
        "meaning": "退房",
        "category": "旅遊",
        "note": "飯店早上退房常用句：『チェックアウトをお願いします』。"
    }
]

KATAKANA_QUIZZES = [
    {
        "question": "在日本飯店問店員「コンセントはどこですか？」，請問你在找什麼？",
        "options": ["電源插座", "同意書", "同心圓尺", "轉換器"],
        "answer": "電源插座",
        "explanation": "コンセント 源自 Concentric plug，在日語中指『壁插/電源插座』，是極具代表性的和製英語！"
    },
    {
        "question": "日語中的「パン (pan)」是麵包的意思，請問它的語源來自哪個語言？",
        "options": ["葡萄牙語 (Pão)", "法語 (Pain)", "英語 (Pan)", "西班牙語 (Pan)"],
        "answer": "葡萄牙語 (Pão)",
        "explanation": "16世紀葡萄牙船隻將天主教與麵包（Pão）傳入日本九州，因此演變為片假名「パン」。"
    },
    {
        "question": "日本人說某人「今日テンション高いね！」，意思是？",
        "options": ["今天情緒超嗨超有活力！", "今天精神壓力極大", "今天肌肉很緊繃", "今天血壓很高"],
        "answer": "今天情緒超嗨超有活力！",
        "explanation": "日文的 テンション (Tension) 轉化為『興奮度、情緒精神狀態』，テンションが高い 就是指情緒極佳、嗨翻天！"
    },
    {
        "question": "在麥當勞點炸薯條時，日文最道地的說法是？",
        "options": ["ポテト (フライドポテト)", "フレンチフライ", "チップス", "イモ"],
        "answer": "ポテト (フライドポテト)",
        "explanation": "日本速食店將炸薯條稱為 フライドポテト (Fried Potato) 或簡稱 ポテト (Potato)。"
    },
    {
        "question": "日語大學生常說的打工「アルバイト (Arbeit)」源自哪個國家的語言？",
        "options": ["德語 (Arbeit：勞動/工作)", "英語", "俄語", "義大利語"],
        "answer": "德語 (Arbeit：勞動/工作)",
        "explanation": "明治時期日本醫學界與學界大量採用德語，將德語中的勞動 Arbeit 轉為指學生的課餘打工。"
    },
    {
        "question": "老闆結帳時笑著對你說「これはサービスです！」，意思是？",
        "options": ["這個是免費招待你的！", "要收你服務費喔！", "需要售後服務嗎？", "請填寫滿意度調查"],
        "answer": "這個是免費招待你的！",
        "explanation": "在居酒屋或餐飲店，『サービス (Service)』常代表店家額外贈送的免費小菜或點心，不用付錢！"
    }
]
