import {
  getFunctionCalls, getFunctionResponses, InMemoryRunner, isFinalResponse, stringifyContent,
} from '@google/adk';
import type { LlmAgent } from '@google/adk';

export interface TraceEntry {
  source: 'ADK runtime' | 'Local deterministic handler' | 'Human confirmation';
  kind: 'call' | 'result';
  payload: unknown;
}

export function requireLiveKey(): void {
  if (!process.env.GEMINI_API_KEY?.trim()) {
    throw new Error('LIVE MODE REQUIRES GEMINI_API_KEY. Set it privately; no automatic offline fallback.');
  }
}

export async function createChat(agent: LlmAgent, onTrace?: (entry: TraceEntry) => void) {
  const runner = new InMemoryRunner({ agent, appName: 'devfest_quest' });
  const userId = 'local_player';
  const session = await runner.sessionService.createSession({ appName: runner.appName, userId });
  return async (request: string) => {
    const trace: TraceEntry[] = [];
    const answers: string[] = [];
    for await (const event of runner.runAsync({
      userId, sessionId: session.id,
      newMessage: { role: 'user', parts: [{ text: request }] },
      runConfig: { maxLlmCalls: 6 },
    })) {
      for (const call of getFunctionCalls(event)) {
        const entry: TraceEntry = { source: 'ADK runtime', kind: 'call', payload: call };
        trace.push(entry);
        onTrace?.(entry);
      }
      for (const result of getFunctionResponses(event)) {
        const entry: TraceEntry = { source: 'ADK runtime', kind: 'result', payload: result };
        trace.push(entry);
        onTrace?.(entry);
      }
      if (event.errorCode || event.errorMessage) {
        throw new Error(`ADK error: ${event.errorCode ?? 'UNKNOWN'} ${event.errorMessage ?? ''}`);
      }
      if (isFinalResponse(event)) {
        const visible = {
          ...event,
          content: { ...event.content, parts: event.content?.parts?.filter(part => !part.thought) ?? [] },
        };
        const answer = stringifyContent(visible).trim();
        if (answer) {
          answers.push(answer);
        }
      }
    }
    if (answers.length === 0) {
      throw new Error('ADK returned no visible final answer. Inspect the runtime; do not claim success.');
    }
    return { answer: answers.join('\n'), trace };
  };
}
