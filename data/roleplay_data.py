# -*- coding: utf-8 -*-
"""
日語實戰情境角色扮演對話資料庫 (Roleplay Data)
提供拉麵店、飯店入住、超商結帳、居酒屋四大場景的分支對話樹。
每個對話步驟包含 NPC 發言、假名、中文翻譯與玩家的多個按鈕選項。
"""

ROLEPLAY_SCENARIOS = {
    "ramen": {
        "title": "🍜 日本拉麵店點餐實戰",
        "badge": "master_ramen",
        "description": "走進道地的日本拉麵小店，老闆親切地向你招呼並詢問用餐偏好...",
        "steps": [
            {
                "npc": "いらっしゃいませ！何名様ですか？",
                "furigana": "いらっしゃいませ！なんめいさまですか？",
                "romaji": "Irasshaimase! Nan-mei-sama desu ka?",
                "translation": "歡迎光臨！請問幾位呢？",
                "options": [
                    {
                        "label": "1 位 (ひとりです)",
                        "furigana": "ひとりです",
                        "romaji": "Hitori desu.",
                        "meaning": "一位。",
                        "next_step": 1,
                        "npc_reaction": "カウンター席へどうぞ！（請往吧台座位入座！）"
                    },
                    {
                        "label": "2 位 (ふたりです)",
                        "furigana": "ふたりです",
                        "romaji": "Futari desu.",
                        "meaning": "兩位。",
                        "next_step": 1,
                        "npc_reaction": "こちらのテーブル席へどうぞ！（請往這邊的桌位入座！）"
                    }
                ]
            },
            {
                "npc": "麺の硬さはどうされますか？",
                "furigana": "めんのかたさはどうされますか？",
                "romaji": "Men no katasa wa dō saremasu ka?",
                "translation": "麵的硬度想要哪一種呢？",
                "options": [
                    {
                        "label": "硬め (かため)",
                        "furigana": "かためでおねがいします",
                        "romaji": "Katame de onegaishimasu.",
                        "meaning": "請幫我做偏硬的麵。",
                        "next_step": 2,
                        "npc_reaction": "はい、麺硬めですね！スープの濃さは？（好的，偏硬！那湯頭濃度呢？）"
                    },
                    {
                        "label": "普通 (ふつう)",
                        "furigana": "ふつうでおねがいします",
                        "romaji": "Futsū de onegaishimasu.",
                        "meaning": "一般硬度就好。",
                        "next_step": 2,
                        "npc_reaction": "かしこまりました！普通ですね。（好的！一般硬度。）"
                    }
                ]
            },
            {
                "npc": "トッピングの煮玉子はいかがですか？",
                "furigana": "トッピングのにたまごはいかがですか？",
                "romaji": "Toppingu no nitamago wa ikaga desu ka?",
                "translation": "要加點溏心蛋配料嗎？",
                "options": [
                    {
                        "label": "要加 (お願いします)",
                        "furigana": "おねがいします",
                        "romaji": "Onegaishimasu.",
                        "meaning": "好的，請幫我加！",
                        "next_step": 3,
                        "npc_reaction": "煮玉子一つですね！少々お待ちください。（溏心蛋一份！請稍候片刻。）"
                    },
                    {
                        "label": "不用了 (大丈夫です)",
                        "furigana": "だいじょうぶです",
                        "romaji": "Daijōbu desu.",
                        "meaning": "不用了，謝謝。",
                        "next_step": 3,
                        "npc_reaction": "承知いたしました！すぐにお作りします。（瞭解！馬上為您製作。）"
                    }
                ]
            },
            {
                "npc": "お待たせいたしました！特製ラーメンです。ごゆっくりどうぞ！",
                "furigana": "おまたせいたしました！とくせいラーメンです。ごゆっくりどうぞ！",
                "romaji": "Omatase itashimashita! Tokusei rāmen desu. Goyukkuri dōzo!",
                "translation": "讓您久等了！這是您的特製拉麵。請慢用！",
                "options": [
                    {
                        "label": "いただきます！",
                        "furigana": "いただきます",
                        "romaji": "Itadakimasu!",
                        "meaning": "我要開動了！（日本用餐最高禮儀）",
                        "next_step": "end",
                        "npc_reaction": "ごゆっくり召し上がれ！🍜（請慢慢享用！恭喜完成拉麵店點餐實戰！）"
                    }
                ]
            }
        ]
    },
    "hotel": {
        "title": "🏨 飯店辦理入住 (Check-in) 實戰",
        "badge": "master_hotel",
        "description": "抵達日本下榻飯店，櫃台人員禮貌地向你鞠躬問候...",
        "steps": [
            {
                "npc": "いらっしゃいませ。チェックインでございますか？",
                "furigana": "いらっしゃいませ。チェックインでございますか？",
                "romaji": "Irasshaimase. Chekkuin de gozaimasu ka?",
                "translation": "歡迎光臨。請問是要辦理入住登記嗎？",
                "options": [
                    {
                        "label": "是的，我有預約 (はい、予約しています)",
                        "furigana": "はい、よやくしています",
                        "romaji": "Hai, yoyaku shiteimasu.",
                        "meaning": "是的，我有事先預約。",
                        "next_step": 1,
                        "npc_reaction": "ご予約ありがとうございます。（感謝您的預約。）"
                    },
                    {
                        "label": "我有預約名字是... (予約した〇〇です)",
                        "furigana": "よやくした〇〇です",
                        "romaji": "Yoyaku shita 〇〇 desu.",
                        "meaning": "我有預約，名字是...",
                        "next_step": 1,
                        "npc_reaction": "確認が取れました。（已為您確認預約資訊。）"
                    }
                ]
            },
            {
                "npc": "パスポートをお預かりできますでしょうか？",
                "furigana": "パスポートをおあずかりできますでしょうか？",
                "romaji": "Pasupōto o oazukari dekimasu deshō ka?",
                "translation": "可以借看一下您的護照嗎？",
                "options": [
                    {
                        "label": "好的，給您 (はい、どうぞ)",
                        "furigana": "はい、どうぞ",
                        "romaji": "Hai, dōzo.",
                        "meaning": "好的，請拿去。",
                        "next_step": 2,
                        "npc_reaction": "ありがとうございます。コピーを取らせていただきます。（謝謝您，借印一份複本。）"
                    }
                ]
            },
            {
                "npc": "こちらがお部屋のカードキーと朝食券でございます。チェックアウトは11時です。",
                "furigana": "こちらがおへやのカードキーとちょうしょくけんでございます。チェックアウトはじゅういちじです。",
                "romaji": "Kochira ga oheya no kādokī to chōshokuken de gozaimasu. Chekkuauto wa jūichiji desu.",
                "translation": "這是您的房間房卡與早餐券。退房時間是上午 11 點。",
                "options": [
                    {
                        "label": "謝謝 (ありがとうございます)",
                        "furigana": "ありがとうございます",
                        "romaji": "Arigatō gozaimasu.",
                        "meaning": "非常感謝！",
                        "next_step": 3,
                        "npc_reaction": "他にご質問はございますか？（請問還有其他問題嗎？）"
                    },
                    {
                        "label": "WiFi 密碼在哪？(Wi-Fiのパスワードは？)",
                        "furigana": "Wi-Fiのパスワードはどこですか？",
                        "romaji": "Waifai no pasuwādo wa doko desu ka?",
                        "meaning": "請問 Wi-Fi 密碼在哪裡？",
                        "next_step": 3,
                        "npc_reaction": "カードキーの裏面に記載されております！（印在房卡背面喔！）"
                    }
                ]
            },
            {
                "npc": "それでは、ごゆっくりお寛ぎくださいませ！",
                "furigana": "それでは、ごゆっくりおくつろぎくださいませ！",
                "romaji": "Soredeha, goyukkuri okutsurogi kudasaimase!",
                "translation": "那麼，祝您住宿愉快、好好放鬆休息！",
                "options": [
                    {
                        "label": "感謝！(お世話になります)",
                        "furigana": "おせわになります",
                        "romaji": "Osewa ni narimasu.",
                        "meaning": "這幾天承蒙關照了！",
                        "next_step": "end",
                        "npc_reaction": "よいご滞在を！✨（祝您旅途愉快！恭喜順利完成入住實戰！）"
                    }
                ]
            }
        ]
    },
    "convenience": {
        "title": "🏪 日本超商結帳生存實戰",
        "badge": "master_convenience",
        "description": "拿著飯糰與炸雞到 Lawson/7-11 櫃台結帳，店員連珠炮提問...",
        "steps": [
            {
                "npc": "いらっしゃいませ。お弁当、温めますか？",
                "furigana": "いらっしゃいませ。おべんとう、あたためますか？",
                "romaji": "Irasshaimase. Obentō, atatamemasu ka?",
                "translation": "歡迎光臨。請問便當需要加熱嗎？",
                "options": [
                    {
                        "label": "請幫我加熱 (温めてください)",
                        "furigana": "あたためてください",
                        "romaji": "Atatamete kudasai.",
                        "meaning": "請幫我微波加熱。",
                        "next_step": 1,
                        "npc_reaction": "はい、少々お待ちくださいね。（好的，請稍候片刻喔。）"
                    },
                    {
                        "label": "不用加熱 (そのままでいいです)",
                        "furigana": "そのままでいいです",
                        "romaji": "Sono mama de ii desu.",
                        "meaning": "這樣直接吃就可以。",
                        "next_step": 1,
                        "npc_reaction": "かしこまりました。（好的了解。）"
                    }
                ]
            },
            {
                "npc": "レジ袋はご利用になりますか？",
                "furigana": "レジぶくろはごりようになりますか？",
                "romaji": "Rejibukuro wa goriyō ni narimasu ka?",
                "translation": "請問需要塑膠提袋嗎？",
                "options": [
                    {
                        "label": "不用袋子 (袋は大丈夫です)",
                        "furigana": "ふくろはだいじょうぶです",
                        "romaji": "Fukuro wa daijōbu desu.",
                        "meaning": "不用塑膠袋，謝謝。",
                        "next_step": 2,
                        "npc_reaction": "テープをお貼りしますね。（那幫您貼上已結帳貼紙喔。）"
                    },
                    {
                        "label": "請給我一個 (一枚お願いします)",
                        "furigana": "いちまいおねがいします",
                        "romaji": "Ichimai onegaishimasu.",
                        "meaning": "請給我一個塑膠袋。",
                        "next_step": 2,
                        "npc_reaction": "はい、3円いただきます。（好的，提袋加收3日圓。）"
                    }
                ]
            },
            {
                "npc": "お会計、750円でございます。お支払い方法はどうされますか？",
                "furigana": "おかいけい、ななひゃくごじゅうえんでございます。おしはらいほうほうはどうされますか？",
                "romaji": "Okaikei, nanahyaku gojū-en de gozaimasu. Oshiharai hōhō wa dō saremasu ka?",
                "translation": "一共是 750 日圓。請問要用哪種方式付款？",
                "options": [
                    {
                        "label": "Suica / 西瓜卡 (Suicaで)",
                        "furigana": "スイカで",
                        "romaji": "Suica de.",
                        "meaning": "用交通卡/西瓜卡嗶卡結帳。",
                        "next_step": "end",
                        "npc_reaction": "ピッ！お支払い完了です。ありがとうございました！（嗶！付款完成，非常感謝您！）"
                    },
                    {
                        "label": "付現 (現金で)",
                        "furigana": "げんきんで",
                        "romaji": "Genkin de.",
                        "meaning": "用日圓現金支付。",
                        "next_step": "end",
                        "npc_reaction": "1000円お預かりします。250円のお返しです。ありがとうございました！（收您1000日圓，找您250日圓。非常感謝！）"
                    }
                ]
            }
        ]
    },
    "izakaya": {
        "title": "🏮 居酒屋乾杯實戰",
        "badge": "master_izakaya",
        "description": "走進熱鬧溫馨的日本居酒屋，感受最道地的飲酒社交文化...",
        "steps": [
            {
                "npc": "いらっしゃい！お飲み物、まず何にされますか？",
                "furigana": "いらっしゃい！おのみもの、まずなににされますか？",
                "romaji": "Irasshai! Onomimono, mazu nani ni saremasu ka?",
                "translation": "歡迎光臨！首先要先來點什麼喝的嗎？",
                "options": [
                    {
                        "label": "總之先來杯生啤！(とりあえず生ビールで！)",
                        "furigana": "とりあえずなまビールで！",
                        "romaji": "Toriaezu nama biiru de!",
                        "meaning": "日本經典第一句：總之先來杯生啤酒！",
                        "next_step": 1,
                        "npc_reaction": "生一つね！すぐお持ちします！（生啤一杯！馬上來！）"
                    },
                    {
                        "label": "來杯烏龍茶 (ウーロン茶をお願いします)",
                        "furigana": "ウーロンちゃをおねがいします",
                        "romaji": "Ūroncha o onegaishimasu.",
                        "meaning": "不喝酒也沒問題：請給我一杯烏龍茶。",
                        "next_step": 1,
                        "npc_reaction": "ウーロン茶かしこまりました！（烏龍茶好的！）"
                    }
                ]
            },
            {
                "npc": "こちらお通しの枝豆とビールです！ご注文はお決まりですか？",
                "furigana": "こちらおとおしのえだまめとビールです！ごちゅうもんはあきまりですか？",
                "romaji": "Kochira otōshi no edamame to bīru desu! Gochūmon wa okimari desu ka?",
                "translation": "這是開胃小菜毛豆與啤酒！請問決定好要點什麼餐點了嗎？",
                "options": [
                    {
                        "label": "推薦什麼？(おすすめは何ですか？)",
                        "furigana": "おすすめはなんですか？",
                        "romaji": "Osusume wa nan desu ka?",
                        "meaning": "請問店裡的招牌推薦是什麼呢？",
                        "next_step": 2,
                        "npc_reaction": "今日は焼き鳥盛り合わせがイチオシですよ！（今天最推薦綜合烤雞肉串拼盤喔！）"
                    },
                    {
                        "label": "請再給我一下時間 (もう少し時間をください)",
                        "furigana": "もうすこしじかんをください",
                        "romaji": "Mō sukoshi jikan o kudasai.",
                        "meaning": "我還在看菜單，請再給我一點時間。",
                        "next_step": 2,
                        "npc_reaction": "はい、決まりましたらお呼びくださいね！（好的，決定好了再叫我喔！）"
                    }
                ]
            },
            {
                "npc": "はーい！焼き鳥盛り合わせですね！塩とタレ、どちらにされますか？",
                "furigana": "はーい！やきとりもりあわせですね！しおとタレ、どちらにされますか？",
                "romaji": "Hāi! Yakitori moriawase desu ne! Shio to tare, dochira ni saremasu ka?",
                "translation": "好嘞！綜合烤雞肉串一份！口味要選鹽烤還是醬燒呢？",
                "options": [
                    {
                        "label": "鹽烤 (塩で)",
                        "furigana": "しおでおねがいします",
                        "romaji": "Shio de onegaishimasu.",
                        "meaning": "原汁原味：請做鹽烤口味。",
                        "next_step": "end",
                        "npc_reaction": "塩ですね！乾杯（かんぱい）！おいしい夜を！（鹽烤好的！乾杯！祝您度過美好的一夜！居酒屋實戰通關！）"
                    },
                    {
                        "label": "醬燒 (タレで)",
                        "furigana": "タレでおねがいします",
                        "romaji": "Tare de onegaishimasu.",
                        "meaning": "經典濃郁：請做醬燒口味。",
                        "next_step": "end",
                        "npc_reaction": "タレですね！乾杯（かんぱい）！じっくり焼きますね！（醬燒好的！乾杯！為您精心現烤！居酒屋實戰通關！）"
                    }
                ]
            }
        ]
    }
}
