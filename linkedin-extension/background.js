'use strict';

// Forward messages from content scripts to popup
chrome.runtime.onMessage.addListener((msg, sender) => {
  // Re-broadcast to all extension views (popup)
  chrome.runtime.sendMessage(msg).catch(() => {});
});

// Reset daily stats at midnight
function scheduleDailyReset() {
  const now   = new Date();
  const next  = new Date(now);
  next.setDate(now.getDate() + 1);
  next.setHours(0, 0, 0, 0);
  const msUntilMidnight = next - now;

  setTimeout(() => {
    chrome.storage.local.get(['stats'], data => {
      const stats = data.stats || {};
      stats.connections = 0;
      stats.messages    = 0;
      stats.likes       = 0;
      stats.comments    = 0;
      chrome.storage.local.set({ stats });
    });
    scheduleDailyReset();
  }, msUntilMidnight);
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(['settings'], data => {
    if (!data.settings) {
      chrome.storage.local.set({
        settings: {
          dailyConnLimit: 50,
          dailyMsgLimit:  30,
          safeMode:       true,
          autoScroll:     true,
        },
        stats: {
          connections: 0,
          messages:    0,
          likes:       0,
          comments:    0,
          extracted:   0,
        },
      });
    }
  });
  scheduleDailyReset();
});
