import { readFileSync } from 'node:fs';
import { createServer } from 'node:http';
import type { IncomingMessage, ServerResponse } from 'node:http';
import { z } from 'zod';
import { createQuestAgent } from './agent.ts';
import { createChat, requireLiveKey } from './chat.ts';
import type { TraceEntry } from './chat.ts';
import { QuestStore, WorkshopError } from './store.ts';
import { createQuestTools } from './tools.ts';

function json(response: ServerResponse, status: number, value: unknown): void {
  response.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  response.end(JSON.stringify(value));
}

async function body(request: IncomingMessage): Promise<unknown> {
  if (request.headers['content-type']?.split(';')[0]?.trim() !== 'application/json') {
    throw new WorkshopError('CONTENT_TYPE', 'Use application/json for game actions.');
  }
  const chunks: Buffer[] = [];
  let size = 0;
  for await (const chunk of request.iterator({ destroyOnReturn: false })) {
    if (!Buffer.isBuffer(chunk) && typeof chunk !== 'string') {
      throw new Error('Unexpected HTTP request chunk.');
    }
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    size += buffer.length;
    if (size > 8192) {
      request.resume();
      throw new WorkshopError('BODY_TOO_LARGE', 'Game requests must be at most 8 KB.');
    }
    chunks.push(buffer);
  }
  try {
    const value: unknown = JSON.parse(Buffer.concat(chunks).toString('utf8'));
    return value;
  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new WorkshopError('INVALID_JSON', 'Request body is not valid JSON.');
    }
    throw error;
  }
}

function logTrace(entry: TraceEntry): void {
  console.log(`[${entry.source} | ${entry.kind}]`, JSON.stringify(entry.payload));
}

export function createQuestServer(store: QuestStore, chat?: Awaited<ReturnType<typeof createChat>>) {
  const { handlers } = createQuestTools(store);
  let busy = false;
  const server = createServer(async (request, response) => {
    response.setHeader('Cache-Control', 'no-store');
    response.setHeader('X-Content-Type-Options', 'nosniff');
    response.setHeader('Cross-Origin-Resource-Policy', 'same-origin');
    response.setHeader('Content-Security-Policy',
      "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; "
      + "base-uri 'none'; frame-ancestors 'none'; form-action 'self'");
    try {
      const address = server.address();
      if (!address || typeof address === 'string') {
        throw new Error('Game server has no loopback address.');
      }
      const host = `127.0.0.1:${address.port}`;
      const origin = `http://${host}`;
      if (request.headers.host !== host) {
        throw new WorkshopError('FORBIDDEN_HOST', 'Use the exact 127.0.0.1 game URL.');
      }
      if (!request.url) {
        throw new WorkshopError('INVALID_URL', 'The request URL is missing.');
      }
      const url = new URL(request.url, origin);
      if (request.method === 'GET') {
        if (url.pathname === '/api/state') {
          json(response, 200, { mode: chat ? 'live' : 'offline', ...store.snapshot() });
          return;
        }
        const assets = new Map([
          ['/', ['index.html', 'text/html; charset=utf-8']],
          ['/app.js', ['app.js', 'text/javascript; charset=utf-8']],
          ['/style.css', ['style.css', 'text/css; charset=utf-8']],
        ]);
        const asset = assets.get(url.pathname);
        if (asset) {
          const [name, contentType] = asset;
          if (!name || !contentType) {
            throw new Error('Invalid static asset definition.');
          }
          response.writeHead(200, { 'Content-Type': contentType });
          response.end(readFileSync(new URL(`../public/${name}`, import.meta.url)));
        } else if (url.pathname === '/favicon.ico') {
          response.writeHead(204);
          response.end();
        } else {
          json(response, 404, { error: { code: 'NOT_FOUND', message: 'No such game page.' } });
        }
        return;
      }
      if (request.method !== 'POST') {
        json(response, 405, { error: { code: 'METHOD_NOT_ALLOWED', message: 'Use GET or POST.' } });
        return;
      }
      if (request.headers.origin !== origin) {
        throw new WorkshopError('FORBIDDEN_ORIGIN', 'Game actions must come from the local game page.');
      }
      if (busy) {
        throw new WorkshopError('BUSY', 'A game action is in progress. Wait, then refresh the actual state.');
      }
      busy = true;
      try {
        const input = await body(request);
        if (url.pathname === '/api/chat') {
          if (!chat) {
            throw new WorkshopError('LIVE_NOT_ENABLED', 'Offline mode has no model chat. Restart with npm run dev:live.');
          }
          const args = z.object({ message: z.string().trim().min(1).max(800) }).strict().parse(input);
          const result = await chat(args.message);
          json(response, 200, { ...result, state: store.snapshot() });
          return;
        }
        if (url.pathname === '/api/approve') {
          const args = z.object({
            proposalId: z.string().regex(/^BADGE-[a-f0-9-]{36}$/),
            confirmation: z.literal('PUBLISH'),
          }).strict().parse(input);
          const proposal = store.decide(args.proposalId, 'approved');
          const trace: TraceEntry[] = [{
            source: 'Human confirmation', kind: 'result', payload: { proposal, applied: true },
          }];
          trace.forEach(logTrace);
          json(response, 200, { state: store.snapshot(), trace });
          return;
        }
        const routes = {
          '/api/challenge': { name: 'get_challenge', execute: handlers.getChallenge },
          '/api/hint': { name: 'get_hint', execute: handlers.getHint },
          '/api/answer': { name: 'check_answer', execute: handlers.checkAnswer },
          '/api/propose': { name: 'propose_badge', execute: handlers.proposeBadge },
        };
        const route = Object.entries(routes).find(([path]) => path === url.pathname)?.[1];
        if (!route) {
          json(response, 404, { error: { code: 'NOT_FOUND', message: 'No such game action.' } });
          return;
        }
        const result = route.execute(input);
        const trace: TraceEntry[] = [
          { source: 'Local deterministic handler', kind: 'call', payload: { name: route.name, arguments: input } },
          { source: 'Local deterministic handler', kind: 'result', payload: result },
        ];
        trace.forEach(logTrace);
        if (result.status === 'error') {
          json(response, result.code === 'INVALID_ARGUMENTS' ? 400 : 409, { error: result, trace });
        } else {
          json(response, 200, { result, state: store.snapshot(), trace });
        }
      } finally {
        busy = false;
      }
    } catch (error) {
      const domain = error instanceof WorkshopError;
      const invalid = error instanceof z.ZodError;
      const code = domain ? error.code : invalid ? 'INVALID_ARGUMENTS' : 'SERVER_ERROR';
      const message = error instanceof Error ? error.message : 'Unknown request failure.';
      const key = process.env.GEMINI_API_KEY;
      console.error('[REQUEST FAILED]', code, key ? message.replaceAll(key, '[redacted]') : message);
      const status = invalid || ['INVALID_JSON', 'INVALID_URL'].includes(code) ? 400
        : ['FORBIDDEN_HOST', 'FORBIDDEN_ORIGIN'].includes(code) ? 403
          : code === 'BODY_TOO_LARGE' ? 413 : code === 'CONTENT_TYPE' ? 415
            : domain ? 409 : 500;
      json(response, status, { error: {
        code, message: domain || invalid ? message
          : 'The request failed. Check the presenter terminal and refresh game state; no offline fallback occurred.',
      } });
    }
  });
  server.requestTimeout = 30_000;
  return server;
}

if (import.meta.main) {
  const args = process.argv.slice(2);
  if (args.some(arg => arg !== '--live') || args.length > 1) {
    throw new Error('Usage: npm run dev | npm run dev:live');
  }
  const live = args.includes('--live');
  if (live) {
    requireLiveKey();
  }
  const store = new QuestStore();
  const chat = live ? await createChat(createQuestAgent(store), logTrace) : undefined;
  const server = createQuestServer(store, chat);
  const port = z.coerce.number().int().min(1024).max(65535).parse(process.env.PORT ?? 18767);
  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen(port, '127.0.0.1', resolve);
  });
  console.log(`DEVFEST QUEST | http://127.0.0.1:${port} | ${live ? 'LIVE ADK host' : 'OFFLINE: deterministic tools, no LLM'}`);
  console.log('Single-player local demo. Badge publication is local, not deployment or an official certificate.');
  process.once('SIGINT', () => server.close());
}
