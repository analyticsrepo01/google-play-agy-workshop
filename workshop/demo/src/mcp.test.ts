import assert from 'node:assert/strict';
import { join } from 'node:path';
import { test } from 'node:test';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { z } from 'zod';

test('local MCP starts over stdio, discovers two read-only tools, and returns agent-building context', async t => {
  const client = new Client({ name: 'devfest-mcp-test', version: '1.0.0' });
  const transport = new StdioClientTransport({
    command: process.execPath,
    args: [join(import.meta.dirname, 'mcp.ts')],
    stderr: 'pipe',
  });
  t.after(() => client.close());
  await client.connect(transport);
  const { tools } = await client.listTools();
  assert.deepEqual(tools.map(tool => tool.name).sort(), [
    'get_agent_build_checklist', 'get_workshop_overview',
  ]);
  assert.ok(tools.every(tool => tool.annotations?.readOnlyHint === true));
  const textResult = z.object({
    content: z.tuple([z.object({ type: z.literal('text'), text: z.string() })]),
  });
  const overview = textResult.parse(await client.callTool({
    name: 'get_workshop_overview', arguments: {},
  }));
  const outline = z.object({
    minutes: z.number(),
    sequence: z.array(z.string()),
    distinction: z.string(),
  }).parse(JSON.parse(overview.content[0].text));
  assert.equal(outline.minutes, 60);
  assert.equal(outline.sequence[0], 'vibe coding');
  assert.equal(outline.sequence.at(-1), 'building agents');
  assert.match(outline.distinction, /not ADK game tools/);
  const checklist = textResult.parse(await client.callTool({
    name: 'get_agent_build_checklist', arguments: {},
  }));
  const steps = z.object({ steps: z.array(z.string()), boundaries: z.string() })
    .parse(JSON.parse(checklist.content[0].text));
  assert.ok(steps.steps.some(step => step.includes('LlmAgent')));
  assert.ok(steps.steps.some(step => step.includes('separate human confirmation')));
  assert.match(steps.boundaries, /No file access, network access, credentials/);
});
