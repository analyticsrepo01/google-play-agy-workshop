# Facilitator run of show: Name Race

**21 November 2026 | 19:30-20:30 Nepal Time**

Use the [current demo script](./DEMO_SCRIPT.md), both updated decks, and
[Name Race source](https://github.com/sajeetharan/name-race-agent-workshop).
The [workshop agenda](./README.md#one-hour-agenda) allocates 40 minutes to the
presentation, two to transition, 14 to the live quiz, and four to Q&A.
Participants need only a phone/browser, not an installation.

## Current preparation

- Run the standalone repo's `npm ci` and `npm run check` before class
  (Node 24.13+ / npm 11+; ten tests, strict build, frontend syntax).
- Rehearse both host and separate participant views. Local rehearsal uses
  `npm run dev` at **http://127.0.0.1:18769**; no ADK or model key is required.
- Open the [live host](https://name-race-e9a2-261121.azurewebsites.net).
  Log in privately before sharing. Never display the host password or API key.
- Create a fresh room shortly before the demo; the two-hour expiry begins at creation.
  Share only the room's actual QR/join link, not your loopback address.
- Inspect `.agents/skills/name-race-builder/SKILL.md`, `src/mcp.ts`,
  `src/agent.ts`, and the numbered [build guide](https://github.com/sajeetharan/name-race-agent-workshop/blob/main/BUILD_GUIDE.md).
- Guide MCP must retain `--guide`, expose `get_game_rules`/`get_build_steps`,
  and use your actual absolute source path. Merge only its entry and respect
  native approvals. Verify editor discovery separately from protocol tests.
- Optional Gemini needs private key/model/quota/connectivity rehearsal.
  The quiz's actual MCP calls work with **AI OFF**. Do not invent a model trace.
- Present the animated deck with manual clicks. Rehearse its actual slideshow
  on the shared display; use the PDF for no-motion delivery.

## Current slide walkthrough

| Slides | Demonstration |
| --- | --- |
| 1-5 | Outcome, five-question brief, Think/Build/Verify |
| 6-8 | Tool choices; Antigravity builds the software, not the quiz rankings |
| 9-11 | Clone the standalone repo, run checks, review trust and private credentials |
| 12-13 | Verify `name-race-builder` discovery; request one approved wording change |
| 14-15 | Guide MCP is static; runtime MCP operates rooms through the HTTP adapter |
| 16-18 | `createCommentator`: one anonymous read, validated phase/style, code-owned facts |
| 19-20 | Play the quiz, reveal the podium, recap human and code boundaries |
| 21 | Source repos, handbook, Q&A |

## Fourteen-minute live quiz

Use the full [read-aloud script](./DEMO_SCRIPT.md).
Review nicknames, then type **START**. Participants submit one final answer
per question. Type **CLOSE** to reveal scores and progress, then **NEXT** for
the next question. Repeat through all five topics. Correct answers earn
100 points and move cars 20%; wrong/unanswered earn zero.
The final named top-three podium ranks by score, then total correct-answer
receipt time. Exact ties share rank; network/polling delay affects times.
The projector shows up to 12 cars, but all 120 entries are ranked.

Show actual `submit_answer`, `read_room`, and `host_control` MCP results.
Never expose cookie proofs, broker authority, private timestamps, or credentials.
The optional commentator receives only `read_race_summary`, not names,
answers, or host-control tools. **RESET** retains nicknames for replay;
**DELETE** removes the room after the event.

If Gemini fails, show the error and continue the real quiz with AI OFF.
If guide discovery fails, show the error and source; do not claim IDE connection.
Cut optional edits or product tab-hopping when behind, not the quiz or Q&A.
Do not deploy during a live race or modify shared Azure infrastructure.

---

# Historical reference only: DevFest Quest

> **Current demo:** [Name Race script](./DEMO_SCRIPT.md) and
> [standalone repo](https://github.com/sajeetharan/name-race-agent-workshop).
> Use its easy-English script, Skill, MCP tools, and small Gemini agent.
> The timed ADK/Quest instructions below are kept as the **previous reference**;
> do not use their tool names or badge route for the new game.

**Beyond AI-Assisted Coding: Understanding and Building AI Agents**

GDG Kathmandu / Road to DevFest Nepal 2026 / Online Workshop Series #1

Sajeetharan Sinnathurai | 21 November 2026 | **19:30-20:30 NPT**

**Goal:** vibe coding -> Antigravity and other tools -> setup -> Skills -> MCP
-> a concrete Google ADK agent-building demo using DevFest Quest.

**Format:** 60 minutes, presenter-led. Attendees watch setup and participate
through questions and A/B/C votes. No mandatory installation or coding lab.
The scoring RED/GREEN exercise is now optional take-home, not the session's spine.

## Before the event

- Present the [animated deck](./Beyond_AI_Assisted_Coding_Animated.pptx) in desktop
  PowerPoint Slide Show mode (F5). Each click reveals a whole card, not individual
  bullets; allow one to three reveal clicks per slide before advancing.
  Titles/photo and transitions use short fades; nothing advances automatically.
  Use the chapter ribbon and footer questions to invite brief chat responses.
  Notes remain unchanged read-aloud narration. Use the
  [current static PDF](./Beyond_AI_Assisted_Coding_Animated.pdf) for no-motion
  delivery, or PowerPoint's **Show without animation** option.
- Prepare an untouched [reference demo](./demo/) and a separate build copy.
  Open the build copy as its own Antigravity workspace.
- Install Antigravity from the [official download](https://antigravity.google/download).
  Rehearse the actual account/surface UI. Do not download installers during class.
- Use Node >=24.13.0 and npm >=11.8.0. Restore the locked dependencies before class.
  Run `npm run check`: **13 reference tests**, including a real local MCP protocol test.
- Review the [workspace skill](./demo/.agents/skills/devfest-agent-builder/SKILL.md)
  and rehearse P9-P11 in [prompt cards](./PROMPTS.md).
- Review [mcp.ts](./demo/src/mcp.ts), run `npm run test:mcp`, and connect the
  [example MCP entry](./demo/mcp_config.example.json) to your own Antigravity host
  after replacing its absolute path. Preserve existing servers and native approvals.
  Rehearse discovery and both read-only calls. No Gemini key is needed for this server.
- Privately set the separate Gemini key/model and rehearse `npm run dev:live`.
  Preparation used a scripted ADK test model, **not a live Gemini API call**.
- Reset your reference with `npm run reset`, type `reset`, then start your own
  server and open **http://127.0.0.1:18767**. Start at QUEST-1, zero points, badge locked.
- Rehearse the quick game route: hint on QUEST-1 -> **B / A / C** -> **275**
  -> propose -> review -> type **PUBLISH** -> refresh actual state.
- Hide credential entry, notifications, billing, unrelated tabs, and personal files.
  The co-host collects votes, posts the bundle, and protects Q&A time.

## 19:30-19:40 | Vibe coding first | Slides 1-4 | 10 minutes

**Opening:** "We start with an idea, choose the tools, set up the environment,
add reusable skills and connected tools, then build a real application agent."

- Slide 1, 1 min: welcome and the six-part journey.
- Slide 2, 3 min: handbook slides 5-6: describe intent in natural language,
  iterate with AI, and stay responsible for verification. Poll prior experience.
- Slide 3, 3 min: handbook slide 17's role/goal/context/AI/style/visual layers.
  Compare "Build me a cool game" with the scoped DevFest brief. Ask what is missing.
- Slide 4, 3 min: Think -> Build -> Verify. Tests, review, and real UI evidence.
  Do not repeat the source's guaranteed-sounding 15-minute, free, or production claims.

**Transition:** "That is the workflow. Now choose the environment that supports it."

## 19:40-19:50 | Tools and Antigravity | Slides 5-7 | 10 minutes

- Slide 5, 3 min: handbook slides 9-11: AI Studio for browser-first prototypes,
  Stitch for visual design, Antigravity for project-level agentic coding.
  Mention Copilot, Cursor, and Claude Code as other entry points, not a ranking.
  All six tools have official links; the main three cards show clickable web addresses.
  Do not open every product or claim feature/pricing parity.
- Slide 6, 3 min: source Antigravity deck slides 3 and 7: workspace context,
  plans/artifacts, terminal, browser, and review. Show the actual installed surface.
- Slide 7, 4 min: source slides 7-9 and 18: clarify requirements -> review a plan
  -> make a focused change -> inspect execution/browser evidence -> capture reuse.
  Show a prepared plan and diff. Use plain-language prompts when slash workflows differ.

**Say:** "Antigravity builds the software. ADK will run the agent inside that software."

## 19:50-20:00 | Presenter setup walkthrough | Slides 8-10 | 10 minutes

- Slide 8, 3 min: official download -> permitted sign-in -> open the build copy
  -> workspace trust -> available model. Explain personal vs business sign-in.
  The source deck's enterprise-only path is not mandatory for this community event.
- Slide 9, 4 min: show the project and pre-run commands:

```powershell
npm ci
npm run check
npm run dev
```

Locate [agent.ts](./demo/src/agent.ts), [tools.ts](./demo/src/tools.ts),
the [public UI](./demo/public/), and the [workspace skill](./demo/.agents/skills/devfest-agent-builder/SKILL.md).
Show the mode banner. Offline buttons are deterministic handlers, not model reasoning.
Antigravity sign-in and the server-side Gemini API key are separate credentials.
Explain `preflight` and `dev:live` with the key already set privately.

- Slide 10, 3 min: review permissions, scripts, commands, credentials, and connector scope.
  Honor native prompts. Do not switch on blanket auto-approval or expose the server publicly.

**Hard gate: at 20:00 move to Skills.** Installation waiting belongs before/after class.

## 20:00-20:06 | Skills | Slides 11-12 | 6 minutes

- Slide 11, 3 min: a focused folder with `SKILL.md`, discovery metadata, instructions,
  and optional resources/scripts. Contrast a project rule with a reusable task recipe.
- Slide 12, 3 min: open the bundled skill, show its real name/description and steps.
  Invoke **devfest-agent-builder** using P9. In Antigravity App, named slash invocation
  is documented; otherwise use the installed surface's supported invocation.
  Ask for the agent goal, instructions, existing tools, and verification plan.
  **Do not approve edits yet.**

**Checkpoint:** visible reviewed plan. Skill text does not authorize writes or tools.

## 20:06-20:12 | MCP | Slides 13-14 | 6 minutes

- Slide 13, 2 min: coding agent -> MCP client -> server -> scoped tools.
  **Skill = how to work; MCP = how tools connect; ADK FunctionTool = application capability.**
- Slide 14, 4 min: in Antigravity App show **Customizations -> Installed -> MCP Servers**.
  Use **Copy Config File Path** to locate your host's actual configuration.
  Show the reviewed example entry with your real absolute `src/mcp.ts` path.
  Merge only `devfest-workshop`, preserving other entries. Never overwrite all host settings.
  If the installed surface uses different controls, follow its official MCP guide.
- Inspect the two discovered tools: `get_workshop_overview` and `get_agent_build_checklist`.
  Use P10 to call the checklist with `{}` and inspect the actual result.
- Explain that Node runs this server over **stdio**, not HTTP. It returns static
  workshop context and cannot read files, call external services, change game state,
  or publish a badge. Read-only annotations are hints, not a substitute for reviewing code.
- These tools are connected to the **coding environment**, not to the ADK game host.

**Recovery:** if host connection fails, show its actual error and the real
`npm run test:mcp` discovery/call output. Say the host connection remains unverified;
do not pass CLI evidence off as an IDE call.

**Hard gate: at 20:12 move to agent building.**

## 20:12-20:26 | Build and run an application agent | Slides 15-19 | 14 minutes

### Slide 15 | Agent specification | 2 minutes

Use the skill's plan and MCP checklist to define:
friendly host, player-supplied choices, actual progress, four typed game tools,
deterministic scoring, and separate human confirmation.
Identify `LlmAgent` identity, instructions, model, tools, and runner.
ADK is **Google Agent Development Kit for TypeScript**, not the Antigravity Python SDK.

### Slide 16 | Construct/configure the agent | 4 minutes

Open the actual factory in [agent.ts](./demo/src/agent.ts). Show:
`new LlmAgent({ name, model, instruction, tools })`.
Open [tools.ts](./demo/src/tools.ts): show `check_answer`'s strict
`challengeId`/A-B-C schema and `handlers.checkAnswer`.

Use P11 for an approved, instruction-only coach-persona edit **in the build copy**.
This demonstrates authoring agent behavior while reusing tested tool implementation.
Inspect the actual diff and focused build/tool-test output; never weaken assertions.
Keep the four tools and runtime bounds unchanged. Do not build the entire backend/site live.

**Recovery gate: at 20:18 use the untouched reference if optional edits are not verified.**
Explain which copy is running.

### Slide 17 | Actual ADK call | 3 minutes

In the live browser host:

```text
Show my current quest and progress. Do not answer it for me.
```

Inspect **ADK runtime** function -> arguments -> actual result -> grounded answer.
Compare progress with the UI. Button traces are labeled **Local deterministic handler**.
The local MCP checklist is a separate development-time interaction.

If live API access fails, surface the error, inspect progress before retrying,
and explicitly restart your own server with `npm run dev` if needed.
Announce deterministic offline mode. Do not fabricate a model trace or claim a live success.

### Slide 18 | Play, propose, confirm | 4 minutes

Collect quick votes and use the rehearsed route:

| Quest | Correct choice | Lesson |
| --- | --- | --- |
| Builder Bridge / QUEST-1 | **B** | Antigravity builds and verifies code |
| Tool Temple / QUEST-2 | **A** | Typed deterministic answer checker |
| Badge Vault / QUEST-3 | **C** | Human-only publication |

One agreed hint on QUEST-1 gives **75 + 100 + 100 = 275**.
In live mode, use `Give me a hint for QUEST-1. I accept the 25-point cost.`
Then submit player choices; in offline mode use the explicit buttons.
Request the badge: pending, earned score, **applied:false**. Open review,
type **PUBLISH** outside chat, confirm, and refresh actual state.
This is local publication, not a deployed service or official certificate.
Do not spend this block on the optional terminal approval path or full negative suite.

### Slide 19 | Whole-journey recap | 1 minute

Vibe coding -> tool choice -> setup -> skill -> MCP -> a bounded ADK agent.
Tests cover scores, schemas, locked actions, stale/repeat approval, and real scripted
ADK wiring; presenter live evaluation still checks grounding, hint consent, and errors.
Exit question: **"How is a skill different from MCP and a runtime tool?"**

**Hard gate: stop demonstrations at 20:26.**

## 20:26-20:30 | Q&A and resources | Slide 20 | 4 minutes

Share the updated bundle, public handbook, setup/skills/MCP docs, and optional scorer lab.
Finish on time. Stop only presenter-owned helpers and clear credentials privately.

## If you fall behind

Cut product tab-hopping, waiting for installs, persona edits, and optional scorer wiring.
Keep the requested sequence, one real MCP protocol result, the ADK construction/tools,
one actual ADK call when your key works, human confirmation, and Q&A.
Production connectors, authentication, deployment, and multi-agent architecture are follow-ons.
