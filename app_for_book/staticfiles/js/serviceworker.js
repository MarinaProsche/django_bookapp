self.addEventListener('install', function(event) {
  console.log('Service Worker created');
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', function(event) {
});
