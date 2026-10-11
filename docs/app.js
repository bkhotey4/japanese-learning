/* 日語學習道場 — 由 Discord bot 移植的靜態網站。資料來自 data.js（tools/export_web_data.py 產生）。 */
(() => {
  "use strict";
  const D = window.JP_DATA;
  const $app = document.getElementById("app");

  /* ---------------- 工具 ---------------- */
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  // 把 bot 內 Discord markdown（**粗體**、`code`、*斜體*、### 標題）轉成 HTML
  const md = (s) => esc(s)
    .split("\n")
    .map((line) => {
      const h = line.match(/^#{1,3}\s+(.*)$/);
      return h ? `<h4>${h[1]}</h4>` : line;
    })
    .join("<br>")
    .replace(/<\/h4><br>/g, "</h4>")
    .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/(^|[^*])\*([^*\s][^*]*?)\*(?!\*)/g, "$1<i>$2</i>");
  const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const pick = (a) => a[Math.floor(Math.random() * a.length)];
  const todayStr = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
  const dayIndex = () => Math.floor(Date.now() / 86400000);

  function toast(msg) {
    const t = document.getElementById("toast");
    t.textContent = msg;
    t.classList.remove("hidden");
    clearTimeout(toast._t);
    toast._t = setTimeout(() => t.classList.add("hidden"), 2600);
  }

  /* ---------------- 語音（瀏覽器內建 TTS，取代 bot 的 edge-tts） ---------------- */
  let jaVoice = null;
  function loadVoices() {
    const vs = speechSynthesis.getVoices().filter((v) => v.lang && v.lang.toLowerCase().startsWith("ja"));
    jaVoice = vs.find((v) => /Nanami|Google|Kyoko|Haruka/i.test(v.name)) || vs[0] || null;
  }
  if ("speechSynthesis" in window) { loadVoices(); speechSynthesis.onvoiceschanged = loadVoices; }
  // 去掉中文註解、羅馬拼音括號等，只念日文
  const speakable = (s) => String(s || "")
    .replace(/[（(][^）)]*[A-Za-z一-鿿][^）)]*[）)]/g, (m) => (/[぀-ヿ]/.test(m) && !/[A-Za-z]/.test(m) ? m : ""))
    .replace(/[【】『』「」*`#]/g, "")
    .replace(/[A-Za-z]+/g, "")
    .trim();
  function speak(text, rate) {
    if (!("speechSynthesis" in window)) { toast("此瀏覽器不支援語音朗讀"); return; }
    const t = speakable(text);
    if (!t) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(t);
    u.lang = "ja-JP";
    if (jaVoice) u.voice = jaVoice;
    u.rate = rate || Number(localStorage.getItem("jp_rate") || 0.8);
    speechSynthesis.speak(u);
  }
  const speakBtn = (text, label = "🔊") => `<button class="btn small speak" data-speak="${esc(text)}" title="朗讀">${label}</button>`;
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-speak]");
    if (b) { e.preventDefault(); speak(b.dataset.speak, b.dataset.rate ? Number(b.dataset.rate) : undefined); }
  });

  /* ---------------- 發音評分（瀏覽器語音辨識） ---------------- */
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  // alt：同一句的假名寫法，辨識結果是假名或漢字都能對得上
  const micBtn = (text, alt = "") => SR
    ? `<button class="btn small mic" data-mic="${esc(text)}" data-alt="${esc(alt)}" title="念出來，幫你打分數">🎤 跟讀評分</button>` : "";
  const normJa = (s) => String(s || "")
    .replace(/[（(][^）)]*[）)]/g, "")
    .replace(/[\s、。，,.!！?？～〜「」『』【】・…ー\-*`]/g, "")
    .replace(/[ァ-ヶ]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0x60));
  function lcsMask(a, b) {
    const dp = Array.from({ length: a.length + 1 }, () => new Array(b.length + 1).fill(0));
    for (let i = a.length - 1; i >= 0; i--) for (let j = b.length - 1; j >= 0; j--)
      dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
    const hit = new Array(a.length).fill(false);
    for (let i = 0, j = 0; i < a.length && j < b.length;) {
      if (a[i] === b[j]) { hit[i] = true; i++; j++; } else if (dp[i + 1][j] >= dp[i][j + 1]) i++; else j++;
    }
    return { len: dp[0][0], hit };
  }
  function scoreSpeech(targets, heard) {
    let best = { score: 0, target: targets[0], hit: [] };
    for (const t of targets.filter(Boolean)) {
      const a = normJa(t);
      for (const h of heard) {
        const b = normJa(h);
        if (!a || !b) continue;
        const { len, hit } = lcsMask(a, b);
        const score = Math.round((len / a.length) * (len / b.length) * 100); // 念到的比例 × 沒多念的比例
        if (score > best.score) best = { score, target: a, hit, heard: h };
      }
    }
    return best;
  }
  let recog = null;
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-mic]");
    if (!b) return;
    e.preventDefault();
    if (recog) { recog.abort(); recog = null; }
    if ("speechSynthesis" in window) speechSynthesis.cancel();
    const holder = b.closest(".row") || b.parentElement;
    let out = holder.nextElementSibling;
    if (!out || !out.classList.contains("mic-result")) { out = document.createElement("div"); out.className = "mic-result"; holder.after(out); }
    out.innerHTML = `<div class="box small">🎙️ 正在聽…請念：<span class="jp">${esc(b.dataset.mic)}</span></div>`;
    const label = b.textContent;
    b.textContent = "🔴 錄音中…";
    recog = new SR();
    recog.lang = "ja-JP";
    recog.maxAlternatives = 5;
    recog.interimResults = false;
    recog.onresult = (ev) => {
      const heard = Array.from(ev.results[0]).map((r) => r.transcript);
      const r = scoreSpeech([b.dataset.mic, b.dataset.alt], heard);
      const grade = r.score >= 90 ? ["🌸 完美！", "ok"] : r.score >= 70 ? ["👍 很不錯！", "ok"] : r.score >= 40 ? ["💪 再試一次！", "bad"] : ["🤔 聽不太出來，慢慢念看看", "bad"];
      const diff = [...r.target].map((c, i) => `<span style="color:var(${r.hit[i] ? "--ok" : "--bad"});font-weight:700">${esc(c)}</span>`).join("");
      out.innerHTML = `<div class="feedback ${grade[1]}"><div class="spread"><b>${grade[0]}</b><b style="font-size:1.4rem">${r.score} 分</b></div>
        <div class="small">目標：<span class="jp">${diff}</span>（紅字＝沒念到或念不清楚）</div>
        <div class="small muted">聽到：${esc(r.heard || heard[0] || "")}</div></div>`;
      P.micTries = (P.micTries || 0) + 1;
      if (r.score > (P.micBest || 0)) P.micBest = r.score;
      save();
      activity();
      if (r.score >= 80) unlock("badge_shadowing");
    };
    recog.onerror = (ev) => {
      const msg = ev.error === "not-allowed" || ev.error === "service-not-allowed" ? "麥克風權限被拒絕，請在瀏覽器網址列允許使用麥克風。"
        : ev.error === "no-speech" ? "沒有聽到聲音，請靠近麥克風再試一次。" : `語音辨識失敗（${ev.error}），建議使用 Chrome 或 Edge。`;
      out.innerHTML = `<div class="feedback bad small">${msg}</div>`;
    };
    recog.onend = () => { b.textContent = label; recog = null; };
    try { recog.start(); } catch { b.textContent = label; }
  });

  /* ---------------- 學習進度（localStorage，取代 user_progress.json） ---------------- */
  const KEY = "jp_progress_v1";
  const blank = () => ({ level: 1, completed: [], streak: 0, lastDate: null, badges: [], mistakes: [], answered: 0, correct: 0 });
  let P;
  try { P = Object.assign(blank(), JSON.parse(localStorage.getItem(KEY) || "{}")); } catch { P = blank(); }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(P)); } catch { /* 私密模式 */ } renderStat(); };

  function unlock(id) {
    if (!D.badges[id] || P.badges.includes(id)) return;
    P.badges.push(id);
    save();
    toast(`🎖️ 解鎖成就：${D.badges[id].name}`);
  }
  // 每日打卡：累積天數只增不減（同 bot 規則）
  function activity() {
    const t = todayStr();
    if (P.lastDate !== t) { P.streak += 1; P.lastDate = t; save(); }
    P.days = P.days || [];
    if (!P.days.includes(t)) { P.days.push(t); save(); }
    unlock("first_step");
    if (P.streak >= 3) unlock("badge_streak_3");
    if (P.streak >= 7) unlock("badge_streak_7");
    const wd = new Date().getDay();
    if (wd === 0 || wd === 6) unlock("badge_weekend");
  }
  function completeLevel(n) {
    if (!P.completed.includes(n)) P.completed.push(n);
    if (P.level === n && n < 20) P.level = n + 1;
    save();
    if (P.completed.length >= 10) unlock("badge_quest_master");
    if (P.completed.length >= 20) unlock("badge_quest_20");
  }
  function addMistake(q) {
    if (!P.mistakes.some((m) => m.question === q.question)) {
      P.mistakes.push({ question: q.question, answer: q.answer, explanation: q.explanation, options: q.options });
      save();
    }
  }
  function renderStat() {
    document.getElementById("statPill").textContent = `🔥 累積 ${P.streak} 天 · ⚔️ 第 ${P.level} 關 · 🎖️ ${P.badges.length}`;
  }

  /* ---------------- 共用：選擇題元件 ---------------- */
  // q: {question, options, answer, explanation}; onDone(correct)
  function mountQuiz(el, q, { onDone, trackMistake = true, nextLabel, onNext } = {}) {
    const opts = shuffle(q.options);
    el.innerHTML = `
      <div class="md jp-q">${md(q.question)}</div>
      <div class="options">${opts.map((o, i) => `<button class="option" data-i="${i}">${esc(o)}</button>`).join("")}</div>
      <div class="fb"></div>`;
    el.querySelectorAll(".option").forEach((b) => b.addEventListener("click", () => {
      const chosen = opts[Number(b.dataset.i)];
      const ok = chosen === q.answer;
      el.querySelectorAll(".option").forEach((x) => {
        x.disabled = true;
        const v = opts[Number(x.dataset.i)];
        if (v === q.answer) x.classList.add("correct");
        else if (x === b) x.classList.add("wrong");
      });
      P.answered += 1; if (ok) P.correct += 1; save();
      activity();
      if (!ok && trackMistake) addMistake(q);
      el.querySelector(".fb").innerHTML = `
        <div class="feedback ${ok ? "ok" : "bad"}">
          <b>${ok ? "⭕ 答對了！" : `❌ 正確答案：${esc(q.answer)}`}</b>
          ${q.explanation ? `<div class="md small" style="margin-top:4px">${md(q.explanation)}</div>` : ""}
          ${!ok && trackMistake ? `<div class="small muted">已加入錯題本 🔄</div>` : ""}
        </div>
        ${onNext ? `<div class="row" style="margin-top:10px"><button class="btn primary nx">${nextLabel || "下一題 ➡️"}</button></div>` : ""}`;
      if (onNext) el.querySelector(".nx").addEventListener("click", onNext);
      onDone && onDone(ok);
    }));
  }

  /* ---------------- 頁面 ---------------- */
  const NAV = [
    ["", "🏠 首頁"], ["daily", "🗓️ 挑戰"], ["cards", "🃏 單字卡"], ["quest", "⚔️ 闖關"], ["kana", "🔤 五十音"], ["quiz", "🎯 測驗"],
    ["talk", "🍜 會話"], ["grammar", "🧩 文法"], ["speak", "🗣️ 跟讀"], ["travel", "✈️ 旅遊"],
    ["anime", "🎌 動漫"], ["songs", "🎐 童謡"], ["news", "📰 新聞"], ["plan", "📋 計畫"], ["me", "👑 我的"],
  ];

  const pages = {};

  /* ---------------- 新手引導：依學習目標推薦路線 ---------------- */
  const GOALS = {
    travel: { icon: "✈️", name: "日本自由行", desc: "點餐、購物、問路、退稅", steps: [
      ["quest/1", "⚔️ 第 1 關：これ、ください", "最萬用的點餐神句"], ["talk/ramen", "🍜 拉麵店角色扮演", "實際走一遍點餐流程"], ["travel/sos", "🚨 SOS 手指卡", "出發前一定要存"]] },
    anime: { icon: "🎌", name: "看懂動漫日劇", desc: "聽懂台詞、不靠字幕", steps: [
      ["anime", "🎌 動漫名台詞教室", "鬼滅、咒術、柯南…"], ["kana/game", "🎮 五十音消除遊戲", "先把假名練成反射"], ["talk/anime", "💬 動漫常用口語", "すごい、やばい、まじで"]] },
    life: { icon: "🏠", name: "日本生活", desc: "超商、看醫生、租屋", steps: [
      ["talk/daily", "🏠 日常生活會話", "每天都用得到"], ["talk/convenience", "🏪 超商結帳角色扮演", "要加熱嗎？要袋子嗎？"], ["travel/culture", "🛡️ 文化避坑指南", "居酒屋、電車、溫泉禮儀"]] },
    work: { icon: "💼", name: "職場工作", desc: "敬語、商務應對", steps: [
      ["talk/work", "💼 職場敬語入門", "かしこまりました"], ["grammar", "🧩 動詞變化", "て形口訣歌一次搞懂"], ["news", "📰 NHK 簡易新聞", "練商務閱讀"]] },
  };
  function onboardingHTML() {
    return `<div class="card hero">
      <h1>歡迎來到日語學習道場 🌸</h1>
      <p>完全免費、不用註冊，每天 15 分鐘，從五十音學到日本自由行。<br><b>你學日語最想做到什麼？</b></p>
      <div class="options">${Object.entries(GOALS).map(([k, g]) => `
        <button class="option" data-goal="${k}"><span style="font-size:1.5rem">${g.icon}</span> <b>${g.name}</b><br><span class="small muted">${g.desc}</span></button>`).join("")}</div>
      <p class="small muted" style="margin:0">或直接 <a href="#/daily">▶ 玩今天的 3 分鐘挑戰</a></p></div>`;
  }
  function goalPathHTML() {
    const g = GOALS[P.goal];
    return `<div class="card"><div class="spread"><h2>🧭 你的專屬路線：${g.icon} ${g.name}</h2><button class="btn small" data-goal="">換目標</button></div>
      <div class="grid" style="margin-top:8px">${g.steps.map(([h, t, d], i) => `
        <a class="card link" href="#/${h}" style="box-shadow:none"><div class="small muted">STEP ${i + 1}</div><b>${t}</b><div class="small muted">${d}</div></a>`).join("")}</div></div>`;
  }
  document.addEventListener("click", (e) => {
    const b = e.target.closest("[data-goal]");
    if (!b) return;
    P.goal = b.dataset.goal || null;
    save();
    if (P.goal) toast(`${GOALS[P.goal].icon} 已為你規劃「${GOALS[P.goal].name}」路線！`);
    route();
  });

  // ===== 首頁（/hub + /daily + /omikuji） =====
  pages[""] = () => {
    const cats = Object.values(D.scenarios);
    const allPhrases = cats.flatMap((c) => c.phrases.map((p) => ({ ...p, cat: c.title })));
    const daily = allPhrases[dayIndex() % allPhrases.length];
    const trivia = D.trivia[dayIndex() % D.trivia.length];
    const next = D.quests[String(P.level)];
    const done = (P.dailyResults || {})[todayStr()];
    $app.innerHTML = `
      ${P.goal ? `<h1>おかえりなさい！🌸</h1>
      <p class="lead">每天 15 分鐘，從五十音到日本自由行、生活與職場。進度存在這台裝置的瀏覽器裡。</p>` : onboardingHTML()}
      <a class="card link daily-cta" href="#/daily" style="margin:16px 0">
        <div class="spread"><div><h2 style="margin:0">🗓️ 今日挑戰 ${todayStr().slice(5).replace("-", "/")}</h2>
          <div class="small muted">全站同一組 5 題・3 分鐘・做完可以分享成績</div></div>
          <span class="btn ${done ? "" : "primary"}">${done ? `${done.marks} ${done.score}/5` : "開始挑戰 ➡️"}</span></div></a>
      ${(() => { const n = dueCount(); return `<a class="card link" href="#/cards${n ? "/study" : ""}" style="margin-bottom:16px">
        <div class="spread"><div><h2 style="margin:0">🃏 單字卡複習</h2><div class="small muted">${n ? `今天有 ${n} 張要練，大約 ${Math.max(1, Math.round(n * 0.15))} 分鐘` : "今天的卡片都練完了 🎉"}</div></div>
        <span class="btn ${n ? "primary" : ""}">${n ? "開始 ➡️" : "查看牌組"}</span></div></a>`; })()}
      ${P.goal ? goalPathHTML() : ""}
      <div class="grid" style="margin-top:16px">
        <div class="card">
          <div class="spread"><h2>✨ 今日一句</h2><span class="small muted">${esc(daily.cat)}</span></div>
          <div class="jp-big">${esc(daily.japanese)}</div>
          <div class="furi">${esc(daily.furigana)}</div>
          <div class="romaji">${esc(daily.romaji)}</div>
          <p><b>${esc(daily.meaning)}</b></p>
          <div class="small muted md">${md(daily.usage)}</div>
          <div class="row" style="margin-top:10px">${speakBtn(daily.japanese, "🔊 聽發音")}${micBtn(daily.japanese, daily.furigana)}</div>
        </div>
        <div class="card">
          <h2>⚔️ 繼續闖關</h2>
          <p class="muted small">第 ${P.level} / 20 關</p>
          <div class="progress"><div style="width:${(P.completed.length / 20) * 100}%"></div></div>
          <p style="margin-top:12px"><b>${esc(next.title)}</b></p>
          <div class="jp">${esc(next.phrase)}</div>
          <div class="row" style="margin-top:12px"><a class="btn primary" href="#/quest/${P.level}">開始今天的關卡 ➡️</a></div>
        </div>
        <div class="card">
          <h2>💡 日語冷知識</h2>
          <h3>${esc(trivia.title)}</h3>
          <div class="small md">${md(trivia.story)}</div>
        </div>
        <div class="card" id="omikuji">
          <h2>⛩️ 今日御神籤</h2>
          <p class="muted small">搖一搖，看看今天的學習運勢！</p>
          <button class="btn primary" id="drawOmikuji">🎋 抽籤</button>
          <div id="omikujiOut"></div>
        </div>
      </div>
      <h2 style="margin-top:28px">🚀 快速入口</h2>
      <div class="grid tight">
        ${[
          ["kana/game", "🎮", "五十音消除遊戲"], ["quiz", "🎯", "隨堂測驗"], ["review", "🔄", `錯題本 (${P.mistakes.length})`],
          ["talk", "🍜", "角色扮演"], ["travel", "🚨", "SOS 手指卡"], ["songs", "🎐", "童謡跟唱"],
          ["speak", "🔊", "日文發音機"], ["kana_player.html", "🌸", "五十音播放器"], ["handwriting.html", "✍️", "手寫練習板"],
        ].map(([h, e, t]) => `<a class="card link" href="${h.endsWith(".html") ? h : "#/" + h}"><div class="emoji">${e}</div><b>${t}</b></a>`).join("")}
      </div>`;
    document.getElementById("drawOmikuji").addEventListener("click", () => {
      activity();
      const o = pick(D.omikuji);
      document.getElementById("omikujiOut").innerHTML = `
        <div class="box gold" style="margin-top:12px">
          <div class="jp-big">${esc(o.fortune)}</div>
          <div class="jp">「${esc(o.quote)}」 ${speakBtn(o.quote)}</div>
          <div class="romaji">${esc(o.romaji)}</div>
          <p>${esc(o.meaning)}</p>
          <div class="small">🍀 幸運物：${esc(o.lucky_item)}<br>🔤 幸運詞：${esc(o.lucky_word)}</div>
          <div class="small md" style="margin-top:6px">${md(o.detail)}</div>
        </div>`;
    });
  };

  // ===== 每日挑戰：同一天全站同一組題目，可分享成績 =====
  const SITE_URL = "https://bkhotey4.github.io/japanese-learning/";
  function seededRandom(seedStr) {
    let h = 1779033703 ^ seedStr.length;
    for (let i = 0; i < seedStr.length; i++) { h = Math.imul(h ^ seedStr.charCodeAt(i), 3432918353); h = (h << 13) | (h >>> 19); }
    return () => { h = Math.imul(h ^ (h >>> 16), 2246822507); h = Math.imul(h ^ (h >>> 13), 3266489909); return ((h ^= h >>> 16) >>> 0) / 4294967296; };
  }
  function dailyQuestions(date) {
    const rnd = seededRandom("jp-daily-" + date);
    const pickR = (a) => a[Math.floor(rnd() * a.length)];
    const sample = (a, n) => { const c = a.slice(), out = []; while (out.length < n && c.length) out.push(c.splice(Math.floor(rnd() * c.length), 1)[0]); return out; };
    const kanaQ = () => {
      const c = pickR(D.kanaCards);
      const toKata = rnd() < 0.5;
      const field = toKata ? "kata" : "romaji";
      const pool = [...new Set(D.kanaCards.map((x) => x[field]).filter((v) => v !== c[field]))];
      return { question: `### 『 ${c.hira} 』的${toKata ? "片假名" : "羅馬拼音"}是？`, options: [c[field], ...sample(pool, 3)], answer: c[field], explanation: `🧠 ${c.mnemonic}`, kana: true };
    };
    const quests = Object.values(D.quests).map((q) => q.quiz);
    const katakana = D.katakanaQuizzes;
    return [kanaQ(), ...sample(D.quiz, 2), pickR(quests), pickR(katakana)];
  }
  function dailyStreak() {
    const r = P.dailyResults || {};
    let n = 0;
    const d = new Date();
    if (!r[todayStr()]) d.setDate(d.getDate() - 1); // 今天還沒做，不算斷
    for (;;) {
      const k = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
      if (!r[k]) return n;
      n++; d.setDate(d.getDate() - 1);
    }
  }
  function heatmapHTML() {
    const days = new Set([...(P.days || []), ...Object.keys(P.dailyResults || {})]);
    const cells = [];
    const d = new Date(); d.setDate(d.getDate() - 34);
    for (let i = 0; i < 35; i++) {
      const k = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
      const res = (P.dailyResults || {})[k];
      const lvl = res ? (res.score >= 4 ? 3 : 2) : days.has(k) ? 1 : 0;
      cells.push(`<div class="heat l${lvl}" title="${k}${res ? ` 挑戰 ${res.score}/5` : days.has(k) ? " 有學習" : ""}"></div>`);
      d.setDate(d.getDate() + 1);
    }
    return `<div class="heatmap">${cells.join("")}</div><div class="small muted" style="margin-top:6px">最近 5 週：淺色＝有學習，深色＝完成每日挑戰</div>`;
  }
  pages.daily = () => {
    const date = todayStr();
    P.dailyResults = P.dailyResults || {};
    const done = P.dailyResults[date];
    $app.innerHTML = `<h1>🗓️ 今日挑戰</h1><p class="lead">${date.replace(/-/g, "/")}・全站同一組 5 題，每天只能挑戰一次，做完把成績分享給朋友！</p>
      <div class="card" id="dc" style="max-width:760px"></div>
      <div class="card" style="max-width:760px;margin-top:14px"><div class="spread"><h2>📅 學習紀錄</h2><span>🔥 連續挑戰 <b>${dailyStreak()}</b> 天</span></div>${heatmapHTML()}</div>`;
    const el = document.getElementById("dc");
    if (done) return showDailyResult(el, date, done);
    const qs = dailyQuestions(date);
    const marks = [];
    let i = 0;
    const next = () => {
      if (i >= qs.length) {
        const score = marks.filter((m) => m === "⭕").length;
        P.dailyResults[date] = { score, marks: marks.join("") };
        save();
        activity();
        unlock("badge_quiz");
        return pages.daily();
      }
      const q = qs[i++];
      mountQuiz(el, q, {
        trackMistake: !q.kana,
        onDone: (ok) => marks.push(ok ? "⭕" : "❌"),
        onNext: next,
        nextLabel: i === qs.length ? "看結果 🎉" : "下一題 ➡️",
      });
      el.insertAdjacentHTML("afterbegin", `<div class="spread small muted"><span>第 ${i} / ${qs.length} 題</span><span>${marks.join("")}</span></div>
        <div class="progress" style="margin:6px 0 12px"><div style="width:${((i - 1) / qs.length) * 100}%"></div></div>`);
    };
    next();
  };
  function showDailyResult(el, date, r) {
    const msg = r.score === 5 ? "🌸 全對！太強了！" : r.score >= 4 ? "👏 很棒！差一點就全對" : r.score >= 2 ? "💪 不錯，明天再來！" : "🌱 每天一點點，明天一定更好！";
    const text = `🌸 日語學習道場 每日挑戰 ${date.slice(5).replace("-", "/")}\n${r.marks} ${r.score}/5\n🔥 連續挑戰 ${dailyStreak()} 天\n一起來學日語 👉 ${SITE_URL}#/daily`;
    el.innerHTML = `<div style="text-align:center"><div style="font-size:2.4rem;letter-spacing:4px">${r.marks}</div>
        <div class="jp-big">${r.score} / 5</div><p><b>${msg}</b></p>
        <pre class="share-text">${esc(text)}</pre>
        <div class="row" style="justify-content:center"><button class="btn primary" id="shareBtn">📤 分享成績</button>
        <a class="btn" href="#/review">🔄 複習錯題</a><a class="btn" href="#/quest">⚔️ 繼續闖關</a></div>
        <p class="small muted">明天 00:00 會有新的題目 ⏰</p></div>`;
    document.getElementById("shareBtn").addEventListener("click", async () => {
      try {
        if (navigator.share) { await navigator.share({ text }); return; }
        await navigator.clipboard.writeText(text);
        toast("✅ 已複製成績，貼到 LINE、IG 或 Threads 吧！");
      } catch (e) { if (e && e.name !== "AbortError") toast("請手動複製上方文字分享"); }
    });
  }

  // ===== 闖關（/quest） =====
  pages.quest = (arg) => {
    if (arg) return questLevel(Number(arg));
    $app.innerHTML = `
      <h1>⚔️ 系統化闖關</h1>
      <p class="lead">20 關，一關一句核心句型 + 五十音 + 隨堂測驗。答對即可解鎖下一關。</p>
      <div class="card">
        <div class="spread"><b>已完成 ${P.completed.length} / 20</b>
          <button class="btn small" id="resetQuest">↺ 重置進度</button></div>
        <div class="progress" style="margin:10px 0 16px"><div style="width:${(P.completed.length / 20) * 100}%"></div></div>
        <div class="level-grid">
          ${Array.from({ length: 20 }, (_, i) => i + 1).map((n) => {
            const cls = P.completed.includes(n) ? "done" : n === P.level ? "current" : n > P.level ? "locked" : "";
            return `<a class="level ${cls}" ${n > P.level ? "" : `href="#/quest/${n}"`} title="${esc(D.quests[n].title)}">${P.completed.includes(n) ? "✓" : n}</a>`;
          }).join("")}
        </div>
      </div>
      <div class="stack" style="margin-top:18px">
        ${Object.values(D.quests).map((q) => `
          <a class="card link ${q.level > P.level ? "muted" : ""}" ${q.level > P.level ? "" : `href="#/quest/${q.level}"`}>
            <div class="spread"><b>${esc(q.title)}</b><span class="small">${P.completed.includes(q.level) ? "✅" : q.level > P.level ? "🔒" : "▶"}</span></div>
            <span class="jp">${esc(q.phrase)}</span> <span class="small muted">— ${esc(q.meaning)}</span>
          </a>`).join("")}
      </div>`;
    document.getElementById("resetQuest").addEventListener("click", () => {
      if (!confirm("確定要把闖關進度重置回第 1 關嗎？")) return;
      P.level = 1; P.completed = []; save(); route();
    });
  };
  function questLevel(n) {
    const q = D.quests[String(n)];
    if (!q) { location.hash = "#/quest"; return; }
    if (n > P.level) { toast("🔒 這一關還沒解鎖喔！"); location.hash = "#/quest"; return; }
    activity();
    $app.innerHTML = `
      <p><a href="#/quest">← 關卡列表</a></p>
      <h1>${esc(q.title)}</h1>
      <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
        <div class="card stack">
          <div>
            <div class="jp-big">${esc(q.phrase)}</div>
            <div class="romaji">${esc(q.romaji)}</div>
            <div class="small">${esc(q.phonetic)}</div>
            <p><b>${esc(q.meaning)}</b></p>
            <div class="row">${speakBtn(q.phrase, "🔊 正常")}<button class="btn small speak" data-speak="${esc(q.phrase)}" data-rate="0.55">🐢 慢速</button>${micBtn(q.phrase)}</div>
          </div>
          <div class="box"><b>📍 使用情境</b><div class="md small">${md(q.scenario)}</div></div>
          <div class="box gold md small">${md(q.mnemonic_story)}</div>
        </div>
        <div class="stack">
          ${q.card_image ? `<div class="card"><img class="card-img" src="${esc(q.card_image)}" alt="${esc(q.phrase)} 圖卡" loading="lazy"></div>` : ""}
          <div class="card"><h3>🔤 ${esc(q.kana_group)}</h3><div class="md small">${md(q.kana_tip)}</div></div>
        </div>
      </div>
      <div class="card" style="margin-top:14px"><h2>📝 隨堂測驗</h2><div id="qz"></div></div>`;
    mountQuiz(document.getElementById("qz"), q.quiz, {
      onDone: (ok) => {
        if (!ok) return;
        completeLevel(n);
        const fb = document.querySelector("#qz .fb");
        fb.insertAdjacentHTML("beforeend", `<div class="row" style="margin-top:10px">
          ${n < 20 ? `<a class="btn primary" href="#/quest/${n + 1}">🎉 前往第 ${n + 1} 關 ➡️</a>` : `<b>🎓 恭喜全 20 關大圓滿！</b>`}
          <a class="btn" href="#/quest">關卡列表</a></div>`);
      },
    });
  }

  // ===== 五十音（/kana、/kana_game、/write、/kana_loop） =====
  pages.kana = (arg) => {
    if (arg === "game") return kanaGame();
    if (arg !== undefined && arg !== "") return kanaCard(Number(arg));
    $app.innerHTML = `
      <h1>🔤 五十音</h1>
      <p class="lead">點任一假名看字源、記憶口訣與發音技巧。</p>
      <div class="row" style="margin-bottom:16px">
        <a class="btn primary" href="#/kana/game">🎮 五十音消除遊戲</a>
        <a class="btn" href="kana_player.html">🌸 語音循環播放器</a>
        <a class="btn" href="handwriting.html">✍️ 米字格手寫板</a>
      </div>
      ${Object.values(D.kanaRows).map((row) => `
        <div class="card" style="margin-bottom:12px">
          <div class="spread"><h3>${esc(row.name)}</h3>${speakBtn(row.items.map((i) => i.hira).join("、"), "🔊 整行")}</div>
          <div class="grid tight" style="grid-template-columns:repeat(auto-fill,minmax(96px,1fr))">
            ${row.items.map((it) => {
              const idx = D.kanaCards.findIndex((c) => c.hira === it.hira);
              return `<a class="kana-cell" href="#/kana/${idx}" style="text-decoration:none;color:inherit">
                <div class="k">${esc(it.hira)}</div><div class="jp muted">${esc(it.kata)}</div><div class="small">${esc(it.romaji)}</div></a>`;
            }).join("")}
          </div>
        </div>`).join("")}`;
  };
  function kanaCard(i) {
    const c = D.kanaCards[i];
    if (!c) { location.hash = "#/kana"; return; }
    activity();
    $app.innerHTML = `
      <p><a href="#/kana">← 五十音表</a></p>
      <div class="card" style="max-width:640px;margin:0 auto">
        <div class="spread"><span class="muted">${esc(c.row)} · ${i + 1} / ${D.kanaCards.length}</span>${speakBtn(c.hira, "🔊 發音")}</div>
        <div class="row" style="justify-content:center;gap:28px;margin:10px 0">
          <div style="text-align:center"><div class="jp-huge">${esc(c.hira)}</div><div class="small muted">平假名</div></div>
          <div style="text-align:center"><div class="jp-huge">${esc(c.kata)}</div><div class="small muted">片假名</div></div>
        </div>
        <p style="text-align:center;font-size:1.3rem"><b>${esc(c.romaji)}</b></p>
        <div class="stack">
          <div class="box"><b>📜 字源</b><div class="small">${esc(c.origin)}</div></div>
          <div class="box gold"><b>🧠 記憶口訣</b><div class="small">${esc(c.mnemonic)}</div></div>
          <div class="box"><b>👄 發音技巧</b><div class="small">${esc(c.sound_tip)}</div></div>
          <div class="box"><b>📖 單字</b> <span class="jp">${esc(c.vocab)}</span> — ${esc(c.vocab_tw)} ${speakBtn(c.vocab)}</div>
        </div>
        <div class="spread" style="margin-top:14px">
          ${i > 0 ? `<a class="btn" href="#/kana/${i - 1}">⬅️ ${esc(D.kanaCards[i - 1].hira)}</a>` : "<span></span>"}
          ${i < D.kanaCards.length - 1 ? `<a class="btn primary" href="#/kana/${i + 1}">${esc(D.kanaCards[i + 1].hira)} ➡️</a>` : ""}
        </div>
      </div>`;
  }
  function kanaGame() {
    let round = 1, combo = 0;
    $app.innerHTML = `<p><a href="#/kana">← 五十音</a></p><h1>🎮 五十音極速消除</h1>
      <p class="lead">不計分、無壓力，答對立刻下一題，答錯給你口訣提示。</p><div class="card" id="game" style="max-width:640px"></div>`;
    const el = document.getElementById("game");
    const next = () => {
      const c = pick(D.kanaCards);
      const mode = pick(["hira_to_kata", "kata_to_hira", "hira_to_romaji"]);
      const field = mode === "hira_to_kata" ? "kata" : mode === "kata_to_hira" ? "hira" : "romaji";
      const shown = mode === "kata_to_hira" ? c.kata : c.hira;
      const ask = { hira_to_kata: "對應的【片假名】", kata_to_hira: "對應的【平假名】", hira_to_romaji: "的【羅馬拼音】" }[mode];
      const pool = [...new Set(D.kanaCards.map((x) => x[field]).filter((v) => v !== c[field]))];
      const opts = shuffle([c[field], ...shuffle(pool).slice(0, 3)]);
      el.innerHTML = `
        <div class="spread"><b>🎯 第 ${round} 輪</b><span class="small muted">連擊 ${combo} 🔥</span></div>
        <div style="text-align:center;margin:12px 0"><div class="jp-huge">${esc(shown)}</div><div class="muted">${ask}是？</div></div>
        <div class="options">${opts.map((o) => `<button class="option jp" style="text-align:center;font-size:1.4rem">${esc(o)}</button>`).join("")}</div>
        <div class="fb"></div>`;
      el.querySelectorAll(".option").forEach((b) => b.addEventListener("click", () => {
        activity();
        if (b.textContent === c[field]) {
          combo += 1; round += 1; speak(c.hira);
          b.classList.add("correct");
          setTimeout(next, 450);
        } else {
          combo = 0;
          el.querySelectorAll(".option").forEach((x) => { x.disabled = true; if (x.textContent === c[field]) x.classList.add("correct"); });
          b.classList.add("wrong");
          el.querySelector(".fb").innerHTML = `<div class="feedback bad">
            <b>💡 差一點！</b>『${esc(c.hira)}』/『${esc(c.kata)}』= <b>${esc(c.romaji)}</b><br>
            <span class="small">🧠 ${esc(c.mnemonic)}</span></div>
            <div class="row" style="margin-top:10px"><button class="btn primary">➡️ 繼續消除</button></div>`;
          el.querySelector(".fb .btn").addEventListener("click", () => { round += 1; next(); });
        }
      }));
    };
    next();
  }

  // ===== 測驗（/quiz、/review、/katakana） =====
  pages.quiz = (arg) => {
    const all = [...D.quiz, ...D.katakanaQuizzes.map((q) => ({ ...q, category: "片假名外來語" }))];
    const cats = [...new Set(all.map((q) => q.category))];
    const cat = arg ? decodeURIComponent(arg) : "";
    const pool = cat ? all.filter((q) => q.category === cat) : all;
    $app.innerHTML = `
      <h1>🎯 隨堂測驗</h1>
      <p class="lead">答錯的題目會自動收進 <a href="#/review">錯題本</a>。</p>
      <div class="row" style="margin-bottom:14px">
        <a class="chip ${cat ? "" : "active"}" href="#/quiz">🎲 全部隨機</a>
        ${cats.map((c) => `<a class="chip ${c === cat ? "active" : ""}" href="#/quiz/${encodeURIComponent(c)}">${esc(c)}</a>`).join("")}
      </div>
      <div class="card" id="qz" style="max-width:760px"></div>`;
    let order = shuffle(pool), i = 0;
    const el = document.getElementById("qz");
    const next = () => {
      if (i >= order.length) { order = shuffle(pool); i = 0; }
      const q = order[i++];
      mountQuiz(el, q, { onDone: () => unlock("badge_quiz"), onNext: next });
      el.insertAdjacentHTML("afterbegin", `<div class="small muted">${esc(q.category)}</div>`);
    };
    next();
  };
  /* ---------------- 單字卡：間隔重複複習（簡化版 SM-2，類似 Anki） ---------------- */
  const addDays = (n) => { const d = new Date(); d.setDate(d.getDate() + n); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
  const DECKS = {
    kana: { name: "🔤 五十音", build: () => D.kanaCards.map((c) => ({ id: "kana:" + c.hira, front: c.hira, reading: `${c.romaji}・片假名 ${c.kata}`, back: c.romaji, extra: `🧠 ${c.mnemonic}`, say: c.hira })) },
    quest: { name: "⚔️ 闖關句子", build: () => Object.values(D.quests).map((q) => ({ id: "quest:" + q.level, front: q.phrase, reading: q.romaji, back: q.meaning, extra: q.scenario, say: q.phrase })) },
    phrase: { name: "🍜 情境會話", build: () => Object.values(D.scenarios).flatMap((s) => s.phrases.map((p) => ({ id: "phrase:" + p.japanese, front: p.japanese, reading: `${p.furigana}｜${p.romaji}`, back: p.meaning, extra: p.usage, say: p.japanese }))) },
    katakana: { name: "🧩 片假名外來語", build: () => D.katakanaWords.map((w) => ({ id: "kata:" + w.word, front: w.word, reading: w.romaji, back: w.meaning, extra: `${w.origin}｜${w.note}`, say: w.word })) },
    travel: { name: "✈️ 旅遊單字", build: () => [
      ...Object.values(D.menu).flatMap((m) => m.items.map((i) => ({ id: "menu:" + i.japanese, front: i.japanese.replace(/\s*\(.*\)$/, ""), reading: i.furigana, back: i.meaning, extra: i.detail, say: i.furigana }))),
      ...Object.values(D.scan).flatMap((s) => s.items.map((i) => ({ id: "scan:" + i.jp, front: i.jp, reading: `${i.furigana}｜${i.romaji}`, back: i.meaning, extra: i.tip, say: i.furigana }))),
      ...Object.entries(D.signs).map(([k, v]) => ({ id: "sign:" + k, front: k, reading: `${v.furigana}｜${v.romaji}`, back: v.meaning, extra: v.tip, say: v.furigana })),
    ] },
    words: { name: "📖 新聞・童謡單字", build: () => [
      ...D.news.flatMap((n) => n.vocabulary.map((v) => ({ id: "news:" + v.word, front: v.word, reading: "", back: v.meaning, extra: `📰 ${n.title}`, say: v.word.split(/[ (（]/)[0] }))),
      ...Object.values(D.doyo).flatMap((s) => s.vocab.map((v) => ({ id: "doyo:" + v.word, front: v.word, reading: v.reading, back: v.meaning, extra: `🎐 ${s.title}`, say: v.word }))),
    ] },
  };
  let _allCards = null;
  const allCards = () => _allCards || (_allCards = Object.entries(DECKS).flatMap(([deck, d]) => d.build().map((c) => ({ ...c, deck }))));
  const srsState = (id) => (P.srs || {})[id];
  const srsSettings = () => Object.assign({ newPerDay: 10, decks: ["kana", "quest", "phrase"] }, P.srsSettings || {});
  function newLeftToday() {
    const t = todayStr();
    const used = P.srsNew && P.srsNew.date === t ? P.srsNew.count : 0;
    return Math.max(0, srsSettings().newPerDay - used);
  }
  function srsQueue() {
    const t = todayStr(), set = srsSettings();
    const cards = allCards().filter((c) => set.decks.includes(c.deck));
    const due = cards.filter((c) => { const s = srsState(c.id); return s && s.due <= t; }).sort((a, b) => srsState(a.id).due.localeCompare(srsState(b.id).due));
    const fresh = cards.filter((c) => !srsState(c.id)).slice(0, newLeftToday());
    return { due, fresh };
  }
  // 依評分算下次間隔（天）。0=忘記 1=困難 2=記得 3=簡單
  function nextInterval(s, g) {
    s = s || { iv: 0, ease: 2.5, reps: 0 };
    if (g === 0) return 0;
    if (g === 1) return Math.max(1, Math.round(s.iv * 1.2));
    if (g === 2) return s.reps === 0 ? 1 : s.reps === 1 ? 3 : Math.round(Math.max(s.iv, 1) * s.ease);
    return s.reps === 0 ? 4 : Math.round(Math.max(s.iv, 1) * s.ease * 1.3);
  }
  function rateCard(c, g) {
    P.srs = P.srs || {};
    const old = P.srs[c.id];
    if (!old) { const t = todayStr(); P.srsNew = { date: t, count: (P.srsNew && P.srsNew.date === t ? P.srsNew.count : 0) + 1 }; }
    const s = Object.assign({ iv: 0, ease: 2.5, reps: 0, lapses: 0 }, old);
    const iv = nextInterval(s, g);
    if (g === 0) { s.reps = 0; s.lapses += 1; s.ease = Math.max(1.3, s.ease - 0.2); }
    else { s.reps += 1; if (g === 1) s.ease = Math.max(1.3, s.ease - 0.15); if (g === 3) s.ease += 0.15; }
    s.iv = iv;
    s.due = addDays(iv);
    P.srs[c.id] = s;
    P.srsReviews = (P.srsReviews || 0) + 1;
    save();
  }
  const ivLabel = (n) => (n === 0 ? "<1 分" : n < 30 ? `${n} 天` : n < 365 ? `${Math.round(n / 30)} 個月` : `${(n / 365).toFixed(1)} 年`);
  function dueCount() { const q = srsQueue(); return q.due.length + q.fresh.length; }

  pages.cards = (arg) => {
    if (arg === "study") return cardStudy();
    const set = srsSettings(), t = todayStr();
    const q = srsQueue();
    const rows = Object.entries(DECKS).map(([k, d]) => {
      const cs = allCards().filter((c) => c.deck === k);
      const learned = cs.filter((c) => srsState(c.id)).length;
      const due = cs.filter((c) => { const s = srsState(c.id); return s && s.due <= t; }).length;
      const mature = cs.filter((c) => { const s = srsState(c.id); return s && s.iv >= 21; }).length;
      return `<tr><td><label><input type="checkbox" data-deck="${k}" ${set.decks.includes(k) ? "checked" : ""}> ${d.name}</label></td>
        <td>${cs.length}</td><td>${learned}</td><td>${mature}</td><td><b>${due}</b></td></tr>`;
    }).join("");
    $app.innerHTML = `<h1>🃏 單字卡</h1>
      <p class="lead">間隔重複複習：記得的卡片會越隔越久才出現，忘記的會馬上再考。每天清空待複習，記憶最牢。</p>
      <div class="card" style="max-width:760px">
        <div class="spread"><div><div style="font-size:2rem;font-weight:700">${q.due.length + q.fresh.length}</div>
          <div class="small muted">今天要練：複習 ${q.due.length} 張・新卡 ${q.fresh.length} 張</div></div>
          ${q.due.length + q.fresh.length ? `<a class="btn primary" href="#/cards/study">▶ 開始複習</a>` : `<span class="btn">🎉 今天完成了！</span>`}</div>
      </div>
      <div class="card" style="max-width:760px;margin-top:14px">
        <h2>📚 牌組</h2><p class="small muted">勾選要練習的牌組。「熟記」＝間隔超過 21 天。</p>
        <div class="table-wrap"><table class="small"><tr><th>牌組</th><th>總數</th><th>學過</th><th>熟記</th><th>待複習</th></tr>${rows}</table></div>
        <div class="row" style="margin-top:12px"><label class="small">每天新卡數量
          <select id="newPerDay" style="width:auto;display:inline-block;margin-left:6px">${[5, 10, 15, 20, 30].map((n) => `<option ${n === set.newPerDay ? "selected" : ""}>${n}</option>`).join("")}</select></label>
          <span class="small muted">今天還可學 ${newLeftToday()} 張新卡</span></div>
      </div>`;
    const saveSet = (patch) => { P.srsSettings = Object.assign(srsSettings(), patch); save(); route(); };
    document.querySelectorAll("[data-deck]").forEach((cb) => cb.addEventListener("change", () => {
      saveSet({ decks: [...document.querySelectorAll("[data-deck]:checked")].map((x) => x.dataset.deck) });
    }));
    document.getElementById("newPerDay").addEventListener("change", (e) => saveSet({ newPerDay: Number(e.target.value) }));
  };
  function cardStudy() {
    const q = srsQueue();
    // 複習卡與新卡穿插，忘記的卡放回佇列尾端再考一次
    const queue = [];
    const due = q.due.slice(), fresh = q.fresh.slice();
    while (due.length || fresh.length) { if (due.length) queue.push(due.shift()); if (due.length) queue.push(due.shift()); if (fresh.length) queue.push(fresh.shift()); }
    const total = queue.length;
    let doneN = 0;
    $app.innerHTML = `<p><a href="#/cards">← 單字卡</a></p><div class="card flashcard" id="fc" style="max-width:640px;margin:0 auto"></div>
      <p class="small muted" style="text-align:center">⌨️ 空白鍵翻面・1 忘記・2 困難・3 記得・4 簡單</p>`;
    const el = document.getElementById("fc");
    let cur = null, flipped = false;
    const show = () => {
      cur = queue.shift();
      flipped = false;
      if (!cur) {
        activity();
        el.innerHTML = `<div style="text-align:center"><div style="font-size:3rem">🎉</div><h2>今天的單字卡完成了！</h2>
          <p class="muted">練了 ${doneN} 次，明天再來。</p><a class="btn primary" href="#/cards">回單字卡</a></div>`;
        return;
      }
      const isNew = !srsState(cur.id);
      el.innerHTML = `<div class="spread small muted"><span>${DECKS[cur.deck].name}${isNew ? "・🆕 新卡" : ""}</span><span>剩 ${queue.length + 1} 張</span></div>
        <div class="progress" style="margin:6px 0 18px"><div style="width:${total ? (doneN / (doneN + queue.length + 1)) * 100 : 0}%"></div></div>
        <div style="text-align:center;min-height:150px">
          <div class="${cur.front.length <= 2 ? "jp-huge" : "jp-big"}">${esc(cur.front)}</div>
          <div class="row" style="justify-content:center;margin-top:8px">${speakBtn(cur.say)}${micBtn(cur.say, cur.reading.split("｜")[0])}</div>
          <div id="ans"></div>
        </div>
        <div id="act" style="margin-top:16px"><button class="btn primary" id="flip" style="width:100%">顯示答案（空白鍵）</button></div>`;
      document.getElementById("flip").addEventListener("click", flip);
      if (localStorage.getItem("jp_autospeak") !== "0") speak(cur.say);
    };
    const flip = () => {
      if (!cur || flipped) return;
      flipped = true;
      const s = srsState(cur.id);
      document.getElementById("ans").innerHTML = `<hr style="border:none;border-top:1px solid var(--border);margin:16px 0">
        ${cur.reading ? `<div class="furi">${esc(cur.reading)}</div>` : ""}
        <div style="font-size:1.2rem;margin:6px 0"><b>${esc(cur.back)}</b></div>
        ${cur.extra ? `<div class="small muted md">${md(cur.extra)}</div>` : ""}`;
      const labels = [["忘記", "bad"], ["困難", ""], ["記得", "ok"], ["簡單", "ok"]];
      document.getElementById("act").innerHTML = `<div class="options" style="grid-template-columns:repeat(4,1fr)">${labels.map(([t], g) => `
        <button class="option" data-g="${g}" style="text-align:center"><b>${t}</b><br><span class="small muted">${ivLabel(nextInterval(s, g))}</span></button>`).join("")}</div>`;
      document.querySelectorAll("[data-g]").forEach((b) => b.addEventListener("click", () => rate(Number(b.dataset.g))));
    };
    const rate = (g) => {
      if (!cur || !flipped) return;
      rateCard(cur, g);
      doneN++;
      if (g === 0) queue.splice(Math.min(queue.length, 3), 0, cur); // 忘記：幾張後再出現
      show();
    };
    const onKey = (e) => {
      if (!document.getElementById("fc")) { document.removeEventListener("keydown", onKey); return; }
      if (e.target.closest && e.target.closest("input, textarea, select, button")) return;
      if (e.code === "Space" || e.key === "Enter") { e.preventDefault(); flipped ? rate(2) : flip(); }
      else if (/^[1-4]$/.test(e.key)) rate(Number(e.key) - 1);
    };
    document.addEventListener("keydown", onKey);
    show();
  }

  pages.review = () => {
    $app.innerHTML = `<h1>🔄 錯題本</h1><p class="lead">答對就從錯題本移除，全部清空就是你的勝利！</p><div id="rv"></div>`;
    const el = document.getElementById("rv");
    const next = () => {
      if (!P.mistakes.length) {
        el.innerHTML = `<div class="card"><h2>🎉 錯題本是空的！</h2><p>去 <a href="#/quiz">隨堂測驗</a> 或 <a href="#/quest">闖關</a> 繼續挑戰吧。</p></div>`;
        return;
      }
      const q = P.mistakes[0];
      el.innerHTML = `<div class="card" style="max-width:760px"><div class="small muted">剩餘 ${P.mistakes.length} 題</div><div id="one"></div></div>`;
      mountQuiz(document.getElementById("one"), q, {
        trackMistake: false,
        onDone: (ok) => {
          P.mistakes.shift();
          if (!ok) P.mistakes.push(q); // 答錯就排到最後再考一次
          else unlock("badge_review");
          save();
        },
        onNext: next,
      });
    };
    next();
  };

  // ===== 會話（/scenario + /chat 角色扮演 + /katakana） =====
  pages.talk = (arg) => {
    if (arg && D.roleplay[arg]) return roleplay(arg);
    const tab = arg || "roleplay";
    const tabs = [["roleplay", "🎭 角色扮演"], ...Object.entries(D.scenarios).map(([k, v]) => [k, v.title]), ["katakana", "🧩 片假名外來語"]];
    let body = "";
    if (tab === "roleplay") {
      body = `<div class="grid">${Object.entries(D.roleplay).map(([k, r]) => `
        <a class="card link" href="#/talk/${k}"><h3>${esc(r.title)}</h3><p class="small muted">${esc(r.description)}</p>
        <span class="small">${P.badges.includes(r.badge) ? "🎖️ 已通關" : `${r.steps.length} 回合`}</span></a>`).join("")}</div>`;
    } else if (tab === "katakana") {
      const cats = [...new Set(D.katakanaWords.map((w) => w.category))];
      body = cats.map((c) => `<h2 style="margin-top:12px">${esc(c)}</h2><div class="grid">${D.katakanaWords.filter((w) => w.category === c).map((w) => `
        <div class="card"><div class="spread"><span class="jp-big">${esc(w.word)}</span>${speakBtn(w.word)}</div>
        <div class="romaji">${esc(w.romaji)}</div><p><b>${esc(w.meaning)}</b> <span class="small muted">← ${esc(w.origin)}</span></p>
        <div class="small md">${md(w.note)}</div></div>`).join("")}</div>`).join("") +
        `<p style="margin-top:14px"><a class="btn primary" href="#/quiz/${encodeURIComponent("片假名外來語")}">🎯 片假名小測驗</a></p>`;
    } else {
      const s = D.scenarios[tab];
      body = `<p class="muted">${esc(s.description)}</p><div class="grid">${s.phrases.map((p) => `
        <div class="card"><div class="spread"><span class="jp" style="font-size:1.2rem">${esc(p.japanese)}</span>${speakBtn(p.japanese)}</div>
        <div class="furi">${esc(p.furigana)}</div><div class="romaji">${esc(p.romaji)}</div>
        <p><b>${esc(p.meaning)}</b></p><div class="small muted md">${md(p.usage)}</div>${SR ? `<div class="row" style="margin-top:8px">${micBtn(p.japanese, p.furigana)}</div>` : ""}</div>`).join("")}</div>`;
    }
    $app.innerHTML = `<h1>🍜 情境會話</h1><p class="lead">先學句子，再到角色扮演實戰。</p>
      <div class="row" style="margin-bottom:14px">${tabs.map(([k, t]) => `<a class="chip ${k === tab ? "active" : ""}" href="#/talk/${k}">${esc(t)}</a>`).join("")}</div>${body}`;
  };
  function roleplay(id) {
    const r = D.roleplay[id];
    activity();
    $app.innerHTML = `<p><a href="#/talk">← 情境會話</a></p><h1>${esc(r.title)}</h1><p class="lead">${esc(r.description)}</p>
      <div class="card" style="max-width:760px"><div class="chat" id="chat"></div><div id="choices" style="margin-top:14px"></div></div>`;
    const chat = document.getElementById("chat"), choices = document.getElementById("choices");
    const say = (cls, html) => { chat.insertAdjacentHTML("beforeend", `<div class="bubble ${cls}">${html}</div>`); chat.lastElementChild.scrollIntoView({ block: "nearest", behavior: "smooth" }); };
    const step = (n) => {
      const s = r.steps[n];
      say("npc", `<div class="spread"><span class="jp">${esc(s.npc)}</span>${speakBtn(s.npc)}</div>
        <div class="furi">${esc(s.furigana)}</div><div class="romaji">${esc(s.romaji)}</div><div class="small">${esc(s.translation)}</div>`);
      speak(s.npc);
      choices.innerHTML = `<div class="small muted">👇 選一句大聲念出來回覆：</div><div class="options">${s.options.map((o, i) => `
        <button class="option" data-i="${i}"><b>${esc(o.label)}</b><br><span class="small romaji">${esc(o.romaji)}</span></button>`).join("")}</div>`;
      choices.querySelectorAll(".option").forEach((b) => b.addEventListener("click", () => {
        const o = s.options[Number(b.dataset.i)];
        say("me", `<span class="jp">${esc(o.furigana)}</span><div class="small">${esc(o.meaning)}</div>`);
        speak(o.furigana);
        if (o.npc_reaction) setTimeout(() => say("npc", `<span class="small">${esc(o.npc_reaction)}</span>`), 300);
        if (o.next_step === "end" || o.next_step >= r.steps.length) {
          choices.innerHTML = `<div class="feedback ok"><b>🎉 實戰通關！</b> ${D.badges[r.badge] ? `獲得成就 ${esc(D.badges[r.badge].name)}` : ""}</div>
            <div class="row" style="margin-top:10px"><button class="btn primary" id="replay">🔁 再玩一次</button><a class="btn" href="#/talk">其他情境</a></div>`;
          document.getElementById("replay").addEventListener("click", () => roleplay(id));
          unlock(r.badge);
        } else setTimeout(() => step(o.next_step), 900);
      }));
    };
    step(0);
  }

  // ===== 文法（/grammar） =====
  pages.grammar = () => {
    unlock("badge_grammar");
    $app.innerHTML = `<h1>🧩 動詞變化</h1><p class="lead">七個最常用動詞的完整變化，配上て形口訣歌。</p>
      <div class="card box gold md" style="margin-bottom:16px">${md(D.teForm)}</div>
      <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(320px,1fr))">${Object.values(D.verbs).map((v) => `
        <div class="card"><div class="spread"><h3 class="jp">${esc(v.verb)}</h3>${speakBtn(v.verb.split(" ")[0])}</div>
        <div class="small muted">${esc(v.meaning)} · ${esc(v.type)}</div>
        <div class="table-wrap"><table class="small">${Object.entries(v.forms).map(([k, f]) => `<tr><td class="muted">${esc(k)}</td><td class="jp">${esc(f)}</td></tr>`).join("")}</table></div>
        ${v.example ? `<div class="box small md" style="margin-top:8px">${md(v.example)}</div>` : ""}</div>`).join("")}</div>`;
  };

  // ===== 跟讀（/voice + /shadowing） =====
  pages.speak = () => {
    const rate = Number(localStorage.getItem("jp_rate") || 0.8);
    $app.innerHTML = `<h1>🗣️ 發音與跟讀</h1><p class="lead">先聽 🔊，再按 🎤 念一次，網站會幫你的發音打分數。建議用 Chrome / Edge${SR ? "" : "（你目前的瀏覽器不支援語音辨識，所以看不到 🎤 按鈕）"}。</p>
      <div class="card" style="margin-bottom:16px">
        <h2>🔊 日文發音機</h2>
        <textarea id="ttsText" placeholder="輸入任何日文，例如：すみません、駅はどこですか？">すみません、駅はどこですか？</textarea>
        <div class="row" style="margin-top:10px">
          <button class="btn primary" id="ttsGo">▶ 朗讀</button>${SR ? `<button class="btn" id="ttsMic">🎤 念念看評分</button>` : ""}
          <label class="small">語速 <input type="range" id="rate" min="0.4" max="1.3" step="0.05" value="${rate}"> <span id="rateVal">${rate}</span></label>
        </div>
        <p class="small muted" id="voiceInfo"></p>
      </div>
      <h2>📈 影子跟讀挑戰</h2>
      <p class="small muted">聽一遍 → 慢速再聽 → 落後 0.5 秒跟著念，連續 3 次。</p>
      <div class="grid">${D.shadowing.map((s) => `
        <div class="card"><div class="small muted">${esc(s.scenario)} ${esc(s.stars)}</div>
        <div class="jp" style="font-size:1.2rem">${esc(s.sentence)}</div>
        <div class="furi">${esc(s.furigana)}</div><div class="romaji">${esc(s.romaji)}</div>
        <p><b>${esc(s.meaning)}</b></p><div class="small md box">${md(s.pitch_tip)}</div>
        <div class="row" style="margin-top:10px">${speakBtn(s.sentence, "🔊 正常")}<button class="btn small speak" data-speak="${esc(s.sentence)}" data-rate="0.55">🐢 慢速</button>${micBtn(s.sentence, s.furigana)}</div></div>`).join("")}</div>`;
    unlock("badge_shadowing");
    const info = () => { const el = document.getElementById("voiceInfo"); if (el) el.textContent = jaVoice ? `使用語音：${jaVoice.name}` : "⚠️ 找不到日語語音，請在系統安裝日語語音套件，或改用 Edge / Chrome。"; };
    info(); setTimeout(info, 800);
    document.getElementById("ttsGo").addEventListener("click", () => { activity(); speak(document.getElementById("ttsText").value); });
    const tm = document.getElementById("ttsMic");
    if (tm) tm.addEventListener("click", () => { tm.dataset.mic = document.getElementById("ttsText").value; });
    const r = document.getElementById("rate");
    r.addEventListener("input", () => { document.getElementById("rateVal").textContent = r.value; try { localStorage.setItem("jp_rate", r.value); } catch {} });
  };

  // ===== 旅遊（/menu + /drugstore + /scan + /sos + /culture） =====
  pages.travel = (arg) => {
    const tab = arg || "sos";
    const tabs = [["sos", "🚨 SOS 手指卡"], ["culture", "🛡️ 文化避坑"], ["menu", "🥩 美食菜單"], ["shop", "💊 藥妝/超市標示"], ["signs", "🪧 招牌解碼"]];
    let body = "";
    if (tab === "sos") {
      unlock("badge_sos");
      body = `<div class="card" style="margin-bottom:14px"><h2>☎️ 緊急電話</h2><div class="table-wrap"><table>${D.sosContacts.map((c) => `
          <tr><td>${esc(c.name)}</td><td><a href="tel:${esc(c.number.replace(/[^+\d]/g, ""))}"><b>${esc(c.number)}</b></a></td><td class="small muted">${esc(c.note)}</td></tr>`).join("")}</table></div></div>
        ${Object.values(D.sos).map((s) => `<h2 style="margin-top:16px">${esc(s.title)}</h2><p class="small muted">${esc(s.intro)}</p>
          <div class="grid">${s.cards.map((c) => `<div class="card"><div class="small muted">${esc(c.tag)}</div>
            <div class="jp" style="font-size:1.25rem">${esc(c.japanese)}</div><div class="furi">${esc(c.furigana)}</div>
            <p><b>${esc(c.chinese)}</b></p>${speakBtn(c.japanese, "🔊 播放給對方聽")}</div>`).join("")}</div>`).join("")}`;
    } else if (tab === "culture") {
      unlock("badge_culture");
      body = `<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(320px,1fr))">${Object.values(D.culture).map((c) => `
        <div class="card"><div class="small muted">${esc(c.category)}</div><h3>${esc(c.title)}</h3>
        <p class="small"><b>😵 問題：</b>${esc(c.problem)}</p><p class="small">${esc(c.explanation)}</p>
        <ul class="small">${c.rules.map((r) => `<li>${esc(r)}</li>`).join("")}</ul>
        <div class="box"><span class="jp">${esc(c.japanese_phrase)}</span> ${speakBtn(c.japanese_phrase)}<div class="romaji">${esc(c.romaji)}</div></div></div>`).join("")}</div>`;
    } else if (tab === "menu") {
      unlock("badge_menu");
      body = Object.values(D.menu).map((m) => `<h2 style="margin-top:12px">${esc(m.title)}</h2><p class="small muted">${esc(m.description)}</p>
        <div class="grid">${m.items.map((i) => `<div class="card"><div class="spread"><span class="jp" style="font-size:1.15rem">${esc(i.japanese)}</span>${speakBtn(i.furigana)}</div>
        <div class="furi">${esc(i.furigana)}</div><p><b>${esc(i.meaning)}</b></p><div class="small muted">${esc(i.detail)}</div></div>`).join("")}</div>`).join("");
    } else if (tab === "shop") {
      body = Object.values(D.scan).map((s) => `<h2 style="margin-top:12px">${esc(s.title)}</h2><p class="small muted">${esc(s.desc)}</p>
        <div class="grid">${s.items.map((i) => `<div class="card"><div class="spread"><span class="jp" style="font-size:1.15rem">${esc(i.jp)}</span>${speakBtn(i.furigana)}</div>
        <div class="furi">${esc(i.furigana)} · <span class="romaji">${esc(i.romaji)}</span></div><p><b>${esc(i.meaning)}</b></p><div class="small muted">${esc(i.tip)}</div></div>`).join("")}</div>`).join("");
    } else if (tab === "signs") {
      body = `<div class="card" style="margin-bottom:14px"><input type="text" id="signQ" placeholder="🔍 輸入看到的招牌字，例如：替玉、免税、準備中"></div><div class="grid" id="signList"></div>`;
    }
    $app.innerHTML = `<h1>✈️ 日本旅遊生存</h1><p class="lead">緊急求助、文化地雷、看懂菜單與商品標示。</p>
      <div class="row" style="margin-bottom:14px">${tabs.map(([k, t]) => `<a class="chip ${k === tab ? "active" : ""}" href="#/travel/${k}">${t}</a>`).join("")}</div>${body}`;
    if (tab === "signs") {
      const list = document.getElementById("signList");
      const draw = (q) => {
        const items = Object.entries(D.signs).filter(([k, v]) => !q || k.includes(q) || q.includes(k) || v.meaning.includes(q) || v.romaji.includes(q.toLowerCase()) || v.furigana.includes(q));
        list.innerHTML = items.length ? items.map(([k, v]) => `<div class="card"><div class="spread"><span class="jp-big">${esc(k)}</span>${speakBtn(v.furigana)}</div>
          <div class="furi">${esc(v.furigana)} · <span class="romaji">${esc(v.romaji)}</span></div><p><b>${esc(v.meaning)}</b></p><div class="small muted">${esc(v.tip)}</div></div>`).join("")
          : `<div class="card"><p>資料庫裡還沒有「${esc(q)}」。</p><p class="small">🗺️ 生存小秘訣：指著招牌問店員 <span class="jp">これは何ですか？</span> ${speakBtn("これは何ですか？")}</p>
             <p class="small">或聽聽它的發音：${speakBtn(q, "🔊 " + esc(q))}</p></div>`;
      };
      draw("");
      document.getElementById("signQ").addEventListener("input", (e) => draw(e.target.value.trim()));
    }
  };

  // ===== 動漫（/anime） =====
  pages.anime = () => {
    $app.innerHTML = `<h1>🎌 動漫名台詞教室</h1><p class="lead">用最熱血的台詞學口語、語尾與文法。</p>
      <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(320px,1fr))">${Object.values(D.anime).map((a) => `
        <div class="card"><div class="spread"><b>${esc(a.anime)}</b><span class="small muted">${esc(a.character)}</span></div>
        <div class="jp" style="font-size:1.3rem;margin-top:6px">${esc(a.quote)}</div>
        <div class="furi">${esc(a.furigana)}</div><div class="romaji">${esc(a.romaji)}</div><div class="small">${esc(a.phonetic)}</div>
        <p><b>${esc(a.meaning)}</b></p>
        <div class="row">${speakBtn(a.quote, "🔊 正常")}<button class="btn small speak" data-speak="${esc(a.quote)}" data-rate="0.55">🐢 慢速</button>${micBtn(a.quote, a.furigana)}</div>
        <details style="margin-top:8px"><summary class="small">📖 場景與文法解析</summary>
          <p class="small">${md(a.scene)}</p>
          <div class="small box md">${md(Array.isArray(a.grammar_breakdown) ? a.grammar_breakdown.join("\n") : a.grammar_breakdown)}</div>
          ${a.practice_template ? `<p class="small"><b>✏️ 造句練習：</b>${md(a.practice_template)}<br>${md(a.practice_example || "")}</p>` : ""}
        </details></div>`).join("")}</div>`;
  };

  const credit = (s) => `<div class="small muted">作詞：${esc(s.lyricist || "—")}　作曲：${esc(s.composer || "—")}</div>`;

  // ===== 公共領域童謡・唱歌 =====
  pages.songs = (arg) => {
    if (arg && arg.startsWith("doyo-") && D.doyo[arg.slice(5)]) return doyo(arg.slice(5));
    doyoList();
  };
  function doyoList() {
    $app.innerHTML = `<h1>🎐 童謡・唱歌</h1><p class="lead">作者過世超過 50 年、已屬公共領域的經典童謡與唱歌：用字簡單、發音清楚，最適合初學者跟唱。</p>
      <div class="grid">${Object.entries(D.doyo).map(([k, s]) => `
        <a class="card link" href="#/songs/doyo-${k}"><div class="jp" style="font-size:1.3rem">${esc(s.title)}</div>
          <div class="romaji">${esc(s.romaji_title)}</div><div class="small muted">${esc(s.year)}</div></a>`).join("")}</div>`;
  }
  function doyo(k) {
    const s = D.doyo[k];
    activity();
    const has = Boolean(s.lyrics_jp && s.lyrics_jp.trim());
    $app.innerHTML = `<p><a href="#/songs">← 童謡列表</a></p>
      <div class="card">
        <div class="spread"><h1 style="font-size:1.5rem">${esc(s.title)}</h1>${speakBtn(s.reading, "🔊 歌名")}</div>
        <div class="romaji">${esc(s.romaji_title)}</div>${credit(s)}
        <div class="small muted">${esc(s.year)}　·　✅ ${esc(s.pd_note)}</div>
        <p>${esc(s.story)}</p>
        <a class="btn small" href="${esc(s.lyrics_source)}" target="_blank" rel="noopener">📖 歌詞與歷史（維基百科）</a>
      </div>
      ${has ? `<div class="card" style="margin-top:14px">
        <div class="spread"><h2>🎤 完整歌詞</h2><div class="row">${speakBtn(s.lyrics_jp, "🔊 朗讀")}<button class="btn small speak" data-speak="${esc(s.lyrics_jp)}" data-rate="0.55">🐢 慢速</button></div></div>
        <div class="jp" style="white-space:pre-line;font-size:1.15rem;line-height:2">${esc(s.lyrics_jp)}</div>
        ${s.lyrics_reading ? `<details><summary class="small">顯示假名讀音</summary><div class="furi" style="white-space:pre-line">${esc(s.lyrics_reading)}</div></details>` : ""}
        ${s.lyrics_romaji ? `<details><summary class="small">顯示羅馬拼音</summary><div class="romaji" style="white-space:pre-line">${esc(s.lyrics_romaji)}</div></details>` : ""}
        ${s.lyrics_meaning ? `<div class="box small" style="white-space:pre-line;margin-top:8px">${esc(s.lyrics_meaning)}</div>` : ""}
      </div>` : ""}
      <div class="card" style="margin-top:14px"><h2>💡 學習重點</h2>
        <div class="stack">${s.learn_points.map((p) => `<div class="box small md">${md(p)}</div>`).join("")}</div></div>
      <div class="card" style="margin-top:14px"><h2>📖 歌詞單字</h2>
        <div class="table-wrap"><table class="small">${s.vocab.map((v) => `<tr><td class="jp">${esc(v.word)}</td><td>${esc(v.reading)}</td><td>${esc(v.meaning)}</td><td>${speakBtn(v.word)}</td></tr>`).join("")}</table></div></div>`;
  }

  // ===== 新聞（/news） =====
  pages.news = () => {
    unlock("badge_news");
    $app.innerHTML = `<h1>📰 NHK 簡易日語新聞</h1><p class="lead">短篇時事閱讀，邊聽邊跟讀關鍵單字。</p>
      ${D.news.map((n) => `<div class="card" style="margin-bottom:14px"><div class="small muted">${esc(n.date)}</div><h2>${esc(n.title)}</h2>
        <div class="jp" style="font-size:1.1rem;line-height:2">${esc(n.japanese)}</div>
        <details><summary class="small">顯示假名讀音</summary><div class="furi">${esc(n.furigana)}</div></details>
        <div class="row" style="margin:10px 0">${speakBtn(n.japanese, "🔊 朗讀全文")}</div>
        <div class="box small md">${md(n.summary)}</div>
        <div class="table-wrap" style="margin-top:8px"><table class="small">${n.vocabulary.map((v) => `<tr><td class="jp">${esc(v.word)}</td><td>${esc(v.meaning)}</td><td>${speakBtn(v.word.split(/[ (（]/)[0])}</td></tr>`).join("")}</table></div>
      </div>`).join("")}`;
  };

  // ===== 學習計畫（/plan） =====
  pages.plan = (arg) => {
    const tab = arg || "weekday";
    const plans = {
      weekday: `<h2>☕ 平日通勤：每日 15 分鐘微學習</h2>
        <p>目標不是苦讀，而是<b>維持語感不中斷</b>。</p>
        <div class="stack">
          <div class="box"><b>☀️ 前 5 分鐘【熱身刷卡】</b><br>首頁看 <a href="#/">今日一句</a>，或用 <a href="#/kana">五十音</a> 複習一行發音。</div>
          <div class="box"><b>🧠 中 7 分鐘【微量吸收】</b><br>挑戰 1 個 <a href="#/quest">主線關卡</a>，或在 <a href="#/grammar">文法</a> 速查 1 個動詞變化。</div>
          <div class="box"><b>🗣️ 後 3 分鐘【開口跟讀】</b><br>大聲跟讀 3 次，完成隨堂測驗就打卡收工！</div>
          <div class="box gold">💡 今天太累也沒關係，哪怕只做 1 題 <a href="#/quiz">測驗</a>，累積天數就會 +1。</div>
        </div>`,
      weekend: `<h2>🏖️ 週末：30～45 分鐘沉浸實戰</h2>
        <p>任選 2～3 個 15 分鐘模組自由搭配：</p>
        <div class="stack">
          <div class="box"><b>🎬 模組 1【動漫時事精聽】</b><br><a href="#/anime">動漫名台詞</a>、<a href="#/news">NHK 簡易新聞</a>、<a href="#/songs">童謡跟唱</a></div>
          <div class="box"><b>🍜 模組 2【情境模擬與美食解碼】</b><br><a href="#/talk">角色扮演</a>、<a href="#/travel/menu">燒肉壽司菜單</a>、<a href="#/travel/culture">文化避坑</a></div>
          <div class="box"><b>🗣️ 模組 3【影子跟讀與錯題清倉】</b><br><a href="#/speak">影子跟讀</a>、<a href="#/review">錯題本</a></div>
          <div class="box gold">🎖️ 週六日學習即可解鎖「🏖️ 週末充電王」成就！</div>
        </div>`,
      roadmap: `<h2>🗺️ 全階段日語路線圖</h2>
        <div class="stack">
          ${[
            ["階段 0：發音與五十音", "2～4 週", "假名直覺反射"],
            ["階段 1：旅遊生存與基礎會話", "JLPT N5｜2～3 個月", "自由行通關 ✈️"],
            ["階段 2：生活溝通與休閒娛樂", "JLPT N4～N3｜4～6 個月", "獨立生活 🏠 + 娛樂沉浸 🎮"],
            ["階段 3：職場入門與流暢交流", "JLPT N2｜6～9 個月", "日商求職、商務書信 💼"],
            ["階段 4：專業商務與深度融入", "JLPT N1 / BJT", "深度談判與商務協作"],
          ].map(([a, b, c], i) => `<div class="box"><b>${a}</b> <span class="small muted">（${b}）</span><br>${c}</div>${i < 4 ? '<div style="text-align:center" class="muted">↓</div>' : ""}`).join("")}
          <div class="box gold"><b>🎯 四大核心場景</b><br>✈️ 旅遊：點餐、問路、交通、退稅<br>🏠 生活：超商、租屋、看診<br>🎮 休閒：動漫、日劇、日本社群<br>💼 工作：日商應對、商業 Email、敬語</div>
        </div>`,
    };
    $app.innerHTML = `<h1>📋 學習計畫</h1><p class="lead">上班族專屬：能長久堅持，遠比一次讀很久更重要。</p>
      <div class="row" style="margin-bottom:14px">${[["weekday", "☕ 平日 15 分"], ["weekend", "🏖️ 假日沉浸"], ["roadmap", "🗺️ 路線圖"]].map(([k, t]) => `<a class="chip ${k === tab ? "active" : ""}" href="#/plan/${k}">${t}</a>`).join("")}</div>
      <div class="card" style="max-width:760px">${plans[tab] || plans.weekday}</div>`;
  };

  // ===== 我的（/profile） =====
  pages.me = () => {
    const acc = P.answered ? Math.round((P.correct / P.answered) * 100) : 0;
    $app.innerHTML = `<h1>👑 我的學習檔案</h1>
      <div class="grid tight" style="margin-bottom:16px">
        ${[["🔥", P.streak, "累積學習天數"], ["⚔️", `${P.completed.length}/20`, "已通關"], ["🎯", `${acc}%`, `答題正確率 (${P.answered} 題)`], ["🔄", P.mistakes.length, "待複習錯題"], ["🗓️", dailyStreak(), "連續每日挑戰"], ["🎤", P.micBest ? `${P.micBest} 分` : "—", `最佳發音 (${P.micTries || 0} 次)`], ["🃏", Object.keys(P.srs || {}).length, `學過的單字卡 (複習 ${P.srsReviews || 0} 次)`]]
          .map(([e, v, t]) => `<div class="card"><div class="emoji">${e}</div><div style="font-size:1.6rem;font-weight:700">${v}</div><div class="small muted">${t}</div></div>`).join("")}
      </div>
      <div class="card" style="margin-bottom:16px"><div class="spread"><h2>📅 學習紀錄</h2>
        ${P.goal ? `<span class="small">目標：${GOALS[P.goal].icon} ${GOALS[P.goal].name} <button class="btn small" data-goal="">更換</button></span>` : `<a class="btn small" href="#/">🧭 選擇學習目標</a>`}</div>${heatmapHTML()}</div>
      <h2>🎖️ 成就勳章 (${P.badges.length}/${Object.keys(D.badges).length})</h2>
      <div class="grid tight">${Object.entries(D.badges).map(([k, b]) => `
        <div class="card badge-tile ${P.badges.includes(k) ? "" : "locked"}"><div style="font-size:1.05rem"><b>${esc(b.name)}</b></div><div class="small muted">${esc(b.desc)}</div></div>`).join("")}</div>
      <div class="card" style="margin-top:20px">
        <h2>💾 進度備份</h2>
        <p class="small muted">進度只存在這個瀏覽器。換裝置時可匯出再匯入。</p>
        <div class="row"><button class="btn" id="exp">⬇️ 匯出進度</button><button class="btn" id="imp">⬆️ 匯入進度</button><button class="btn" id="wipe">🗑️ 清除全部進度</button></div>
        <textarea id="io" class="hidden" style="margin-top:10px;font-family:monospace;font-size:.8rem"></textarea>
        <button class="btn primary hidden" id="impGo" style="margin-top:8px">確認匯入</button>
      </div>`;
    const io = document.getElementById("io"), go = document.getElementById("impGo");
    document.getElementById("exp").onclick = () => { io.classList.remove("hidden"); go.classList.add("hidden"); io.value = btoa(unescape(encodeURIComponent(JSON.stringify(P)))); io.select(); toast("已產生備份碼，請複製保存"); };
    document.getElementById("imp").onclick = () => { io.classList.remove("hidden"); go.classList.remove("hidden"); io.value = ""; io.placeholder = "貼上備份碼"; };
    go.onclick = () => {
      try { P = Object.assign(blank(), JSON.parse(decodeURIComponent(escape(atob(io.value.trim()))))); save(); toast("✅ 匯入成功"); route(); }
      catch { toast("❌ 備份碼格式錯誤"); }
    };
    document.getElementById("wipe").onclick = () => { if (confirm("確定清除全部學習進度？此動作無法復原。")) { P = blank(); save(); route(); } };
  };

  /* ---------------- 路由 ---------------- */
  function route() {
    if ("speechSynthesis" in window) speechSynthesis.cancel();
    const [name = "", arg] = location.hash.replace(/^#\/?/, "").split("/");
    const page = pages[name] || pages[""];
    document.getElementById("nav").innerHTML = NAV.map(([k, t]) =>
      `<a href="#/${k}" class="${k === name || (name === "review" && k === "quiz") ? "active" : ""}">${t}</a>`).join("");
    const active = document.querySelector(".nav a.active");
    if (active) active.scrollIntoView({ inline: "center", block: "nearest" });
    page(arg);
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", route);

  /* ---------------- 主題 ---------------- */
  const root = document.documentElement;
  try { const t = localStorage.getItem("jp_theme"); if (t) root.dataset.theme = t; } catch {}
  document.getElementById("themeBtn").addEventListener("click", () => {
    const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("jp_theme", root.dataset.theme); } catch {}
  });

  renderStat();
  route();

  // 可安裝成 App、離線可用（本機預覽時不啟用，避免快取干擾開發）
  if ("serviceWorker" in navigator && !/^(localhost|127\.0\.0\.1)$/.test(location.hostname)) {
    navigator.serviceWorker.register("sw.js").catch(() => {});
  }
})();
