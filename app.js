const $ = (s) => document.querySelector(s);
const audio = $('#audio');
const DEFAULT = { chapter: 1, layer: 'pribeh', time: 0, queueIndex: 0, speed: 1, autoplay: true };
let M;
let state;
let queue = [];

try {
  state = { ...DEFAULT, ...JSON.parse(localStorage.getItem('zmierenie-state') || '{}') };
} catch {
  state = { ...DEFAULT };
}

const save = () => {
  state.time = audio.currentTime || 0;
  state.speed = audio.playbackRate || 1;
  state.autoplay = $('#autoplay').checked;
  localStorage.setItem('zmierenie-state', JSON.stringify(state));
};

const currentChapter = () => M.chapters.find((c) => c.number === state.chapter);
const makeQueue = () => {
  const c = currentChapter();
  const ids = state.layer === 'all' ? M.layers.map((l) => l.id) : [state.layer];
  return ids.map((id) => ({ chapter: c.number, layer: id, src: c.layers[id].audio }));
};
function fmt(seconds) {
  if (!Number.isFinite(seconds)) return '0:00';
  return `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
}

function tick() {
  $('#elapsed').textContent = fmt(audio.currentTime);
  $('#duration').textContent = fmt(audio.duration);
  $('#seek').value = audio.duration ? (audio.currentTime / audio.duration) * 1000 : 0;
}

function loadTrack(time = 0, autoplay = false) {
  const item = queue[state.queueIndex] || queue[0];
  if (!item) return;
  audio.src = item.src;
  audio.load();
  audio.addEventListener('loadedmetadata', () => {
    audio.currentTime = Math.min(time, audio.duration || 0);
    audio.playbackRate = state.speed || 1;
    tick();
    if (autoplay) audio.play().catch(() => {});
  }, { once: true });
}

function render(autoplay = false) {
  const c = currentChapter();
  $('#number').textContent = `Kapitola ${String(c.number).padStart(2, '0')}`;
  $('#title').textContent = c.title;  const choices = [...M.layers.map((l) => [l.id, l.label]), ['all', 'CelĂ© za sebou']];
  $('#layers').innerHTML = choices.map(([id, label]) =>
    `<button data-layer="${id}" class="${state.layer === id ? 'active' : ''}">${label}</button>`
  ).join('');
  $('#chapters').innerHTML = M.chapters.map((x) =>
    `<button class="chapter ${x.number === c.number ? 'active' : ''}" data-chapter="${x.number}">` +
    `<span>${String(x.number).padStart(2, '0')}</span>${x.title}</button>`
  ).join('');

  queue = makeQueue();
  if (state.layer !== 'all') state.queueIndex = 0;
  state.queueIndex = Math.max(0, Math.min(state.queueIndex || 0, queue.length - 1));
  loadTrack(state.time || 0, autoplay);
}

function goChapter(delta, autoplay = true) {
  const numbers = M.chapters.map((c) => c.number);
  const index = numbers.indexOf(state.chapter);
  const next = Math.max(0, Math.min(numbers.length - 1, index + delta));
  if (next === index && delta !== 0) return;
  state.chapter = numbers[next];
  state.queueIndex = 0;
  state.time = 0;
  render(autoplay);
  save();
}

function move(delta) {
  if (state.layer === 'all') {    const next = state.queueIndex + delta;
    if (next >= 0 && next < queue.length) {
      state.queueIndex = next;
      state.time = 0;
      loadTrack(0, true);
      save();
      return;
    }
  }
  goChapter(delta, true);
}

$('#layers').addEventListener('click', (e) => {
  const layer = e.target.dataset.layer;
  if (!layer) return;
  state.layer = layer;
  state.queueIndex = 0;
  state.time = 0;
  render(false);
  save();
});

$('#chapters').addEventListener('click', (e) => {
  const button = e.target.closest('[data-chapter]');
  if (!button) return;
  state.chapter = Number(button.dataset.chapter);
  state.queueIndex = 0;
  state.time = 0;
  render(false);
  save();
});
$('#play').addEventListener('click', () => audio.paused ? audio.play() : audio.pause());
audio.addEventListener('play', () => { $('#play').textContent = 'â…ˇ'; });
audio.addEventListener('pause', () => { $('#play').textContent = 'â–¶'; });
audio.addEventListener('timeupdate', () => {
  tick();
  if (Math.floor(audio.currentTime) % 5 === 0) save();
});
$('#seek').addEventListener('input', (e) => {
  if (audio.duration) audio.currentTime = audio.duration * Number(e.target.value) / 1000;
});
$('#speed').addEventListener('change', (e) => {
  state.speed = parseFloat(e.target.value);
  audio.playbackRate = state.speed;
  save();
});
$('#prev').addEventListener('click', () => move(-1));
$('#next').addEventListener('click', () => move(1));

audio.addEventListener('ended', () => {
  if (state.layer === 'all' && state.queueIndex < queue.length - 1) {
    state.queueIndex += 1;
    state.time = 0;
    loadTrack(0, true);
    save();
    return;
  }
  if ($('#autoplay').checked) goChapter(1, true);
});
$('#download').addEventListener('click', async () => {
  if (!('caches' in window)) {
    $('#status').textContent = 'Offline uloĹľenie tento prehliadaÄŤ nepodporuje.';
    return;
  }
  const urls = M.chapters.flatMap((c) => M.layers.map((l) => c.layers[l.id].audio));
  const cache = await caches.open('zmierenie-downloads-v1');
  if (navigator.storage?.persist) await navigator.storage.persist().catch(() => false);
  $('#download').disabled = true;
  try {
    for (let i = 0; i < urls.length; i += 1) {
      $('#status').textContent = `UkladĂˇm knihu na cestuâ€¦ ${i + 1}/${urls.length}`;
      const request = new Request(urls[i], { cache: 'reload' });
      const response = await fetch(request);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      await cache.put(request, response);
    }
    $('#status').textContent = 'CelĂˇ kniha je uloĹľenĂˇ na offline poÄŤĂşvanie.';
  } catch (error) {
    $('#status').textContent = `Offline uloĹľenie sa preruĹˇilo: ${error.message}. SkĂşs tlaÄŤidlo znova.`;
  } finally {
    $('#download').disabled = false;
  }
});

M = await fetch('./manifest.json').then((r) => {
  if (!r.ok) throw new Error(`Manifest HTTP ${r.status}`);
  return r.json();
});
if (!M.chapters.some((c) => c.number === state.chapter)) state = { ...DEFAULT };
$('#autoplay').checked = state.autoplay !== false;
$('#speed').value = `${state.speed || 1}Ă—`;
render(false);
addEventListener('beforeunload', save);
if ('serviceWorker' in navigator) navigator.serviceWorker.register('./sw.js', { scope: './' });

