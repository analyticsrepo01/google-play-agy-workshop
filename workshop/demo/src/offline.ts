import { QuestStore } from './store.ts';
import { createQuestTools } from './tools.ts';

const store = new QuestStore();
const { handlers } = createQuestTools(store);
console.log('OFFLINE TOOL WALKTHROUGH: deterministic game handlers, no LLM and no live ADK reasoning.');
if (store.snapshot().progress.completedCount !== 0) {
  throw new Error('Start this walkthrough with fresh local progress. Use npm run reset and explicitly confirm first.');
}
console.log('Read quest:', JSON.stringify(handlers.getChallenge({ challengeId: 'current' }), null, 2));
console.log('Hint (25-point cost):', JSON.stringify(handlers.getHint({ challengeId: 'QUEST-1' }), null, 2));
for (const [challengeId, choice] of [['QUEST-1', 'B'], ['QUEST-2', 'A'], ['QUEST-3', 'C']]) {
  const result = handlers.checkAnswer({ challengeId, choice });
  if (result.status === 'error') {
    throw new Error(`${result.code}: ${result.message}`);
  }
  console.log('Check answer:', JSON.stringify(result, null, 2));
}
console.log('Propose, never publish:', JSON.stringify(handlers.proposeBadge({}), null, 2));
console.log('Real state:', JSON.stringify(store.snapshot(), null, 2));
console.log('Expected: 275 points, badgePublished:false. Review with npm run state; a human approves separately.');
