# -*- coding: utf-8 -*-
"""
動漫名台詞資料庫 (Anime Quotes Data)
精選超人氣動漫名台詞，提供振假名、文法拆解、諧音記憶與造句仿造練習。
"""

ANIME_QUOTES = {
    "kimetsu": {
        "id": "kimetsu",
        "anime": "《鬼滅之刃》⚔️",
        "character": "竈門炭治郎",
        "quote": "俺は長男だから我慢できた！",
        "furigana": "おれは ちょうなんだから がまんできた！",
        "romaji": "Ore wa chōnan dakara gaman dekita!",
        "phonetic": "【 歐 咧 哇、秋 男 打 卡 拉、嘎 曼 爹 ㄎㄧ 塔 】",
        "meaning": "因為我是長男，所以我才能忍耐下來！",
        "scene": "炭治郎在鼓之宅邸身負重傷，面對劇痛時激勵自己意志的超熱血名場面！",
        "grammar_breakdown": [
            "• **俺（おれ）**：第一人稱「我」（男性常用，較豪爽）",
            "• **長男（ちょうなん）**：長子、老大",
            "• **～だから**：因為是～（名詞＋だから＝表原因理由）",
            "• **我慢（がまん）**：忍耐、克制",
            "• **できた**：能夠（できる「可以」的過去式，代表「能做到了」）"
        ],
        "practice_template": "「私は【身分/理由】だから、【動詞】できた！」",
        "practice_example": "例：私は大人だから、我慢できた！（因為我是大人，所以我忍住了！）"
    },
    "jujutsu": {
        "id": "jujutsu",
        "anime": "《咒術迴戰》🤞",
        "character": "五條悟",
        "quote": "大丈夫、僕、最強だから。",
        "furigana": "だいじょうぶ、ぼく、さいきょうだから。",
        "romaji": "Daijōbu, boku, saikyō dakara.",
        "phonetic": "【 帶 就 補、波 庫、賽 ㄎㄧㄡ 打 卡 拉 】",
        "meaning": "沒事，因為我可是最強的。",
        "scene": "面對特級咒物宿儺現身，五條老師雲淡風輕自信一笑的標誌性名台詞！",
        "grammar_breakdown": [
            "• **大丈夫（だいじょうぶ）**：沒問題、別擔心",
            "• **僕（ぼく）**：我（男性謙遜自稱，溫和友好）",
            "• **最強（さいきょう）**：最強、天下第一",
            "• **～だから**：因為～（放在句尾表自信的理由補充）"
        ],
        "practice_template": "「大丈夫、私は【形容詞/名詞】だから。」",
        "practice_example": "例：大丈夫、私はプロだから。（別擔心，因為我是專業的。）"
    },
    "conan": {
        "id": "conan",
        "anime": "《名偵探柯南》🔍",
        "character": "江戶川柯南",
        "quote": "真実はいつもひとつ！",
        "furigana": "しんじつは いつも ひとつ！",
        "romaji": "Shinjitsu wa itsumo hitotsu!",
        "phonetic": "【 心 雞 疵 哇、一 次 摸、比 透 疵 】",
        "meaning": "真相永遠只有一個！",
        "scene": "每一集柯南片頭與破案高潮必定出現的招牌指人手勢神句！",
        "grammar_breakdown": [
            "• **真実（しんじつ）**：真相、真實",
            "• **いつも**：總是、永遠、一直",
            "• **ひとつ**：一個（日文原生數字數法：ひとつ、ふたつ、みっつ...）"
        ],
        "practice_template": "「【事物】は いつも ひとつ！」",
        "practice_example": "例：答えはいつもひとつ！（答案永遠只有一個！）"
    },
    "onepiece": {
        "id": "onepiece",
        "anime": "《航海王 ONE PIECE》👒",
        "character": "蒙其·D·魯夫",
        "quote": "海賊王に、おれはなる！",
        "furigana": "かいぞくおうに、おれは なる！",
        "romaji": "Kaizoku-ō ni, ore wa naru!",
        "phonetic": "【 開 左 庫 歐 逆、歐 咧 哇、那 嚕 】",
        "meaning": "我是要成為海賊王的男人！",
        "scene": "航海王開播至今最振奮人心的出海宣言，宣示無比堅定的人生志願！",
        "grammar_breakdown": [
            "• **海賊王（かいぞくおう）**：海賊王",
            "• **～に なる**：成為～（目標對象＋助詞に＋動詞「なる」變成）",
            "• **おれは**：倒裝強調「我」的堅定決心！"
        ],
        "practice_template": "「【目標職業/夢想】に、おれはなる！」",
        "practice_example": "例：エンジニアに、おれはなる！（我要成為工程師！）"
    },
    "slamdunk": {
        "id": "slamdunk",
        "anime": "《灌籃高手》🏀",
        "character": "安西教練",
        "quote": "あきらめたら そこで試合終了ですよ。",
        "furigana": "あきらめたら そこで しあいしゅうりょう ですよ。",
        "romaji": "Akirametara sokode shiai shūryō desu yo.",
        "phonetic": "【 阿 ㄎㄧ 拉 妹 他 拉、搜 摳 爹、西 阿 衣 修 溜、爹 斯 唷 】",
        "meaning": "要是放棄的話，比賽就到此結束了喔。",
        "scene": "三井壽國中決賽陷入絕境時，安西教練遞球說出這句點醒一生的神級心靈名言！",
        "grammar_breakdown": [
            "• **あきらめたら**：要是放棄的話（動詞「諦める」假定形「～たら」）",
            "• **そこで**：就在那個當下/那裡",
            "• **試合終了（しあいしゅうりょう）**：比賽結束",
            "• **～ですよ**：溫和而肯定的叮嚀語氣"
        ],
        "practice_template": "「【動詞たら】、そこで【名詞】ですよ。」",
        "practice_example": "例：寝たら、そこで勉強終了ですよ。（要是睡著的話，讀書就到此結束了喔。）"
    },
    "frieren": {
        "id": "frieren",
        "anime": "《葬送的芙莉蓮》🪄",
        "character": "芙莉蓮",
        "quote": "ヒンメルなら、そうした。",
        "furigana": "ヒンメルなら、そうした。",
        "romaji": "Hinmeru nara, sō shita.",
        "phonetic": "【 辛 美 魯 那 拉、搜 西 他 】",
        "meaning": "如果是欣梅爾的話，他一定也會這麼做的。",
        "scene": "每次芙莉蓮面臨抉擇、選擇無私幫助他人時，心中溫柔浮現勇者欣梅爾的名言！",
        "grammar_breakdown": [
            "• **ヒンメル**：勇者欣梅爾（人名）",
            "• **～なら**：如果是～的話（假設助詞）",
            "• **そう**：那樣地、那樣做",
            "• **した**：做了（動詞「する」過去式）"
        ],
        "practice_template": "「【崇拜的人】なら、そうした。」",
        "practice_example": "例：先生なら、そうした。（如果是老師的話，他也會這麼做的。）"
    },
    "spyfamily": {
        "id": "spyfamily",
        "anime": "《SPY×FAMILY 間諜家家酒》🥜",
        "character": "安妮亞·佛傑",
        "quote": "アーニャ、ピーナッツが好き！",
        "furigana": "アーニャ、ピーナッツが すき！",
        "romaji": "Ānya, pīnattsu ga suki!",
        "phonetic": "【 阿 娘、披 納 刺 嘎、蘇 ㄎㄧ 】",
        "meaning": "安妮亞最喜歡花生了！",
        "scene": "安妮亞被洛伊德問到喜歡什麼時，雙眼發光、可愛度爆表的經典台詞！",
        "grammar_breakdown": [
            "• **ピーナッツ**：花生（Peanuts 外來語片假名）",
            "• **が**：喜好對象標記助詞",
            "• **好き（すき）**：喜歡（「好」字，發音「Suki」）"
        ],
        "practice_template": "「私は、【喜歡的人事物】が好き！」",
        "practice_example": "例：私は、日本のアニメが好き！（我喜歡日本動漫！）"
    },
    "shingeki": {
        "id": "shingeki",
        "anime": "《進擊的巨人》⚔️",
        "character": "艾連·葉卡",
        "quote": "戦わなければ、勝てない。戦え、戦え！",
        "furigana": "たたかわなければ、かてない。たたかえ、たたかえ！",
        "romaji": "Tatakawanakereba, katenai. Tatakae, tatakae!",
        "phonetic": "【 他 他 卡 哇 那 ㄎㄟ 咧 八、卡 貼 那 衣。他 他 卡 ㄝ、他 他 卡 ㄝ 】",
        "meaning": "不戰鬥的話就贏不了。戰鬥吧！戰鬥吧！",
        "scene": "艾連救下米卡莎時，喚醒靈魂、貫穿整部作品靈魂的絕對生存信條！",
        "grammar_breakdown": [
            "• **戦わなければ**：如果不戰鬥的話（否定假定形「～なければ」）",
            "• **勝てない（かてない）**：贏不了（可能形否定「勝てる」→「勝てない」）",
            "• **戦え（たたかえ）**：戰鬥吧！（動詞命令形，最強烈的呼喊）"
        ],
        "practice_template": "「【動詞なければ】、勝てない！」",
        "practice_example": "例：勉強しなければ、合格できない！（如果不讀書的話，就考不上！）"
    }
}
