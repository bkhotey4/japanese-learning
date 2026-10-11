# -*- coding: utf-8 -*-
"""
互動測驗題庫：五十音平假名、片假名、情境單字選擇題
"""

QUIZ_QUESTIONS = [
    {
        "category": "五十音（平假名）",
        "question": "請選出平假名「あ」對應的羅馬拼音：",
        "options": ["a", "o", "u", "e"],
        "answer": "a",
        "explanation": "「あ」發音為 a，像是中文的『阿』。"
    },
    {
        "category": "五十音（平假名）",
        "question": "請選出平假名「し」對應的發音：",
        "options": ["shi", "si", "chi", "tsu"],
        "answer": "shi",
        "explanation": "「し」不是 si，而是舌尖放平微吐氣的 shi（西/吸）。"
    },
    {
        "category": "五十音（片假名）",
        "question": "在餐廳菜單常見的「コーヒー」(kōhī) 是指什麼？",
        "options": ["咖啡", "可樂", "啤酒", "紅茶"],
        "answer": "咖啡",
        "explanation": "「コーヒー」(Coffee) 是咖啡，長音符號『ー』表示拉長兩拍。"
    },
    {
        "category": "五十音（片假名）",
        "question": "平假名「さ」對應的片假名是哪一個？",
        "options": ["サ", "シ", "セ", "ソ"],
        "answer": "サ",
        "explanation": "「さ」對應的片假名是「サ」。"
    },
    {
        "category": "旅遊情境",
        "question": "在日本餐廳結帳時，向店員說哪句話最適合？",
        "options": ["お会計をお願いします。", "いただきます。", "ごちそうさまでした。", "すみません、トイレはどこですか？"],
        "answer": "お会計をお願いします。",
        "explanation": "「お会計をお願いします。(Okaikei o onegai shimasu.)」是請幫我結帳的意思。"
    },
    {
        "category": "旅遊情境",
        "question": "在超商或藥妝店買東西，想問「可以退稅嗎？」，應該說：",
        "options": ["免税できますか？", "領収書をください。", "袋はいりません。", "温めてください。"],
        "answer": "免税できますか？",
        "explanation": "「免税できますか？(Menzei dekimasu ka?)」是詢問是否可辦理免稅。"
    },
    {
        "category": "職場情境",
        "question": "在日商公司，下班準備離開時，對還在工作的同事應該說：",
        "options": ["お先に失礼します。", "おやすみなさい。", "バイバイ。", "いただきます。"],
        "answer": "お先に失礼します。",
        "explanation": "「お先に失礼します。(我先失陪/下班了)」是日本職場不可或缺的下班禮儀。"
    },
    {
        "category": "生活情境",
        "question": "在超商買便當時，店員常問是否需要加熱，想要加熱時說：",
        "options": ["温めてください。", "冷やしてください。", "袋はいりません。", "別々でお願いします。"],
        "answer": "温めてください。",
        "explanation": "「温めてください。(Atatame te kudasai.)」表示請幫我微波加熱。"
    },
    {
        "category": "五十音（平假名）",
        "question": "請選出平假名「つ」對應的發音：",
        "options": ["tsu", "su", "chi", "tu"],
        "answer": "tsu",
        "explanation": "「つ」不是 tu，是舌尖抵齒後吐氣發 tsu（疵/次）。"
    },
    {
        "category": "五十音（平假名）",
        "question": "請選出平假名「ふ」對應的羅馬拼音：",
        "options": ["fu", "hu", "pu", "bu"],
        "answer": "fu",
        "explanation": "「ふ」不咬下唇，上下唇靠近微吹氣發 fu。"
    },
    {
        "category": "五十音（平假名）",
        "question": "平假名「ぬ」與「ね」，哪個字尾巴有蜷曲的小圓圈？",
        "options": ["兩個都有", "只有ぬ有", "只有ね有", "兩個都沒有"],
        "answer": "兩個都有",
        "explanation": "「ぬ」(nu) 與「ね」(ne) 右下角都有打結的小圈圈！ぬ像一碗拉麵，ね像貓咪捲尾巴。"
    },
    {
        "category": "五十音（平假名）",
        "question": "請選出平假名「を」在現代日語中的正確發音：",
        "options": ["o (同お)", "wo (我)", "wa (哇)", "n (嗯)"],
        "answer": "o (同お)",
        "explanation": "「を」僅作為受詞助詞使用（如 みず を のむ），現代發音同「お (o)」。"
    },
    {
        "category": "五十音（片假名）",
        "question": "平假名「あ」對應的片假名是哪一個？",
        "options": ["ア", "イ", "ウ", "オ"],
        "answer": "ア",
        "explanation": "「あ」對應片假名「ア」，取自楷書「阿」的左耳偏旁。"
    },
    {
        "category": "五十音（片假名）",
        "question": "日本招牌常見的「ラーメン」(Rāmen) 中，「ラ」是哪一行的假名？",
        "options": ["ら行 (ra)", "わ行 (wa)", "や行 (ya)", "ま行 (ma)"],
        "answer": "ら行 (ra)",
        "explanation": "「ラ」是ら行平假名「ら」對應的片假名，源自草書「良」之初筆。"
    },
    {
        "category": "五十音（片假名）",
        "question": "片假名「シ」與「ツ」常讓人混淆，三點筆畫主要由下往上提的是哪一個？",
        "options": ["シ (shi)", "ツ (tsu)", "ン (n)", "ソ (so)"],
        "answer": "シ (shi)",
        "explanation": "「シ」(shi) 最下一筆由下往上提；而「ツ」(tsu) 是由上往下落筆！"
    },
    {
        "category": "五十音（平假名）",
        "question": "日語鼻音（撥音）「ん」在發音時佔幾拍？",
        "options": ["一整拍", "半拍", "不佔拍子", "兩拍"],
        "answer": "一整拍",
        "explanation": "「ん」(n) 在日語節奏中佔完整的一拍！例如「に・ほ・ん」共有三拍。"
    }
]

def get_quizzes_by_category(category: str = "all") -> list:
    if category == "kana":
        return [q for q in QUIZ_QUESTIONS if "五十音" in q["category"]]
    elif category == "scenario":
        return [q for q in QUIZ_QUESTIONS if "情境" in q["category"]]
    return QUIZ_QUESTIONS

