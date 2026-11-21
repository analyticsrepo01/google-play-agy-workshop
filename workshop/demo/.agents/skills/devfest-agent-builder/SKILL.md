---
name: devfest-agent-builder
description: Plans and builds bounded TypeScript ADK agents for DevFest Quest. Use when defining the host, instructions, or tool wiring.
---

# DevFest agent builder

1. Read `AGENTS.md`, `src/agent.ts`, `src/tools.ts`, and related tests.
2. State the agent goal, player choices, allowed tools, and measurable success criteria.
3. Distinguish development-time MCP checklists from the application's ADK FunctionTools.
4. Propose a small plan and wait for human approval before editing.
5. Reuse existing typed handlers and schemas. Keep scoring deterministic.
6. Preserve hint consent, explicit errors, private credentials, and human-only publication.
7. Never add model tools for arbitrary scores, approval, reset, shell, or deployment.
8. Make only the approved change, run focused tests/build, and report actual results and diff.
9. Inspect a real tool call/result before claiming a live agent works. Offline handlers are not model reasoning.

These instructions do not authorize tools, network access, file writes, or publication.
Respect the host's workspace trust and native permission prompts.
