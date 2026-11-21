import { createInterface } from 'node:readline/promises';
import { stdin, stdout } from 'node:process';
import { rootAgent } from './agent.ts';
import { createChat, requireLiveKey } from './chat.ts';

requireLiveKey();
const chat = await createChat(rootAgent, entry => {
  console.log(`[TOOL ${entry.kind.toUpperCase()}]`, JSON.stringify(entry.payload, null, 2));
});
const prompt = createInterface({ input: stdin, output: stdout });
console.log(`LIVE ADK GAME HOST | ${rootAgent.model} | fictional local game | type exit to quit`);
console.log('Actual tool calls/results are shown; private model reasoning is not.');
try {
  while (true) {
    const request = (await prompt.question('\nPlayer: ')).trim();
    if (request === 'exit') {
      break;
    }
    if (!request) {
      continue;
    }
    const result = await chat(request);
    console.log('[AGENT ANSWER]', result.answer);
  }
} finally {
  prompt.close();
}
