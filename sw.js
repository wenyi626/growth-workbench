/* 个人成长工作台 · Service Worker
 * 离线缓存应用外壳（index.html 内联了全部 CSS/JS，缓存它即可离线使用）。
 * 不改动任何业务代码，仅做静态资源缓存与离线回退。 */
const CACHE = 'pgwb-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png'
];

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(ASSETS).catch(function () {});
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) {
        return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (event) {
  var req = event.request;
  // 只处理同源 GET；POST（如 /__backup 云端备份）与跨域请求直接放行
  if (req.method !== 'GET') return;
  if (new URL(req.url).origin !== self.location.origin) return;

  // 页面导航：网络优先，失败回退到缓存的 index.html（保证离线可打开）
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req).catch(function () { return caches.match('./index.html'); })
    );
    return;
  }

  // 其他静态资源：缓存优先，缺失再请求
  event.respondWith(
    caches.match(req).then(function (cached) {
      return cached || fetch(req).catch(function () { return cached; });
    })
  );
});

// 由页面触发「立即更新」：跳过 waiting，立即激活新 SW 并接管客户端
self.addEventListener('message', function (event) {
  if (event.data === 'skip') self.skipWaiting();
});
