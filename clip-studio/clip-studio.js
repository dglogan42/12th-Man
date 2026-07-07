/**
 * Sports Clip Studio — shared audio clip, trim, download & social/podcast share.
 * Usage: ClipStudio.init({ appId, appName, hashtags, ttsUrl, ... });
 */
(function (global) {
  const DEFAULTS = {
    appId: 'sports-app',
    appName: 'Sports Broadcast',
    shareTitle: 'Sports Clip',
    hashtags: '#Sports',
    defaultAnnouncer: 'default',
    defaultAnnouncerName: 'Announcer',
    ttsUrl: '/api/tts',
    ttsLocale: null,
    clipsApiUrl: '/api/clips',
    podcastFeedUrl: '/api/podcast/feed.rss',
    eventTitleSelector: null,
    eventTitle: null,
    filePrefix: 'sports-clip',
    storageKey: null,
    maxSaved: 24,
    injectModal: true,
    librarySelector: '#clip-library',
  };

  const state = {
    config: { ...DEFAULTS },
    cache: new Map(),
    saved: [],
    active: null,
    ready: false,
  };

  const MODAL_HTML = `
<div id="clip-modal" class="clip-modal" hidden>
  <div class="clip-modal-inner">
    <button type="button" id="clip-modal-close" class="clip-modal-close" aria-label="Close">✕</button>
    <h2>✂️ Clip Studio</h2>
    <p class="clip-modal-sub">Trim audio and share to social or podcast</p>
    <blockquote class="clip-quote-wrap">
      <p id="clip-quote" class="clip-quote"></p>
      <cite id="clip-announcer"></cite>
    </blockquote>
    <div class="clip-trim-row">
      <label>Start <span id="clip-trim-start-label">0:00</span></label>
      <input type="range" id="clip-trim-start" min="0" max="10" value="0" step="0.1">
    </div>
    <div class="clip-trim-row">
      <label>End <span id="clip-trim-end-label">0:00</span></label>
      <input type="range" id="clip-trim-end" min="0" max="10" value="10" step="0.1">
    </div>
    <p class="clip-duration">Clip length: <span id="clip-trim-duration">0:00</span></p>
    <audio id="clip-preview" controls class="clip-preview"></audio>
    <label class="clip-caption-label" for="clip-caption">Share caption</label>
    <textarea id="clip-caption" class="clip-caption" rows="4"></textarea>
    <div class="clip-actions-primary">
      <button type="button" id="clip-preview-btn" class="btn-clip">▶ Preview</button>
      <button type="button" id="clip-download-btn" class="btn-clip">⬇ Download</button>
      <button type="button" id="clip-copy-btn" class="btn-clip">📋 Copy caption</button>
    </div>
    <h3 class="clip-share-heading">Share to social</h3>
    <div class="clip-share-grid">
      <button type="button" id="clip-share-twitter" class="btn-share twitter">𝕏 Twitter</button>
      <button type="button" id="clip-share-bluesky" class="btn-share bluesky">🦋 Bluesky</button>
      <button type="button" id="clip-share-mastodon" class="btn-share mastodon">🐘 Mastodon</button>
      <button type="button" id="clip-share-threads" class="btn-share threads">🧵 Threads</button>
      <button type="button" id="clip-share-native" class="btn-share native">📤 Share / AirDrop</button>
    </div>
    <h3 class="clip-share-heading">Podcast platforms</h3>
    <div class="clip-share-grid">
      <button type="button" class="btn-share podcast" data-podcast="spotify">Spotify for Podcasters</button>
      <button type="button" class="btn-share podcast" data-podcast="apple">Apple Podcasts</button>
      <button type="button" class="btn-share podcast" data-podcast="anchor">Anchor</button>
      <button type="button" class="btn-share podcast" data-podcast="buzzsprout">Buzzsprout</button>
      <button type="button" class="btn-share podcast" data-podcast="iheart">iHeart Podcasts</button>
      <button type="button" id="clip-podcast-pack" class="btn-share podcast-pack">📦 Export show notes</button>
    </div>
    <p class="clip-rss-hint">Podcast RSS: <a id="podcast-rss-url" href="/api/podcast/feed.rss" target="_blank" rel="noopener">Subscribe to clip feed</a></p>
    <p id="clip-status" class="clip-status"></p>
  </div>
</div>`;

  function normalizeLine(line) {
    const ts = line.timestamp || Date.now();
    return {
      text: line.text || '',
      commentator: line.commentator || state.config.defaultAnnouncer,
      commentator_name: line.commentator_name || line.announcer || state.config.defaultAnnouncerName,
      event_label: line.event_label || line.event || '',
      timestamp: ts,
    };
  }

  function clipId(line) {
    const n = normalizeLine(line);
    return `${n.timestamp}-${n.commentator}-${n.text.slice(0, 32)}`;
  }

  function slugify(text) {
    return (text || 'clip').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40);
  }

  function formatDuration(sec) {
    const s = Math.max(0, sec || 0);
    return `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
  }

  function getEventTitle() {
    if (state.config.eventTitle) return state.config.eventTitle;
    if (state.config.eventTitleSelector) {
      const el = document.querySelector(state.config.eventTitleSelector);
      if (el?.textContent) return el.textContent.trim();
    }
    return state.config.appName;
  }

  function shareCaption(line) {
    const n = normalizeLine(line);
    const quote = n.text.slice(0, 220);
    return `"${quote}"\n\n— ${n.commentator_name} · ${getEventTitle()}\n\n${state.config.hashtags}`;
  }

  function setStatus(msg, isError) {
    const el = document.getElementById('clip-status');
    if (!el) return;
    el.textContent = msg;
    el.classList.toggle('error', !!isError);
  }

  function cacheLineAudio(line, blob) {
    if (!line || !blob || blob.size < 100) return;
    const n = normalizeLine(line);
    const id = clipId(n);
    const prev = state.cache.get(id);
    if (prev?.url) URL.revokeObjectURL(prev.url);
    state.cache.set(id, { line: n, blob, url: URL.createObjectURL(blob), id });
    if (state.cache.size > 48) {
      const first = state.cache.keys().next().value;
      const entry = state.cache.get(first);
      if (entry?.url) URL.revokeObjectURL(entry.url);
      state.cache.delete(first);
    }
  }

  async function getAudioDuration(blob) {
    return new Promise((resolve) => {
      const url = URL.createObjectURL(blob);
      const audio = new Audio();
      audio.onloadedmetadata = () => { URL.revokeObjectURL(url); resolve(audio.duration || 5); };
      audio.onerror = () => { URL.revokeObjectURL(url); resolve(5); };
      audio.src = url;
    });
  }

  function audioBufferToWav(buffer) {
    const numCh = buffer.numberOfChannels;
    const sampleRate = buffer.sampleRate;
    const numFrames = buffer.length;
    const blockAlign = numCh * 2;
    const dataSize = numFrames * blockAlign;
    const array = new ArrayBuffer(44 + dataSize);
    const view = new DataView(array);
    const writeStr = (o, s) => { for (let i = 0; i < s.length; i++) view.setUint8(o + i, s.charCodeAt(i)); };
    writeStr(0, 'RIFF');
    view.setUint32(4, 36 + dataSize, true);
    writeStr(8, 'WAVE');
    writeStr(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numCh, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * blockAlign, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, 16, true);
    writeStr(36, 'data');
    view.setUint32(40, dataSize, true);
    let offset = 44;
    for (let i = 0; i < numFrames; i++) {
      for (let ch = 0; ch < numCh; ch++) {
        const sample = Math.max(-1, Math.min(1, buffer.getChannelData(ch)[i]));
        view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
        offset += 2;
      }
    }
    return new Blob([array], { type: 'audio/wav' });
  }

  async function trimAudioBlob(blob, startSec, endSec) {
    const ctx = new AudioContext();
    try {
      const audioBuffer = await ctx.decodeAudioData(await blob.arrayBuffer());
      const start = Math.max(0, Math.min(startSec, audioBuffer.duration));
      const end = Math.max(start + 0.1, Math.min(endSec, audioBuffer.duration));
      const startSample = Math.floor(start * audioBuffer.sampleRate);
      const endSample = Math.floor(end * audioBuffer.sampleRate);
      const length = Math.max(1, endSample - startSample);
      const trimmed = ctx.createBuffer(audioBuffer.numberOfChannels, length, audioBuffer.sampleRate);
      for (let ch = 0; ch < audioBuffer.numberOfChannels; ch++) {
        trimmed.getChannelData(ch).set(audioBuffer.getChannelData(ch).subarray(startSample, endSample));
      }
      return audioBufferToWav(trimmed);
    } finally {
      await ctx.close();
    }
  }

  async function fetchLineAudio(line) {
    const n = normalizeLine(line);
    if (!n.text) return null;
    const params = new URLSearchParams({ text: n.text, announcer: n.commentator });
    if (state.config.ttsLocale) params.set('locale', state.config.ttsLocale);
    try {
      const res = await fetch(`${state.config.ttsUrl}?${params}`);
      if (!res.ok) return null;
      const blob = await res.blob();
      return blob.size >= 100 ? blob : null;
    } catch {
      return null;
    }
  }

  function bindModal() {
    if (state.ready) return;
    if (state.config.injectModal && !document.getElementById('clip-modal')) {
      document.body.insertAdjacentHTML('beforeend', MODAL_HTML);
    }
    const rss = document.getElementById('podcast-rss-url');
    if (rss && state.config.podcastFeedUrl) rss.href = state.config.podcastFeedUrl;

    document.getElementById('clip-modal-close')?.addEventListener('click', close);
    document.getElementById('clip-trim-start')?.addEventListener('input', updateTrimLabels);
    document.getElementById('clip-trim-end')?.addEventListener('input', updateTrimLabels);
    document.getElementById('clip-preview-btn')?.addEventListener('click', previewClip);
    document.getElementById('clip-download-btn')?.addEventListener('click', downloadClip);
    document.getElementById('clip-copy-btn')?.addEventListener('click', copyCaption);
    document.getElementById('clip-share-native')?.addEventListener('click', shareNative);
    document.getElementById('clip-share-twitter')?.addEventListener('click', () => shareSocial('twitter'));
    document.getElementById('clip-share-bluesky')?.addEventListener('click', () => shareSocial('bluesky'));
    document.getElementById('clip-share-mastodon')?.addEventListener('click', () => shareSocial('mastodon'));
    document.getElementById('clip-share-threads')?.addEventListener('click', () => shareSocial('threads'));
    document.getElementById('clip-podcast-pack')?.addEventListener('click', exportPodcastPack);
    document.querySelectorAll('[data-podcast]').forEach((btn) => {
      btn.addEventListener('click', () => sharePodcastPlatform(btn.dataset.podcast));
    });
    document.getElementById('clip-modal')?.addEventListener('click', (e) => {
      if (e.target?.id === 'clip-modal') close();
    });
    state.ready = true;
    renderSavedClips();
  }

  function updateTrimLabels() {
    if (!state.active) return;
    const start = parseFloat(document.getElementById('clip-trim-start').value);
    const end = parseFloat(document.getElementById('clip-trim-end').value);
    state.active.trimStart = Math.min(start, end - 0.1);
    state.active.trimEnd = Math.max(end, state.active.trimStart + 0.1);
    document.getElementById('clip-trim-start-label').textContent = formatDuration(state.active.trimStart);
    document.getElementById('clip-trim-end-label').textContent = formatDuration(state.active.trimEnd);
    document.getElementById('clip-trim-duration').textContent =
      formatDuration(state.active.trimEnd - state.active.trimStart);
  }

  async function getExportBlob() {
    if (!state.active) return null;
    const { blob, trimStart, trimEnd, duration } = state.active;
    if (trimStart <= 0.05 && trimEnd >= duration - 0.05) return blob;
    return trimAudioBlob(blob, trimStart, trimEnd);
  }

  async function open(line) {
    bindModal();
    const n = normalizeLine(line);
    let entry = state.cache.get(clipId(n));
    if (!entry) {
      setStatus('Generating audio…');
      const blob = await fetchLineAudio(n);
      if (!blob) { setStatus('Could not generate audio. Run clip-server or enable TTS API.', true); return; }
      cacheLineAudio(n, blob);
      entry = state.cache.get(clipId(n));
    }
    state.active = {
      ...entry,
      duration: await getAudioDuration(entry.blob),
      trimStart: 0,
      trimEnd: null,
      eventTitle: getEventTitle(),
    };
    state.active.trimEnd = state.active.duration;
    const modal = document.getElementById('clip-modal');
    modal.hidden = false;
    document.body.classList.add('clip-modal-open');
    document.getElementById('clip-quote').textContent = n.text;
    document.getElementById('clip-announcer').textContent = n.commentator_name;
    document.getElementById('clip-caption').value = shareCaption(n);
    const startSlider = document.getElementById('clip-trim-start');
    const endSlider = document.getElementById('clip-trim-end');
    startSlider.max = Math.max(0, state.active.duration - 0.1).toFixed(1);
    endSlider.max = state.active.duration.toFixed(1);
    startSlider.value = '0';
    endSlider.value = state.active.duration.toFixed(1);
    updateTrimLabels();
    setStatus('');
    renderSavedClips();
  }

  function close() {
    const modal = document.getElementById('clip-modal');
    if (modal) modal.hidden = true;
    document.body.classList.remove('clip-modal-open');
    const preview = document.getElementById('clip-preview');
    if (preview) { preview.pause(); preview.removeAttribute('src'); }
  }

  async function previewClip() {
    const exportBlob = await getExportBlob();
    if (!exportBlob) return;
    const preview = document.getElementById('clip-preview');
    if (preview.src?.startsWith('blob:')) URL.revokeObjectURL(preview.src);
    preview.src = URL.createObjectURL(exportBlob);
    preview.play().catch(() => {});
  }

  async function registerOnServer(line, caption) {
    if (!state.config.clipsApiUrl) return null;
    try {
      const n = normalizeLine(line);
      const res = await fetch(state.config.clipsApiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: n.text,
          announcer: n.commentator,
          commentator_name: n.commentator_name,
          event_title: getEventTitle(),
          caption,
        }),
      });
      const data = await res.json();
      if (data.feed_url) {
        const rss = document.getElementById('podcast-rss-url');
        if (rss) rss.href = data.feed_url;
      }
      return data;
    } catch { return null; }
  }

  function saveToLibrary(blob) {
    if (!state.active) return;
    const caption = document.getElementById('clip-caption').value;
    const entry = {
      id: `saved-${Date.now()}`,
      line: state.active.line,
      caption,
      blob,
      url: URL.createObjectURL(blob),
    };
    state.saved.unshift(entry);
    if (state.saved.length > state.config.maxSaved) {
      const old = state.saved.pop();
      if (old?.url) URL.revokeObjectURL(old.url);
    }
    const key = state.config.storageKey || `${state.config.appId}_clips_meta`;
    try {
      localStorage.setItem(key, JSON.stringify(state.saved.map((c) => ({
        id: c.id, caption: c.caption, text: c.line.text, announcer: c.line.commentator_name,
      }))));
    } catch { /* quota */ }
    registerOnServer(state.active.line, caption);
    renderSavedClips();
  }

  async function downloadClip() {
    const exportBlob = await getExportBlob();
    if (!exportBlob || !state.active) return;
    const ext = exportBlob.type.includes('wav') ? 'wav' : 'mp3';
    const name = `${state.config.filePrefix}-${slugify(state.active.line.commentator_name)}-${Date.now()}.${ext}`;
    const url = URL.createObjectURL(exportBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    a.click();
    URL.revokeObjectURL(url);
    saveToLibrary(exportBlob);
    setStatus(`Downloaded ${name}`);
  }

  function renderSavedClips() {
    const list = document.querySelector(state.config.librarySelector);
    if (!list) return;
    if (!state.saved.length) {
      list.innerHTML = '<p class="clip-empty">No saved clips — tap ✂️ on any line.</p>';
      return;
    }
    list.innerHTML = state.saved.map((c) => `
      <div class="clip-library-item">
        <div class="clip-lib-info">
          <strong>${c.line.commentator_name}</strong>
          <span>${c.line.text.slice(0, 55)}${c.line.text.length > 55 ? '…' : ''}</span>
        </div>
        <div class="clip-lib-actions">
          <button type="button" class="btn-clip-mini" data-play="${c.id}">▶</button>
          <button type="button" class="btn-clip-mini" data-copy="${c.id}">📋</button>
        </div>
      </div>`).join('');
    list.querySelectorAll('[data-play]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const item = state.saved.find((c) => c.id === btn.dataset.play);
        if (!item) return;
        const preview = document.getElementById('clip-preview');
        if (preview?.src?.startsWith('blob:')) URL.revokeObjectURL(preview.src);
        if (preview) { preview.src = item.url; preview.play().catch(() => {}); }
      });
    });
    list.querySelectorAll('[data-copy]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const item = state.saved.find((c) => c.id === btn.dataset.copy);
        if (item) navigator.clipboard.writeText(item.caption).then(() => setStatus('Caption copied.'));
      });
    });
  }

  function getShareText() {
    return document.getElementById('clip-caption')?.value || '';
  }

  function openShareUrl(base, text) {
    window.open(`${base}${encodeURIComponent(text)}`, '_blank', 'noopener,noreferrer,width=600,height=700');
  }

  async function shareSocial(platform) {
    const text = getShareText();
    const urls = {
      twitter: 'https://twitter.com/intent/tweet?text=',
      bluesky: 'https://bsky.app/intent/compose?text=',
      threads: 'https://www.threads.net/intent/post?text=',
    };
    if (platform === 'mastodon') {
      const instance = prompt('Mastodon instance (e.g. mastodon.social):', 'mastodon.social');
      if (!instance) return;
      const host = instance.replace(/^https?:\/\//, '').replace(/\/$/, '');
      openShareUrl(`https://${host}/share?text=`, text);
    } else if (urls[platform]) {
      openShareUrl(urls[platform], text);
    }
    const blob = await getExportBlob();
    if (blob) saveToLibrary(blob);
  }

  async function shareNative() {
    const exportBlob = await getExportBlob();
    const text = getShareText();
    if (!exportBlob) return;
    const ext = exportBlob.type.includes('wav') ? 'wav' : 'mp3';
    const file = new File([exportBlob], `${state.config.filePrefix}.${ext}`, { type: exportBlob.type });
    if (navigator.share && navigator.canShare?.({ files: [file] })) {
      try {
        await navigator.share({ title: state.config.shareTitle, text, files: [file] });
        saveToLibrary(exportBlob);
        return;
      } catch (e) { if (e.name === 'AbortError') return; }
    }
    await downloadClip();
    setStatus('Audio downloaded — attach manually to your post.');
  }

  function sharePodcastPlatform(platform) {
    const links = {
      spotify: 'https://podcasters.spotify.com/',
      apple: 'https://podcastsconnect.apple.com/',
      buzzsprout: 'https://www.buzzsprout.com/',
      anchor: 'https://anchor.fm/',
      iheart: 'https://www.iheart.com/podcast-network/',
    };
    downloadClip();
    if (links[platform]) {
      setStatus('Clip downloaded — upload to podcast host.');
      window.open(links[platform], '_blank', 'noopener');
    }
  }

  async function exportPodcastPack() {
    const clips = state.saved.length ? state.saved : (state.active ? [state.active] : []);
    if (!clips.length) { setStatus('Save a clip first.', true); return; }
    const notes = clips.map((c, i) => {
      const line = c.line || c;
      return `Clip ${i + 1}\n${line.commentator_name}: "${line.text}"`;
    }).join('\n\n---\n\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([notes], { type: 'text/plain' }));
    a.download = `${state.config.filePrefix}-show-notes-${Date.now()}.txt`;
    a.click();
    if (state.active) await downloadClip();
    setStatus('Show notes exported.');
  }

  function copyCaption() {
    navigator.clipboard.writeText(getShareText()).then(() => setStatus('Caption copied.'))
      .catch(() => setStatus('Could not copy.', true));
  }

  function createButton(line, label) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn-clip-line clip-studio-btn';
    btn.title = 'Clip & share';
    btn.setAttribute('aria-label', 'Clip audio');
    btn.textContent = label || '✂️';
    btn.addEventListener('click', (e) => { e.stopPropagation(); open(line); });
    return btn;
  }

  function attachButton(parent, line, label) {
    if (!parent) return null;
    const btn = createButton(line, label);
    parent.appendChild(btn);
    return btn;
  }

  function makeLine(text, commentatorName, commentator, extra) {
    return {
      text,
      commentator_name: commentatorName || state.config.defaultAnnouncerName,
      commentator: commentator || state.config.defaultAnnouncer,
      timestamp: Date.now(),
      ...extra,
    };
  }

  function init(userConfig) {
    state.config = { ...DEFAULTS, ...userConfig };
    if (state.config.storageKey == null) {
      state.config.storageKey = `${state.config.appId}_clips_meta`;
    }
    bindModal();
    return ClipStudio;
  }

  const ClipStudio = {
    init,
    open,
    close,
    cacheLineAudio,
    createButton,
    attachButton,
    makeLine,
    shareCaption,
    fetchLineAudio,
    renderSavedClips,
  };

  global.ClipStudio = ClipStudio;
  global.cacheLineAudio = cacheLineAudio;
  global.openClipStudio = open;
  global.initClips = () => init(global.__clipStudioConfig || {});

})(typeof window !== 'undefined' ? window : globalThis);