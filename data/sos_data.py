# -*- coding: utf-8 -*-
"""
日本緊急生存與就醫求助手指卡資料庫 (SOS Data)
提供急救、看病、報警、護照/物品遺失、迷路等場景的中日雙語大字手指卡。
赴日旅遊突發狀況時，可直接出示手機螢幕給日本人、站務員或醫護人員看！
"""

EMERGENCY_CONTACTS = [
    {"name": "🚨 警察報案 (交通事故、竊盜、遺失)", "number": "110", "note": "全日本通用，免費撥打。"},
    {"name": "🚑 消防與急救救護車 (急病、重傷、火警)", "number": "119", "note": "全日本通用，免費撥打。"},
    {"name": "🇹🇼 台灣駐日代表處 (緊急急難救助專線)", "number": "+81-3-3280-7811", "note": "專供車禍、強盜、危及生命等緊急重大事件聯繫。"},
    {"name": "🏥 日本觀光廳 24小時多語言呼叫中心", "number": "050-3816-2787", "note": "提供中文、英文、日語等多語種旅遊諮詢與緊急醫療指引。"}
]

SOS_SCENARIOS = {
    "medical": {
        "title": "🏥 身體不適 / 就醫看病手指卡",
        "category": "醫療急救",
        "intro": "【請將此卡片直接出示給藥局藥師或診所醫生看】",
        "cards": [
            {
                "japanese": "急に激しい頭痛がして、寒気が止まりません。",
                "furigana": "きゅうにはげしいずつうがして、さむけがとまりません。",
                "romaji": "Kyū ni hageshii zutsū ga shite, samuke ga tomarimasen.",
                "chinese": "我突然感到劇烈頭痛，而且全身一直發冷顫抖。",
                "tag": "頭痛・發燒"
            },
            {
                "japanese": "お腹が痛くて、下痢と吐き気が続いています。",
                "furigana": "おなかがいたくて、げりとはきけがつづいています。",
                "romaji": "Onaka ga itakute, geri to hakike ga tsuzuiteimasu.",
                "chinese": "我肚子非常痛，並且一直拉肚子和想吐。",
                "tag": "胃腸炎・拉肚子"
            },
            {
                "japanese": "私は薬物（アスピリン / ペニシリン）のアレルギーがあります。",
                "furigana": "わたしはやくぶつのアレルギーがあります。",
                "romaji": "Watashi wa yakubutsu no arerugī ga arimasu.",
                "chinese": "我對某些藥物（如阿斯匹靈/盤尼西林）有過敏反應！",
                "tag": "⚠️ 藥物過敏"
            },
            {
                "japanese": "近くに英語か中国語が通じる病院はありますか？",
                "furigana": "ちかくにえいごかちゅうごくごがつうじるびょういんはありますか？",
                "romaji": "Chikaku ni eigo ka chūgokugo ga tsūjiru byōin wa arimasu ka?",
                "chinese": "請問這附近有能通英文或中文的綜合醫院嗎？",
                "tag": "找醫院"
            }
        ]
    },
    "lost": {
        "title": "👛 護照 / 貴重物品遺失求助卡",
        "category": "遺失協尋",
        "intro": "【請將此卡片出示給警察局 (交番 Kōban) 或車站站務員看】",
        "cards": [
            {
                "japanese": "電車の中に財布（パスポート）を忘れてしまいました。",
                "furigana": "でんしゃのなかにさいふ（パスポート）をわすれてしまいました。",
                "romaji": "Densha no naka ni saifu (pasupōto) o wasurete shimaimashita.",
                "chinese": "我把錢包（護照）遺落在剛才搭乘的電車車廂裡了。",
                "tag": "電車遺失物"
            },
            {
                "japanese": "何両目か覚えていませんが、山手線の内回りでした。",
                "furigana": "なんりょうめかおぼえていませんが、やまのてせんのうちまわりでした。",
                "romaji": "Nanryōme ka oboete imasen ga, yamanotesen no uchimawari deshita.",
                "chinese": "我不記得是第幾節車廂，但搭的是山手線順時針內環。",
                "tag": "車次線索"
            },
            {
                "japanese": "遺失物届（いしつぶつとどけ）を出したいのですが、手伝っていただけますか？",
                "furigana": "いしつぶつとどけをだしたいのですが、てつだっていただけますか？",
                "romaji": "Ishitsubutsutodoke o dashitai no desu ga, tetsudatte itadakemasu ka?",
                "chinese": "我想填寫並申報遺失物登記表，可以協助我嗎？",
                "tag": "報案登記"
            }
        ]
    },
    "police": {
        "title": "🚨 交通事故 / 緊急報警求助卡",
        "category": "緊急報警",
        "intro": "【遭遇危急狀況、盜竊或交通事故時出示】",
        "cards": [
            {
                "japanese": "助けてください！スリ（盗難）の被害に遭いました。",
                "furigana": "たすけてください！スリのひがいにあいました。",
                "romaji": "Tasukete kudasai! Suri no higai ni aimashita.",
                "chinese": "請救救我！我剛才遭遇小偷扒竊了。",
                "tag": "竊盜遇害"
            },
            {
                "japanese": "事故です！怪我人がいるので、救急車を呼んでください！",
                "furigana": "じこです！けがにんがいるので、きゅうきゅうしゃをよんでください！",
                "romaji": "Jiko desu! Keganin ga iru node, kyūkyūsha o yonde kudasai!",
                "chinese": "發生車禍了！現場有傷患，請立刻幫忙叫救護車！",
                "tag": "叫救護車"
            },
            {
                "japanese": "ここはどこですか？警察署（交番）はどこですか？",
                "furigana": "ここはどこですか？けいさつしょ（こうばん）はどこですか？",
                "romaji": "Koko wa doko desu ka? Keisatsusho (kōban) wa doko desu ka?",
                "chinese": "請問這裡是什麼地址？最近的派出所（交番）在哪裡？",
                "tag": "找派出所"
            }
        ]
    },
    "direction": {
        "title": "🧭 迷路 / 錯過末班車求助卡",
        "category": "交通迷路",
        "intro": "【深夜迷路或找不到回飯店的路時出示】",
        "cards": [
            {
                "japanese": "道に迷ってしまいました。このホテルに行きたいのですが、どう行けばいいですか？",
                "furigana": "みちにまよってしまいました。このホテルにいきたいのですが、どういけばいいですか？",
                "romaji": "Michi ni mayotte shimaimashita. Kono hoteru ni ikitai no desu ga, dō ikeba ii desu ka?",
                "chinese": "我迷路了。我想去這間飯店（手指地圖/訂房資訊），請問該怎麼走？",
                "tag": "問路回飯店"
            },
            {
                "japanese": "終電（しゅうでん）を逃してしまいました。タクシー乗り場はどこですか？",
                "furigana": "しゅうでんをのがしてしまいました。タクシーのりばはどこですか？",
                "romaji": "Shūden o nogashite shimaimashita. Takushī noriba wa doko desu ka?",
                "chinese": "我錯過最後一班電車了。請問計程車招呼站在哪裡？",
                "tag": "搭計程車"
            }
        ]
    }
}
