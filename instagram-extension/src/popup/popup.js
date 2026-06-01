// ── TAB NAVIGATION ────────────────────────────────────────────────────────────

document.querySelectorAll(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
    if (tab.dataset.tab === "leads") renderLeads();
    if (tab.dataset.tab === "dashboard") loadStats();
  });
});

// ── LOAD STATS ────────────────────────────────────────────────────────────────

function loadStats() {
  chrome.runtime.sendMessage({ type: "GET_STATS" }, stats => {
    document.getElementById("stat-likes").textContent = stats.likes || 0;
    document.getElementById("stat-comments").textContent = stats.comments || 0;
    document.getElementById("stat-follows").textContent = stats.follows || 0;
    document.getElementById("stat-leads").textContent = stats.leads || 0;
  });
}

// ── LOAD SETTINGS ─────────────────────────────────────────────────────────────

function loadSettings() {
  chrome.runtime.sendMessage({ type: "GET_SETTINGS" }, s => {
    document.getElementById("autoLike").checked = !!s.autoLike;
    document.getElementById("autoComment").checked = !!s.autoComment;
    document.getElementById("collectLeads").checked = !!s.collectLeads;
    document.getElementById("likeDelay").value = s.likeDelay || 30;
    document.getElementById("commentDelay").value = s.commentDelay || 60;
    document.getElementById("maxLikesPerHour").value = s.maxLikesPerHour || 50;
    document.getElementById("maxCommentsPerHour").value = s.maxCommentsPerHour || 10;
    document.getElementById("comments").value = (s.comments || []).join("\n");
  });
}

// ── SAVE SETTINGS ─────────────────────────────────────────────────────────────

document.getElementById("btn-save").addEventListener("click", () => {
  const data = {
    autoLike: document.getElementById("autoLike").checked,
    autoComment: document.getElementById("autoComment").checked,
    collectLeads: document.getElementById("collectLeads").checked,
    likeDelay: parseInt(document.getElementById("likeDelay").value) || 30,
    commentDelay: parseInt(document.getElementById("commentDelay").value) || 60,
    maxLikesPerHour: parseInt(document.getElementById("maxLikesPerHour").value) || 50,
    maxCommentsPerHour: parseInt(document.getElementById("maxCommentsPerHour").value) || 10,
    comments: document.getElementById("comments").value
      .split("\n")
      .map(c => c.trim())
      .filter(Boolean)
  };

  chrome.runtime.sendMessage({ type: "SAVE_SETTINGS", data }, () => {
    const status = document.getElementById("save-status");
    status.textContent = "✅ Configurações salvas!";
    setTimeout(() => status.textContent = "", 2000);

    // Notify active Instagram tabs
    chrome.tabs.query({ url: "https://www.instagram.com/*" }, tabs => {
      tabs.forEach(tab => chrome.tabs.sendMessage(tab.id, { type: "SETTINGS_UPDATED" }));
    });
  });
});

// ── LEADS ─────────────────────────────────────────────────────────────────────

function renderLeads() {
  chrome.runtime.sendMessage({ type: "GET_LEADS" }, leads => {
    document.getElementById("leads-count").textContent = `${leads.length} leads capturados`;
    const list = document.getElementById("leads-list");

    if (!leads.length) {
      list.innerHTML = `<div class="empty-state">📭 Nenhum lead capturado ainda.<br/>Ative a coleta e navegue no Instagram.</div>`;
      return;
    }

    list.innerHTML = leads.slice().reverse().map(l => `
      <div class="lead-card">
        <div class="lead-username">@${l.username}</div>
        <div class="lead-meta">
          ${l.followers ? `👥 ${l.followers} &nbsp;` : ""}
          📍 ${l.source === "profile" ? "Perfil" : "Feed"} &nbsp;
          🕐 ${new Date(l.capturedAt).toLocaleDateString("pt-BR")}
        </div>
        ${l.bio ? `<div class="lead-bio">${l.bio}</div>` : ""}
        ${l.profileUrl ? `<a href="${l.profileUrl}" target="_blank" style="font-size:11px;color:#833ab4;">Ver perfil →</a>` : ""}
      </div>
    `).join("");
  });
}

function exportLeadsCSV() {
  chrome.runtime.sendMessage({ type: "GET_LEADS" }, leads => {
    if (!leads.length) return;
    const header = "username,profileUrl,bio,followers,source,capturedAt";
    const rows = leads.map(l =>
      [l.username, l.profileUrl, `"${(l.bio || "").replace(/"/g, "'")}"`, l.followers, l.source, l.capturedAt].join(",")
    );
    const csv = [header, ...rows].join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `leads_instagram_${new Date().toISOString().split("T")[0]}.csv`;
    a.click();
  });
}

document.getElementById("btn-export").addEventListener("click", exportLeadsCSV);

document.getElementById("btn-clear-leads").addEventListener("click", () => {
  if (!confirm("Limpar todos os leads?")) return;
  chrome.runtime.sendMessage({ type: "CLEAR_LEADS" }, () => renderLeads());
});

// ── QUICK ACTIONS ─────────────────────────────────────────────────────────────

document.getElementById("btn-open-ig").addEventListener("click", () => {
  chrome.tabs.create({ url: "https://www.instagram.com/brindesmarceloewagner/" });
});

document.getElementById("btn-reset-stats").addEventListener("click", () => {
  chrome.storage.local.set({ stats: { likes: 0, comments: 0, follows: 0, leads: 0 } }, loadStats);
});

// ── INIT ──────────────────────────────────────────────────────────────────────

loadStats();
loadSettings();
