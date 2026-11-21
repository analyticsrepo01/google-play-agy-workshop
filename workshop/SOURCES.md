# Source map and verification notes

## Current Name Race alignment (21 November 2026)

The saved 21-slide decks use the
[Name Race source](https://github.com/sajeetharan/name-race-agent-workshop),
revision **fdbbc14** (five-question quiz), as their current demo reference:

- `README.md`, `src/questions.ts`, and `src/race.ts`: 120 entries, five questions,
  correct = 100 points / 20% progress, score/time ranking, named podium,
  one-shot answers, private grades until CLOSE, and two-hour room expiry.
- `package.json`: Node 24.13+, npm 11+, `npm run check`, `npm run dev`,
  no ADK dependency. Local port is 18769.
- `.agents/skills/name-race-builder/SKILL.md`: reviewed plan, smallest approved
  change, privacy and host controls, actual checks and separate browser flows.
- `mcp_config.example.json` and `src/mcp.ts`: guide mode requires `--guide`
  and exposes `get_game_rules`/`get_build_steps`; the runtime broker separately
  exposes registration, answer, read, and authorized host operations.
- `src/agent.ts`: `createCommentator`, one model-selected anonymous
  `read_race_summary` call, validated phase/style, freshness check, and
  code-rendered facts. No participant names, answers, scoring or host controls.
- `BUILD_GUIDE.md`, `DEMO_SCRIPT.md`, `DEPLOY.md`, and `VALIDATION.md`:
  build steps, live narration, private host login and single-owner deployment limits.

Both decks retain their saved layouts, cover photo,
official tool links, and animation timelines. Demo-specific notes are rewritten
to match the current code. `update_demo_slides.py` updates the saved packages;
`build_slides.py` only produces a separately named historical Quest deck.
The cover's blue journey title is enlarged to 27 pt. The closing resource link
and regenerated static QR now target the Name Race repository, with a separate
link to its numbered build guide.

### Current slide map

| Slides | Current teaching content |
| --- | --- |
| 1-5 | Welcome, Name Race Outcome, vibe coding, brief, verification |
| 6-8 | Tools and Antigravity development workflow |
| 9-11 | Current project setup and permissions |
| 12-13 | `name-race-builder` Skill |
| 14-15 | Guide versus runtime MCP; valid guide configuration |
| 16-18 | Optional bounded Gemini loop and actual MCP evidence |
| 19-20 | Five-question quiz, podium, human and code boundaries |
| 21 | Handbook, Name Race source, Antigravity docs, workshop repo |

The Quest/ADK implementation below is retained only as historical provenance;
its commands, tools, and dependency claims do not describe Name Race.

---

## Historical Quest preparation

Prepared for the 21 November 2026 GDG Kathmandu session.
Product documentation was checked on **20 November 2026**.

## User-supplied material

| Source | Adapted teaching element |
| --- | --- |
| Session poster / GDG Kathmandu announcement | Event title, speaker, date, Google Meet, Road to DevFest Nepal 2026, online series #1; the original duration/scenario are superseded below |
| Presenter confirmation on 20 November 2026 | One-hour presenter-led format, 19:30-20:30 NPT, and the newly authored DevFest Quest game instead of tickets |
| Revised presenter goal on 20 November 2026 | Vibe coding first, then Antigravity/other tools, setup, Skills, MCP, and finally building an ADK agent; setup is a presenter walkthrough |
| `AGY_Dev_Workshop_Slides.pdf`, slides 1-9 | Antigravity setup, requirements interview, reviewable plan, tool/browser evidence, human oversight |
| Same PDF, slides 10-14 | Model choice, quota/context awareness; benchmark figures are not repeated as workshop promises |
| Same PDF, slides 15-19 | Distinguish development subagents, verification roles, reusable team instructions; advanced multi-agent/plugin demos moved out of the beginner core |
| Supplied English translation | Terminology continuity, not independent verification of source product claims |
| `Copy of [PUBLIC] Build with AI Handbook _ g.dev_ai_build.pptx`, slides 2, 4-6, 9-12, 14, 17-18, 28-29, 31-33 | Vibe-coding definition and builder audience, tool entry points, prompt anatomy, Think/Build/Publish framing, Antigravity introduction, public handbook link |
| [Repository hands-on guide](../HANDS_ON_LAB_GUIDE.md) | Scope -> rules -> plan -> RED -> GREEN -> human confirmation -> verify |
| [Repository feature reference](../AGY_FEATURES.md) | Antigravity artifacts, file context, rules, and optional commands; not an ADK API reference |
| [Repository guardrails](../.agents/rules/play-standards.md) | Test-first workflow, explicit human confirmation, no hardcoded keys |

The newly authored deck adapts concepts rather than redistributing the entire
65.8 MB public handbook or copying its images. Share the handbook's requested
short link: **https://g.dev/ai/build**.

### Revised teaching map

| Workshop slides | Source / adaptation |
| --- | --- |
| 1-4: vibe coding, prompt, verification | Handbook 5-6, 9, 14, 17; repository review/test workflow. The Antigravity PDF itself does not contain the handbook's vibe-coding introduction. |
| 5-7: tools and Antigravity | Handbook 9-11, 28-29; supplied Antigravity PDF 3, 7-9, 18. Other tool names are illustrative alternatives, not a benchmark or parity claim. |
| 8-10: setup and permissions | Supplied PDF 3-6, corrected using current official setup/account documentation. No enterprise-only or blanket Turbo requirement. |
| 11-12: Skills | Handbook glossary 12, supplied PDF 18, official skills documentation, and the newly authored DevFest workspace skill. |
| 13-14: MCP | Handbook glossary 12, repository feature reference, official MCP documentation, and the newly authored local read-only server/configuration. |
| 15-19: build/run an agent | Existing TypeScript ADK implementation, bounded instruction-edit walkthrough, actual tool evidence, and the preserved DevFest game/human confirmation. |
| 20: resources | Public handbook and official product/runtime documentation. |

The original deck's long model-comparison and multi-agent exercises are not
the one-hour core. The earlier scoring RED/GREEN block is now optional take-home.

### Handbook visual alignment

The editable workshop deck also adapts the handbook's visual language:
cover/resource composition and bottom rainbow accent (slide 2), shadowed
rounded roadmap rows (slide 4), outlined cards and colored pill headings
(slide 9), full-bleed gradient phase treatments (slides 14 and 18),
black/bright-green Antigravity styling (slide 28), and coding-brace/resource
motifs (slide 33). The page size matches the original 720 x 405 points.
These are newly drawn PowerPoint shapes, not flattened handbook screenshots.
The closing slide's QR code is regenerated for the public handbook URL.
The cover does not include a QR code or handbook shortlink.

Google Sans is specified to match the source, but fonts are not redistributed.
This machine has no installed Google Sans font, so PowerPoint's local font
substitution is used in the verified PDF. Installing an appropriately licensed
Google Sans font can change text metrics; recheck the render after changing fonts.
This is an independently prepared community workshop, not an official Google deck.

## Official sources used for the runnable demo

- [TypeScript ADK quickstart](https://adk.dev/get-started/typescript/):
  `@google/adk`, `@google/adk-devtools`, `LlmAgent`, `FunctionTool`, Zod,
  `rootAgent`, `npx adk run agent.ts`, `npx adk web`,
  Node.js >=24.13.0 and npm >=11.8.0.
- [ADK LlmAgent](https://adk.dev/agents/llm-agents/):
  instructions, tools, identity, and nondeterministic behavior.
- [Function tools](https://adk.dev/tools-custom/function-tools/):
  schema-defined tool interfaces; language-specific support must be checked.
- [Antigravity setup](https://antigravity.google/docs/getting-started):
  supported surfaces and personal/enterprise sign-in.
- [Antigravity skills](https://antigravity.google/docs/skills):
  reusable `SKILL.md` bundles; not ADK runtime tools.
- [Antigravity MCP](https://antigravity.google/docs/mcp):
  App Customizations/Installed/MCP Servers, host configuration discovery,
  `mcpServers`, local `command`/`args`, and `enabledTools`. Preserve existing configuration.
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk):
  the runnable local example pins `@modelcontextprotocol/sdk` **1.32.2**,
  uses `McpServer`/`StdioServerTransport`, and is tested with the actual stdio client.
- [Gemini model catalog](https://aistudio.google.com/docs/models):
  select a currently available function-calling model for the presenter's account.

The demo dependencies are locked with `package-lock.json`; the ADK runtime
is pinned to the official npm release **2.5.0**, with Zod **4.6.7**.
Devtools 2.5.0 brings database drivers that attempted to compile SQLite on this
Windows machine, requiring an unavailable C++ toolchain even with Node 24.
The core `LlmAgent` / `FunctionTool` teaching API does not need those drivers.
An older lightweight runtime was initially tested, then replaced with the
current runtime after its dependency tree generated npm audit warnings.
Run `npm ci`, not an unreviewed upgrade during the workshop; use Node 24 LTS
for the rehearsed path. The explicit `@opentelemetry/api` 1.9.0 dependency
keeps the telemetry API compatible with its SDK dependencies.
The narrow `gaxios@7.1.3 -> 7.3.1` override removes a known metadata dependency
advisory chain without crossing a major version. Remaining upstream advisories
and the limits of this decision are recorded in [validation notes](./VALIDATION.md).
The core demo **does not install or use ADK devtools/Web**. A smoke test of the
0.2.5 Web UI successfully loaded the agent but exposed upstream limitations:
debug Trace endpoints returned 501, and the `--host 127.0.0.1` option changed
the advertised URL without restricting the actual listening address.
Instead, `src/live.ts` uses the official runtime's `InMemoryRunner`,
`getFunctionCalls`, `getFunctionResponses`, `isFinalResponse`, and
`stringifyContent` APIs to print real application events.
[chat.ts](./demo/src/chat.ts) shares the event handling between terminal and browser,
filters private thought parts, and limits each turn to six model calls.
The terminal host opens no listener. The new [browser controller](./demo/src/server.ts)
uses Node's built-in HTTP server, binds only to 127.0.0.1, checks exact Host/Origin,
limits JSON bodies to 8 KB, and serves only the three public game assets.
The vanilla HTML/CSS/JavaScript UI needs no new framework or browser CDN dependency.
Local handlers, live ADK calls, and human confirmations have distinct trace labels.
Offline mode disables chat rather than fabricating model reasoning.

The newly authored [workspace skill](./demo/.agents/skills/devfest-agent-builder/SKILL.md)
is discoverable when the demo copy is the workspace root. Its workflow is not authorization.
[mcp.ts](./demo/src/mcp.ts) returns only static workshop outline/checklist data:
no files, network, credentials, game state, or publication. Its two MCP tools are
for the coding environment, **not attached to the ADK game host**.
The [configuration example](./demo/mcp_config.example.json) contains a placeholder
absolute path and is intentionally not an active host config.
No user's Antigravity settings, account, skills, or connectors were installed/changed
while preparing this pack. The protocol smoke test is distinct from host UI verification.

## Deliberate corrections and exclusions

1. **ADK vs SDK:** this event uses **Google Agent Development Kit for TypeScript**,
   not the Antigravity Python SDK or coding-agent harness.
2. **Authentication:** the Korean deck's mandatory enterprise login was specific
   to that workshop. This community session supports attendees' permitted
   personal or enterprise sign-in; ADK's model API key is a separate credential.
3. **Commands:** `/grill-me`, `/plan`, `/goal`, `/learn`, `/boost`, and `/teamwork`
   are not treated as universally available on every Antigravity surface.
   Prompt cards include natural-language alternatives. Check installed command menus.
4. **Models and price:** the default example follows the official ADK quickstart
   (`gemini-flash-latest`) and permits an environment override. No guarantee of
   free quota, exact throughput, fixed output capacity, or benchmark ranking is made.
5. **Publish:** a local demonstration is not a deployed application. The
   production roadmap is a discussion, not a false "one-click ready" claim.
6. **Safety:** an instruction file is not authorization. The model's four tools
   cannot publish, reset, run shell commands, or set arbitrary scores.
   A separate browser confirmation controller or approval terminal publishes
   the earned badge locally. This is not production authentication, anti-cheat,
   or proof that an HTTP caller is human. The JSON store is single-user only.
7. **Testing:** thirteen completed-reference tests (including one MCP protocol test) and three intentionally RED learner
   tests are distinct. Local tool tests do not prove model reasoning or account access.
8. **Data:** three quests, stories, points, and badges are fictional. No real
   registration service, company data, participant identity, or official certificate is used.
   The new state file is `.workshop-data/quest-state.json`; legacy ticket state is not read or migrated.

## Suggested follow-on sessions

- More quests, accessibility refinement, and consent-aware hints.
- ADK sequential/parallel agents after defining a measurable evaluation need.
- Remote/production MCP integration, authentication, and least-privilege tool exposure
  beyond the core local read-only example.
- Durable database, authenticated API/UI, and production deployment.
- Advanced skill packaging, plugins, and team workflows beyond the core workspace skill.

These are intentionally not prerequisites for the one-hour core workshop.
