# -*- coding: utf-8 -*-
"""
四大情境（旅遊、生活、工作、休閒）實用語庫與每日一句庫
"""

SCENARIOS = {
    "travel": {
        "title": "✈️ 日本旅遊與生存日語",
        "description": "自由行最常使用的情境金句（點餐、問路、結帳、退稅等）",
        "phrases": [
            {
                "japanese": "これをお願いします。",
                "furigana": "これを おねがいします。",
                "romaji": "Kore o onegai shimasu.",
                "meaning": "請給我這個。（點餐/購物指著物品必備神句）",
                "usage": "在餐廳看著菜單、或在超商商品架前，指著想買的東西對店員說即可。"
            },
            {
                "japanese": "おすすめは何ですか？",
                "furigana": "おすすめは なんですか？",
                "romaji": "Osusume wa nan desu ka?",
                "meaning": "請問有推薦的嗎？",
                "usage": "不知道點什麼時，讓店家或店員推薦人氣招牌菜。"
            },
            {
                "japanese": "お会計をお願いします。",
                "furigana": "おかいけいを おねがいします。",
                "romaji": "Okaikei o onegai shimasu.",
                "meaning": "請幫我結帳。",
                "usage": "在居酒屋或餐廳吃飽後，招手向店員示意買單。"
            },
            {
                "japanese": "すみません、トイレはどこですか？",
                "furigana": "すみません、トイレは どこですか？",
                "romaji": "Sumimasen, toire wa doko desu ka?",
                "meaning": "不好意思，請問洗手間在哪裡？",
                "usage": "外出急需上廁所時萬用語。"
            },
            {
                "japanese": "免税できますか？",
                "furigana": "めんぜい できますか？",
                "romaji": "Menzei dekimasu ka?",
                "meaning": "請問可以辦理免稅嗎？",
                "usage": "在藥妝店、Bic Camera、百貨專櫃結帳前出示護照並詢問。"
            },
            {
                "japanese": "別々でお願いします。",
                "furigana": "べつべつで おねがいします。",
                "romaji": "Betsubetsu de onegai shimasu.",
                "meaning": "請分開結帳。",
                "usage": "和朋友同行想各自付帳時告知櫃檯。"
            }
        ]
    },
    "daily": {
        "title": "🏠 日常生活實用語句",
        "description": "在日生活、超商採購、郵政、看診求助必備",
        "phrases": [
            {
                "japanese": "袋はいりません。",
                "furigana": "ふくろは いりません。",
                "romaji": "Fukuro wa irimasen.",
                "meaning": "不需要塑膠袋。",
                "usage": "超商結帳時店員問「袋はお付けしますか？」時回答。"
            },
            {
                "japanese": "温めてください。",
                "furigana": "あたためて ください。",
                "romaji": "Atatame te kudasai.",
                "meaning": "請幫我加熱/微波。",
                "usage": "超商買便當、熟食時請店員微波。"
            },
            {
                "japanese": "頭／お腹が痛いです。",
                "furigana": "あたま／おなかが いたいです。",
                "romaji": "Atama / Onaka ga itai desu.",
                "meaning": "頭痛 / 肚子痛。",
                "usage": "身體不適去藥局諮詢藥劑師或診所就醫時使用。"
            },
            {
                "japanese": "ちょっと教えていただけますか？",
                "furigana": "ちょっと おしえて いただけますか？",
                "romaji": "Chotto oshiete itadakemasu ka?",
                "meaning": "能稍微教我／告訴我一下嗎？",
                "usage": "在生活或公家機關中，需要別人指點步驟時的禮貌請求。"
            }
        ]
    },
    "anime": {
        "title": "🎮 休閒娛樂與動漫影視",
        "description": "日劇、動漫、推特、遊戲中超高頻出現的生活感嘆與口語",
        "phrases": [
            {
                "japanese": "さすが！",
                "furigana": "さすが！",
                "romaji": "Sasuga!",
                "meaning": "不愧是你！/ 真有一套！",
                "usage": "讚嘆對方的能力或表現一如既往地出色。"
            },
            {
                "japanese": "大丈夫です。",
                "furigana": "だいじょうぶです。",
                "romaji": "Daijōbu desu.",
                "meaning": "沒事、沒關係、不要緊。",
                "usage": "日本生活與動漫最萬用的金句，表拒絕或安慰皆可。"
            },
            {
                "japanese": "なるほど！",
                "furigana": "なるほど！",
                "romaji": "Naruhodo!",
                "meaning": "原來如此！",
                "usage": "聽完對方的解說或得知新資訊時的即時反饋。"
            },
            {
                "japanese": "うそでしょ！",
                "furigana": "うそでしょ！",
                "romaji": "Uso desho!",
                "meaning": "騙人的吧！/ 不會吧！",
                "usage": "影視作品中主角遇到驚人事件時極常見的感嘆。"
            },
            {
                "japanese": "応援してます！",
                "furigana": "おうえん してます！",
                "romaji": "Ōen shitemasu!",
                "meaning": "我會一直支持你！",
                "usage": "追星、看比賽、鼓勵朋友時的熱情應援。"
            }
        ]
    },
    "work": {
        "title": "💼 職場與商務敬語入門",
        "description": "日商職場必備、商業信件與禮貌應對",
        "phrases": [
            {
                "japanese": "お疲れ様です。",
                "furigana": "おつかれさまです。",
                "romaji": "Otsukaresama desu.",
                "meaning": "辛苦了。",
                "usage": "日本職場第一萬用句！見面問候、回覆郵件開頭、走廊擦身而過皆適用。"
            },
            {
                "japanese": "お先に失礼します。",
                "furigana": "おさきに しつれいします。",
                "romaji": "Osaki ni shitsurei shimasu.",
                "meaning": "我先下班了（先失陪了）。",
                "usage": "比同事早離開辦公室時必備禮貌用語。"
            },
            {
                "japanese": "かしこまりました。",
                "furigana": "かしこまりました。",
                "romaji": "Kashikomarimashita.",
                "meaning": "我明白了／遵照辦理。",
                "usage": "向客戶或主管回覆要求，比『分かりました』更具專業敬意。"
            },
            {
                "japanese": "よろしくお願いいたします。",
                "furigana": "よろしく おねがいいたします。",
                "romaji": "Yoroshiku onegai itashimasu.",
                "meaning": "請多指教 / 拜託您了。",
                "usage": "商業郵件標準結尾，或委託工作時使用。"
            },
            {
                "japanese": "確認していただけますでしょうか？",
                "furigana": "かくにん していただけます でしょうか？",
                "romaji": "Kakunin shite itadakemasu deshō ka?",
                "meaning": "能否請您過目／確認一下呢？",
                "usage": "繳交文件、提案時請主管或客戶確認的極禮貌表達方式。"
            }
        ]
    }
}
