const CACHE_NAME = "health-alert-cache-v1";

const URLS_TO_CACHE = [
  "/",
  "/static/manifest.json"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(URLS_TO_CACHE);
    })
  );
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    }).catch(() => {
      return new Response(
        "<h3>Offline Mode: Showing last saved data</h3>",
        { headers: { "Content-Type": "text/html" } }
      );
    })
  );
});
