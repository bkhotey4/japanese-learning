# -*- coding: utf-8 -*-
"""
神社御神籤 (Omikuji) 資料庫
包含大吉、中吉、小吉、吉、末吉等多樣化運勢，
結合古風日語諺語、哲理名言、發音、中文解說與今日開運物！
"""

OMIKUJI_DATA = [
    {
        "id": "daikichi_1",
        "fortune": "大吉 (Daikichi)",
        "color": 0xFF4500, # 橙紅色
        "quote": "果報は寝て待て",
        "romaji": "Kahou wa nete mate",
        "meaning": "好事多磨，靜候佳音。好運自然會降臨，放寬心胸順其自然即是最好的安排。",
        "lucky_item": "熱抹茶拿鐵 (抹茶ラテ)",
        "lucky_word": "希望 (きぼう / kibou)",
        "detail": "願望：順風順水，持之以恆必能成真。\n學習：靈感湧現，今天適合隨心聽聽喜歡的日語歌曲！\n旅行：出門遇貴人，旅途平安愉快。"
    },
    {
        "id": "daikichi_2",
        "fortune": "大吉 (Daikichi)",
        "color": 0xFF4500,
        "quote": "一期一会",
        "romaji": "Ichigo ichie",
        "meaning": "一生僅有一次的珍貴相遇。珍惜眼前的每一個瞬間與遇見的人事物。",
        "lucky_item": "御守鑰匙圈 (お守り)",
        "lucky_word": "感謝 (かんしゃ / kansha)",
        "detail": "願望：把握良機，勇敢邁出第一步！\n學習：今天吸收力極佳，假名與單字過目不忘。\n人際：會遇見投緣的朋友或獲得意外的溫暖鼓勵。"
    },
    {
        "id": "chukichi_1",
        "fortune": "中吉 (Chukichi)",
        "color": 0xFF8C00, # 深橙
        "quote": "笑う門には福来る",
        "romaji": "Warau kado ni wa fuku kitaru",
        "meaning": "笑口常開，福氣自來。保持愉快開朗的心情，好運就會被你吸引！",
        "lucky_item": "可口的草莓蛋糕 (ショートケーキ)",
        "lucky_word": "笑顔 (えがお / egao)",
        "detail": "願望：急躁則慢，微笑應對，水到渠成。\n學習：邊聽輕音樂邊學，效果倍增。\n健康：多伸展筋骨，喝杯熱茶放鬆身心。"
    },
    {
        "id": "chukichi_2",
        "fortune": "中吉 (Chukichi)",
        "color": 0xFF8C00,
        "quote": "千里の道も一歩から",
        "romaji": "Senri no michi mo ippo kara",
        "meaning": "千里之行，始於足下。任何偉大的目標，都是由微小的累積開始。",
        "lucky_item": "白色帆布鞋 (スニーカー)",
        "lucky_word": "一歩 (いっぽ / ippo)",
        "detail": "願望：腳踏實地，不用焦慮，每一步都算數！\n學習：今天哪怕只背一個假名或單字，都是巨大的進步。\n財運：細水長流，理性消費會有意外小確幸。"
    },
    {
        "id": "shokichi_1",
        "fortune": "小吉 (Shokichi)",
        "color": 0x32CD32, # 萊姆綠
        "quote": "雨降って地固まる",
        "romaji": "Ame futte ji katamaru",
        "meaning": "不經風雨，怎見彩虹（下雨後地面更結實）。經歷挫折反而能讓基底更穩固。",
        "lucky_item": "折疊傘或雨具 (折りたたみ傘)",
        "lucky_word": "絆 (きずな / kizuna)",
        "detail": "願望：遇到小插曲別灰心，這正是讓事情變得更圓滿的契機。\n學習：之前記混的假名，今天重看一眼就會恍然大悟。\n日常：宜早點休息，泡個熱水澡。"
    },
    {
        "id": "kichi_1",
        "fortune": "吉 (Kichi)",
        "color": 0x1E90FF, # 道奇藍
        "quote": "急がば回れ",
        "romaji": "Isogaba maware",
        "meaning": "欲速則不達，繞道反而更快。按部就班穩健前行，才是最有效率的捷徑。",
        "lucky_item": "手沖咖啡 (ドリップコーヒー)",
        "lucky_word": "落ち着く (おちつく / ochitsuku)",
        "detail": "願望：放慢步調，看清全局再行動更安全。\n學習：不用追求一天學很多，輕鬆看一眼就能自然內化。\n人際：耐心傾聽，會收穫滿滿的信賴感。"
    },
    {
        "id": "suekichi_1",
        "fortune": "末吉 (Suekichi)",
        "color": 0x9370DB, # 紫色
        "quote": "待てば海路の日和あり",
        "romaji": "Mateba kairo no biyori ari",
        "meaning": "耐心等待，終會迎來適合出海的晴朗好天氣。黎明前的寧靜，蓄勢待發。",
        "lucky_item": "熱烘烘的拉麵 (熱いラーメン)",
        "lucky_word": "未来 (みらい / mirai)",
        "detail": "願望：眼下先養精蓄銳，好時機即將在轉角處出現。\n學習：今天放空休息也完全沒問題！給大腦充電。\n日常：整理一下書桌或手機相簿，能帶來清新好心情。"
    }
]

def draw_omikuji():
    import random
    return random.choice(OMIKUJI_DATA)
