/* 離線快取：有網路時一律抓最新版（network-first），斷線才用快取，避免部署後還看到舊版 */
const CACHE = "jp-dojo-v2";
const SHELL = ["./", "index.html", "style.css", "app.js", "data.js", "manifest.webmanifest", "icons/icon-192.png", "kana_player.html", "handwriting.html"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
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
      const cached = await cache.match(req);
      if (cached) return cached;
      throw err;
    }
  })());
});
