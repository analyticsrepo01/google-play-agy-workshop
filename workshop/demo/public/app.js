'use strict';

function element(id) {
  const node = document.getElementById(id);
  if (!node) throw new Error(`Missing game element: ${id}`);
  return node;
}

let state;
let challenge = null;
let busy = false;
let pending;
const dialog = element('badge-dialog');
dialog.addEventListener('keydown', event => {
  if (event.key === 'Escape') {
    event.preventDefault();
    dialog.close();
  }
});

function message(author, value) {
  const item = document.createElement('div');
  item.className = `message${author === 'Player' ? ' player' : ''}`;
  const name = document.createElement('strong');
  name.textContent = author;
  item.append(name, document.createTextNode(value));
  element('conversation').append(item);
}

function appendTrace(entries) {
  if (!entries?.length) return;
  const container = element('trace');
  container.querySelector('p')?.remove();
  for (const entry of entries) {
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    const payload = entry.payload;
    const name = payload?.name || payload?.functionResponse?.name || '';
    summary.textContent = `${entry.source} / ${entry.kind}${name ? ` / ${name}` : ''}`;
    const code = document.createElement('pre');
    code.textContent = JSON.stringify(payload, null, 2);
    details.append(summary, code);
    container.append(details);
  }
}

async function request(path, data) {
  const response = await fetch(path, data === undefined
    ? { signal: AbortSignal.timeout(80000) }
    : {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data), signal: AbortSignal.timeout(80000),
    });
  const payload = await response.json();
  appendTrace(payload.trace);
  if (!response.ok) {
    throw new Error(payload.error?.message || `Game request failed: HTTP ${response.status}.`);
  }
  return payload;
}

function controls() {
  const solved = challenge && state?.progress.completedIds.includes(challenge.id);
  const done = state?.progress.completedCount === 3;
  element('check').disabled = busy || !challenge || solved;
  element('choices').disabled = busy || !challenge || solved;
  element('hint').disabled = busy || !challenge || solved || state?.progress.hintedIds.includes(challenge.id);
  element('next').hidden = !solved || done;
  element('next').disabled = busy;
  element('propose').disabled = busy || !done || state?.progress.badgePublished || Boolean(pending);
  element('review').hidden = !pending || state?.progress.badgePublished;
  element('review').disabled = busy;
  element('refresh').disabled = busy;
  element('publish').disabled = busy;
  element('chat-input').disabled = busy || state?.mode !== 'live';
  element('send').disabled = busy || state?.mode !== 'live';
}

function renderState(value) {
  state = value;
  const progress = state.progress;
  pending = state.proposals.find(item => item.decision === 'pending'
    && item.expectedVersion === progress.version);
  element('completed').textContent = `${progress.completedCount} / 3`;
  element('score').textContent = String(progress.score);
  element('badge-status').textContent = progress.badgePublished ? 'Published'
    : pending ? 'Pending review' : progress.completedCount === 3 ? 'Unlocked' : 'Locked';
  element('completion').hidden = progress.completedCount !== 3;
  element('completion-score').textContent = String(progress.score);
  element('completion-status').textContent = progress.badgePublished ? 'Published locally'
    : pending ? 'Pending human review' : 'Earned, not published';
  if (progress.badgePublished) {
    element('badge-note').textContent = `DevFest Agent Builder / ${progress.score} points. Published only to this local game.`;
  } else if (pending) {
    element('badge-note').textContent = `Proposal ${pending.id} is pending. The badge is NOT published.`;
  } else {
    element('badge-note').textContent = 'Complete all three quests to unlock your badge. A proposal is not publication.';
  }
  const map = element('quest-map');
  map.replaceChildren();
  for (const quest of state.map) {
    const item = document.createElement('li');
    item.className = quest.status;
    const title = document.createElement('strong');
    title.textContent = quest.title;
    const status = document.createElement('span');
    status.textContent = quest.status;
    item.append(title, status);
    map.append(item);
  }
  if (state.mode) {
    const live = state.mode === 'live';
    element('mode').classList.toggle('live', live);
    element('mode').textContent = live
      ? 'LIVE ADK host enabled. Quiz buttons still run deterministic game code; host chat uses the model.'
      : 'OFFLINE MODE / Deterministic game tools only. No model calls or simulated AI reasoning.';
    element('chat-help').textContent = live
      ? 'Try: "Show my current quest." Model wording can vary; inspect the actual tool trace.'
      : 'To enable real ADK chat, the presenter must restart with npm run dev:live and a private Gemini key.';
  }
  controls();
}

function mergeState(value) {
  renderState({ ...value, mode: state.mode });
}

async function loadChallenge(focus = false) {
  const payload = await request('/api/challenge', { challengeId: 'current' });
  mergeState(payload.state);
  challenge = payload.result.data.challenge;
  element('quest-title').textContent = challenge ? challenge.title : 'Adventure complete!';
  element('quest-number').textContent = challenge ? challenge.id : 'THE BADGE VAULT IS OPEN';
  element('story').textContent = challenge ? challenge.story
    : 'Three quests cleared. Review your score, request the badge, and make the final decision yourself.';
  element('question').textContent = challenge ? challenge.question : '';
  element('answer-form').hidden = !challenge;
  element('hint-text').hidden = true;
  element('feedback').textContent = '';
  element('feedback').classList.remove('wrong');
  element('options').replaceChildren();
  if (challenge) {
    for (const option of challenge.options) {
      const label = document.createElement('label');
      label.className = 'option';
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = 'choice';
      input.value = option.id;
      input.required = true;
      const text = document.createElement('span');
      text.textContent = `${option.id}. ${option.text}`;
      label.append(input, text);
      element('options').append(label);
    }
  }
  controls();
  if (focus) element('quest-title').focus();
}

async function perform(operation) {
  if (busy) return;
  busy = true;
  element('error').hidden = true;
  element('request-status').textContent = 'Working...';
  controls();
  try {
    await operation();
  } catch (error) {
    element('error').textContent = `${error instanceof Error ? error.message : 'Game request failed.'} Refresh state before retrying actions.`;
    element('error').hidden = false;
  } finally {
    busy = false;
    element('request-status').textContent = '';
    controls();
  }
}

element('answer-form').addEventListener('submit', event => {
  event.preventDefault();
  let correct = false;
  void perform(async () => {
    if (!challenge) throw new Error('There is no current quest.');
    const selected = element('options').querySelector('input:checked');
    if (!selected) throw new Error('Choose A, B, or C before checking your answer.');
    const payload = await request('/api/answer', { challengeId: challenge.id, choice: selected.value });
    mergeState(payload.state);
    const result = payload.result.data;
    correct = result.correct;
    if (correct && state.progress.completedCount === 3) await loadChallenge();
    element('feedback').textContent = `${result.message} Total: ${state.progress.score} points; ${state.progress.completedCount} of 3 quests complete.`;
    element('feedback').classList.toggle('wrong', !result.correct);
  }).then(() => {
    if (correct) element(state.progress.completedCount === 3 ? 'propose' : 'next').focus();
  });
});

element('hint').addEventListener('click', () => void perform(async () => {
  if (!challenge) throw new Error('There is no current quest.');
  const payload = await request('/api/hint', { challengeId: challenge.id });
  mergeState(payload.state);
  element('hint-text').textContent = `${payload.result.data.hint} This quest now awards 75 points for a correct answer.`;
  element('hint-text').hidden = false;
}));
element('next').addEventListener('click', () => void perform(() => loadChallenge(true)));
element('refresh').addEventListener('click', () => void perform(async () => {
  renderState(await request('/api/state'));
  await loadChallenge();
}));
element('propose').addEventListener('click', () => void perform(async () => {
  const payload = await request('/api/propose', {});
  mergeState(payload.state);
  element('feedback').textContent = 'Badge proposed, not published. You make the final decision.';
}));
element('review').addEventListener('click', () => {
  if (!pending) return;
  element('proposal-details').textContent = JSON.stringify(pending, null, 2);
  element('confirmation').value = '';
  element('confirmation-error').textContent = '';
  dialog.showModal();
  element('confirmation').focus();
});
element('publish-form').addEventListener('submit', event => {
  event.preventDefault();
  element('confirmation-error').textContent = '';
  if (element('confirmation').value !== 'PUBLISH') {
    element('confirmation-error').textContent = 'Type PUBLISH exactly to confirm; nothing was published.';
    element('confirmation').focus();
    return;
  }
  void perform(async () => {
    if (!pending) throw new Error('No pending badge proposal. Refresh the actual game state.');
    try {
      const payload = await request('/api/approve', { proposalId: pending.id, confirmation: 'PUBLISH' });
      mergeState(payload.state);
      dialog.close();
      element('quest-title').focus();
      element('feedback').textContent = `Badge published locally! You earned ${state.progress.score} points.`;
    } catch (error) {
      element('confirmation-error').textContent = error instanceof Error ? error.message : 'Publication failed.';
      throw error;
    }
  });
});
element('chat-form').addEventListener('submit', event => {
  event.preventDefault();
  void perform(async () => {
    const text = element('chat-input').value.trim();
    if (!text) throw new Error('Enter a message for the live game host.');
    message('Player', text);
    const payload = await request('/api/chat', { message: text });
    mergeState(payload.state);
    message('ADK game host', payload.answer);
    element('chat-input').value = '';
    await loadChallenge();
  });
});
element('clear-trace').addEventListener('click', () => {
  element('trace').replaceChildren();
  const note = document.createElement('p');
  note.textContent = 'Displayed trace cleared. Game state and terminal evidence are unchanged.';
  element('trace').append(note);
});
void perform(async () => {
  renderState(await request('/api/state'));
  message('Workshop guide', state.mode === 'live'
    ? 'The live ADK host is ready. Ask it to read your current quest; choose answers yourself.'
    : 'You can play all three quests without a key. This guide is static; offline tools are not a live agent.');
  await loadChallenge();
});
