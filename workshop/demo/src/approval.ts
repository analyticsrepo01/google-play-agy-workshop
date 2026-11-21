import { createInterface } from 'node:readline/promises';
import { stdin, stdout } from 'node:process';
import { QuestStore } from './store.ts';

const store = new QuestStore();
const [command, proposalId] = process.argv.slice(2);
if (command === 'list') {
  console.log(JSON.stringify({ mode: 'FICTIONAL LOCAL GAME; no external publication', ...store.snapshot() }, null, 2));
} else if (command === 'approve' || command === 'reject') {
  if (!proposalId) {
    throw new Error(`Usage: npm run ${command} -- BADGE-<id>`);
  }
  const proposal = store.snapshot().proposals.find(item => item.id === proposalId);
  if (!proposal) {
    throw new Error(`Unknown proposal: ${proposalId}`);
  }
  console.log(JSON.stringify(proposal, null, 2));
  const prompt = createInterface({ input: stdin, output: stdout });
  try {
    const answer = await prompt.question(`Human review: type ${command} ${proposalId} to confirm: `);
    if (answer.trim() !== `${command} ${proposalId}`) {
      throw new Error('Confirmation did not match. No state was changed.');
    }
    console.log(JSON.stringify(store.decide(proposalId, command === 'approve' ? 'approved' : 'rejected'), null, 2));
  } finally {
    prompt.close();
  }
} else if (command === 'reset') {
  const prompt = createInterface({ input: stdin, output: stdout });
  try {
    const answer = await prompt.question('Reset ONLY this local fictional game and badge proposals? Type reset: ');
    if (answer.trim() !== 'reset') {
      throw new Error('Reset cancelled. No state was changed.');
    }
    store.reset();
    console.log('Local DevFest Quest state reset.');
  } finally {
    prompt.close();
  }
} else {
  throw new Error('Usage: npm run state | approve -- <id> | reject -- <id> | reset');
}
