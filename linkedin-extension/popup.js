'use strict';

// Tab navigation
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab, .tab-content').forEach(el => el.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(`tab-${tab.dataset.tab}`).classList.add('active');
  });
});

// Character counter for connection message
const connMsg = document.getElementById('conn-message');
const connChar = document.getElementById('conn-char');
if (connMsg) {
  connMsg.addEventListener('input', () => {
    connChar.textContent = connMsg.value.length;
  });
}

// Show/hide comment textarea based on post action
const postAction = document.getElementById('post-action');
const commentGroup = document.getElementById('comment-group');
postAction?.addEventListener('change', () => {
  const show = postAction.value === 'comment' || postAction.value === 'like-comment';
  commentGroup.style.display = show ? 'block' : 'none';
});

// Load settings and stats from storage
chrome.storage.local.get(['settings', 'stats', 'extractedData'], data => {
  const s = data.settings || {};
  const st = data.stats || {};

  if (s.dailyConnLimit) document.getElementById('daily-conn-limit').value = s.dailyConnLimit;
  if (s.dailyMsgLimit)  document.getElementById('daily-msg-limit').value  = s.dailyMsgLimit;
  if (s.safeMode    !== undefined) document.getElementById('safe-mode').checked    = s.safeMode;
  if (s.autoScroll  !== undefined) document.getElementById('auto-scroll').checked  = s.autoScroll;

  document.getElementById('stat-conn').textContent      = st.connections  || 0;
  document.getElementById('stat-msg').textContent       = st.messages      || 0;
  document.getElementById('stat-likes').textContent     = st.likes         || 0;
  document.getElementById('stat-comments').textContent  = st.comments      || 0;
  document.getElementById('stat-extracted').textContent = st.extracted      || 0;

  if (data.extractedData && data.extractedData.length > 0) {
    renderExtractPreview(data.extractedData);
    document.getElementById('btn-download').classList.remove('hidden');
  }
});

// Save settings
document.getElementById('btn-save-settings').addEventListener('click', () => {
  const settings = {
    dailyConnLimit: +document.getElementById('daily-conn-limit').value,
    dailyMsgLimit:  +document.getElementById('daily-msg-limit').value,
    safeMode:       document.getElementById('safe-mode').checked,
    autoScroll:     document.getElementById('auto-scroll').checked,
  };
  chrome.storage.local.set({ settings }, () => {
    const btn = document.getElementById('btn-save-settings');
    btn.textContent = '✅ Salvo!';
    setTimeout(() => { btn.textContent = '💾 Salvar Configurações'; }, 1500);
  });
});

// Reset stats
document.getElementById('btn-reset-stats').addEventListener('click', () => {
  chrome.storage.local.set({ stats: {} }, () => {
    ['conn', 'msg', 'likes', 'comments', 'extracted'].forEach(k => {
      const el = document.getElementById(`stat-${k}`) || document.getElementById(`stat-${k}s`);
      if (el) el.textContent = '0';
    });
    document.getElementById('stat-conn').textContent      = '0';
    document.getElementById('stat-msg').textContent       = '0';
    document.getElementById('stat-likes').textContent     = '0';
    document.getElementById('stat-comments').textContent  = '0';
    document.getElementById('stat-extracted').textContent = '0';
  });
});

// ─── Helpers ────────────────────────────────────────────────────────────────

function setStatus(text, type = 'idle') {
  const badge = document.getElementById('status-badge');
  badge.textContent = text;
  badge.className = `badge badge-${type}`;
}

function addLog(containerId, message, type = 'info') {
  const box = document.getElementById(containerId);
  if (!box) return;
  const line = document.createElement('div');
  line.className = `log-line log-${type}`;
  line.textContent = `${new Date().toLocaleTimeString()} — ${message}`;
  box.appendChild(line);
  box.scrollTop = box.scrollHeight;
}

function setProgress(prefix, done, total) {
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;
  const fillEl = document.getElementById(`${prefix}-fill`);
  const doneEl = document.getElementById(`${prefix}-done`);
  const totEl  = document.getElementById(`${prefix}-total`);
  if (fillEl) fillEl.style.width = `${pct}%`;
  if (doneEl) doneEl.textContent = done;
  if (totEl)  totEl.textContent  = total;
}

function showProgress(prefix) {
  document.getElementById(`${prefix}-progress`)?.classList.remove('hidden');
}

function showStopBtn(action, show) {
  document.getElementById(`btn-${action}`)?.classList.toggle('hidden', show);
  document.getElementById(`btn-stop-${action}`)?.classList.toggle('hidden', !show);
}

// ─── Send to active tab content script ──────────────────────────────────────

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function sendToContent(message) {
  const tab = await getActiveTab();
  if (!tab) return { error: 'Nenhuma aba ativa.' };
  try {
    return await chrome.tabs.sendMessage(tab.id, message);
  } catch (e) {
    return { error: e.message };
  }
}

// ─── CONNECTIONS ─────────────────────────────────────────────────────────────

let runConnections = false;

document.getElementById('btn-send-connections').addEventListener('click', async () => {
  runConnections = true;
  showStopBtn('connections', true);
  showProgress('conn');
  setStatus('Enviando conexões…', 'running');

  const limit   = +document.getElementById('conn-limit').value;
  const message = document.getElementById('conn-message').value.trim();
  const delay   = +document.getElementById('conn-delay').value;

  const result = await sendToContent({
    action: 'SEND_CONNECTIONS',
    limit,
    message,
    delay,
  });

  if (result?.error) {
    addLog('conn-log', result.error, 'err');
    setStatus('Erro', 'error');
  } else {
    addLog('conn-log', result?.message || 'Iniciado', 'info');
  }
});

document.getElementById('btn-stop-connections').addEventListener('click', async () => {
  runConnections = false;
  await sendToContent({ action: 'STOP_CONNECTIONS' });
  showStopBtn('connections', false);
  setStatus('Parado', 'idle');
});

// ─── MESSAGES ─────────────────────────────────────────────────────────────────

document.getElementById('btn-send-messages').addEventListener('click', async () => {
  showStopBtn('messages', true);
  showProgress('msg');
  setStatus('Enviando mensagens…', 'running');

  const limit   = +document.getElementById('msg-limit').value;
  const message = document.getElementById('msg-text').value.trim();
  const delay   = +document.getElementById('msg-delay').value;

  if (!message) {
    addLog('msg-log', 'Digite uma mensagem antes de continuar.', 'err');
    showStopBtn('messages', false);
    setStatus('Erro', 'error');
    return;
  }

  const result = await sendToContent({
    action: 'SEND_MESSAGES',
    limit,
    message,
    delay,
  });

  if (result?.error) {
    addLog('msg-log', result.error, 'err');
    setStatus('Erro', 'error');
  } else {
    addLog('msg-log', result?.message || 'Iniciado', 'info');
  }
});

document.getElementById('btn-stop-messages').addEventListener('click', async () => {
  await sendToContent({ action: 'STOP_MESSAGES' });
  showStopBtn('messages', false);
  setStatus('Parado', 'idle');
});

// ─── POSTS ────────────────────────────────────────────────────────────────────

document.getElementById('btn-interact-posts').addEventListener('click', async () => {
  showStopBtn('interact-posts', true);
  showProgress('post');
  setStatus('Interagindo com posts…', 'running');

  const postActionVal = document.getElementById('post-action').value;
  const comments      = document.getElementById('post-comments').value
    .split('\n')
    .map(l => l.trim())
    .filter(Boolean);
  const limit = +document.getElementById('post-limit').value;
  const delay = +document.getElementById('post-delay').value;

  const result = await sendToContent({
    action: 'INTERACT_POSTS',
    postAction: postActionVal,
    comments,
    limit,
    delay,
  });

  if (result?.error) {
    addLog('post-log', result.error, 'err');
    setStatus('Erro', 'error');
  } else {
    addLog('post-log', result?.message || 'Iniciado', 'info');
  }
});

document.getElementById('btn-stop-posts').addEventListener('click', async () => {
  await sendToContent({ action: 'STOP_POSTS' });
  document.getElementById('btn-interact-posts').classList.remove('hidden');
  document.getElementById('btn-stop-posts').classList.add('hidden');
  setStatus('Parado', 'idle');
});

// ─── EXTRACT ──────────────────────────────────────────────────────────────────

let extractedProfiles = [];

document.getElementById('btn-extract').addEventListener('click', async () => {
  extractedProfiles = [];
  showStopBtn('extract', true);
  showProgress('ext');
  setStatus('Extraindo dados…', 'running');
  document.getElementById('ext-preview').classList.add('hidden');

  const fields = {
    name:        document.getElementById('ext-name').checked,
    headline:    document.getElementById('ext-headline').checked,
    location:    document.getElementById('ext-location').checked,
    connections: document.getElementById('ext-connections').checked,
    url:         document.getElementById('ext-url').checked,
  };
  const limit  = +document.getElementById('ext-limit').value;
  const format = document.getElementById('ext-format').value;

  const result = await sendToContent({
    action: 'EXTRACT_PROFILES',
    fields,
    limit,
    format,
  });

  if (result?.error) {
    addLog('ext-log', result.error, 'err');
    setStatus('Erro', 'error');
  } else {
    addLog('ext-log', result?.message || 'Extração iniciada', 'info');
  }
});

document.getElementById('btn-stop-extract').addEventListener('click', async () => {
  await sendToContent({ action: 'STOP_EXTRACT' });
  showStopBtn('extract', false);
  setStatus('Parado', 'idle');
});

document.getElementById('btn-download').addEventListener('click', () => {
  chrome.storage.local.get(['extractedData', 'extractFormat'], data => {
    const profiles = data.extractedData || [];
    const format   = data.extractFormat || 'csv';
    if (!profiles.length) return;

    let content, filename, mime;
    if (format === 'json') {
      content  = JSON.stringify(profiles, null, 2);
      filename = 'linkedin_perfis.json';
      mime     = 'application/json';
    } else {
      const keys = Object.keys(profiles[0]);
      const rows = [keys.join(','), ...profiles.map(p => keys.map(k => `"${(p[k] || '').replace(/"/g, '""')}"`).join(','))];
      content  = rows.join('\n');
      filename = 'linkedin_perfis.csv';
      mime     = 'text/csv';
    }

    const blob = new Blob([content], { type: mime });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  });
});

// ─── Listen to messages from content script ──────────────────────────────────

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === 'PROGRESS') {
    const { prefix, done, total, log, logType } = msg;
    setProgress(prefix, done, total);
    if (log) addLog(`${prefix}-log`, log, logType || 'info');
    if (done >= total && total > 0) {
      setStatus('Concluído', 'done');
      showStopBtn(prefixToAction(prefix), false);
    }
  }

  if (msg.type === 'EXTRACT_RESULT') {
    extractedProfiles = msg.profiles;
    chrome.storage.local.set({ extractedData: msg.profiles, extractFormat: msg.format });
    renderExtractPreview(msg.profiles);
    document.getElementById('btn-download').classList.remove('hidden');
    setStatus('Extração concluída', 'done');
    showStopBtn('extract', false);
    updateStat('extracted', msg.profiles.length);
  }

  if (msg.type === 'STAT_UPDATE') {
    updateStat(msg.key, msg.value);
  }
});

function prefixToAction(prefix) {
  const map = { conn: 'connections', msg: 'messages', post: 'interact-posts', ext: 'extract' };
  return map[prefix] || prefix;
}

function updateStat(key, value) {
  const el = document.getElementById(`stat-${key}`);
  if (el) el.textContent = value;
}

function renderExtractPreview(profiles) {
  if (!profiles || !profiles.length) return;
  const keys = Object.keys(profiles[0]);
  const thead = document.getElementById('ext-thead');
  const tbody = document.getElementById('ext-tbody');
  thead.innerHTML = keys.map(k => `<th>${k}</th>`).join('');
  tbody.innerHTML = profiles.slice(0, 20).map(p =>
    `<tr>${keys.map(k => `<td title="${p[k] || ''}">${p[k] || ''}</td>`).join('')}</tr>`
  ).join('');
  document.getElementById('ext-count').textContent = profiles.length;
  document.getElementById('ext-preview').classList.remove('hidden');
}
