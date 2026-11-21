import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

export function createWorkshopMcpServer() {
  const server = new McpServer({ name: 'devfest-workshop', version: '1.0.0' });
  const annotations = {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: false,
  };
  server.registerTool('get_workshop_overview', {
    description: 'Read the public one-hour DevFest workshop outline. No files, network, or game state.',
    inputSchema: {},
    annotations,
  }, () => ({
    content: [{ type: 'text', text: JSON.stringify({
      minutes: 60,
      sequence: ['vibe coding', 'tools', 'setup', 'skills', 'MCP', 'building agents'],
      demo: 'DevFest Quest: Antigravity builds; TypeScript ADK hosts; code scores; humans publish locally.',
      distinction: 'This MCP server supplies static development checklists, not ADK game tools.',
    }) }],
  }));
  server.registerTool('get_agent_build_checklist', {
    description: 'Read a bounded agent-building checklist for the fictional DevFest game.',
    inputSchema: {},
    annotations,
  }, () => ({
    content: [{ type: 'text', text: JSON.stringify({
      steps: [
        'Define the agent goal, player choices, and success criteria.',
        'Read existing TypeScript agent, handlers, schemas, and tests before editing.',
        'Configure LlmAgent identity, instructions, model, and existing FunctionTools.',
        'Keep scoring deterministic; never add arbitrary-score or publication tools.',
        'Run focused tests and inspect an actual call, arguments, result, and grounded reply.',
        'Keep badge publication in the separate human confirmation path.',
      ],
      boundaries: 'No file access, network access, credentials, game-state writes, or publication.',
    }) }],
  }));
  return server;
}

if (import.meta.main) {
  await createWorkshopMcpServer().connect(new StdioServerTransport());
}
