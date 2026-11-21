import assert from 'node:assert/strict';
import { once } from 'node:events';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import type { TestContext } from 'node:test';
import { z } from 'zod';
import { createQuestServer } from './server.ts';
import { QuestStore } from './store.ts';

const stateResponse = z.object({ mode: z.enum(['offline', 'live']) });

async function fixture(t: TestContext) {
  const folder = mkdtempSync(join(tmpdir(), 'quest-http-'));
  const store = new QuestStore(join(folder, 'quest-state.json'));
  const server = createQuestServer(store);
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(async () => {
    await new Promise<void>((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
    rmSync(folder, { recursive: true, force: true });
  });
  const address = server.address();
  if (!address || typeof address === 'string') throw new Error('Missing HTTP test address.');
  const origin = `http://127.0.0.1:${address.port}`;
  const post = (path: string, data: unknown, from = origin) => fetch(`${origin}${path}`, {
    method: 'POST', headers: { Origin: from, 'Content-Type': 'application/json' }, body: JSON.stringify(data),
  });
  return { store, origin, post };
}

test('local API rejects foreign origins, excess body size, and source-file access', async t => {
  const { origin, post, store } = await fixture(t);
  assert.equal((await post('/api/answer', { challengeId: 'QUEST-1', choice: 'B' }, 'https://example.invalid')).status, 403);
  assert.equal(store.snapshot().progress.score, 0);
  assert.equal((await fetch(`${origin}/src/store.ts`)).status, 404);
  const empty = { padding: '' };
  const paddingLength = 8192 - Buffer.byteLength(JSON.stringify(empty));
  const atLimit = { padding: 'x'.repeat(paddingLength) };
  assert.equal((await post('/api/challenge', atLimit)).status, 400);
  assert.equal((await post('/api/challenge', { padding: `${atLimit.padding}x` })).status, 413);
  const state = stateResponse.parse(await (await fetch(`${origin}/api/state`)).json());
  assert.equal(state.mode, 'offline');
  assert.equal((await post('/api/chat', { message: 'Hello host.' })).status, 409);
});

test('browser API plays three quests, proposes but does not publish, then requires human confirmation', async t => {
  const { post, store } = await fixture(t);
  const premature = await post('/api/propose', {});
  assert.equal(premature.status, 409);
  await post('/api/hint', { challengeId: 'QUEST-1' });
  for (const [challengeId, choice] of [['QUEST-1', 'B'], ['QUEST-2', 'A'], ['QUEST-3', 'C']]) {
    assert.equal((await post('/api/answer', { challengeId, choice })).status, 200);
  }
  assert.equal(store.snapshot().progress.score, 275);
  assert.equal((await post('/api/propose', { score: 10000 })).status, 400);
  const proposalResponse = z.object({
    result: z.object({ data: z.object({
      proposal: z.object({ id: z.string() }), applied: z.boolean(),
    }) }),
  }).parse(await (await post('/api/propose', {})).json());
  const proposalId = proposalResponse.result.data.proposal.id;
  assert.equal(proposalResponse.result.data.applied, false);
  assert.equal(store.snapshot().progress.badgePublished, false);
  assert.equal((await post('/api/approve', { proposalId, confirmation: 'yes' })).status, 400);
  assert.equal(store.snapshot().progress.badgePublished, false);
  const published = await post('/api/approve', { proposalId, confirmation: 'PUBLISH' });
  assert.equal(published.status, 200);
  assert.equal(store.snapshot().progress.badgePublished, true);
  assert.equal((await post('/api/approve', { proposalId, confirmation: 'PUBLISH' })).status, 409);
});

test('live chat errors remain errors rather than changing to offline mode', async t => {
  const folder = mkdtempSync(join(tmpdir(), 'quest-chat-error-'));
  const store = new QuestStore(join(folder, 'quest-state.json'));
  const server = createQuestServer(store, async () => { throw new Error('Scripted upstream failure.'); });
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(async () => {
    await new Promise<void>((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
    rmSync(folder, { recursive: true, force: true });
  });
  const address = server.address();
  if (!address || typeof address === 'string') throw new Error('Missing test address.');
  const origin = `http://127.0.0.1:${address.port}`;
  const response = await fetch(`${origin}/api/chat`, {
    method: 'POST', headers: { Origin: origin, 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Hello host.' }),
  });
  assert.equal(response.status, 500);
  assert.equal(stateResponse.parse(await (await fetch(`${origin}/api/state`)).json()).mode, 'live');
  assert.equal(store.snapshot().progress.score, 0);
});
