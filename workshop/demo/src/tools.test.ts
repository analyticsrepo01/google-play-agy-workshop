import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { BaseLlm } from '@google/adk';
import type { BaseLlmConnection, LlmRequest, LlmResponse } from '@google/adk';
import { createQuestAgent } from './agent.ts';
import { createChat } from './chat.ts';
import { QuestStore } from './store.ts';
import { createQuestTools } from './tools.ts';

function fixture(t: { after: (fn: () => void) => void }) {
  const folder = mkdtempSync(join(tmpdir(), 'quest-tools-'));
  t.after(() => rmSync(folder, { recursive: true, force: true }));
  const store = new QuestStore(join(folder, 'quest-state.json'));
  return { store, ...createQuestTools(store) };
}

test('strict tool schemas reject invented scores and surface locked actions', t => {
  const { handlers, store } = fixture(t);
  const invented = handlers.proposeBadge({ score: 10000 });
  assert.equal(invented.status, 'error');
  if (invented.status === 'error') assert.equal(invented.code, 'INVALID_ARGUMENTS');
  const locked = handlers.checkAnswer({ challengeId: 'QUEST-3', choice: 'C' });
  assert.equal(locked.status, 'error');
  if (locked.status === 'error') assert.equal(locked.code, 'QUEST_LOCKED');
  const invalid = handlers.checkAnswer({ challengeId: 'QUEST-1', choice: 'D' });
  assert.equal(invalid.status, 'error');
  assert.equal(store.snapshot().progress.score, 0);
});

test('the model can propose a computed badge but has no publish or reset tool', t => {
  const { handlers, tools, store } = fixture(t);
  store.checkAnswer('QUEST-1', 'B');
  store.checkAnswer('QUEST-2', 'A');
  store.checkAnswer('QUEST-3', 'C');
  const result = handlers.proposeBadge({});
  assert.equal(result.status, 'success');
  if (result.status === 'success') {
    assert.equal(result.data.applied, false);
    assert.equal(result.data.proposal.score, 300);
  }
  assert.equal(store.snapshot().progress.badgePublished, false);
  assert.deepEqual(tools.map(tool => tool.name), [
    'get_challenge', 'get_hint', 'check_answer', 'propose_badge',
  ]);
});

test('real ADK executes the badge tool without publishing, and private thought parts are filtered', async t => {
  const { store } = fixture(t);
  store.checkAnswer('QUEST-1', 'B');
  store.checkAnswer('QUEST-2', 'A');
  store.checkAnswer('QUEST-3', 'C');
  class ScriptedModel extends BaseLlm {
    private turn = 0;
    constructor() { super({ model: 'offline_scripted_test_model' }); }
    async *generateContentAsync(request: LlmRequest): AsyncGenerator<LlmResponse, void> {
      if (this.turn++ === 0) {
        yield { content: { role: 'model', parts: [{ functionCall: {
          id: 'badge-call', name: 'propose_badge', args: {},
        } }] } };
      } else {
        assert.ok(request.contents.some(content => content.parts?.some(part => part.functionResponse)));
        yield { content: { role: 'model', parts: [
          { text: 'PRIVATE TEST THOUGHT', thought: true },
          { text: 'Your badge proposal is pending human review, not published.' },
        ] } };
      }
    }
    async connect(): Promise<BaseLlmConnection> {
      throw new Error('The scripted test model has no live connection.');
    }
  }
  const chat = await createChat(createQuestAgent(store, new ScriptedModel()));
  const result = await chat('Propose my earned badge.');
  assert.equal(result.trace.length, 2);
  assert.equal(result.trace[0]?.source, 'ADK runtime');
  assert.match(JSON.stringify(result.trace[0]?.payload), /propose_badge/);
  assert.match(JSON.stringify(result.trace[1]?.payload), /"applied":false/);
  assert.doesNotMatch(result.answer, /PRIVATE TEST THOUGHT/);
  assert.match(result.answer, /pending human review/);
  assert.equal(store.snapshot().progress.badgePublished, false);
});
