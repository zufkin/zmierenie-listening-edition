const SHELL='zmierenie-shell-v2';
const AUDIO='zmierenie-downloads-v2';
const FILES=["./", "./index.html", "./styles.css", "./app.js", "./manifest.json", "./app.webmanifest", "./icon-192.png", "./icon-512.png"];
self.addEventListener('install',event=>event.waitUntil(caches.open(SHELL).then(cache=>cache.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET') return;
  event.respondWith(caches.match(event.request).then(hit=>hit||fetch(event.request).then(response=>{
    if(response.ok && new URL(event.request.url).pathname.includes('/audio/')) caches.open(AUDIO).then(cache=>cache.put(event.request,response.clone()));
    return response;
  })));
});

