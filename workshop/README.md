# Beyond AI-Assisted Coding: Understanding and Building AI Agents

## Road to DevFest Nepal 2026 | Online Workshop Series #1

- **Host:** GDG Kathmandu
- **Speaker:** Sajeetharan Sinnathurai, Principal Product Manager, Microsoft (Azure Cosmos DB)
- **Date:** Saturday, 21 November 2026
- **Time:** **7:30-8:30 PM Nepal Time (NPT, UTC+05:45)**
- **Venue:** Google Meet; use the organizer's meeting link
- **Audience:** mixed beginners and developers
- **Format:** **60-minute presentation + presenter-led demo**, with participants joining by QR code
- **Current demo stack:** Antigravity + TypeScript + real MCP tools + optional Gemini agent; no ADK required

The presenter confirmed the shorter slot and game scenario. This supersedes
the poster's original two-hour slot and the earlier ticket-based walkthrough.
Participants do not need to install tools during the live session.

## Learning journey

**Vibe coding -> Antigravity and other tools -> setup -> Skills -> MCP ->
building an application agent.**

The opening adapts the supplied Build with AI Handbook's vibe-coding definition,
builder audience, tool entry points, and prompt anatomy. Your Antigravity deck
supplies the requirements/plan/build/verify workflow and setup concepts.
The current demo uses [Name Race](https://github.com/sajeetharan/name-race-agent-workshop)
to show a live app connected to real MCP tools and an optional bounded agent.
The standalone repo includes numbered build steps, a reusable Skill, prompts,
and an easy-English script.

## Current demo: Name Race

Participants scan a QR code and register nicknames on their phones.
Up to 120 entries answer five questions about vibe coding, Antigravity, Skills,
MCP and human control. Correct answers move differently colored cars.
The host opens and closes each question; score first and correct-answer time
second decide the final named top-three podium, not AI or random luck.
Real MCP connects registrations, answers and reviewed host actions.

Open [the live host](https://name-race-e9a2-261121.azurewebsites.net), log in
privately using the app's Azure HOST_PASSWORD setting, and create a fresh room
shortly before the session. Rooms expire two hours after creation.

Use the [current demo script](./DEMO_SCRIPT.md) and the standalone repo's
[build guide](https://github.com/sajeetharan/name-race-agent-workshop/blob/main/BUILD_GUIDE.md).
The one-hour topic order and presenter-led format stay the same.

Both **21-slide decks**, their speaker notes, and PDFs now use Name Race throughout:
the five-question rules, setup on port **18769**, `name-race-builder`, guide/runtime
MCP separation, and the bounded optional Gemini commentator. Layouts, the cover
photo, official tool links, and existing animation timelines are preserved.
The current source is the standalone repo, not the historical `workshop/demo` folder.
The cover includes the clickable speaker website: https://sajeetharan.dev/.

### Current fast start

Use **Node 24.13+ / npm 11+**:

```powershell
git clone https://github.com/sajeetharan/name-race-agent-workshop.git
Set-Location .\name-race-agent-workshop
npm ci
npm run check
npm run dev
```

Open **http://127.0.0.1:18769**. Real runtime MCP works without a model key.
Optional commentary uses a privately configured `GEMINI_API_KEY` and the same
startup command; there is no `dev:live` or ADK setup for Name Race.

[Guess the Number](https://github.com/sajeetharan/guess-number-agent-workshop)
remains available as the previous single-player demo.

## Previous reference demo: DevFest Quest

A small DevFest-themed adventure game with three quests:

1. **The Builder Bridge:** distinguish Antigravity from the runtime agent.
2. **The Tool Temple:** choose a narrow, deterministic answer-checking tool.
3. **The Badge Vault:** recognize untrusted game content and the human approval boundary.

Correct answers earn **100 points**, or **75 after a hint**; wrong answers earn
zero. Hints cost once per quest, and repeated correct answers cannot score twice.
The **ADK game host** reads quests, offers hints, checks player-provided answers,
and proposes an earned badge. **Application code** computes points.
Only the **player's separate confirmation flow** can publish the badge locally.

There is no login, multiplayer, external scoreboard, official certificate, or
deployment. The audience plays by voting A/B/C while the presenter operates
one local game. The original repository's mobile/Google Play lab stays separate.

## Resources

| Resource | Use |
| --- | --- |
| [Current demo script](./DEMO_SCRIPT.md) | Easy-English Name Race walkthrough and 14-minute demo plan |
| [Standalone game repo](https://github.com/sajeetharan/name-race-agent-workshop) | Current runnable demo, build steps, Skill, MCP tools, agent, and tests |
| [Animated presentation](./Beyond_AI_Assisted_Coding_Animated.pptx) | Presenter-controlled reveals on all 21 slides, including Outcome; preserves saved edits, cover photo, and read-aloud notes |
| [Static handout](./Beyond_AI_Assisted_Coding_Animated.pdf) | Current polished slides with all content visible and no motion |
| [Saved source](./Beyond_AI_Assisted_Coding.pptx) | Your editable, unanimated source presentation, with tool links |
| [Source PDF](./Beyond_AI_Assisted_Coding.pdf) | Current unanimated slides, including your cover photo and tool links |
| [Facilitator guide](./FACILITATOR_GUIDE.md) | Current Name Race run-of-show, with the old Quest instructions labeled historical |
| [Participant guide](./PARTICIPANT_GUIDE.md) | Watch-along checklist and optional post-session setup/exercises |
| [Prompt cards](./PROMPTS.md) | Current Name Race brief, Skill, guide MCP, bounded edit, and verification prompts |
| [Source map](./SOURCES.md) | Supplied material, visual adaptation, SDK and hosting decisions |
| [Validation](./VALIDATION.md) | Completed checks, dependency advisories, and live-model caveats |
| [Historical demo](./demo/) | Previous Quest browser game and ADK host; not the current quiz source |
| [Historical workspace skill](./demo/.agents/skills/devfest-agent-builder/SKILL.md) | Quest agent-building workflow; current Skill is `name-race-builder` in the standalone repo |
| [Historical MCP server](./demo/src/mcp.ts) | Quest's two read-only development-context tools; not Name Race runtime MCP |
| [Historical MCP configuration](./demo/mcp_config.example.json) | Quest configuration only; use the standalone Name Race example for this session |
| [Optional RED exercise](./demo/src/exercise.ts) | Small scoring function for the take-home lab |
| [Solution](./demo/src/exercise.solution.ts) | Reuses the tested production scorer |
| [Animation finishing pass](./animate_slides.ps1) | Animate a separate copy of the saved presentation using Windows PowerPoint |
| [PDF/preview exporter](./export_slides.ps1) | Render both current decks from private copies; leave user-open presentations untouched |
| [Content updater](./update_demo_slides.py) | Update both saved decks while preserving artwork, geometry, and timelines |
| [Historical slide generator](./build_slides.py) | Writes a separate legacy Quest deck, never overwrites the current decks |

## One-hour agenda

| NPT clock | Elapsed | Minutes | Segment | Slides |
| --- | --- | ---: | --- | --- |
| 19:30-19:40 | 00-10 | 10 | Welcome, Outcome, vibe coding, useful prompts, verification | 1-5 |
| 19:40-19:48 | 10-18 | 8 | Tool landscape and Antigravity workflow | 6-8 |
| 19:48-19:54 | 18-24 | 6 | Project setup, credentials, and permissions | 9-11 |
| 19:54-20:00 | 24-30 | 6 | Skills: recipe, discovery, and invocation | 12-13 |
| 20:00-20:06 | 30-36 | 6 | Guide/runtime MCP and reviewed configuration | 14-15 |
| 20:06-20:10 | 36-40 | 4 | Bounded optional Gemini loop and real traces | 16-18 |
| 20:10-20:12 | 40-42 | 2 | Switch to live app; share room QR | 19 |
| 20:12-20:26 | 42-56 | 14 | Five-question Name Race and named podium | 19-20 |
| 20:26-20:30 | 56-60 | 4 | Q&A and resources | 21 |

## Previous reference fast start

Use **Node.js >=24.13.0** and **npm >=11.8.0**. From the repository root:

```powershell
Set-Location .\workshop\demo
npm ci
npm run check
npm run dev
```

Open **http://127.0.0.1:18767**. This starts the **explicitly labeled offline
game**, with deterministic tools and disabled model chat. It is not simulated
AI reasoning. The game works without a key or third-party browser assets.

For real ADK hosting, stop your own server and privately set `GEMINI_API_KEY`
and optionally `GEMINI_MODEL`, then run:

```powershell
npm run preflight
npm run dev:live
```

See [safe credential setup](./PARTICIPANT_GUIDE.md). Live failures remain errors;
there is **no automatic offline fallback**. The browser and terminal show actual
calls/results with a source label: ADK runtime, local handler, or human confirmation.
Private model thought parts are filtered.

The server binds **only to 127.0.0.1**, accepts the exact local Host/Origin,
limits JSON requests to 8 KB, and does not serve source files or API keys.
This is still a single-user local demo, **not an authenticated production service**.
Do not expose it through a tunnel or public host.

### Other commands

```powershell
npm run test:mcp                      # real stdio discovery and two read-only calls
npm run state
npm run agent                         # live terminal host, same local game state
npm run offline                       # fresh-state deterministic walkthrough: 275 points
npm run approve -- BADGE-<actual-id>   # separate human terminal confirmation
npm run reset                         # requires typing reset; local game only
npm run test:exercise                 # three intentional RED failures until implemented
```

The reference game uses the completed [scorer](./demo/src/scoring.ts), not the
unfinished exercise. Keep the reference intact and edit a copy for the build demo.
The two moderate upstream dependency advisories remain documented in
[validation notes](./VALIDATION.md). No live Gemini request was made during preparation.

### Skills and MCP setup

Use the bundled [skill](./demo/.agents/skills/devfest-agent-builder/SKILL.md) in
the demo build copy. It describes a workflow, not new permissions.
The [MCP example](./demo/mcp_config.example.json) is intentionally **not an
active host configuration**. Review the [local server](./demo/src/mcp.ts),
replace the placeholder with your real absolute path, and merge only its entry
through your host's supported settings. Preserve existing entries and native approvals.
Node 24+ must be available on the host's PATH.

The MCP server supplies a static outline/checklist over stdio; it cannot read files,
call external services, change game state, or publish. It is connected to the coding
environment, **not** automatically to the ADK host. See
[participant setup](./PARTICIPANT_GUIDE.md) and [presenter walkthrough](./FACILITATOR_GUIDE.md).

## Distribution and regeneration

Share the workshop repository and separate Name Race repository.
Name Race's source, lockfile, Skill, and deployment guide live in its own repo.
No dependency folders, local progress, credentials, or compiled output belong in git.

### Presenting the polished deck

Open the **animated presentation** in desktop PowerPoint and start Slide Show
with **F5**. Titles/photo fade in; advance with a click, Space, or Right Arrow to
reveal each logical card. There are only **one to three reveal clicks per slide**,
with short Fade/Wipe effects and coordinated fade transitions. Slides never
advance automatically. The six-chapter ribbon tracks the journey; numbered
cards and short audience questions support chat participation. The closing QR
stays static and scannable.

On the tools slide (slide 6), AI Studio, Stitch, and Antigravity have clickable
web addresses in their cards. GitHub Copilot, Cursor, and Claude Code have
linked names in the subtitle. These links work in the exported PDFs too; click
outside linked text when you only want to advance a reveal.

Demo-related speaker notes now explain Name Race in plain English.
Your saved layout, cover photo, slide numbering, and timelines are preserved.
For no-motion delivery, use the current
static handout, or enable PowerPoint's **Set Up Slide Show > Show without animation**.

To reapply the same finishing pass after editing the unanimated saved original,
close the source and output presentations first, then run on Windows with PowerPoint:

```powershell
.\workshop\animate_slides.ps1
```

This writes the separate animated PPTX, not the original. It expects the current
21-slide card layout and rejects an already animated input. Export a fresh PDF
from the output afterward. If you edit the animated copy directly, keep those
edits there; rerunning the finishing pass replaces that output from the source.

### Updating saved content

Close both decks in PowerPoint before running:

```powershell
python .\workshop\update_demo_slides.py
```

The updater changes text, notes, and the demo-source hyperlink in both saved
decks. It verifies slide count, preserved object IDs/geometry, photos, and
timelines before replacing each file. Export both PDFs again with PowerPoint.
It requires the existing `python-pptx` and Pillow slide-tool dependencies.

For native text-fit checks, fresh PDFs, and PNG rehearsal previews on Windows:

```powershell
.\workshop\export_slides.ps1 -ScratchDirectory "$env:TEMP\name-race-slide-preview"
```

The exporter renders private copies and does not close other open presentations.

### Rebuilding the historical authored deck

The Python generator writes **DevFest_Quest_Legacy.pptx**. It does not update
the current decks or include your manual edits, Outcome slide, or cover photo.
Use it only for the historical Quest version.

```powershell
python -m pip install python-pptx qrcode
python .\workshop\build_slides.py
```

Run from the repository root. The deck retains the handbook's **720 x 405 point
16:9 format**, rounded outlined/shadowed panels, gradient labels/phase slides,
and black/green Antigravity styling. Text, code, gradients, and shapes are editable.
The **first slide has no QR code or handbook shortlink**; the closing slide retains
the handbook resource link/QR.

Google Sans is specified but not bundled. PowerPoint substitutes local fonts
where necessary; use the PDF for the verified appearance. Measurement uses
Arial on Windows and Arial/DejaVu elsewhere. Export a fresh PDF with PowerPoint
after regeneration.
