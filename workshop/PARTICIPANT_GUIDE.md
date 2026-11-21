# Participant guide: Name Race

**21 November 2026 | 19:30-20:30 Nepal Time**


## Join during the session

1. Scan the presenter's room QR or open its public join link.
2. Choose a nickname you consent to display; do not use private information.
3. Wait for the host to start. Answer each of five workshop questions on your phone.
4. Each saved answer is final. The host closes a question before revealing grades.
5. Correct answers earn **100 points** and move your car **20%**; wrong or
   unanswered questions earn zero. Watch your car and the final named podium.

Up to 120 entries can join. Score ranks first; total time for correct answers
breaks ties. Server timing includes network/polling delay, so this is a teaching
quiz, not a proctored exam. Exact ties share rank. One browser entry is not
verified real-person identity. Rooms expire two hours after creation.
No installation, account, ADK, or model key is required to participate.

## Repeat after the session

Use [Name Race source](https://github.com/sajeetharan/name-race-agent-workshop)
and its [build guide](https://github.com/sajeetharan/name-race-agent-workshop/blob/main/BUILD_GUIDE.md).
With **Node 24.13+ / npm 11+**:

```powershell
git clone https://github.com/sajeetharan/name-race-agent-workshop.git
Set-Location .\name-race-agent-workshop
npm ci
npm run check
npm run dev
```

Open **http://127.0.0.1:18769**. Local no-password host controls are loopback-only;
never expose that configuration through a tunnel. The deployed HTTPS app uses
a private host login. Follow the standalone deployment guide for your own app.

## Skills, MCP, and the optional agent

- Open the standalone repo as your coding workspace. Inspect
  `.agents/skills/name-race-builder/SKILL.md`; ask for `name-race-builder` and
  verify actual discovery in your installed host. A Skill grants no permissions.
- Review `mcp_config.example.json`. Replace its absolute path, keep `--guide`,
  and merge only `name-race-guide` into host settings. Preserve other servers
  and native approvals. Call `get_build_steps` with `{}` and inspect the result.
- Guide tools (`get_game_rules`, `get_build_steps`) return static context.
  Runtime tools handle real room reads, registrations, answers, and host actions.
  Do not give a coding host the private runtime broker authority.
- Inspect `src/agent.ts`: optional Gemini gets only `read_race_summary`, once
  for the selected room, with anonymous labels. It chooses phase/style;
  code validates the response and renders facts. It cannot score or control rooms.
- **AI OFF** still has real MCP, but is not model reasoning. Optional Gemini
  needs a privately configured server-side `GEMINI_API_KEY`, then the same
  `npm run dev` command. Never put keys in prompts, code, screenshots, or chat.
  Failed model calls remain errors, not hidden fallbacks.
- Make one approved wording change in a build copy, run `npm run check`,
  and verify host and participant screens separately.

See [current prompt cards](./PROMPTS.md) and
[Name Race validation/limits](https://github.com/sajeetharan/name-race-agent-workshop/blob/main/VALIDATION.md).
The folder `workshop/demo` below is an older Quest reference, not the live quiz.

---

# Historical reference only: DevFest Quest

**21 November 2026 | 19:30-20:30 Nepal Time**

**Format:** presenter-led demo. You can participate without installing anything.

## During the one-hour session

- Follow the journey: vibe coding -> tool choice -> Antigravity setup -> Skills
  -> MCP -> building a Google ADK application agent.
- Notice the difference between a useful scoped prompt and a vague request.
- Watch installation/account/project steps; repeat them later, not during the talk.
- Inspect the skill manifest and the actual read-only MCP result.
- Vote A/B/C in Google Meet chat when the presenter opens each quest.
- Notice which agent **builds the code** and which agent **hosts the game**.
- Inspect one real tool call: function name, arguments, result, and final response.
- Check that hints change deterministic scoring and wrong answers earn zero.
- Watch **pending badge proposal** become **published locally** only after human confirmation.
- Ask questions in the final four-minute block.

The presenter shares one local game. Their `127.0.0.1` URL is **not** a public
multiplayer link. Do not paste credentials or personal data into meeting chat.

## Optional setup after the session

Use **Node.js >=24.13.0** and **npm >=11.8.0**. Extract the bundle or clone
the published repository. Copy [demo](./demo/) into your own `my-devfest-quest`
folder before edits; keep a working reference.

From inside the demo copy:

```powershell
npm ci
npm run check
npm run dev
```

Open **http://127.0.0.1:18767**. All **13 reference tests** pass.
The offline game has no model calls: it invokes deterministic handlers and
disables ADK chat. Wrong answers = 0, correct = 100, correct after hint = 75.
The game uses fictional data and no third-party browser assets.

After three quests, request the badge, review it, type **PUBLISH**, and confirm.
This publishes only to your local JSON progress, not a website or official certificate.

### Set up Antigravity and the reusable skill

1. Use the [official download/setup](https://antigravity.google/docs/getting-started)
   for your OS and chosen App/CLI/editor surface.
2. Sign in with a permitted personal or business account. The original source
   deck's enterprise-only sign-in route is not mandatory here.
3. Open your demo build copy as its own workspace and review its trust/permissions.
4. Inspect [.agents/skills/devfest-agent-builder/SKILL.md](./demo/.agents/skills/devfest-agent-builder/SKILL.md).
   The description helps discovery; the body gives a reusable plan/build/verify recipe.
5. Use P9 from [prompt cards](./PROMPTS.md). Antigravity App supports
   `/devfest-agent-builder`; other surfaces may differ. Review the plan before edits.

The skill does not authorize writes, commands, connectors, or publication.
Keep native approvals; do not enable blanket auto-approval.

### Connect the local MCP example

This uses the locked MCP SDK and needs no additional service account or Gemini key.

1. Review [mcp.ts](./demo/src/mcp.ts): two static read-only tools, no file,
   external-network, credential, or game-state access.
2. Run `npm run test:mcp` to verify actual stdio startup, discovery, and tool calls.
3. Open [mcp_config.example.json](./demo/mcp_config.example.json).
   Replace `C:\\REPLACE_WITH_YOUR_DEMO_FOLDER\\src\\mcp.ts` with your real
   **absolute path**, keeping JSON backslashes escaped. Node 24+ must be on PATH;
   otherwise use the absolute path to your permitted Node executable.
4. In Antigravity App, use **Customizations -> Installed -> MCP Servers** and
   **Copy Config File Path** to locate the real host configuration.
   Follow the [official MCP guide](https://antigravity.google/docs/mcp) for your surface.
5. Merge only the example server entry into the existing `mcpServers` map.
   Preserve other entries. The example file is not automatically activated.
   Review any native trust/permission prompts before connecting.
6. Inspect the discovered `get_workshop_overview` and `get_agent_build_checklist`
   tools. Use P10 to call the checklist and inspect the actual result.
7. Disable/remove your example entry when no longer needed, preserving other servers.

The host launches this server over **stdio**; it is not the browser game or a
standalone HTTP endpoint. Running `node src/mcp.ts` directly waits for protocol input.
Read-only annotations are descriptions, not proof; inspect implementation and scope.
**MCP tools connected to Antigravity are not automatically tools of the ADK host.**
The MCP CLI smoke test does not prove a successful connection in your editor.

### Enable real ADK chat privately

Stop only your own offline server. In a terminal that is **not screen-shared**:

```powershell
$secureKey = Read-Host 'Gemini API key (hidden)' -AsSecureString
$env:GEMINI_API_KEY = [System.Net.NetworkCredential]::new('', $secureKey).Password
$env:GEMINI_MODEL = 'gemini-flash-latest' # or a function-calling model available to your key
npm run preflight
npm run dev:live
```

The key is kept server-side, never placed in the browser. Set it again in another
terminal if starting a separate process. Preflight checks versions and key presence,
**not** entitlement, quota, connectivity, or model quality.
No free access or successful live request is guaranteed.

Try these in the game-host panel:

```text
Show my current quest and progress. Do not answer it for me.
Give me a hint for QUEST-1. I accept the 25-point cost.
For QUEST-1, my choice is B. Check my answer.
Propose my earned badge. Do not publish it.
```

The last request works only after all three quests are complete.
Only **ADK runtime** trace entries are model-selected calls. Quiz buttons use
**Local deterministic handler** entries. Human publication has its own label.
Private model thought parts are not displayed.

Clear your key after stopping your own server:

```powershell
Remove-Item Env:GEMINI_API_KEY
```

Use environment variables rather than putting keys in code, source ZIPs, prompts,
screenshots, or `.env` files that might be shared.

## Optional agent-building follow-up

Use P9/P10 to review the host's goal, instructions, and capability boundary.
Use P11 for a small approved coach-persona edit in a build copy. Inspect the actual
`LlmAgent` construction and typed checker, then run the focused build/tool tests.
Rehearse live grounding, hint consent, and error handling separately; wording is
model-dependent, but invented scores/publication are not acceptable.

## Optional take-home exercise: test-first scoring

Use [prompt cards](./PROMPTS.md) P1-P5 and your own build copy.
The completed reference uses [scoring.ts](./demo/src/scoring.ts);
the separate [exercise.ts](./demo/src/exercise.ts) is deliberately unfinished.

1. Run `npm run test:exercise`: **three intentional RED failures**.
2. Implement `scoreAnswer(correct, usedHint)`:
   - correct, no hint -> 100;
   - correct, with hint -> 75;
   - wrong, either hint state -> 0.
3. Run `npm run test:exercise` again: all three should pass.
4. Wire the learner scorer by changing only the import in the build-copy
   [store.ts](./demo/src/store.ts) from `./scoring.ts` to `./exercise.ts`.
5. Run `npm run build` and `node --test src/store.test.ts`, then `npm run check`
   before using the changed copy live.

Do not weaken assertions or expose arbitrary-score/publication tools.
The [solution](./demo/src/exercise.solution.ts) reuses the reference scorer.
For a solution-only rehearsal without changing the stub:

```powershell
$env:SCORING_SOLUTION = '1'
npm run test:exercise
Remove-Item Env:SCORING_SOLUTION
```

Optional next extension: add a read-only progress-summary tool using the
existing snapshot. Test a zero-progress game and a completed game.
Keep human publication out of the model's tool list.

## Reset, offline walkthrough, and terminal approval

```powershell
npm run state
npm run reset     # type reset; resets only this local game
npm run offline   # starts from fresh progress; solves a scripted route with one hint
```

The scripted offline route produces **275 points**, a pending badge, and
**badgePublished:false**. It is not model reasoning.
To approve its actual proposal in a separate terminal:

```powershell
npm run approve -- BADGE-<actual-id>
```

Read the proposal, type the exact requested confirmation, and inspect state again.
Re-approving fails. Restart the live host after resetting to clear conversation history.

## Troubleshooting and boundaries

| Problem | Action |
| --- | --- |
| Installation/engine failure | Use the specified Node/npm versions and matching lockfile. No ADK devtools/SQLite installation is needed. |
| Scoring exercise fails | Expected until implemented; `npm run check` validates the completed reference separately. |
| Chat is disabled | You started offline mode. Set a key privately and restart your own server with `dev:live`. |
| Skill not discovered | Open the demo build copy as the workspace and check its `.agents/skills` folder and your surface's invocation support. |
| MCP cannot start | Replace the absolute source path, check Node 24+ on the host PATH, run `test:mcp`, and inspect host errors. Never invent a connection result. |
| Missing/invalid key, model or quota | Surface the error; check your own permitted account. No automatic fallback or quota bypass. |
| Error after a live request | Refresh actual progress before retrying; tools may have run before the error. |
| Port already occupied | Stop only your own server, or choose a free port with `$env:PORT='18768'` and use that exact 127.0.0.1 URL. |
| Forbidden Host/Origin | Use `127.0.0.1`, not `localhost`, a tunnel, or a remote hostname. |
| Proposal missing or stale | Use the same demo folder/state. Read progress and request a fresh proposal if appropriate. |
| Corrupt state | Error is explicit; inspect your file or use the confirmed local reset. |

This is a single-user local workshop game, not authenticated production hosting,
an anti-cheat system, a durable conversation service, or a concurrent database.
Do not expose it publicly. Upstream dependency advisories and live-model
verification limits remain in [validation notes](./VALIDATION.md).
