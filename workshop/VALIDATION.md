# Workshop validation

## Current Name Race content

On 21 November 2026, the standalone Name Race source at **fdbbc14** passed
`npm run check`: strict TypeScript build, **all ten tests**, and frontend
JavaScript syntax. This run covered the actual MCP-backed tests; it did not
call live Gemini, connect Antigravity, or redeploy the app.

Both saved 21-slide decks are updated from that source. The content updater
checks that there are no obsolete Quest tool/port/badge references in slide
text or speaker notes; explicit "No ADK" dependency statements are allowed.
It also verifies preserved object IDs/geometry, photos, and animation timelines.
The guide configuration is valid JSON and keeps `--guide`.

Both updated decks reopened in desktop PowerPoint and exported to **21-page
PDFs**. All text passed native width/height checks. Setup, guide MCP,
commentator, and quiz/podium previews were visually inspected. PDF checks
confirm the new demo terms, absence of old Quest identifiers/port, and working
Name Race/workshop repository hyperlinks. Existing animation timelines were
preserved byte-for-byte; interactive slideshow playback remains a rehearsal check.

Reapplying the updater on private copies produced byte-identical decks.
The preserved Quest reference also passed its own strict build and all
13 tests before publication; those tests do not validate Name Race.

The current rules are five questions, 120 entries, 100 points and 20% car
progress per correct answer, score/time ranking, named top-three podium, and
host-controlled START/CLOSE/NEXT/RESET/DELETE. Model access is limited to
anonymous `read_race_summary`; code validates phase/style and supplies facts.

See [Name Race validation](https://github.com/sajeetharan/name-race-agent-workshop/blob/main/VALIDATION.md)
for the separate browser/deployment rehearsals and operational limits.
Actual PowerPoint slideshow playback, IDE Skill/guide discovery, and live
Gemini key/model/quota/connectivity still require presenter rehearsal.

---

## Historical Quest/slides checks

The current demo is now [Name Race](https://github.com/sajeetharan/name-race-agent-workshop).
Its separate [validation notes](https://github.com/sajeetharan/name-race-agent-workshop/blob/main/VALIDATION.md)
cover the new MCP/Gemini implementation. The checks below belong to the preserved
Quest/slides reference, not the new game's rules. See the [current demo script](./DEMO_SCRIPT.md).

Validated locally for the **60-minute, 19:30-20:30 NPT**
presenter-led workshop, revised to **vibe coding -> tools -> setup -> Skills ->
MCP -> building an ADK agent**.

## Completed checks

- **Strict TypeScript build:** `npm run build` passes.
- **Source bundle:** all **46** current entries were byte-verified against the
  workspace. Before the presentation-only finishing pass, an extracted
  42-entry copy restored with `npm ci --ignore-scripts` and passed
  `npm run check` plus the frontend syntax check on Node 24.13.0. The HTTP
  game/confirmation flow and actual stdio MCP startup/discovery/calls passed.
  Browser checks below were performed on the unchanged game before this narrative revision.
- **Reference tests:** all **13** pass on Node **24.13.0**: the existing twelve
  game/ADK/HTTP cases plus one actual MCP protocol case. Focused server tests
  also pass after checking the exact **8192-byte accepted / 8193-byte rejected**
  request-body boundary.
- **Scoring and persistence:** wrong answer = zero, hint charged once, correct
  after hint = 75, unhinted correct = 100, repeat scoring rejected, future quests
  locked, and the three-quest one-hint route totals **275**.
- **Badge boundary:** proposal does not publish; premature/invented-score requests
  fail; invalid confirmation, repeat approval, and stale versions are rejected.
  Browser and actual separate terminal confirmation publish the computed badge locally.
- **ADK integration:** a real `InMemoryRunner` executes a registered badge
  `FunctionTool` using a scripted network-free test model. The actual call/result
  loop returns `applied:false`; private thought-marked parts are filtered.
  This test is not a live Gemini request.
- **MCP example:** the actual stdio client starts the server, discovers exactly
  `get_workshop_overview` and `get_agent_build_checklist`, and calls both.
  Results contain the ordered 60-minute outline and bounded ADK-building checklist.
  Handlers return static data only; no game-state, file, credential, or network access.
  These development-context tools are not registered on the ADK game host.
- **Skill/config resources:** the workspace skill and placeholder MCP example are
  bundled. Documentation explains discovery, replacing the absolute path, merging
  without overwriting existing host settings, and respecting native approvals.
- **Browser walkthrough:** played the three quests, checked a wrong answer,
  used a hint, reached 275 points, inspected pending review, blocked an incorrect
  confirmation, confirmed publication, and verified persistence after refresh.
  The earned badge is visible. Next-quest/badge keyboard focus, Escape/cancel,
  and focus restoration after publication were checked.
- **Responsive UI:** no horizontal overflow at **375, 768, 1024, or 1440 px**.
  Reduced-motion mode, native labeled controls, and visible focus are supported.
  Frontend JavaScript syntax check passes.
- **Local HTTP:** listener is IPv4 loopback-only; foreign origins and source-file
  requests are rejected. Offline chat is disabled. A scripted live failure
  stays an error without switching the server to offline mode.
- **CLI / optional exercise:** real offline route and human CLI approval checked.
  The learner stub has **three intentional RED failures**; the facilitator
  solution passes the same three cases. Missing-key live startup fails explicitly.
- **Presentation:** PowerPoint renders all **21 slides** to PDF. All editable
  text is represented in the render; native/rendered bounds and local documentation
  links are checked. Each slide has a plain-language read-aloud script containing
  only its subject matter, without backstage cues, timing headers, or facilitator
  instructions. The facilitator guide retains the **60-minute** schedule;
  the presenter's subsequent manual slide edits are preserved.
  The exact requested topic order, valid rendered MCP JSON example, and event slot
  **19:30-20:30 Nepal Time** were checked. The final rendered contact sheet and
  Skills, MCP, and agent-construction layouts were inspected.
- **Handbook alignment:** 720 x 405 point page size, outlined rounded/shadowed
  panels, gradient phases/pills, black/green runtime styling, and editable code.
  The first slide has **no QR code or handbook shortlink**; the closing QR
  matrix matches the encoded public handbook URL. Cover, contact sheet, code,
  approval, and closing layouts were inspected.
  Google Sans is specified but not installed here; PowerPoint's local substitution
  is used in the verified PDF, as explained in [source notes](./SOURCES.md).
- **Animated finishing pass:** the separate
  [animated presentation](./Beyond_AI_Assisted_Coding_Animated.pptx) preserves all
  **535 original objects**, their positions/hyperlinks and text except updated
  slide counters, all 20 exact original speaker scripts, and the original cover
  photo bytes/crop. The saved source was not regenerated from the old generator.
  All 21 slides have coordinated Fade/Wipe builds:
  **329 effects organized into 51 reveal clicks**, only one to three per slide,
  lasting 0.3-0.5 seconds, plus 0.4-second fade transitions. No automatic slide
  advancement, looping, or per-cell QR animations. PowerPoint reopened the
  output and exported the [21-page static handout](./Beyond_AI_Assisted_Coding_Animated.pdf).
  Added text fits native PowerPoint bounds; the complete rendered contact sheet
  was inspected, including the cover photo and the retained timing footer (now slide 8).
  The new chapter ribbon, numbered cards, and audience questions do not replace
  existing content. Use the PDF or **Show without animation** for no-motion delivery.
- **Outcome insertion:** slide 2 in both decks introduces the live Name Race quiz,
  five questions, colored cars, and the named top-three podium, alongside the
  workshop learning goals. It has new natural narration; the animated version
  adds 29 coordinated effects in two reveal clicks. Package comparisons verify
  that all 20 original slides are byte-identical except their slide counters;
  existing notes, media, hyperlink relationships, and timelines are byte-identical.
  Both decks reopened in PowerPoint. New text passed native text-fit checks, both
  slide previews were inspected, and both refreshed PDFs have 21 pages with the
  expected Outcome text and all six official tool hyperlink targets.
  The updated animation finishing script also completed on a separate 21-slide
  scratch copy; that regenerated copy did not replace the preserved animated deck.
- **Tool links:** slide 6 in both PPTX files links AI Studio, Stitch, Antigravity,
  GitHub Copilot, Cursor, and Claude Code to their verified official sites.
  The three main cards also display their addresses. In the earlier tool-link
  update, only the original tools slide XML and its hyperlink relationships
  changed; all other package parts, including notes,
  photos, and animation timelines, remain byte-identical to the saved decks
  before this addition. Both PDFs were refreshed in PowerPoint, with native
  text-fit and PDF hyperlink-target checks.

## Dependency advisory caveat

The current locked dependencies still report **two moderate advisories**, with
zero high/critical advisories: the upstream Vertex AI chain includes `gaxios`
6.7.1 and `uuid` 9.0.1. The narrow same-major gaxios 7 override removes a
separate metadata dependency chain; no forced cross-major override was added.

ADK **2.5.0**, Zod **4.6.7**, telemetry API **1.9.0**, and the matching tooling
remain in the lockfile. MCP SDK **1.32.2** is now an explicit dependency for the
local setup example. No ADK devtools/SQLite drivers or new frontend framework
dependencies were added. Review upstream fixes before production reuse.
Using the Gemini API path and fictional data is not a security exemption or
proof that all advisories are unreachable.

## Still requires presenter rehearsal

Rehearse the animated deck in desktop PowerPoint Slide Show mode on the actual
presentation display and meeting share. Timeline checks and PDF rendering
verify the file, but are not an interactive slideshow-playback test.

**No live Gemini API call was made.** Rehearse your own permitted key/model,
quota, and connectivity privately before the event. Check that the host reads
actual progress, respects player choices/hint consent, explains tool failures,
and never invents scores or publication.

Antigravity installation/sign-in, workspace skill invocation, and connection in
the presenter's actual MCP host UI also need rehearsal. No host settings or
accounts were changed during preparation. The successful protocol smoke test
does not claim that your editor is connected.

This is a **fictional, single-user local game**, not authenticated hosting,
an anti-cheat system, an official certificate, a durable conversation service,
or a concurrent transactional database. The human UI path is absent from the
model's tool list; it does not establish production identity or prove that an
HTTP caller is human. Do not expose this server through a tunnel or public host.

## Reproduce

From [demo](./demo/) with the matching Node/npm versions:

```powershell
npm ci
npm run check
npm run dev
```

Open **http://127.0.0.1:18767** for the labeled deterministic game.
The optional `npm run test:exercise` intentionally fails until implemented.
See [the facilitator guide](./FACILITATOR_GUIDE.md) for one-hour timing and
[the participant guide](./PARTICIPANT_GUIDE.md) for private live-key setup.
