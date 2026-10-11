# -*- coding: utf-8 -*-
"""
日本超商、藥妝店、超市實戰掃雷辭典 (Drugstore & Supermarket Scanner)
包含美妝保養、常備藥品標示、食品包裝暗號、日中對照與發音指引！
"""

SCAN_CATEGORIES = {
    "drugstore": {
        "title": "💊 日本藥妝店必懂標示辭典 (Drugstore)",
        "desc": "松本清、大國藥妝、Sundrug 採購時包裝上的關鍵詞彙全解！",
        "items": [
            {"jp": "食前服用", "furigana": "しょくぜんふくよう", "romaji": "shokuzen fukuyou", "meaning": "飯前半小時服用", "tip": "胃藥、漢方藥常見，空腹時吸收最佳。"},
            {"jp": "食後服用", "furigana": "しょくごふくよう", "romaji": "shokugo fukuyou", "meaning": "飯後半小時內服用", "tip": "一般感冒藥、止痛藥常見，減低對胃部的刺激。"},
            {"jp": "かゆみ・湿疹", "furigana": "かゆみ・しっしん", "romaji": "kayumi / shisshin", "meaning": "止癢・濕疹", "tip": "蚊蟲叮咬軟膏、皮膚炎藥膏必見標示。"},
            {"jp": "のどの痛み", "furigana": "のどのいたみ", "romaji": "nodo no itami", "meaning": "喉嚨痛", "tip": "感冒藥、噴劑（如龍角散、大正百保能）常見。"},
            {"jp": "鼻水・鼻づまり", "furigana": "はなみず・はなづまり", "romaji": "hanamizu / hanazumari", "meaning": "鼻水・鼻塞", "tip": "花粉症、鼻炎噴霧藥物核心功效。"},
            {"jp": "頭痛・生理痛", "furigana": "ずつう・せいりつう", "romaji": "zutsuu / seiritsuu", "meaning": "頭痛・經痛", "tip": "EVE、BUFFERIN 等止痛藥最醒目的標語。"},
            {"jp": "第2類医薬品", "furigana": "だいにもるいいやくひん", "romaji": "dainirui iyakuhin", "meaning": "第二類醫藥品", "tip": "常見感冒藥或皮膚藥，可在一般藥妝店直接至櫃檯結帳。"},
            {"jp": "目薬 (クール度)", "furigana": "めぐすり (クールど)", "romaji": "megusuri (ku-rudo)", "meaning": "眼藥水 (清涼度)", "tip": "標示 0~8 級，數字越高點起來越冰涼提神！"}
        ]
    },
    "skincare": {
        "title": "💄 美妝護膚關鍵字 (Skincare)",
        "desc": "防曬、面膜、保養品包裝上的核心保養功效！",
        "items": [
            {"jp": "保湿 / しっとり", "furigana": "ほしつ / しっとり", "romaji": "hoshitsu / shittori", "meaning": "保濕 / 滋潤型", "tip": "適合乾性肌膚或冬天使用，質地偏濃稠。"},
            {"jp": "さっぱり", "furigana": "さっぱり", "romaji": "sappari", "meaning": "清爽型 / 不黏膩", "tip": "適合油性肌膚或夏天使用，吸收迅速。"},
            {"jp": "毛穴ケア", "furigana": "けあなケア", "romaji": "keana kea", "meaning": "毛孔緊緻護理", "tip": "泥膜、黑頭粉刺清潔洗面乳必備詞。"},
            {"jp": "美白 / トーンアップ", "furigana": "びはく / トーンアップ", "romaji": "bihaku / to-n appu", "meaning": "美白 / 提亮膚色", "tip": "改善暗沉、淡斑精華與防曬霜常見。"},
            {"jp": "ニキビ予防", "furigana": "ニキビよぼう", "romaji": "nikibi yobou", "meaning": "預防痘痘 / 抗痘", "tip": "油痘肌潔顏慕斯、痘痘貼必認標示。"},
            {"jp": "無香料・弱酸性", "furigana": "むこうりょう・じゃくさんせい", "romaji": "mukouryou / jakusansei", "meaning": "無香精・弱酸性", "tip": "敏感肌安心配方，不刺激溫和親膚。"}
        ]
    },
    "food": {
        "title": "🍱 超商超市食品解密 (Supermarket & Conbini)",
        "desc": "不再買錯！日本超市與超商的保存期限與飲食標示暗號！",
        "items": [
            {"jp": "消費期限", "furigana": "しょうひきげん", "romaji": "shouhi kigen", "meaning": "安全食用期限 (逾期勿吃)", "tip": "生魚片、便當、生乳等短命食品，過了此期限容易腐敗！"},
            {"jp": "賞味期限", "furigana": "しょうみきげん", "romaji": "shoumi kigen", "meaning": "最佳風味期限 (過期通常還能吃)", "tip": "泡麵、餅乾、罐頭等耐放食品，指「在這之前吃最好吃」。"},
            {"jp": "半額 / 2割引", "furigana": "はんがく / にわりびき", "romaji": "hangaku / niwaribiki", "meaning": "半價 (5折) / 打8折", "tip": "超市晚上 7~8 點後的搶便宜貼紙，半額最超值！"},
            {"jp": "無糖 / 微糖", "furigana": "むとう / びとう", "romaji": "mutou / bitou", "meaning": "無糖 (黑咖啡/純茶) / 微糖", "tip": "日本罐裝黑咖啡認準『無糖 / ブラック』。"},
            {"jp": "ノンアルコール", "furigana": "ノンアルコール", "romaji": "non aruko-ru", "meaning": "無酒精飲料 (0.00%)", "tip": "居酒屋或超商的無酒精啤酒風味飲料。"},
            {"jp": "国産 / 地場産", "furigana": "こくさん / じばさん", "romaji": "kokusan / jibasan", "meaning": "日本本國產 / 當地新鮮特產", "tip": "超市買和牛、米、草莓認準『国産』品質極高！"}
        ]
    }
}
