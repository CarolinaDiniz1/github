'use strict';

// ─── State ───────────────────────────────────────────────────────────────────

const state = {
  runConnections: false,
  runMessages:    false,
  runPosts:       false,
  runExtract:     false,
};

// ─── Utilities ────────────────────────────────────────────────────────────────

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function randomDelay(baseMs, safeMode = true) {
  if (!safeMode) return sleep(baseMs);
  const jitter = (Math.random() * 0.6 + 0.7) * baseMs;
  return sleep(jitter);
}

function sendProgress(prefix, done, total, log = null, logType = 'info') {
  chrome.runtime.sendMessage({ type: 'PROGRESS', prefix, done, total, log, logType });
}

function sendStat(key, value) {
  chrome.runtime.sendMessage({ type: 'STAT_UPDATE', key, value });
}

async function incrementStat(key) {
  return new Promise(resolve => {
    chrome.storage.local.get(['stats'], data => {
      const stats = data.stats || {};
      stats[key] = (stats[key] || 0) + 1;
      chrome.storage.local.set({ stats }, () => {
        sendStat(key, stats[key]);
        resolve(stats[key]);
      });
    });
  });
}

function click(el) {
  if (!el) return;
  el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
}

function simulateType(el, text) {
  el.focus();
  el.value = '';
  el.dispatchEvent(new Event('focus', { bubbles: true }));
  for (const char of text) {
    el.value += char;
    el.dispatchEvent(new Event('input', { bubbles: true }));
  }
  el.dispatchEvent(new Event('change', { bubbles: true }));
}

// Finds button by text content
function findButtonByText(text) {
  return Array.from(document.querySelectorAll('button'))
    .find(b => b.textContent.trim().toLowerCase().includes(text.toLowerCase()));
}

// ─── SEND CONNECTIONS ─────────────────────────────────────────────────────────

async function sendConnections({ limit, message, delay }) {
  state.runConnections = true;
  let done = 0;

  const buttons = Array.from(
    document.querySelectorAll('button[aria-label*="Connect"], button[aria-label*="Conectar"]')
  ).slice(0, limit);

  const total = buttons.length;
  if (total === 0) {
    sendProgress('conn', 0, 0, 'Nenhum botão "Conectar" encontrado. Abra uma busca de pessoas.', 'err');
    return;
  }

  sendProgress('conn', 0, total, `${total} perfis encontrados`, 'info');

  for (const btn of buttons) {
    if (!state.runConnections) break;

    const name = btn.closest('li')?.querySelector('.entity-result__title-text, .artdeco-entity-lockup__title')?.textContent?.trim() || 'Desconhecido';

    click(btn);
    await sleep(800);

    // Handle "Add a note" modal if message is provided
    if (message) {
      const addNoteBtn = findButtonByText('Add a note') || findButtonByText('Adicionar nota');
      if (addNoteBtn) {
        click(addNoteBtn);
        await sleep(500);
        const textarea = document.querySelector('textarea[name="message"]');
        if (textarea) simulateType(textarea, message);
        await sleep(300);
      }
    }

    // Confirm send
    const sendBtn = findButtonByText('Send invitation') || findButtonByText('Enviar convite') || findButtonByText('Send');
    if (sendBtn) click(sendBtn);

    await sleep(400);

    // Close any leftover modal
    const closeBtn = document.querySelector('button[aria-label="Dismiss"], button[aria-label="Fechar"]');
    if (closeBtn) click(closeBtn);

    done++;
    await incrementStat('connections');
    sendProgress('conn', done, total, `Convite enviado para ${name}`, 'ok');
    await randomDelay(delay * 1000);
  }

  state.runConnections = false;
  sendProgress('conn', done, total, `Concluído: ${done} convites enviados.`, 'ok');
}

// ─── SEND MESSAGES ────────────────────────────────────────────────────────────

async function sendMessages({ limit, message, delay }) {
  state.runMessages = true;
  let done = 0;

  // Works on /messaging or on search results
  const profileCards = Array.from(
    document.querySelectorAll('.msg-conversation-listitem, .entity-result__item')
  ).slice(0, limit);

  const total = profileCards.length;
  if (total === 0) {
    sendProgress('msg', 0, 0, 'Nenhum perfil encontrado. Abra o Inbox ou uma busca.', 'err');
    return;
  }

  sendProgress('msg', 0, total, `${total} conversas encontradas`, 'info');

  for (const card of profileCards) {
    if (!state.runMessages) break;

    const name = card.querySelector('.msg-conversation-listitem__participant-names, .entity-result__title-text')
      ?.textContent?.trim() || 'Contato';

    click(card);
    await sleep(1200);

    const msgBox = document.querySelector('.msg-form__contenteditable, div[contenteditable="true"][role="textbox"]');
    if (!msgBox) {
      sendProgress('msg', done, total, `Não encontrou caixa de mensagem para ${name}`, 'err');
      continue;
    }

    const personalised = message.replace(/\{nome\}/gi, name.split(' ')[0]);
    msgBox.focus();
    msgBox.textContent = personalised;
    msgBox.dispatchEvent(new Event('input', { bubbles: true }));
    await sleep(400);

    const sendBtn = document.querySelector('button.msg-form__send-button, button[aria-label*="Send"], button[aria-label*="Enviar"]');
    if (sendBtn && !sendBtn.disabled) {
      click(sendBtn);
      done++;
      await incrementStat('messages');
      sendProgress('msg', done, total, `Mensagem enviada para ${name}`, 'ok');
    } else {
      sendProgress('msg', done, total, `Botão enviar desabilitado para ${name}`, 'err');
    }

    await randomDelay(delay * 1000);
  }

  state.runMessages = false;
  sendProgress('msg', done, total, `Concluído: ${done} mensagens enviadas.`, 'ok');
}

// ─── INTERACT WITH POSTS ──────────────────────────────────────────────────────

async function interactPosts({ postAction, comments, limit, delay }) {
  state.runPosts = true;
  let done = 0;

  const posts = Array.from(
    document.querySelectorAll('.feed-shared-update-v2, .occludable-update')
  ).slice(0, limit);

  const total = posts.length;
  if (total === 0) {
    sendProgress('post', 0, 0, 'Nenhum post encontrado. Abra o feed.', 'err');
    return;
  }

  sendProgress('post', 0, total, `${total} posts encontrados`, 'info');

  for (const post of posts) {
    if (!state.runPosts) break;

    // Like
    if (postAction === 'like' || postAction === 'like-comment') {
      const likeBtn = post.querySelector('button[aria-label*="Like"], button[aria-label*="Curtir"], button[aria-label*="React"]');
      if (likeBtn && !likeBtn.classList.contains('react-button--active')) {
        click(likeBtn);
        await sleep(500);
        await incrementStat('likes');
        sendProgress('post', done, total, 'Post curtido', 'ok');
      }
    }

    // Comment
    if (postAction === 'comment' || postAction === 'like-comment') {
      if (comments && comments.length > 0) {
        const commentText = comments[Math.floor(Math.random() * comments.length)];
        const commentBtn = post.querySelector('button[aria-label*="Comment"], button[aria-label*="Comentar"]');
        if (commentBtn) {
          click(commentBtn);
          await sleep(800);
          const commentBox = post.querySelector('.ql-editor, div[contenteditable="true"][role="textbox"]');
          if (commentBox) {
            commentBox.focus();
            commentBox.textContent = commentText;
            commentBox.dispatchEvent(new Event('input', { bubbles: true }));
            await sleep(400);
            const submitBtn = post.querySelector('button.comments-comment-box__submit-button, button[aria-label*="Post comment"]');
            if (submitBtn && !submitBtn.disabled) {
              click(submitBtn);
              await incrementStat('comments');
              sendProgress('post', done, total, `Comentário: "${commentText}"`, 'ok');
            }
          }
        }
      }
    }

    done++;
    sendProgress('post', done, total, null, 'info');
    await randomDelay(delay * 1000);
  }

  state.runPosts = false;
  sendProgress('post', done, total, `Concluído: ${done} posts processados.`, 'ok');
}

// ─── EXTRACT PROFILES ─────────────────────────────────────────────────────────

async function extractProfiles({ fields, limit, format }) {
  state.runExtract = true;
  const profiles = [];

  let page = 1;
  let done = 0;

  while (state.runExtract && done < limit) {
    const cards = Array.from(
      document.querySelectorAll('.entity-result__item, .reusable-search__result-container li')
    );

    if (cards.length === 0) {
      sendProgress('ext', done, limit, 'Nenhum resultado encontrado. Abra uma busca de pessoas.', 'err');
      break;
    }

    for (const card of cards) {
      if (!state.runExtract || done >= limit) break;

      const profile = {};

      if (fields.name) {
        profile.nome = card.querySelector(
          '.entity-result__title-text a span[aria-hidden="true"], .artdeco-entity-lockup__title'
        )?.textContent?.trim() || '';
      }

      if (fields.headline) {
        profile.cargo = card.querySelector(
          '.entity-result__primary-subtitle'
        )?.textContent?.trim() || '';
      }

      if (fields.location) {
        profile.localizacao = card.querySelector(
          '.entity-result__secondary-subtitle'
        )?.textContent?.trim() || '';
      }

      if (fields.connections) {
        profile.conexoes_em_comum = card.querySelector(
          '.entity-result__insights'
        )?.textContent?.trim() || '';
      }

      if (fields.url) {
        profile.url = card.querySelector(
          'a.app-aware-link[href*="/in/"]'
        )?.href?.split('?')[0] || '';
      }

      if (Object.values(profile).some(v => v)) {
        profiles.push(profile);
        done++;
        sendProgress('ext', done, limit, `Extraído: ${profile.nome || profile.url || 'perfil'}`, 'ok');
      }
    }

    // Try next page
    if (done < limit && state.runExtract) {
      const nextBtn = document.querySelector('button[aria-label="Next"], .artdeco-pagination__button--next');
      if (nextBtn && !nextBtn.disabled) {
        click(nextBtn);
        page++;
        sendProgress('ext', done, limit, `Navegando para página ${page}…`, 'info');
        await sleep(2500);
      } else {
        break;
      }
    }
  }

  state.runExtract = false;

  chrome.runtime.sendMessage({
    type:     'EXTRACT_RESULT',
    profiles,
    format,
  });

  const total = profiles.length;
  chrome.storage.local.get(['stats'], data => {
    const stats = data.stats || {};
    stats.extracted = (stats.extracted || 0) + total;
    chrome.storage.local.set({ stats });
  });
}

// ─── Message listener ─────────────────────────────────────────────────────────

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  switch (msg.action) {
    case 'SEND_CONNECTIONS':
      sendConnections(msg).catch(e => sendProgress('conn', 0, 0, e.message, 'err'));
      sendResponse({ message: 'Enviando conexões…' });
      break;

    case 'STOP_CONNECTIONS':
      state.runConnections = false;
      sendResponse({ ok: true });
      break;

    case 'SEND_MESSAGES':
      sendMessages(msg).catch(e => sendProgress('msg', 0, 0, e.message, 'err'));
      sendResponse({ message: 'Enviando mensagens…' });
      break;

    case 'STOP_MESSAGES':
      state.runMessages = false;
      sendResponse({ ok: true });
      break;

    case 'INTERACT_POSTS':
      interactPosts(msg).catch(e => sendProgress('post', 0, 0, e.message, 'err'));
      sendResponse({ message: 'Interagindo com posts…' });
      break;

    case 'STOP_POSTS':
      state.runPosts = false;
      sendResponse({ ok: true });
      break;

    case 'EXTRACT_PROFILES':
      extractProfiles(msg).catch(e => sendProgress('ext', 0, 0, e.message, 'err'));
      sendResponse({ message: 'Extração iniciada…' });
      break;

    case 'STOP_EXTRACT':
      state.runExtract = false;
      sendResponse({ ok: true });
      break;

    default:
      sendResponse({ error: 'Ação desconhecida' });
  }
  return true; // Keep message channel open for async
});
