let settings = {};
let actionQueue = [];
let isProcessing = false;
let actionCounts = { likes: 0, comments: 0, follows: 0, resetAt: Date.now() };

async function loadSettings() {
  return new Promise(resolve => {
    chrome.runtime.sendMessage({ type: "GET_SETTINGS" }, data => {
      settings = data || {};
      resolve(settings);
    });
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function randomDelay(baseSeconds) {
  const base = baseSeconds * 1000;
  const jitter = Math.random() * base * 0.4;
  return base + jitter;
}

function resetCountsIfNeeded() {
  const oneHour = 3600000;
  if (Date.now() - actionCounts.resetAt > oneHour) {
    actionCounts = { likes: 0, comments: 0, follows: 0, resetAt: Date.now() };
  }
}

// ── LIKE ────────────────────────────────────────────────────────────────────

async function likePost(article) {
  resetCountsIfNeeded();
  if (!settings.autoLike) return;
  if (actionCounts.likes >= (settings.maxLikesPerHour || 50)) return;

  const likeBtn = article.querySelector('svg[aria-label="Curtir"], svg[aria-label="Like"]');
  if (!likeBtn) return;

  const btn = likeBtn.closest("button");
  if (!btn) return;

  const alreadyLiked = article.querySelector('svg[aria-label="Descurtir"], svg[aria-label="Unlike"]');
  if (alreadyLiked) return;

  btn.click();
  actionCounts.likes++;
  chrome.runtime.sendMessage({ type: "INCREMENT_STAT", key: "likes" });
  await sleep(randomDelay(settings.likeDelay || 30));
}

// ── COMMENT ─────────────────────────────────────────────────────────────────

async function commentPost(article) {
  resetCountsIfNeeded();
  if (!settings.autoComment) return;
  if (actionCounts.comments >= (settings.maxCommentsPerHour || 10)) return;

  const comments = settings.comments || [];
  if (!comments.length) return;

  const commentInput = article.querySelector('textarea[placeholder], input[placeholder*="coment"], textarea');
  if (!commentInput) return;

  const text = comments[Math.floor(Math.random() * comments.length)];

  commentInput.focus();
  const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
  nativeInputValueSetter.call(commentInput, text);
  commentInput.dispatchEvent(new Event("input", { bubbles: true }));

  await sleep(1500);

  const submitBtn = article.querySelector('div[role="button"][tabindex="0"]:last-child, button[type="submit"]');
  if (submitBtn) {
    submitBtn.click();
    actionCounts.comments++;
    chrome.runtime.sendMessage({ type: "INCREMENT_STAT", key: "comments" });
  }

  await sleep(randomDelay(settings.commentDelay || 60));
}

// ── COLLECT LEAD ─────────────────────────────────────────────────────────────

function collectLeadFromArticle(article) {
  if (!settings.collectLeads) return;

  const usernameEl = article.querySelector("a[role='link'] span, header a span");
  const username = usernameEl?.textContent?.trim();
  if (!username) return;

  const profileLink = article.querySelector("header a[href*='/']");
  const profileUrl = profileLink ? `https://www.instagram.com${profileLink.getAttribute("href")}` : "";

  const bio = article.querySelector("header span:not([class])");
  const bioText = bio?.textContent?.trim() || "";

  if (username) {
    chrome.runtime.sendMessage({
      type: "SAVE_LEAD",
      lead: { username, profileUrl, bio: bioText, source: "feed" }
    });
  }
}

// ── PROCESS FEED ─────────────────────────────────────────────────────────────

async function processFeedPost(article) {
  if (article.dataset.igProcessed) return;
  article.dataset.igProcessed = "1";

  collectLeadFromArticle(article);
  await likePost(article);
  await commentPost(article);
}

// ── MUTATION OBSERVER ────────────────────────────────────────────────────────

function observeFeed() {
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mut => {
      mut.addedNodes.forEach(node => {
        if (node.nodeType !== 1) return;
        const articles = node.tagName === "ARTICLE" ? [node] : [...node.querySelectorAll("article")];
        articles.forEach(a => processFeedPost(a));
      });
    });
  });

  observer.observe(document.body, { childList: true, subtree: true });

  // Process already visible posts
  document.querySelectorAll("article").forEach(a => processFeedPost(a));
}

// ── UI OVERLAY ───────────────────────────────────────────────────────────────

function injectStatusBar() {
  if (document.getElementById("ig-pro-bar")) return;

  const bar = document.createElement("div");
  bar.id = "ig-pro-bar";
  bar.innerHTML = `
    <span id="ig-pro-label">🤖 Instagram Pro Tools</span>
    <span id="ig-pro-status">Ativo</span>
  `;
  document.body.appendChild(bar);
}

// ── PROFILE SCRAPER ──────────────────────────────────────────────────────────

function scrapeProfilePage() {
  if (!settings.collectLeads) return;
  if (!location.pathname.match(/^\/[^/]+\/?$/)) return;

  const username = location.pathname.replace(/\//g, "");
  if (!username) return;

  const bioEl = document.querySelector("span.-vDIg, div._aa_c span, header section div span");
  const bio = bioEl?.textContent?.trim() || "";

  const followersEl = document.querySelector('a[href*="/followers/"] span, li span span');
  const followers = followersEl?.textContent?.trim() || "";

  chrome.runtime.sendMessage({
    type: "SAVE_LEAD",
    lead: { username, profileUrl: location.href, bio, followers, source: "profile" }
  });
}

// ── INIT ──────────────────────────────────────────────────────────────────────

async function init() {
  await loadSettings();
  injectStatusBar();
  observeFeed();
  scrapeProfilePage();

  // Reload settings every 2 minutes
  setInterval(loadSettings, 120000);
}

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "SETTINGS_UPDATED") {
    loadSettings();
  }
  if (msg.type === "SCRAPE_PROFILE") {
    scrapeProfilePage();
  }
});

init();
