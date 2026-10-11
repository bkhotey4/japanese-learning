# -*- coding: utf-8 -*-
"""
日語 10 大關卡闖關資料庫 (Quest Data)
將五十音進度、實戰情境金句、諧音字形口訣與驗收測驗整合為一體化關卡系統。
"""

QUESTS = {
    1: {
        "level": 1,
        "title": "第 1 關：あ行與神級點餐 🍜",
        "kana_group": "あ行（あ、い、う、え、お）",
        "kana_tip": (
            "• **あ (a)**：張開雙手看到大蘋果驚呼「あ (啊)！」\n"
            "• **こ (ko)**：上下兩片漢堡麵包皮\n"
            "• **れ (re)**：昂首挺胸、尾巴俏麗的白天鵝"
        ),
        "phrase": "これ、ください。",
        "romaji": "Kore, kudasai.",
        "phonetic": "【 顆 粒、庫 達 塞 】",
        "mnemonic_story": (
            "🐕 **超萌口訣故事**：\n"
            "一隻柴犬小旅行家走進拉麵店，\n"
            "手指著菜單上的照片，用日文大喊：\n"
            "**「顆粒（これ）、庫達塞（ください）！」**\n"
            "店長秒懂，立刻端上香噴噴的大碗拉麵！\n\n"
            "💡 **萬用技**：把「これ」換成「それ（那個）」「あれ（那邊那個）」，三連發通殺日本餐廳！"
        ),
        "card_image": "cards/card_quest1_kore.jpg",
        "meaning": "This, please!（請給我這個）",
        "scenario": "在日本拉麵店、超商、壽司店，手指著菜單上的照片說出這句，店員秒懂幫您下單！",
        "quiz": {
            "question": "走進居酒屋看著菜單上的招牌烤串，手指著照片想要點餐，應該說哪一句？",
            "options": ["これ、ください。", "トイレはどこですか？", "いくらですか？", "お先に失礼します。"],
            "answer": "これ、ください。",
            "explanation": "「これ、ください (Kore, kudasai)」是自由行第一萬用句：請給我這個！"
        }
    },
    2: {
        "level": 2,
        "title": "第 2 關：か行與購物問價 🏷️",
        "kana_group": "か行（か、き、く、け、こ）",
        "kana_tip": (
            "• **か (ka)**：加號加一點，發音像「卡」\n"
            "• **き (ki)**：像一把金屬鑰匙 (key)\n"
            "• **く (ku)**：像鳥嘴張開大哭 (ku)"
        ),
        "phrase": "いくらですか？",
        "romaji": "Ikura desu ka?",
        "phonetic": "【 一 庫 拉、爹 斯 嘎 】",
        "mnemonic_story": (
            "🦞 **超萌口訣故事**：\n"
            "在秋葉原藥妝店，你拿起一瓶高級面膜，\n"
            "腦海浮現一道「**一庫拉（いくら）**」的鮭魚卵壽司，\n"
            "然後問旁邊的店員：**「爹斯嘎（ですか）？」**\n"
            "口訣：**一顆魚卵（いくら）多少錢？爹爹斯嘎！**\n\n"
            "💡 **趣知識**：「いくら」也是鮭魚卵（salmon roe）的意思！\n"
            "想起魚卵就記住「多少錢」了！"
        ),
        "card_image": "cards/card_quest2_ikura.jpg",
        "meaning": "How much is it?（請問多少錢？）",
        "scenario": "在秋葉原扭蛋店、藥妝店或市集逛街，拿起喜歡的商品向店員詢問價格。",
        "quiz": {
            "question": "在藥妝店拿起一盒眼藥水，想問店員「這個多少錢？」，應該說：",
            "options": ["いくらですか？", "どこですか？", "これ、ください。", "すみません。"],
            "answer": "いくらですか？",
            "explanation": "「いくらですか？ (Ikura desu ka?)」是詢問價格的標準金句！"
        }
    },
    3: {
        "level": 3,
        "title": "第 3 關：さ行與問路尋找 🗺️",
        "kana_group": "さ行（さ、し、す、せ、そ）",
        "kana_tip": (
            "• **さ (sa)**：一把小匕首殺 (sa) 出去\n"
            "• **し (shi)**：釣魚的大魚鉤 (shi)\n"
            "• **す (su)**：捲捲打結的豬尾巴 (su)"
        ),
        "phrase": "トイレはどこですか？",
        "romaji": "Toire wa doko desu ka?",
        "phonetic": "【 透 衣 レ、哇、多 口 爹 斯 嘎 】",
        "mnemonic_story": (
            "🚽 **超萌口訣故事**：\n"
            "觀光客肚子突然痛，在地鐵站狂奔，\n"
            "心裡急喊：**「透衣嘞（トイレ）在哪裡！」**\n"
            "衝向站務員：**「透衣嘞、哇、多口爹斯嘎！」**\n\n"
            "🔑 **解碼**：\n"
            "• トイレ = toilet（英文借來的！）\n"
            "• どこ = where（哪裡）\n"
            "💡 把「トイレ」換成任何地點都行！\n"
            "「駅（えき）はどこですか？」= 車站在哪裡？"
        ),
        "card_image": "cards/card_quest3_toilet.jpg",
        "meaning": "Where is the restroom?（請問洗手間在哪裡？）",
        "scenario": "在外急需洗手間或尋找車站出口時，將「トイレ (廁所)」換成任何地點（如「駅 (車站)」）都能問！",
        "quiz": {
            "question": "在日本地鐵站迷路急著找洗手間，應該向站務員詢問：",
            "options": ["トイレはどこですか？", "温めてください。", "いくらですか？", "袋はいりません。"],
            "answer": "トイレはどこですか？",
            "explanation": "「トイレはどこですか？ (Toire wa doko desu ka?)」是出門在外生存率最高的問路句！"
        }
    },
    4: {
        "level": 4,
        "title": "第 4 關：た行與表達意願 🍜",
        "kana_group": "た行（た、ち、つ、て、と）",
        "kana_tip": (
            "• **た (ta)**：像中文「太」少一點\n"
            "• **ち (chi)**：像數字「5」反過來\n"
            "• **つ (tsu)**：海浪打起的大水滴 (tsu)"
        ),
        "phrase": "ラーメンを食べたいです。",
        "romaji": "Rāmen o tabetai desu.",
        "phonetic": "【 拉 麵、ㄛ、他 被 胎 爹 斯 】",
        "mnemonic_story": (
            "🍜 **超萌口訣故事**：\n"
            "走在寒冷的北海道街道，聞到拉麵香味，\n"
            "脫口而出：**「拉麵（ラーメン）を、他被胎（食べたい）爹斯！」**\n\n"
            "🔑 **文法解碼**：\n"
            "• ～たい = 想做（萬用句型！）\n"
            "• 行きたい（想去）、見たい（想看）、飲みたい（想喝）\n"
            "換掉動詞即可！"
        ),
        "card_image": "cards/card_quest4_tabetai.jpg",
        "meaning": "I want to eat ramen.（我想吃拉麵。）",
        "scenario": "表達「我想做某事（～たいです）」！將動詞加上たい，想去（行きたい）、想吃（食べたい）隨心說。",
        "quiz": {
            "question": "朋友問你想吃什麼晚餐，你想表達「我想吃拉麵」，應該說：",
            "options": ["ラーメンを食べたいです。", "ラーメンを食べました。", "ラーメンをください。", "ラーメンはおいしいです。"],
            "answer": "ラーメンを食べたいです。",
            "explanation": "「～たいです (tai desu)」代表「想做...」，「食べたいです」就是「想吃」！"
        }
    },
    5: {
        "level": 5,
        "title": "第 5 關：な行與商品詢問 🏪",
        "kana_group": "な行（な、に、ぬ、ね、の）",
        "kana_tip": (
            "• **な (na)**：十隻眼睛那 (na) 樣看\n"
            "• **に (ni)**：一豎兩橫像是「你 (ni)」\n"
            "• **の (no)**：一筆畫圓圈像打禁止 (no)"
        ),
        "phrase": "傘はありますか？",
        "romaji": "Kasa wa arimasu ka?",
        "phonetic": "【 卡 撒、哇、阿 里 媽 斯 嘎 】",
        "mnemonic_story": (
            "☂️ **超萌口訣故事**：\n"
            "突然下起大雨，急衝進超商，\n"
            "上氣不接下氣：**「卡撒（傘）哇、阿里媽斯嘎！」**\n"
            "店員微笑指向角落的雨傘架！\n\n"
            "💡 **萬用替換公式**：\n"
            "「[物品] はありますか？」= 請問有 [物品] 嗎？\n"
            "例：「充電器はありますか？」= 有充電器嗎？"
        ),
        "card_image": "cards/card_quest5_kasa.jpg",
        "meaning": "Do you have umbrellas?（請問有賣傘嗎？）",
        "scenario": "遇到下雨走進超商，或者在電器行找特定轉接頭時，用「[物品] はありますか？」直接問！",
        "quiz": {
            "question": "突然下大雨跑進 7-11，想問店員「有雨傘嗎？」，應該說：",
            "options": ["傘はありますか？", "傘はいくらですか？", "傘をください。", "傘はどこですか？"],
            "answer": "傘はありますか？",
            "explanation": "「～はありますか？ (arimasu ka?)」代表「請問有...嗎？」，找商品必備！"
        }
    },
    6: {
        "level": 6,
        "title": "第 6 關：は行與超商微波 🍱",
        "kana_group": "は行（は、ひ、ふ、へ、ほ）",
        "kana_tip": (
            "• **は (ha)**：左豎右圈哈哈笑 (ha)\n"
            "• **ひ (hi)**：微笑咧嘴吸氣 (hi)\n"
            "• **へ (he)**：像一座小小山峰 (he)"
        ),
        "phrase": "温めてください。",
        "romaji": "Atatame te kudasai.",
        "phonetic": "【 阿 他 他 妹 貼、庫 達 塞 】",
        "mnemonic_story": (
            "🍱 **超萌口訣故事**：\n"
            "買了一個冰涼的便當，遞給超商店員，\n"
            "說：**「阿他他妹貼（温めて）、庫達塞（ください）！」**\n"
            "店員嗶嗶嗶，微波爐叮一聲，熱騰騰端出來！\n\n"
            "💡 **口訣聯想**：\n"
            "「阿他他妹」→ 啊！打打她（便當）妹妹（加熱她！）\n"
            "就記住「加熱」的感覺了！"
        ),
        "card_image": "cards/card_quest6_atatame.jpg",
        "meaning": "Please warm this up.（請幫我加熱/微波。）",
        "scenario": "在日本超商買便當、炸物、炸雞排，請店員微波時的主動金句。",
        "quiz": {
            "question": "在 Lawson 買了豬排便當想吃熱騰騰的，向店員請託加熱時說：",
            "options": ["温めてください。", "袋はいりません。", "別々でお願いします。", "冷やしてください。"],
            "answer": "温めてください。",
            "explanation": "「温めてください (Atatame te kudasai)」就是「請幫我微波加熱」！"
        }
    },
    7: {
        "level": 7,
        "title": "第 7 關：ま行與居酒屋買單 🍶",
        "kana_group": "ま行（ま、み、む、め、も）",
        "kana_tip": (
            "• **ま (ma)**：兩橫小青蛙臉 (ma)\n"
            "• **み (mi)**：三條斜線咪咪眼 (mi)\n"
            "• **も (mo)**：魚鉤加上兩根刺 (mo)"
        ),
        "phrase": "お会計をお願いします。",
        "romaji": "Okaikei o onegai shimasu.",
        "phonetic": "【 歐 開 ㄎㄟ、ㄛ、歐 內 嘎 衣、喜 媽 斯 】",
        "mnemonic_story": (
            "🍶 **超萌口訣故事**：\n"
            "居酒屋吃飽喝足，高舉雙手向店員喊：\n"
            "**「歐開ㄎㄟ（お会計）！歐內嘎衣喜媽斯（お願いします）！」**\n\n"
            "💡 **超好記方法**：\n"
            "「お会計」就是漢字「會計」！台灣人天然認識！\n"
            "只要記住開頭「歐（お）」是尊稱前綴就夠了！"
        ),
        "card_image": "cards/card_quest7_okaikei.jpg",
        "meaning": "Check, please.（請幫我結帳。）",
        "scenario": "在居酒屋或家庭餐廳吃飽喝足，在座位上向店員舉手示意買單。",
        "quiz": {
            "question": "在居酒屋用餐完畢，想請店員過來算帳買單，最得體的說法是：",
            "options": ["お会計をお願いします。", "ごちそうさまでした。", "すみません、トイレはどこですか？", "これ、ください。"],
            "answer": "お会計をお願いします。",
            "explanation": "「お会計をお願いします (Okaikei o onegai shimasu)」是居酒屋結帳最標準的用語！"
        }
    },
    8: {
        "level": 8,
        "title": "第 8 關：や行與招牌推薦 🍣",
        "kana_group": "や行（や、ゆ、よ）",
        "kana_tip": (
            "• **や (ya)**：一隻帶長矛的野豬 (ya)\n"
            "• **ゆ (yu)**：像一尾優雅的金魚 (yu)\n"
            "• **よ (yo)**：像一個溜溜球 (yo)"
        ),
        "phrase": "おすすめは何ですか？",
        "romaji": "Osusume wa nan desu ka?",
        "phonetic": "【 歐 蘇 蘇 妹、哇、難 爹 斯 嘎 】",
        "mnemonic_story": (
            "🍣 **超萌口訣故事**：\n"
            "看著密密麻麻全是日文的壽司菜單一個頭兩個大，\n"
            "直接問主廚：**「歐蘇蘇妹（おすすめ）哇、難爹斯嘎？」**\n"
            "主廚眼睛一亮，端上今天最新鮮的大拖羅！\n\n"
            "💡 **口訣**：**蘇蘇妹妹**最推薦！（すすめ = 推薦）\n"
            "「今日のおすすめ」= 今日特推！讓主廚幫你決定！"
        ),
        "card_image": "cards/card_quest8_osusume.jpg",
        "meaning": "What do you recommend?（有什麼推薦的嗎？）",
        "scenario": "看著密密麻麻的菜單不知道點什麼時，讓主廚或店員推薦人氣冠軍招牌！",
        "quiz": {
            "question": "走進迴轉壽司店，不知道當季哪種魚最新鮮，想問主廚推薦哪一款：",
            "options": ["おすすめは何ですか？", "いくらですか？", "これをお願いします。", "別々でお願いします。"],
            "answer": "おすすめは何ですか？",
            "explanation": "「おすすめは何ですか？ (Osusume wa nan desu ka?)」讓你輕鬆吃到隱藏招牌！"
        }
    },
    9: {
        "level": 9,
        "title": "第 9 關：ら行與藥妝退稅 🛍️",
        "kana_group": "ら行（ら、り、る、れ、ろ）",
        "kana_tip": (
            "• **ら (ra)**：像馬桶抽水馬桶座 (ra)\n"
            "• **り (ri)**：一短一長兩根竹子 (ri)\n"
            "• **る (ru)**：尾巴帶個小圈圈 (ru)"
        ),
        "phrase": "免税できますか？",
        "romaji": "Menzei dekimasu ka?",
        "phonetic": "【 麵 賊、爹 ㄎㄧ 媽 斯 嘎 】",
        "mnemonic_story": (
            "🛍️ **超萌口訣故事**：\n"
            "在唐吉訶德推著滿滿購物車，\n"
            "結帳前大聲問：**「麵賊（免税）！爹ㄎㄧ媽斯嘎！」**\n"
            "店員看了護照立刻幫你省下一大筆稅金！\n\n"
            "💡 **口訣**：**「麵條賊貴！免稅才划算！」**\n"
            "記得帶護照！門檻通常是 5,000 日圓以上！"
        ),
        "card_image": "cards/card_quest9_menzei.jpg",
        "meaning": "Can I get tax-free?（請問可以退稅嗎？）",
        "scenario": "在唐吉訶德、Bic Camera、藥妝店結帳前，拿出護照詢問是否能享 10% 退稅優惠。",
        "quiz": {
            "question": "在松本清藥妝店買滿 5000 日圓，想辦理免稅退稅，應該問：",
            "options": ["免税できますか？", "袋はいりません。", "領収書をください。", "温めてください。"],
            "answer": "免税できますか？",
            "explanation": "「免税できますか？ (Menzei dekimasu ka?)」是出國血拼省錢第一句！"
        }
    },
    10: {
        "level": 10,
        "title": "第 10 關：わ行・撥音與大圓滿感謝 🎌",
        "kana_group": "わ行與撥音（わ、を、ん）",
        "kana_tip": (
            "• **わ (wa)**：大肚子青蛙哇哇叫 (wa)\n"
            "• **を (wo/o)**：挺大肚子的動作貼紙 (o)\n"
            "• **ん (n)**：像英文小寫 h，唯一的鼻音 (n)"
        ),
        "phrase": "ありがとうございました！",
        "romaji": "Arigatō gozaimashita!",
        "phonetic": "【 阿 里 嘎 透、溝 扎 衣 媽 喜 他 】",
        "mnemonic_story": (
            "🎌 **超萌口訣故事**：\n"
            "退房離開溫泉飯店，店員們全體深深鞠躬，\n"
            "你感動地回應：\n"
            "**「阿里嘎透！溝扎衣媽喜他！」**\n"
            "這一句讓所有日本人都知道你真心感謝！\n\n"
            "💡 **程度差異一覽**：\n"
            "• ありがとう！（謝謝！輕鬆版）\n"
            "• ありがとうございます！（非常感謝！正式版）\n"
            "• ありがとうございました！（十萬分感謝！離別版）"
        ),
        "card_image": "cards/card_quest10_arigatou.jpg",
        "meaning": "Thank you very much!（非常感謝您！）",
        "scenario": "退房離開飯店、離開餐廳店員鞠躬時，送上最誠摯的感謝告別。",
        "quiz": {
            "question": "退房離開溫泉飯店，店員熱情揮手送行，你應該微笑回應：",
            "options": ["ありがとうございました！", "お先に失礼します。", "ごめんなさい。", "さようなら。"],
            "answer": "ありがとうございました！",
            "explanation": "「ありがとうございました！」是過去式的誠摯大感謝，日本旅行最完美的句點！"
        }
    },
    11: {
        "level": 11,
        "title": "第 11 關：新幹線購票與指定席劃位 🚅",
        "kana_group": "進階交通詞彙：新幹線 (しんかんせん)・指定席 (していせき)",
        "kana_tip": "• **指定席 (していせき)**：對號座\n• **自由席 (じゆうせき)**：自由座\n• **のぞみ (Nozomi)**：希望號最速列車",
        "phrase": "のぞみ号の指定席を1枚お願いします。",
        "romaji": "Nozomi-gō no shiteiseki o ichimai onegaishimasu.",
        "phonetic": "【 諾 走 米 溝 諾、喜 貼 衣 ㄙㄟ ㄎㄧ 歐、一 起 買、歐 內 嘎 衣 喜 媽 斯 】",
        "mnemonic_story": (
            "🚅 **口訣故事**：\n"
            "走到 JR 綠色窗口 (みどりの窓口)，想買東京到京都最快的希望號對號座，\n"
            "直接說：**「のぞみ号の指定席を1枚お願いします」**，\n"
            "想要靠窗座位還可以加上：『窓側 (まどがわ / Madogawa) で』！"
        ),
        "card_image": "cards/card_kore_kudasai.jpg",
        "meaning": "One reserved seat ticket for the Nozomi train, please.（請給我一張希望號的指定席車票。）",
        "scenario": "在 JR 綠色窗口或售票機購買新幹線或特急對號座車票。",
        "quiz": {
            "question": "在日本搭乘新幹線想買『對號入座的座位』，日語應該說：",
            "options": ["指定席 (していせき)", "自由席 (じゆうせき)", "立席 (たちせき)", "優先席 (ゆうせんせき)"],
            "answer": "指定席 (していせき)",
            "explanation": "指定席 (Shiteiseki) 即為預約對號座；自由席 (Jiyūseki) 則為自由入座車廂。"
        }
    },
    12: {
        "level": 12,
        "title": "第 12 關：藥妝店急救買退燒止痛藥 💊",
        "kana_group": "醫療常備詞：薬 (くすり)・頭痛 (ずつう)・風邪 (かぜ)",
        "kana_tip": "• **薬 (くすり / Kusuri)**：藥品\n• **頭痛 (ずつう / Zutsū)**：頭痛 (EVE止痛藥必備詞)\n• **風邪 (かぜ / Kaze)**：感冒",
        "phrase": "頭痛薬と風邪薬はどこにありますか？",
        "romaji": "Zutsūyaku to kazegusuri wa doko ni arimasu ka?",
        "phonetic": "【 租 茲 壓 庫、偷、卡 賊 固 酥 哩、哇、多 口 逆、阿里媽斯嘎 】",
        "mnemonic_story": (
            "💊 **口訣故事**：\n"
            "逛街吹風突然頭痛發燒，走進大國藥妝或松本清，\n"
            "問店員：**「頭痛薬はどこですか？」**\n"
            "店員立刻帶你找到 EVE 或大正感冒微粒！"
        ),
        "card_image": "cards/card_kore_kudasai.jpg",
        "meaning": "Where are the headache pills and cold medicines?（請問頭痛藥和感冒藥在哪裡？）",
        "scenario": "日本旅遊突發著涼或偏頭痛時，在藥妝店快速找到合適成藥。",
        "quiz": {
            "question": "頭痛想買止痛藥時，包裝上最常出現的漢字是：",
            "options": ["頭痛薬 / 鎮痛薬", "胃腸薬", "湿布", "目薬"],
            "answer": "頭痛薬 / 鎮痛薬",
            "explanation": "頭痛藥 (Zutsūyaku) 或解熱鎮痛藥是緩解頭痛與發燒最常見的成藥標籤。"
        }
    },
    13: {
        "level": 13,
        "title": "第 13 關：居酒屋隱藏菜單與辛口日本酒 🍶",
        "kana_group": "日本酒風味：甘口 (あまくち)・辛口 (からくち)",
        "kana_tip": "• **甘口 (あまくち)**：帶果香微甜清酒\n• **辛口 (からくち)**：不甜、清爽凜冽的辣口清酒\n• **冷酒 (れいしゅ)**：冰鎮清酒",
        "phrase": "辛口の日本酒でおすすめはありますか？",
        "romaji": "Karakuchi no nihonshu de osusume wa arimasu ka?",
        "phonetic": "【 卡 拉 庫 起 諾、逆 轟 秀、得、歐 酥 酥 妹 哇、阿里媽斯嘎 】",
        "mnemonic_story": (
            "🍶 **口訣故事**：\n"
            "居酒屋喝完啤酒，想來杯道地日本地酒，\n"
            "問居酒屋老闆：**「辛口の日本酒でおすすめはありますか？」**\n"
            "老闆一聽就知道你是行家，立刻拿出鎮店私藏獺祭或十四代！"
        ),
        "card_image": "cards/card_kore_kudasai.jpg",
        "meaning": "Do you have any recommendations for dry Japanese sake?（請問有推薦偏不甜、辛口的日本酒嗎？）",
        "scenario": "在居酒屋或居酒屋專門店品嚐地道日本清酒。",
        "quiz": {
            "question": "日本清酒若標註『辛口 (からくち)』，代表這款清酒的風味通常是：",
            "options": ["清爽乾脆、不甜、酒精感鮮明", "像麻辣鍋一樣辣", "甜度極高如利口酒", "酸度極高像果醋"],
            "answer": "清爽乾脆、不甜、酒精感鮮明",
            "explanation": "日本酒的『辛口 (Karakuchi)』是指糖分低、口感乾脆俐落，並非辣椒的辣！"
        }
    },
    14: {
        "level": 14,
        "title": "第 14 關：日本郵局寄明信片與國際包裹 📮",
        "kana_group": "郵務核心：郵便局 (ゆうびんきょく)・切手 (きって)",
        "kana_tip": "• **切手 (きって / Kitte)**：郵票 (⚠️不是切手！)\n• **航空便 (エアメール)**：國際航空郵件\n• **葉書 (はがき)**：明信片",
        "phrase": "台湾までエアメールで送りたいです。",
        "romaji": "Taiwan made eamēru de okuritai desu.",
        "phonetic": "【 台 灣、媽 得、欸 阿 美 魯 得、歐 庫 哩 踏 衣 得 斯 】",
        "mnemonic_story": (
            "📮 **口訣故事**：\n"
            "買了精美風景明信片，走進紅色標誌的日本郵局 (郵便局)，\n"
            "跟櫃台說：**「台湾までエアメールで送りたいです」**，\n"
            "付大約 100 日圓貼上限定郵票，就能將回憶寄回台灣！"
        ),
        "card_image": "cards/card_kore_kudasai.jpg",
        "meaning": "I would like to send this to Taiwan by airmail.（我想用航空便寄到台灣。）",
        "scenario": "在日本郵局購買郵票、寄送明信片或寄送特產紀念品回家。",
        "quiz": {
            "question": "在日本郵局買『郵票』，日語寫法是：",
            "options": ["切手 (きって)", "切符 (きっぷ)", "小包 (こづつみ)", "封筒 (ふうとう)"],
            "answer": "切手 (きって)",
            "explanation": "切手 (Kitte) 是郵票；切符 (Kippu) 則是車票，千萬不要搞混喔！"
        }
    },
    15: {
        "level": 15,
        "title": "第 15 關：診所就醫症狀描述與量體溫 🏥",
        "kana_group": "症狀描述：熱 (ねつ)・痛い (いたい)・喉 (のど)",
        "kana_tip": "• **熱 (ねつ / Netsu)**：發燒體溫\n• **喉 (のど / Nodo)**：喉嚨\n• **痛い (いたい / Itai)**：疼痛",
        "phrase": "熱があって、喉がとても痛いです。",
        "romaji": "Netsu ga atte, nodo ga totemo itai desu.",
        "phonetic": "【 內 茲 嘎、阿 貼、諾 多 嘎、透 貼 摸、衣 踏 衣 得 斯 】",
        "mnemonic_story": (
            "🏥 **口訣故事**：\n"
            "旅遊途中身體抱恙看診，見到醫生指著喉嚨：\n"
            "**「熱があって、喉がとても痛いです」**，\n"
            "醫生聽了立刻為你開立退燒消炎藥水！"
        ),
        "card_image": "cards/card_kore_kudasai.jpg",
        "meaning": "I have a fever, and my throat hurts very much.（我發燒了，而且喉嚨非常痛。）",
        "scenario": "在耳鼻喉科或內科診所掛號看診時清楚表達生理症狀。",
        "quiz": {
            "question": "告訴日本醫生自己『發燒了』，最標準的表達是：",
            "options": ["熱があります (ねつがあります)", "火があります", "暑いです", "寒いです"],
            "answer": "熱があります (ねつがあります)",
            "explanation": "「熱があります (Netsu ga arimasu)」表示有發燒症狀。"
        }
    },
    16: {
        "level": 16,
        "title": "第 16 關：百貨公司服飾試穿確認 🛍️",
        "kana_group": "購物進階：試着 (しちゃく)・サイズ (Size)",
        "kana_tip": "• **試着 (しちゃく / Shichaku)**：試穿衣服\n• **試着室 (しちゃくしつ)**：更衣室 / 試衣間\n• **サイズ (Saizu)**：尺寸 (S, M, L)",
        "phrase": "これを試着してみてもいいですか？",
        "romaji": "Kore o shichaku shite mite mo ii desu ka?",
        "phonetic": "【 口 咧 歐、喜 洽 庫、喜 貼、米 貼 摸、衣 衣 得 斯 嘎 】",
        "mnemonic_story": (
            "🛍️ **口訣故事**：\n"
            "在 GU 或 LUMINE 挑中一件好看的大衣，\n"
            "日本試衣間前一定要先問店員：\n"
            "**「これを試着してみてもいいですか？」**，\n"
            "店員會微笑遞給你防弄髒妝容的白色面罩並引導進更衣室！"
        ),
        "card_image": "cards/card_kore_kudasai.jpg",
        "meaning": "May I try this on?（請問我可以試穿看看這件嗎？）",
        "scenario": "服飾店進試衣間前禮貌詢問店員。",
        "quiz": {
            "question": "日本女性試穿套頭衣物時，店員遞上的白色薄紙頭套稱為：",
            "options": ["フェイスカバー (Face Cover)", "マスク", "ティッシュ", "タオル"],
            "answer": "フェイスカバー (Face Cover)",
            "explanation": "Face Cover 用來防止臉上口紅粉底沾染新衣，是日本細緻貼心的服務！"
        }
    },
    17: {
        "level": 17,
        "title": "第 17 關：搭計程車指示目的地與口訣 🚕",
        "kana_group": "計程車術語：タクシー・出口 (ぐち)・右 (みぎ)・左 (ひだり)",
        "kana_tip": "• **～までお願いします**：請載我到某地\n• **ここで降ろしてください**：請在這邊讓我下車\n• ⚠️ 日本計程車後門為自動開關，切勿手動推拉！",
        "phrase": "東京駅の八重洲口までお願いします。",
        "romaji": "Tōkyō-eki no Yaesu-guchi made onegaishimasu.",
        "phonetic": "【 偷 ㄎㄧㄡ 欸 ㄎㄧ 諾、壓 欸 酥 姑 起、媽 得、歐 內 嘎 衣 喜 媽 斯 】",
        "mnemonic_story": (
            "🚕 **口訣故事**：\n"
            "大包小包行李搭計程車，上車後司機回頭詢問，\n"
            "你直接說：**「〇〇までお願いします」**，\n"
            "司機立刻俐落開車，直達目的地！"
        ),
        "card_image": "cards/card_kore_kudasai.jpg",
        "meaning": "To the Yaesu exit of Tokyo Station, please.（請載我到東京車站的八重洲出口。）",
        "scenario": "趕飛機、深夜錯過電車或攜帶大型行李搭計程車。",
        "quiz": {
            "question": "日本計程車最特別的乘車禮儀是：",
            "options": ["後車門由司機自動控制開關，乘客不要手動推拉", "必須給司機 15% 小費", "上車必須脫鞋", "副駕駛座不能坐人"],
            "answer": "後車門由司機自動控制開關，乘客不要手動推拉",
            "explanation": "日本計程車左後門由司機連桿操控自動開閉，手動硬拉容易損壞機械！"
        }
    },
    18: {
        "level": 18,
        "title": "第 18 關：特色喫茶店晨間套餐點餐 ☕",
        "kana_group": "早餐美食：モーニング (Morning)・トースト (Toast)",
        "kana_tip": "• **モーニング (Mōningu)**：晨間優惠套餐\n• **ホット (Hotto)**：熱飲\n• **アイス (Aisu)**：冰飲",
        "phrase": "モーニングセットのホットコーヒーで。",
        "romaji": "Mōningu setto no hotto kōhī de.",
        "phonetic": "【 摸 寧 估、ㄙㄟ 偷 諾、火 偷、口 喜 得 】",
        "mnemonic_story": (
            "☕ **口訣故事**：\n"
            "早上 9 點走進復古喫茶店（如 Komeda 客美多），\n"
            "指著晨間菜單說：**「モーニングセット、ホットコーヒーで！」**，\n"
            "點一杯香濃咖啡，立刻免費贈送香脆厚片吐司與現煮水煮蛋！"
        ),
        "card_image": "cards/card_kore_kudasai.jpg",
        "meaning": "The morning set with hot coffee, please.（請給我晨間套餐搭配熱咖啡。）",
        "scenario": "在日本自由行早晨享受道地喫茶店早餐文化。",
        "quiz": {
            "question": "日本名古屋最具代表性的早餐文化是：",
            "options": ["點一杯熱咖啡，免費贈送厚片吐司與水煮蛋", "早上吃生魚片丼飯", "早上喝味噌湯不能配飯", "早餐必須站著吃"],
            "answer": "點一杯熱咖啡，免費贈送厚片吐司與水煮蛋",
            "explanation": "這就是聞名全日本的『モーニング (Morning Service)』晨間特惠文化！"
        }
    },
    19: {
        "level": 19,
        "title": "第 19 關：商務拜訪與電話禮儀開場 💼",
        "kana_group": "職場敬語：お世話 (おせわ)・失礼 (しつれい)",
        "kana_tip": "• **お世話になっております**：承蒙關照 (商務第一神句)\n• **お先に失礼します**：我先下班告退了\n• **少々お待ちください**：請稍候片刻",
        "phrase": "いつも大変お世話になっております。",
        "romaji": "Itsumo taihen osewa ni natte orimasu.",
        "phonetic": "【 一 茲 摸、太 嘿 恩、歐 ㄙㄟ 哇 逆、哪 貼、歐 哩 媽 斯 】",
        "mnemonic_story": (
            "💼 **口訣故事**：\n"
            "接起日本客戶或廠商的電話，\n"
            "開口第一句永遠是：\n"
            "**「いつも大変お世話になっております」**，\n"
            "展現最專業、得體的商業交流素養！"
        ),
        "card_image": "cards/card_kore_kudasai.jpg",
        "meaning": "Thank you very much for your continuous support.（一直以來承蒙您的悉心照顧與關照。）",
        "scenario": "日商職場接聽電話、發送商務 Email 或拜訪客戶的第一句開場白。",
        "quiz": {
            "question": "日本職場下班要離開辦公室時，對還在加班的同事說的禮貌用語是：",
            "options": ["お先に失礼します (我先告退了)", "さようなら", "バイバイ", "お疲れ様でした (只對後輩說)"],
            "answer": "お先に失礼します (我先告退了)",
            "explanation": "「お先に失礼します (Osaki ni shitsurei shimasu)」是日本職場下班最標準的告辭敬語！"
        }
    },
    20: {
        "level": 20,
        "title": "第 20 關：大圓滿終極通關・自由融入日本生活 🎓",
        "kana_group": "大成總結：おかげさまで・大好き・上達",
        "kana_tip": "• **おかげさまで**：多虧大家的照顧與福氣\n• **大好き (だいすき)**：超級喜歡\n• 🏆 恭喜完成全套 20 關自由行與生活會話神功！",
        "phrase": "おかげさまで、日本が大好きになりました！",
        "romaji": "Okagesama de, Nihon ga daisuki ni narimashita!",
        "phonetic": "【 歐 卡 給 撒 媽 得、逆 轟 嘎、代 酥 ㄎㄧ 逆、哪 哩 媽 喜 他 】",
        "mnemonic_story": (
            "🎓 **大圓滿口訣故事**：\n"
            "從五十音零基礎，到能點餐、問路、看懂菜單、應對生活，\n"
            "你微笑對著日本朋友說：\n"
            "**「おかげさまで、日本が大好きになりました！」**\n"
            "這就是語言最美麗的意義——帶你走進全新的世界！"
        ),
        "card_image": "cards/card_quest10_arigatou.jpg",
        "meaning": "Thanks to your kindness, I have grown to love Japan very much!（多虧了大家的關照，讓我超級喜歡日本！）",
        "scenario": "旅程結尾向日本友人、民宿老闆或自己宣布日語學習大圓滿達成！",
        "quiz": {
            "question": "「おかげさまで (Okagesama de)」在日語對話中蘊含的核心情感是：",
            "options": ["謙虛感激：『多虧了您的福氣與照顧』", "責備他人", "自高自大", "單純道別"],
            "answer": "謙虛感激：『多虧了您的福氣與照顧』",
            "explanation": "「おかげさまで」是日本傳統神道與文化中極具代表性的謙卑感恩用語！"
        }
    }
}

