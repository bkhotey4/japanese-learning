# -*- coding: utf-8 -*-
"""
五十音數據與資料庫
包含清音、濁音、半濁音與常用說明
"""

KANA_ROWS = {
    "a": {
        "name": "あ行 (a, i, u, e, o)",
        "items": [
            {"hira": "あ", "kata": "ア", "romaji": "a", "tip": "像中文的『阿』，口型自然張開。"},
            {"hira": "い", "kata": "イ", "romaji": "i", "tip": "嘴唇向左右微拉，像發『一』。"},
            {"hira": "う", "kata": "ウ", "romaji": "u", "tip": "注意！嘴唇不要突出（不要發成中文的『屋』），微閉放鬆發音。"},
            {"hira": "え", "kata": "エ", "romaji": "e", "tip": "嘴巴微張，介於『ㄝ』與『ㄟ』之間。"},
            {"hira": "お", "kata": "オ", "romaji": "o", "tip": "嘴唇成圓形，發出圓潤的『喔』。"}
        ]
    },
    "ka": {
        "name": "か行 (ka, ki, ku, ke, ko)",
        "items": [
            {"hira": "か", "kata": "カ", "romaji": "ka", "tip": "清脆的『卡』。"},
            {"hira": "き", "kata": "キ", "romaji": "ki", "tip": "像『key』的發音。"},
            {"hira": "く", "kata": "ク", "romaji": "ku", "tip": "『哭』但嘴巴不要嘟起。"},
            {"hira": "け", "kata": "ケ", "romaji": "ke", "tip": "『開』的短促版。"},
            {"hira": "こ", "kata": "コ", "romaji": "ko", "tip": "『扣』。"}
        ]
    },
    "sa": {
        "name": "さ行 (sa, shi, su, se, so)",
        "items": [
            {"hira": "さ", "kata": "サ", "romaji": "sa", "tip": "『薩』。"},
            {"hira": "し", "kata": "シ", "romaji": "shi", "tip": "注意！不是 si，是輕柔的『吸 / 西』。"},
            {"hira": "す", "kata": "ス", "romaji": "su", "tip": "牙齒輕閉發『絲』。"},
            {"hira": "せ", "kata": "セ", "romaji": "se", "tip": "『塞』。"},
            {"hira": "そ", "kata": "ソ", "romaji": "so", "tip": "『搜』。"}
        ]
    },
    "ta": {
        "name": "た行 (ta, chi, tsu, te, to)",
        "items": [
            {"hira": "た", "kata": "タ", "romaji": "ta", "tip": "『踏』。"},
            {"hira": "ち", "kata": "チ", "romaji": "chi", "tip": "注意！不是 ti，是『七』。"},
            {"hira": "つ", "kata": "ツ", "romaji": "tsu", "tip": "注意！舌尖抵齒後吐氣發『疵 / 次』。"},
            {"hira": "て", "kata": "テ", "romaji": "te", "tip": "『太』。"},
            {"hira": "と", "kata": "ト", "romaji": "to", "tip": "『拖』。"}
        ]
    },
    "na": {
        "name": "な行 (na, ni, nu, ne, no)",
        "items": [
            {"hira": "な", "kata": "ナ", "romaji": "na", "tip": "『那』。"},
            {"hira": "に", "kata": "ニ", "romaji": "ni", "tip": "『你』。"},
            {"hira": "ぬ", "kata": "ヌ", "romaji": "nu", "tip": "『奴』。"},
            {"hira": "ね", "kata": "ネ", "romaji": "ne", "tip": "『捏』。"},
            {"hira": "の", "kata": "ノ", "romaji": "no", "tip": "『諾 / 弄』。"}
        ]
    },
    "ha": {
        "name": "は行 (ha, hi, fu, he, ho)",
        "items": [
            {"hira": "は", "kata": "ハ", "romaji": "ha", "tip": "『哈』。作為主題助詞時唸作 wa。"},
            {"hira": "ひ", "kata": "ヒ", "romaji": "hi", "tip": "『西』與『希』之間。"},
            {"hira": "ふ", "kata": "フ", "romaji": "fu", "tip": "注意！上下唇靠近不咬唇吹氣（微弱的呼/副）。"},
            {"hira": "へ", "kata": "ヘ", "romaji": "he", "tip": "『黑』。作為方向助詞時唸作 e。"},
            {"hira": "ほ", "kata": "ホ", "romaji": "ho", "tip": "『後』。"}
        ]
    },
    "ma": {
        "name": "ま行 (ma, mi, mu, me, mo)",
        "items": [
            {"hira": "ま", "kata": "マ", "romaji": "ma", "tip": "『媽』。"},
            {"hira": "み", "kata": "ミ", "romaji": "mi", "tip": "『咪』。"},
            {"hira": "む", "kata": "ム", "romaji": "mu", "tip": "『母』。"},
            {"hira": "め", "kata": "メ", "romaji": "me", "tip": "『妹』。"},
            {"hira": "も", "kata": "モ", "romaji": "mo", "tip": "『摸』。"}
        ]
    },
    "ya": {
        "name": "や行 (ya, yu, yo)",
        "items": [
            {"hira": "や", "kata": "ヤ", "romaji": "ya", "tip": "『呀』。"},
            {"hira": "ゆ", "kata": "ユ", "romaji": "yu", "tip": "『優』。"},
            {"hira": "よ", "kata": "ヨ", "romaji": "yo", "tip": "『唷』。"}
        ]
    },
    "ra": {
        "name": "ら行 (ra, ri, ru, re, ro)",
        "items": [
            {"hira": "ら", "kata": "ラ", "romaji": "ra", "tip": "非捲舌音！舌尖輕彈上顎發 la/da。"},
            {"hira": "り", "kata": "リ", "romaji": "ri", "tip": "輕彈舌發 li。"},
            {"hira": "る", "kata": "ル", "romaji": "ru", "tip": "輕彈舌發 lu。"},
            {"hira": "れ", "kata": "レ", "romaji": "re", "tip": "輕彈舌發 le。"},
            {"hira": "ろ", "kata": "ロ", "romaji": "ro", "tip": "輕彈舌發 lo。"}
        ]
    },
    "wa": {
        "name": "わ行與撥音 (wa, wo, n)",
        "items": [
            {"hira": "わ", "kata": "ワ", "romaji": "wa", "tip": "『哇』。"},
            {"hira": "を", "kata": "ヲ", "romaji": "wo (o)", "tip": "僅作為受詞助詞使用，發音同『お』。"},
            {"hira": "ん", "kata": "ン", "romaji": "n", "tip": "鼻音 / 撥音，佔一拍。"}
        ]
    }
}

# 46 個基礎清音卡片流（含字源、圖像記憶口訣、發音嘴型、高頻單字）
ALL_KANA_CARDS = [
    # あ行
    {"index": 0, "row": "あ行", "hira": "あ", "kata": "ア", "romaji": "a",
     "origin": "平假名源自「安」之草書；片假名源自「阿」之左耳偏旁。",
     "mnemonic": "肚子圓圓像個『安』，孕婦摸著肚子說『啊～真安心』！",
     "sound_tip": "嘴巴自然放鬆張大，像看醫生時說『啊～』的輕鬆元音。",
     "vocab": "ありがとう (arigatou)", "vocab_tw": "謝謝"},
    {"index": 1, "row": "あ行", "hira": "い", "kata": "イ", "romaji": "i",
     "origin": "平假名源自「以」之草書；片假名源自「伊」之單人旁。",
     "mnemonic": "兩根直立的吸管（以/伊），發出一（i）的聲音！",
     "sound_tip": "嘴角向左右兩側微拉，發出清晰乾淨的『一』。",
     "vocab": "いいえ (iie)", "vocab_tw": "不是 / 不客氣"},
    {"index": 2, "row": "あ行", "hira": "う", "kata": "ウ", "romaji": "u",
     "origin": "平假名源自「宇」之草書；片假名源自「宇」之寶蓋頭。",
     "mnemonic": "被人在肚子上捶了一拳，整個人痛苦彎腰說『嗚～』！",
     "sound_tip": "特別注意！嘴唇千萬不要向前嘟起，嘴唇放鬆微閉發音。",
     "vocab": "うどん (udon)", "vocab_tw": "烏龍麵"},
    {"index": 3, "row": "あ行", "hira": "え", "kata": "エ", "romaji": "e",
     "origin": "平假名源自「衣」之草書；片假名源自「江」之右半部。",
     "mnemonic": "長得像元寶的小鳥，發出『誒？』的驚訝聲！",
     "sound_tip": "嘴角自然微微張開，介於中文的『ㄝ』與『ㄟ』之間。",
     "vocab": "えき (eki)", "vocab_tw": "車站"},
    {"index": 4, "row": "あ行", "hira": "お", "kata": "オ", "romaji": "o",
     "origin": "平假名源自「於」之草書；片假名源自「於」之左旁偏旁。",
     "mnemonic": "皮帶繫在圓滾滾肚子上，興奮喊出『喔！』！",
     "sound_tip": "雙唇微收呈圓形，發出飽滿圓潤的『喔』。",
     "vocab": "おいしい (oishii)", "vocab_tw": "好吃的 / 美味"},

    # か行
    {"index": 5, "row": "か行", "hira": "か", "kata": "カ", "romaji": "ka",
     "origin": "平假名源自「加」之草書；片假名源自「加」之力旁。",
     "mnemonic": "『力』字加上一點，卡（ka）住拔不出來！",
     "sound_tip": "舌根抵住軟顎後爆破，清脆短促的 ka。",
     "vocab": "かわいい (kawaii)", "vocab_tw": "可愛的"},
    {"index": 6, "row": "か行", "hira": "き", "kata": "キ", "romaji": "ki",
     "origin": "平假名源自「幾」之草書；片假名源自「幾」之上半。",
     "mnemonic": "兩橫一豎帶個圈，長得像一把雙齒鑰匙（Key / き）！",
     "sound_tip": "舌面貼近硬顎發出清脆俐落的 ki。",
     "vocab": "きっぷ (kippu)", "vocab_tw": "車票"},
    {"index": 7, "row": "か行", "hira": "く", "kata": "ク", "romaji": "ku",
     "origin": "平假名源自「久」之草書；片假名源自「久」之初筆。",
     "mnemonic": "小鳥長開尖尖嘴巴『<』，肚子餓哭（ku）著要食物！",
     "sound_tip": "嘴唇放鬆不向前突出，輕發 ku。",
     "vocab": "くち (kuchi)", "vocab_tw": "嘴巴 / 出口"},
    {"index": 8, "row": "か行", "hira": "け", "kata": "ケ", "romaji": "ke",
     "origin": "平假名源自「計」之草書；片假名源自「介」之初筆。",
     "mnemonic": "寶劍佩掛在木架上，等待佩劍的客（ke）人！",
     "sound_tip": "短促有力的 ke，不拖沓帶尾音。",
     "vocab": "けいさつ (keisatsu)", "vocab_tw": "警察"},
    {"index": 9, "row": "か行", "hira": "こ", "kata": "コ", "romaji": "ko",
     "origin": "平假名源自「己」之草書；片假名源自「己」之上半。",
     "mnemonic": "上下兩條平行線，像個開口笑的扣（ko）子！",
     "sound_tip": "圓唇發 ko，聲音落在喉腔前側。",
     "vocab": "こんにちは (konnichiwa)", "vocab_tw": "你好 (白天問候)"},

    # さ行
    {"index": 10, "row": "さ行", "hira": "さ", "kata": "サ", "romaji": "sa",
     "origin": "平假名源自「左」之草書；片假名源自「散」之初筆。",
     "mnemonic": "雙手合十，在寺廟前灑（sa）水祈福洗手！",
     "sound_tip": "舌尖靠近上齒齦發出摩擦音 sa。",
     "vocab": "さくら (sakura)", "vocab_tw": "櫻花"},
    {"index": 11, "row": "さ行", "hira": "し", "kata": "シ", "romaji": "shi",
     "origin": "平假名源自「之」之草書；片假名源自「之」之草書水部。",
     "mnemonic": "長得像吸（shi）管，也像釣魚時彎彎的魚鉤！",
     "sound_tip": "特別注意！不是 si，而是舌面抬起發輕柔的 shi（西/吸）。",
     "vocab": "しんかんせん (shinkansen)", "vocab_tw": "新幹線"},
    {"index": 12, "row": "さ行", "hira": "す", "kata": "ス", "romaji": "su",
     "origin": "平假名源自「寸」之草書；片假名源自「須」之右旁。",
     "mnemonic": "一根繩子打了個圓圈小結，吐氣如絲（su）！",
     "sound_tip": "上下齒輕合留細縫，發出細微的 su（絲）。",
     "vocab": "すし (sushi)", "vocab_tw": "壽司"},
    {"index": 13, "row": "さ行", "hira": "せ", "kata": "セ", "romaji": "se",
     "origin": "平假名源自「世」之草書；片假名源自「世」之初筆。",
     "mnemonic": "世界的『世』少了一筆，發音就是 se（世）！",
     "sound_tip": "嘴角微張，發音清爽俐落。",
     "vocab": "せんせい (sensei)", "vocab_tw": "老師"},
    {"index": 14, "row": "さ行", "hira": "そ", "kata": "ソ", "romaji": "so",
     "origin": "平假名源自「曾」之草書；片假名源自「曾」之頭兩筆。",
     "mnemonic": "連續轉彎的折線，縮（so）在一團！",
     "sound_tip": "圓唇清脆發 so。",
     "vocab": "そば (soba)", "vocab_tw": "蕎麥麵"},

    # た行
    {"index": 15, "row": "た行", "hira": "た", "kata": "タ", "romaji": "ta",
     "origin": "平假名源自「太」之草書；片假名源自「多」之初筆。",
     "mnemonic": "長得像英文字母『ta』的合體，發音正是 ta！",
     "sound_tip": "舌尖抵上齒齦快速彈開，俐落發 ta。",
     "vocab": "たべる (taberu)", "vocab_tw": "吃"},
    {"index": 16, "row": "た行", "hira": "ち", "kata": "チ", "romaji": "chi",
     "origin": "平假名源自「知」之草書；片假名源自「千」。",
     "mnemonic": "長得像數字『5』，發音像中文的『七（chi）』！",
     "sound_tip": "注意！不是 ti，而是像中文『七』的 chi。",
     "vocab": "ちかてつ (chikatetsu)", "vocab_tw": "地下鐵"},
    {"index": 17, "row": "た行", "hira": "つ", "kata": "ツ", "romaji": "tsu",
     "origin": "平假名源自「川」之草書；片假名源自「川」之三點水。",
     "mnemonic": "像彎彎的月亮，刺（tsu）痛了黑夜！",
     "sound_tip": "重要！舌尖抵住上門牙內側，突然放氣發 tsu（疵）。",
     "vocab": "つき (tsuki)", "vocab_tw": "月亮"},
    {"index": 18, "row": "た行", "hira": "て", "kata": "テ", "romaji": "te",
     "origin": "平假名源自「天」之草書；片假名源自「天」之初筆。",
     "mnemonic": "長得像一隻伸出來要糖吃的小手（手 / te）！",
     "sound_tip": "舌尖彈開爆破發 te。",
     "vocab": "てがみ (tegami)", "vocab_tw": "書信 / 信件"},
    {"index": 19, "row": "た行", "hira": "と", "kata": "ト", "romaji": "to",
     "origin": "平假名源自「止」之草書；片假名源自「止」之初筆。",
     "mnemonic": "長得像一根刺扎進腳趾（Toe / と）！",
     "sound_tip": "圓唇乾淨發 to。",
     "vocab": "とうきょう (toukyou)", "vocab_tw": "東京"},

    # な行
    {"index": 20, "row": "な行", "hira": "な", "kata": "ナ", "romaji": "na",
     "origin": "平假名源自「奈」之草書；片假名源自「奈」之初筆。",
     "mnemonic": "美麗的奈良（na）小鹿向你點頭要鹿仙貝！",
     "sound_tip": "鼻音微起，舌尖貼上門牙發 na。",
     "vocab": "なまえ (namae)", "vocab_tw": "名字"},
    {"index": 21, "row": "な行", "hira": "に", "kata": "ニ", "romaji": "ni",
     "origin": "平假名源自「仁」之草書；片假名源自漢字「二」。",
     "mnemonic": "片假名就是『二』，發音像中文的『你 (ni)』！",
     "sound_tip": "舌面貼硬顎發 ni。",
     "vocab": "にほん (nihon)", "vocab_tw": "日本"},
    {"index": 22, "row": "な行", "hira": "ぬ", "kata": "ヌ", "romaji": "nu",
     "origin": "平假名源自「奴」之草書；片假名源自「奴」之右旁。",
     "mnemonic": "一碗香噴噴的拉麵（Noodle / ぬ），帶個打結小圈圈！",
     "sound_tip": "雙唇放鬆不要嘟起，輕柔發 nu（奴）。",
     "vocab": "ぬいぐるみ (nuigurumi)", "vocab_tw": "玩偶布偶"},
    {"index": 23, "row": "な行", "hira": "ね", "kata": "ネ", "romaji": "ne",
     "origin": "平假名源自「禰」之草書；片假名源自「禰」之示字旁。",
     "mnemonic": "像一隻尾巴捲捲可愛的小貓咪（ねこ / 猫 / ne）！",
     "sound_tip": "自然發 ne（捏）。",
     "vocab": "ねこ (neko)", "vocab_tw": "貓咪"},
    {"index": 24, "row": "な行", "hira": "の", "kata": "ノ", "romaji": "no",
     "origin": "平假名源自「乃」之草書；片假名源自「乃」之左撇。",
     "mnemonic": "一筆畫畫個禁止通行圓圈（NO / の），超好記！",
     "sound_tip": "圓唇發 no，聲線溫柔。",
     "vocab": "のみもの (nomimono)", "vocab_tw": "飲料"},

    # は行
    {"index": 25, "row": "は行", "hira": "は", "kata": "ハ", "romaji": "ha",
     "origin": "平假名源自「波」之草書；片假名源自漢字「八」。",
     "mnemonic": "開心時哈哈（ha）大笑！作為主題助詞時唸 wa！",
     "sound_tip": "喉頭微開氣音 ha。注意作為主題助詞時發 wa 音。",
     "vocab": "はい (hai)", "vocab_tw": "是的"},
    {"index": 26, "row": "は行", "hira": "ひ", "kata": "ヒ", "romaji": "hi",
     "origin": "平假名源自「比」之草書；片假名源自「比」之右旁。",
     "mnemonic": "長得像一張裂開傻笑的嘴臉（He-he / ひひ）！",
     "sound_tip": "舌面貼近硬顎擦出微弱氣流，介於『希』與『西』。",
     "vocab": "ひこうき (hikouki)", "vocab_tw": "飛機"},
    {"index": 27, "row": "は行", "hira": "ふ", "kata": "フ", "romaji": "fu",
     "origin": "平假名源自「不」之草書；片假名源自「不」之初筆。",
     "mnemonic": "富士山（Fujisan / ふ）頭頂冒出雪花與火花！",
     "sound_tip": "千萬不要咬下唇！上下唇微合留小縫，輕輕吹氣發 fu。",
     "vocab": "ふじさん (fujisan)", "vocab_tw": "富士山"},
    {"index": 28, "row": "は行", "hira": "へ", "kata": "ヘ", "romaji": "he",
     "origin": "平假名與片假名皆源自草書「部」之右旁。",
     "mnemonic": "平假名與片假名長得完全一樣！像一座尖尖屋頂（へ）！",
     "sound_tip": "氣流穿過喉部發 he。作為方向助詞時唸 e。",
     "vocab": "へや (heya)", "vocab_tw": "房間"},
    {"index": 29, "row": "は行", "hira": "ほ", "kata": "ホ", "romaji": "ho",
     "origin": "平假名源自「保」之草書；片假名源自「保」之右旁。",
     "mnemonic": "戴了一頂平平的帽子，乖乖在後（ho）面排隊！",
     "sound_tip": "圓唇清爽發 ho。",
     "vocab": "ホテル (hoteru)", "vocab_tw": "飯店 / 旅館"},

    # ま行
    {"index": 30, "row": "ま行", "hira": "ま", "kata": "マ", "romaji": "ma",
     "origin": "平假名源自「末」之草書；片假名源自「末」之上兩筆。",
     "mnemonic": "兩條橫線一個圈，媽媽（ma）摸摸小寶貝的頭！",
     "sound_tip": "雙唇微合鼻音爆破發 ma。",
     "vocab": "また (mata)", "vocab_tw": "再 / 下次"},
    {"index": 31, "row": "ま行", "hira": "み", "kata": "ミ", "romaji": "mi",
     "origin": "平假名源自「美」之草書；片假名源自漢字「三」。",
     "mnemonic": "長得像數字『21』，看到美食眼睛瞇瞇笑（mi）！",
     "sound_tip": "雙唇閉合發 mi。",
     "vocab": "みず (mizu)", "vocab_tw": "水"},
    {"index": 32, "row": "ま行", "hira": "む", "kata": "ム", "romaji": "mu",
     "origin": "平假名源自「武」之草書；片假名源自「牟」之初筆。",
     "mnemonic": "像一頭牛轉頭伸出尾巴，發出『哞～（mu）』的叫聲！",
     "sound_tip": "雙唇放鬆輕發 mu。",
     "vocab": "むすめ (musume)", "vocab_tw": "女兒"},
    {"index": 33, "row": "ま行", "hira": "め", "kata": "メ", "romaji": "me",
     "origin": "平假名源自「女」之草書；片假名源自「女」之末兩筆。",
     "mnemonic": "像一隻美麗的眼睛（目 / me），注意右下角不打結圈圈！",
     "sound_tip": "嘴角自然放鬆發 me（妹）。",
     "vocab": "めがね (megane)", "vocab_tw": "眼鏡"},
    {"index": 34, "row": "ま行", "hira": "も", "kata": "モ", "romaji": "mo",
     "origin": "平假名源自「毛」之草書；片假名源自「毛」之初三筆。",
     "mnemonic": "長得像毛（mo）髮的草書，也是撈金魚的魚鉤！",
     "sound_tip": "雙唇閉合微爆發 mo。",
     "vocab": "もっと (motto)", "vocab_tw": "更多 / 更加"},

    # や行
    {"index": 35, "row": "や行", "hira": "や", "kata": "ヤ", "romaji": "ya",
     "origin": "平假名源自「也」之草書；片假名源自「也」之初筆。",
     "mnemonic": "拍照時比出勝利剪刀手『耶（ya）』！",
     "sound_tip": "舌面快速滑向元音 a 發 ya。",
     "vocab": "やすみ (yasumi)", "vocab_tw": "休息 / 假期"},
    {"index": 36, "row": "や行", "hira": "ゆ", "kata": "ユ", "romaji": "yu",
     "origin": "平假名源自「由」之草書；片假名源自「由」之初筆。",
     "mnemonic": "一隻姿態優雅（yu）游水的小熱帶魚！",
     "sound_tip": "舌面向硬顎滑動發 yu（優）。",
     "vocab": "ゆき (yuki)", "vocab_tw": "雪"},
    {"index": 37, "row": "や行", "hira": "よ", "kata": "ヨ", "romaji": "yo",
     "origin": "平假名源自「与」之草書；片假名源自「与」之初筆。",
     "mnemonic": "像吊車勾起重物，嗨唷（yo）一聲拉上來！",
     "sound_tip": "圓唇發 yo（唷）。",
     "vocab": "ようこそ (youkoso)", "vocab_tw": "歡迎光臨"},

    # ら行
    {"index": 38, "row": "ら行", "hira": "ら", "kata": "ラ", "romaji": "ra",
     "origin": "平假名源自「良」之草書；片假名源自「良」之初筆。",
     "mnemonic": "一個人在溫泉裡舒暢泡湯，大呼好爽啦（ra）！",
     "sound_tip": "絕非捲舌音！舌尖輕彈上齒齦發 la/da。",
     "vocab": "ラーメン (rāmen)", "vocab_tw": "拉麵"},
    {"index": 39, "row": "ら行", "hira": "り", "kata": "リ", "romaji": "ri",
     "origin": "平假名源自「利」之草書；片假名源自「利」之右旁。",
     "mnemonic": "兩條俐落垂直線，右長左短，俐（ri）落清秀！",
     "sound_tip": "舌尖輕彈發 li。",
     "vocab": "りんご (ringo)", "vocab_tw": "蘋果"},
    {"index": 40, "row": "ら行", "hira": "る", "kata": "ル", "romaji": "ru",
     "origin": "平假名源自「留」之草書；片假名源自「流」之末兩筆。",
     "mnemonic": "尾巴捲起一個小圈圈，抓住了一隻嚕（ru）嚕米！",
     "sound_tip": "舌尖輕彈發 lu。",
     "vocab": "るす (rusu)", "vocab_tw": "不在家 / 留守"},
    {"index": 41, "row": "ら行", "hira": "れ", "kata": "レ", "romaji": "re",
     "origin": "平假名源自「礼」之草書；片假名源自「礼」之右旁。",
     "mnemonic": "向神明躬身敬禮（礼 / re），尾巴往右外翹！",
     "sound_tip": "舌尖輕彈發 le。",
     "vocab": "れすとらん (resutoran)", "vocab_tw": "餐廳 (西式)"},
    {"index": 42, "row": "ら行", "hira": "ろ", "kata": "ロ", "romaji": "ro",
     "origin": "平假名源自「呂」之草書；片假名源自「呂」之上方口。",
     "mnemonic": "長得像數字『3』，尾巴不打結，一路順風（ro）！",
     "sound_tip": "舌尖輕彈發 lo。",
     "vocab": "ろく (roku)", "vocab_tw": "數字六"},

    # わ行與撥音
    {"index": 43, "row": "わ行", "hira": "わ", "kata": "ワ", "romaji": "wa",
     "origin": "平假名源自「和」之草書；片假名源自「和」之口旁。",
     "mnemonic": "大白鵝伸長脖子哇（wa）一聲！",
     "sound_tip": "圓唇滑向元音 a 發 wa（哇）。",
     "vocab": "わたし (watashi)", "vocab_tw": "我"},
    {"index": 44, "row": "わ行", "hira": "を", "kata": "ヲ", "romaji": "wo (o)",
     "origin": "平假名源自「遠」之草書；片假名源自「井」之初筆。",
     "mnemonic": "一個人在雪地空中飛躍，哇喔（wo）一聲！",
     "sound_tip": "只作為受詞助詞使用，現代發音同『お (o)』。",
     "vocab": "みず を のむ (mizu o nomu)", "vocab_tw": "喝水"},
    {"index": 45, "row": "わ行", "hira": "ん", "kata": "ン", "romaji": "n",
     "origin": "平假名源自「无」之草書；片假名源自「尓」之草書。",
     "mnemonic": "長得像英文字母『n』，發出鼻音『嗯（n）』！",
     "sound_tip": "鼻音撥音，在日語中佔一整拍！",
     "vocab": "にほん (nihon)", "vocab_tw": "日本"}
]

def get_all_kana_cards() -> list:
    return ALL_KANA_CARDS

def get_kana_card(idx: int) -> dict:
    idx = max(0, min(idx, len(ALL_KANA_CARDS) - 1))
    return ALL_KANA_CARDS[idx]

