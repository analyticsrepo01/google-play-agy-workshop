import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { QuestStore } from './store.ts';

function fixture(t: { after: (fn: () => void) => void }) {
  const folder = mkdtempSync(join(tmpdir(), 'devfest-quest-'));
  t.after(() => rmSync(folder, { recursive: true, force: true }));
  return new QuestStore(join(folder, 'quest-state.json'));
}

function complete(store: QuestStore) {
  store.checkAnswer('QUEST-1', 'B');
  store.checkAnswer('QUEST-2', 'A');
  store.checkAnswer('QUEST-3', 'C');
}

test('wrong answers award zero, hints cost once, and correct answers cannot score twice', t => {
  const store = fixture(t);
  assert.equal(store.checkAnswer('QUEST-1', 'A').awarded, 0);
  assert.equal(store.snapshot().progress.completedCount, 0);
  store.getHint('QUEST-1');
  const version = store.snapshot().progress.version;
  store.getHint('QUEST-1');
  assert.equal(store.snapshot().progress.version, version);
  assert.equal(store.checkAnswer('QUEST-1', 'B').awarded, 75);
  assert.throws(() => store.checkAnswer('QUEST-1', 'B'), { code: 'ALREADY_SOLVED' });
  assert.equal(store.checkAnswer('QUEST-2', 'A').awarded, 100);
  assert.equal(new QuestStore(store.path).snapshot().progress.score, 175);
});

test('future quests and premature badge claims fail explicitly', t => {
  const store = fixture(t);
  assert.throws(() => store.checkAnswer('QUEST-3', 'C'), { code: 'QUEST_LOCKED' });
  assert.throws(() => store.getHint('QUEST-2'), { code: 'QUEST_LOCKED' });
  assert.throws(() => store.proposeBadge(), { code: 'BADGE_LOCKED' });
  assert.equal(store.snapshot().progress.score, 0);
});

test('untrusted game stories stay data, with no answer key or shared mutable seed', t => {
  const store = fixture(t);
  const quest = store.getChallenge('QUEST-3');
  assert.match(quest.challenge?.story ?? '', /UNTRUSTED GAME SCROLL/);
  assert.equal(Object.hasOwn(quest.challenge ?? {}, 'answer'), false);
  assert.equal(store.snapshot().progress.badgePublished, false);
  assert.equal(store.snapshot().proposals.length, 0);
  if (!quest.challenge) throw new Error('Fixture challenge missing.');
  quest.challenge.options.length = 0;
  assert.equal(store.getChallenge('QUEST-3').challenge?.options.length, 3);
});

test('badge proposals are idempotent, unpublished until human approval, and apply once', t => {
  const store = fixture(t);
  complete(store);
  const proposal = store.proposeBadge();
  assert.equal(store.proposeBadge().id, proposal.id);
  assert.equal(proposal.score, 300);
  assert.equal(store.snapshot().progress.badgePublished, false);
  store.decide(proposal.id, 'approved');
  assert.deepEqual(store.snapshot().progress.publishedBadge, {
    name: 'DevFest Agent Builder', score: 300,
  });
  assert.throws(() => store.decide(proposal.id, 'approved'), { code: 'ALREADY_DECIDED' });
  assert.throws(() => store.proposeBadge(), { code: 'BADGE_ALREADY_PUBLISHED' });
});

test('rejecting a proposal leaves publication unchanged', t => {
  const store = fixture(t);
  complete(store);
  const proposal = store.proposeBadge();
  store.decide(proposal.id, 'rejected');
  assert.equal(store.snapshot().progress.badgePublished, false);
  assert.notEqual(store.proposeBadge().id, proposal.id);
});

test('stale badge versions and corrupt persisted state are not silently accepted', t => {
  const store = fixture(t);
  complete(store);
  const proposal = store.proposeBadge();
  const saved = JSON.parse(readFileSync(store.path, 'utf8'));
  saved.version += 1;
  writeFileSync(store.path, JSON.stringify(saved));
  assert.throws(() => store.decide(proposal.id, 'approved'), { code: 'STALE_PROPOSAL' });
  assert.equal(store.snapshot().progress.badgePublished, false);
  writeFileSync(store.path, '{not valid JSON');
  assert.throws(() => store.snapshot(), SyntaxError);
});
