const CACHE_NAME = 'modis-bridgeworks-v1';
const ASSETS = [
  './',
  './qa-bank.html',
  './qa-manager.js',
  './data/questions.json'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
});

self.addEventListener('fetch', (e) => {
  e.respondWith(caches.match(e.request).then((res) => res || fetch(e.request)));
});
