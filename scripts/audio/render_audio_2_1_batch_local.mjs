import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const repo = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/(?:[A-Za-z]:)/, m => m.slice(1))), '..', '..');
const masterPath = path.join(repo, 'book', 'audio-script-master-sk-2026-09-01.md');
const legacyEnvPath = 'C:/Users/zufki/Claude/Projects/web tf.truni.sk/scripts/listening-edition/.env';
const outDir = path.join(repo, 'dist', 'audio-2.1-B-full');
const settings = { stability: 0.65, similarity_boost: 0.80, style: 0, speed: 0.97, use_speaker_boost: true };
const modelId = 'eleven_multilingual_v2';
const outputFormat = 'mp3_44100_128';

function parseEnv(text) {
  const env = {};
  for (const raw of text.split(/\r?\n/u)) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const i = line.indexOf('=');
    if (i > 0) env[line.slice(0, i).trim()] = line.slice(i + 1).trim().replace(/^['"]|['"]$/g, '');
  }
  return env;
}

function chapterText(master, number) {
  const nn = String(number).padStart(2, '0');
  const start = new RegExp(`^## ${nn} · .*$`, 'm').exec(master);
  if (!start) throw new Error(`chapter ${nn} not found`);
  const tail = master.slice(start.index + start[0].length);
  const next = number < 12 ? new RegExp(`^## ${String(number + 1).padStart(2, '0')} · .*$`, 'm').exec(tail) : null;
  return (next ? tail.slice(0, next.index) : tail).replace(/^\*Redakčné označenie — nečíta sa\.\*\s*/m, '').trim();
}

const env = parseEnv(fs.readFileSync(legacyEnvPath, 'utf8'));
let apiKey = env.ELEVENLABS_API_KEY;
const voiceId = env.ELEVENLABS_VOICE_ID;
if (!apiKey || !voiceId) throw new Error('local ElevenLabs config missing');
const master = fs.readFileSync(masterPath, 'utf8');
fs.mkdirSync(outDir, { recursive: true });
const results = [];

for (let chapter = 1; chapter <= 12; chapter++) {
  const nn = String(chapter).padStart(2, '0');
  const text = chapterText(master, chapter);
  const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${encodeURIComponent(voiceId)}?output_format=${outputFormat}`, {
    method: 'POST',
    headers: { 'xi-api-key': apiKey, 'Content-Type': 'application/json', Accept: 'audio/mpeg' },
    body: JSON.stringify({ text, model_id: modelId, voice_settings: settings }),
  });
  if (!response.ok) throw new Error(`chapter ${nn} ElevenLabs HTTP ${response.status}: ${(await response.text()).slice(0, 300)}`);
  const audio = Buffer.from(await response.arrayBuffer());
  if (audio.length < 10000) throw new Error(`chapter ${nn} audio unexpectedly small`);
  const file = `zmierenie-${nn}-reflexia-audio-2.1-B.mp3`;
  fs.writeFileSync(path.join(outDir, file), audio);
  const sha256 = crypto.createHash('sha256').update(audio).digest('hex');
  results.push({ chapter, file, bytes: audio.length, sha256, sourceChars: text.length });
  console.log(`chapter ${nn}: ${audio.length} bytes`);
}
apiKey = '';
const receipt = {
  status: 'FULL_BATCH_PREVIEW_READY',
  profile: 'B',
  voiceId,
  model: modelId,
  outputFormat,
  voiceSettings: settings,
  textSource: 'book/audio-script-master-sk-2026-09-01.md',
  textChanged: false,
  productionAudioChanged: false,
  results,
};
fs.writeFileSync(path.join(outDir, 'receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
console.log('FULL_BATCH_PREVIEW_READY');
