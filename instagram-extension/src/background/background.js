const DEFAULT_SETTINGS = {
  autoLike: false,
  autoComment: false,
  autoFollow: false,
  collectLeads: false,
  likeDelay: 30,
  commentDelay: 60,
  followDelay: 120,
  maxLikesPerHour: 50,
  maxCommentsPerHour: 10,
  maxFollowsPerHour: 20,
  comments: [
    "Produto incrível! 🎁",
    "Que lindo! 😍",
    "Adoro os brindes de vocês! ✨",
    "Ótima opção para presentear! 🎀"
  ],
  targetHashtags: ["brindes", "brindesempresariais", "brindesersonalizados"],
  leads: []
};

chrome.runtime.onInstalled.addListener(async () => {
  const existing = await chrome.storage.local.get("settings");
  if (!existing.settings) {
    await chrome.storage.local.set({ settings: DEFAULT_SETTINGS });
  }
  await chrome.storage.local.set({ stats: { likes: 0, comments: 0, follows: 0, leads: 0 } });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "GET_SETTINGS") {
    chrome.storage.local.get("settings").then(data => sendResponse(data.settings || DEFAULT_SETTINGS));
    return true;
  }

  if (message.type === "SAVE_SETTINGS") {
    chrome.storage.local.set({ settings: message.data }).then(() => sendResponse({ ok: true }));
    return true;
  }

  if (message.type === "GET_STATS") {
    chrome.storage.local.get("stats").then(data => sendResponse(data.stats || {}));
    return true;
  }

  if (message.type === "INCREMENT_STAT") {
    chrome.storage.local.get("stats").then(data => {
      const stats = data.stats || {};
      stats[message.key] = (stats[message.key] || 0) + 1;
      chrome.storage.local.set({ stats });
      sendResponse(stats);
    });
    return true;
  }

  if (message.type === "SAVE_LEAD") {
    chrome.storage.local.get("settings").then(data => {
      const settings = data.settings || DEFAULT_SETTINGS;
      const lead = { ...message.lead, capturedAt: new Date().toISOString() };
      const exists = settings.leads.find(l => l.username === lead.username);
      if (!exists) {
        settings.leads.push(lead);
        chrome.storage.local.set({ settings });
        chrome.runtime.sendMessage({ type: "INCREMENT_STAT", key: "leads" }).catch(() => {});
      }
      sendResponse({ ok: true, total: settings.leads.length });
    });
    return true;
  }

  if (message.type === "GET_LEADS") {
    chrome.storage.local.get("settings").then(data => {
      sendResponse(data.settings?.leads || []);
    });
    return true;
  }

  if (message.type === "CLEAR_LEADS") {
    chrome.storage.local.get("settings").then(data => {
      const settings = data.settings || DEFAULT_SETTINGS;
      settings.leads = [];
      chrome.storage.local.set({ settings });
      sendResponse({ ok: true });
    });
    return true;
  }

  if (message.type === "SHOW_NOTIFICATION") {
    chrome.notifications.create({
      type: "basic",
      iconUrl: "src/icons/icon48.png",
      title: "Instagram Pro Tools",
      message: message.text
    });
    sendResponse({ ok: true });
    return true;
  }
});
