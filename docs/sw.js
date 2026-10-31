/* 離線快取：有網路時一律抓最新版（network-first），斷線才用快取，避免部署後還看到舊版。
   SHELL 有增減時要把 CACHE 版本號 +1，舊快取才會被清掉。 */
const CACHE = "jp-dojo-v4";
const SHELL = [
  "./", "index.html", "style.css", "app.js", "data.js", "manifest.webmanifest",
  "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png", "icons/apple-touch-icon.png",
  "kana_player.html", "handwriting.html",
];

self.addEventListener("install", (e) => {
  // cache: "reload" 跳過瀏覽器 HTTP 快取，確保預先存的是伺服器上的最新檔，而不是舊版殼
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL.map((u) => new Request(u, { cache: "reload" })))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    try {
      const res = await fetch(req, { cache: "no-cache" });
      if (res.ok) e.waitUntil(cache.put(req, res.clone()));
      return res;
    } catch (err) {
      // 離線：先找完全相同的網址，再忽略 ?query，最後頁面請求退回首頁殼
      const cached = (await cache.match(req)) || (await cache.match(req, { ignoreSearch: true }))
        || (req.mode === "navigate" ? await cache.match("./") : undefined);
      if (cached) return cached;
      throw err;
    }
  })());
});
