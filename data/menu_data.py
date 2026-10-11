# -*- coding: utf-8 -*-
"""
日本燒肉部位、壽司魚種與餐廳客製點餐暗號字典 (Menu Data)
專為赴日美食饕客設計，秒懂菜單日文，點餐不再踩雷！
"""

MENU_CATEGORIES = {
    "yakiniku": {
        "title": "🥩 日本燒肉部位大解密",
        "description": "走進敘敘苑或炭火燒肉店，看懂菜單各部位油花與口感：",
        "items": [
            {
                "japanese": "カルビ (Karubi)",
                "furigana": "カルビ",
                "meaning": "牛五花 / 牛胸腹肉",
                "detail": "油花最豐郁多汁的經典部位！上カルビ代表特級牛五花。"
            },
            {
                "japanese": "ロース (Rōsu)",
                "furigana": "ロース",
                "meaning": "牛里肌肉 / 肩胛肉",
                "detail": "油脂適中、肉質細膩柔嫩，怕太油膩老饕的首選。"
            },
            {
                "japanese": "ハラミ (Harami)",
                "furigana": "ハラミ",
                "meaning": "牛橫膈膜肉 (外橫膈膜)",
                "detail": "日本燒肉人氣 No.1！口感像精瘦紅肉，但極為軟嫩濃郁，熱量比五花低。"
            },
            {
                "japanese": "サガリ (Sagari)",
                "furigana": "サガリ",
                "meaning": "牛內橫膈膜",
                "detail": "比ハラミ油脂更少，肉味極濃，肉質厚實彈牙。"
            },
            {
                "japanese": "タン (Tan)",
                "furigana": "タン",
                "meaning": "牛舌",
                "detail": "開場必點！『ネギ塩タン（蔥鹽牛舌）』烤至微脆搭配檸檬汁絕配。"
            },
            {
                "japanese": "ホルモン (Horumon)",
                "furigana": "ホルモン",
                "meaning": "牛大腸 / 內臟總稱",
                "detail": "關西話『捨てるもの（原本要丟棄的東西）』演變而來，富含油脂膠質與嚼勁。"
            },
            {
                "japanese": "ミノ (Mino)",
                "furigana": "ミノ",
                "meaning": "牛第一胃 (牛肚)",
                "detail": "白淨厚實，烤好後口感清脆爽口，下酒必備！"
            }
        ]
    },
    "sushi": {
        "title": "🍣 壽司與海鮮刺身魚種速查",
        "description": "旋轉壽司或板前壽司台必備魚種名稱：",
        "items": [
            {
                "japanese": "まぐろ (Maguro)",
                "furigana": "まぐろ",
                "meaning": "鮪魚 (赤身瘦肉部分)",
                "detail": "清爽微酸，正統江戶前壽司的靈魂主役。"
            },
            {
                "japanese": "中トロ (Chū-toro)",
                "furigana": "ちゅうトロ",
                "meaning": "中腹鮪魚 (油脂與肉質完美平衡)",
                "detail": "比赤身多油脂、比大腹少膩感，CP值最高的入口即化部位。"
            },
            {
                "japanese": "大トロ (Ō-toro)",
                "furigana": "おおトロ",
                "meaning": "大腹鮪魚 (頂級滿滿油脂)",
                "detail": "粉紅雪花紋路，放入口中直接融化的高級珍味。"
            },
            {
                "japanese": "サーモン (Sāmon)",
                "furigana": "サーモン",
                "meaning": "鮭魚 / 三文魚",
                "detail": "炙燒鮭魚稱為『炙りサーモン (Aburi sāmon)』。"
            },
            {
                "japanese": "いくら (Ikura)",
                "furigana": "いくら",
                "meaning": "鮭魚卵 (軍艦壽司)",
                "detail": "源自俄語 ikra（魚卵）。一口咬下在嘴裡爆漿的鮮味。"
            },
            {
                "japanese": "うに (Uni)",
                "furigana": "うに",
                "meaning": "海膽",
                "detail": "北海道產最為極品，濃郁鮮甜無腥味。"
            },
            {
                "japanese": "えび (Ebi)",
                "furigana": "えび",
                "meaning": "鮮蝦 (熟蝦)",
                "detail": "生甜蝦則寫作『甘エビ (Ama-ebi)』。"
            }
        ]
    },
    "custom_order": {
        "title": "🍜 日本餐廳行家點餐客製暗號",
        "description": "松屋、吉野家、一蘭拉麵老饕專用術語：",
        "items": [
            {
                "japanese": "つゆだく (Tsuyudaku)",
                "furigana": "つゆだく",
                "meaning": "牛肉飯醬汁加多 (多汁)",
                "detail": "吉野家傳世密語！喜歡白飯被甘甜牛肉湯汁浸潤的老饕必加！"
            },
            {
                "japanese": "ネギ抜き (Neginuki)",
                "furigana": "ネギぬき",
                "meaning": "去蔥 (不要加蔥花)",
                "detail": "不喜歡生蔥味時，結帳點餐時說『ネギ抜きでお願いします』。"
            },
            {
                "japanese": "大盛り (Ōmori)",
                "furigana": "おおもり",
                "meaning": "大碗 / 加大份量",
                "detail": "普通份量是『並盛り (Namimori)』，特大碗是『特盛り (Tokumori)』。"
            },
            {
                "japanese": "お冷 (Ohya)",
                "furigana": "おひや",
                "meaning": "冰開水 (免費提供)",
                "detail": "想要喝冰水時請說：『お冷をください (Ohiya o kudasai)』。"
            },
            {
                "japanese": "お会計 (Okaikei)",
                "furigana": "おかいけい",
                "meaning": "結帳買單",
                "detail": "在桌邊結帳或走到櫃台時說：『お会計をお願いします』。"
            }
        ]
    }
}
