const API = '';
let selectedMatchId = 'demo-ashes-test';
let selectedSeries = '';
let selectedFormat = '';
let lastTimestamp = 0;
let pollInterval = null;
let scoreInterval = null;
let isRunning = false;
let allSeries = [];

const $ = (sel) => document.querySelector(sel);

async function fetchJSON(path, opts = {}) {
  const res = await fetch(API + path, opts);
  return res.json();
}

function buildQuery() {
  const params = new URLSearchParams();
  if (selectedSeries) params.set('series', selectedSeries);
  if (selectedFormat) params.set('format', selectedFormat);
  const q = params.toString();
  return q ? `?${q}` : '';
}

function renderBroadcastLink(l) {
  const cls = l.platform || 'sky';
  const boosted = l.boosted ? ' boosted' : '';
  const appBtn = l.app_url
    ? `<a href="${l.app_url}" class="open-app" title="Open in app" target="_blank" rel="noopener">App</a>`
    : '';
  return `
    <div class="broadcast-link-wrap">
      <a href="${l.url}" target="_blank" rel="noopener"
         class="broadcast-link ${cls}${boosted}" data-platform="${l.platform}">
        <span class="logo">${l.logo}</span>
        <div class="info">
          <strong>${l.name}</strong>
          <span>${l.description}</span>
        </div>
        <span class="region">${l.region}</span>
      </a>
      ${appBtn}
    </div>`;
}

async function loadBroadcastLinks() {
  const seriesParam = selectedSeries ? `?series=${selectedSeries}` : '';
  const data = await fetchJSON(`/api/broadcast${seriesParam}`);

  const radioEl = $('#radio-links');
  const tvEl = $('#tv-links');

  if (radioEl) {
    const radio = data.radio || [];
    radioEl.innerHTML = radio.length
      ? radio.map(renderBroadcastLink).join('')
      : '<p class="no-matches">No radio links available.</p>';
  }

  if (tvEl) {
    const tv = data.tv || [];
    tvEl.innerHTML = tv.length
      ? tv.map(renderBroadcastLink).join('')
      : '<p class="no-matches">No TV links available.</p>';
  }
}

function populateSeriesFilter(seriesList) {
  allSeries = seriesList;
  const sel = $('#series-filter');
  const current = sel.value;
  sel.innerHTML = '<option value="">All Series</option>' +
    seriesList.map((s) =>
      `<option value="${s.id}">${s.emoji} ${s.name}</option>`
    ).join('');
  sel.value = current;
}

async function loadMatches() {
  const data = await fetchJSON(`/api/matches${buildQuery()}`);

  if (data.series) populateSeriesFilter(data.series);

  const container = $('#match-list');
  if (!data.matches.length) {
    container.innerHTML = '<p class="no-matches">No matches found for these filters.</p>';
  } else {
    container.innerHTML = data.matches.map((m) => {
      const statusCls = m.status === 'live' ? 'status-live' : 'status-upcoming';
      const statusLabel = m.status === 'live' ? '● LIVE' : m.status.toUpperCase();
      const fmtTag = m.format
        ? `<span class="format-tag ${m.format}">${m.format_label || m.format.toUpperCase()}</span>` : '';
      const seriesTag = m.series_name
        ? `<span class="series-tag">${m.series_name}</span>` : '';
      return `
        <div class="match-card ${m.id === selectedMatchId ? 'selected' : ''}"
             data-id="${m.id}" data-series="${m.series}" data-format="${m.format}">
          <div class="title">${m.title}</div>
          <div class="meta">
            ${fmtTag}${seriesTag}
            <span class="${statusCls}">${statusLabel}</span>
            ${m.venue ? ` · ${m.venue}` : ''}
            ${m.score ? ` · ${m.score}` : ''}
          </div>
        </div>`;
    }).join('');
  }

  $('#api-status').textContent = data.api_hint;

  container.querySelectorAll('.match-card').forEach((card) => {
    card.addEventListener('click', () =>
      selectMatch(card.dataset.id, card.dataset.series, card.dataset.format));
  });
}

function selectMatch(id, series, format) {
  if (isRunning) return;
  selectedMatchId = id;
  if (series) {
    selectedSeries = series;
    updateSeriesBadge(series);
  }
  if (format) selectedFormat = format;
  document.querySelectorAll('.match-card').forEach((c) => {
    c.classList.toggle('selected', c.dataset.id === id);
  });
  clearFeed();
  loadScore();
  loadBroadcastLinks();
}

function updateSeriesBadge(seriesId) {
  const s = allSeries.find((x) => x.id === seriesId);
  const fmtLabel = selectedFormat
    ? selectedFormat.toUpperCase() + ' · ' : '';
  if (s) {
    $('#series-badge').textContent = `${fmtLabel}${s.emoji} ${s.name}`;
  }
}

function clearFeed() {
  lastTimestamp = 0;
  const match = document.querySelector(`.match-card[data-id="${selectedMatchId}"]`);
  const title = match ? match.querySelector('.title').textContent : selectedMatchId;
  $('#commentary-feed').innerHTML = `
    <div class="feed-welcome">
      <p>"Get on with it! That's the beauty of limited-overs cricket!"</p>
      <p class="sub">Ready for <strong>${title}</strong>. Open TuneIn, Rova or FOX Sports, then hit Start.</p>
    </div>`;
}

function setLiveState(on) {
  isRunning = on;
  const indicator = $('#live-indicator');
  indicator.classList.toggle('on-air', on);
  indicator.querySelector('span:last-child').textContent = on ? 'ON AIR' : 'OFF AIR';
  $('#btn-start').disabled = on;
  $('#btn-stop').disabled = !on;
}

function initials(name) {
  return name.split(' ').map((w) => w[0]).join('').slice(0, 2);
}

function renderLine(line) {
  const feed = $('#commentary-feed');
  const welcome = feed.querySelector('.feed-welcome');
  if (welcome) welcome.remove();

  const div = document.createElement('div');
  div.className = `commentary-line ${line.event_type}`;
  div.style.setProperty('--line-color', line.color);

  const time = new Date(line.timestamp * 1000).toLocaleTimeString([], {
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  });

  div.innerHTML = `
    <div class="line-avatar">${initials(line.commentator_name)}</div>
    <div class="line-body">
      <div class="line-name">${line.commentator_name}</div>
      <div class="line-text">${line.text}</div>
      ${line.over ? `<div class="line-meta">Over ${line.over}${line.score ? ` · ${line.score}` : ''} · ${time}</div>` : `<div class="line-meta">${time}</div>`}
    </div>`;

  feed.appendChild(div);

  if (typeof speakLine === 'function') {
    speakLine(line);
  }

  if ($('#auto-scroll').checked) {
    feed.scrollTop = feed.scrollHeight;
  }
}

async function pollCommentary() {
  const data = await fetchJSON(
    `/api/commentary?match_id=${selectedMatchId}&since=${lastTimestamp}`
  );
  if (data.lines.length) {
    data.lines.forEach((l) => {
      renderLine(l);
      lastTimestamp = Math.max(lastTimestamp, l.timestamp);
    });
  }
  if (!data.running && isRunning) {
    setLiveState(false);
    stopPolling();
  }
}

async function loadScore() {
  const { score } = await fetchJSON(`/api/score?match_id=${selectedMatchId}`);
  if (score && score.score) {
    $('.score-main').textContent = score.score;
    $('.score-update').textContent = score.status || '';
  }
}

function startPolling() {
  stopPolling();
  pollInterval = setInterval(pollCommentary, 2000);
  scoreInterval = setInterval(loadScore, 5000);
}

function stopPolling() {
  if (pollInterval) clearInterval(pollInterval);
  if (scoreInterval) clearInterval(scoreInterval);
  pollInterval = null;
  scoreInterval = null;
}

async function startCommentary() {
  await fetchJSON('/api/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ match_id: selectedMatchId }),
  });
  setLiveState(true);
  startPolling();
  pollCommentary();
}

async function stopCommentary() {
  await fetchJSON('/api/stop', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ match_id: selectedMatchId }),
  });
  setLiveState(false);
  stopPolling();
  if (typeof stopTts === 'function') stopTts();
}

async function resetCommentary() {
  await stopCommentary();
  await fetchJSON('/api/reset', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ match_id: selectedMatchId }),
  });
  clearFeed();
  loadScore();
}

$('#btn-start').addEventListener('click', startCommentary);
$('#btn-stop').addEventListener('click', stopCommentary);
$('#btn-reset').addEventListener('click', resetCommentary);

$('#series-filter').addEventListener('change', (e) => {
  if (isRunning) return;
  selectedSeries = e.target.value;
  loadMatches();
  loadBroadcastLinks();
  if (selectedSeries) updateSeriesBadge(selectedSeries);
  else $('#series-badge').textContent = selectedFormat ? selectedFormat.toUpperCase() : 'Australia Cricket';
});

$('#format-filter').addEventListener('change', (e) => {
  if (isRunning) return;
  selectedFormat = e.target.value;
  loadMatches();
  if (selectedSeries) updateSeriesBadge(selectedSeries);
  else if (selectedFormat) {
    $('#series-badge').textContent = `${selectedFormat.toUpperCase()} Cricket`;
  } else {
    $('#series-badge').textContent = 'Australia Cricket';
  }
});

initTts();
loadBroadcastLinks();
loadMatches();
loadScore();