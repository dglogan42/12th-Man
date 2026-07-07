/** TTS playback — server Google TTS API + Web Speech API fallback */

const TTS = {
  enabled: true,
  queue: [],
  playing: false,
  currentAudio: null,
  voices: {},
  useServer: true,
};

function loadTtsPrefs() {
  const saved = localStorage.getItem('twelfthman_tts');
  if (saved !== null) TTS.enabled = saved === '1';
  const server = localStorage.getItem('twelfthman_tts_server');
  if (server !== null) TTS.useServer = server === '1';
}

function saveTtsPrefs() {
  localStorage.setItem('twelfthman_tts', TTS.enabled ? '1' : '0');
  localStorage.setItem('twelfthman_tts_server', TTS.useServer ? '1' : '0');
}

async function loadTtsVoices() {
  try {
    const res = await fetch('/api/tts/voices');
    const data = await res.json();
    TTS.voices = Object.fromEntries(data.voices.map((v) => [v.id, v]));
  } catch {
    TTS.voices = {};
  }
}

function updateTtsUI() {
  const toggle = document.getElementById('tts-enabled');
  const serverToggle = document.getElementById('tts-server');
  const status = document.getElementById('tts-status');
  if (toggle) toggle.checked = TTS.enabled;
  if (serverToggle) serverToggle.checked = TTS.useServer;
  if (status) {
    status.textContent = TTS.enabled
      ? (TTS.useServer ? '🔊 Google TTS (free)' : '🔊 Browser voice')
      : '🔇 Muted';
  }
}

function speakLine(line) {
  if (!TTS.enabled || !line?.text) return;
  TTS.queue.push(line);
  drainQueue();
}

function drainQueue() {
  if (TTS.playing || !TTS.queue.length) return;
  const line = TTS.queue.shift();
  TTS.playing = true;
  const done = () => {
    TTS.playing = false;
    drainQueue();
  };
  if (TTS.useServer) {
    playServerTts(line).then(done).catch(done);
  } else {
    playBrowserTts(line).then(done).catch(done);
  }
}

async function playServerTts(line) {
  TTS.playing = true;
  const params = new URLSearchParams({
    text: line.text,
    commentator: line.commentator || 'richie',
  });
  try {
    const res = await fetch(`/api/tts?${params}`);
    if (!res.ok) throw new Error('TTS failed');
    const blob = await res.blob();
    if (blob.size < 100) throw new Error('empty audio');

    if (window.ClipStudio) ClipStudio.cacheLineAudio(line, blob);

    if (TTS.currentAudio) {
      TTS.currentAudio.pause();
      URL.revokeObjectURL(TTS.currentAudio.src);
    }
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    TTS.currentAudio = audio;
    await new Promise((resolve, reject) => {
      audio.onended = () => {
        URL.revokeObjectURL(url);
        resolve();
      };
      audio.onerror = reject;
      audio.play().catch(reject);
    });
  } catch {
    playBrowserTts(line);
  }
}

function playBrowserTts(line) {
  return new Promise((resolve, reject) => {
    if (!window.speechSynthesis) {
      resolve();
      return;
    }
    const cfg = TTS.voices[line.commentator] || { rate_hint: 1, pitch_hint: 1, locale: 'en-au' };
    const utter = new SpeechSynthesisUtterance(line.text);
    utter.rate = cfg.rate_hint || 1;
    utter.pitch = cfg.pitch_hint || 1;
    utter.lang = cfg.locale || 'en-AU';

    const voices = speechSynthesis.getVoices();
    const langPrefix = (cfg.locale || 'en-au').split('-')[0];
    const match = voices.find((v) => v.lang.toLowerCase().startsWith(langPrefix));
    if (match) utter.voice = match;

    utter.onend = resolve;
    utter.onerror = resolve;
    speechSynthesis.speak(utter);
  });
}

function stopTts() {
  TTS.queue = [];
  TTS.playing = false;
  if (TTS.currentAudio) {
    TTS.currentAudio.pause();
    URL.revokeObjectURL(TTS.currentAudio.src);
    TTS.currentAudio = null;
  }
  if (window.speechSynthesis) speechSynthesis.cancel();
}

async function testTts() {
  speakLine({
    text: "Got him, yes! Piss off! You're out! The tension, the drama, the buzz!",
    commentator: 'bill',
    commentator_name: 'Bill Lawry',
  });
}

function initTts() {
  loadTtsPrefs();
  loadTtsVoices().then(updateTtsUI);

  const toggle = document.getElementById('tts-enabled');
  const serverToggle = document.getElementById('tts-server');
  const testBtn = document.getElementById('btn-tts-test');

  if (toggle) {
    toggle.addEventListener('change', (e) => {
      TTS.enabled = e.target.checked;
      saveTtsPrefs();
      updateTtsUI();
      if (!TTS.enabled) stopTts();
    });
  }
  if (serverToggle) {
    serverToggle.addEventListener('change', (e) => {
      TTS.useServer = e.target.checked;
      saveTtsPrefs();
      updateTtsUI();
    });
  }
  if (testBtn) {
    testBtn.addEventListener('click', testTts);
  }

  if (window.speechSynthesis) {
    speechSynthesis.onvoiceschanged = () => loadTtsVoices();
  }
}