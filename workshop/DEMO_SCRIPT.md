# Current demo: Name Race workshop quiz

The one-hour journey stays: vibe coding -> tools -> setup -> Skills -> MCP ->
building an agent. Use 40 minutes for the presentation, 14 for this demo,
four for Q&A, and two for transitions. No ADK or participant installation is required.

- [Live host](https://name-race-e9a2-261121.azurewebsites.net)
- [Public game repo](https://github.com/sajeetharan/name-race-agent-workshop)
- [Full read-aloud script](https://github.com/sajeetharan/name-race-agent-workshop/blob/main/DEMO_SCRIPT.md)
- [Numbered build guide and prompts](https://github.com/sajeetharan/name-race-agent-workshop/blob/main/BUILD_GUIDE.md)

## Prepare privately

Log in with the app's private HOST_PASSWORD before sharing your screen.
Create a fresh room shortly before the session; its lifetime is two hours.
Share only the QR code or public join link. Up to 120 participants enter
nicknames and receive differently colored cars. Do not use private information.

For local rehearsal:

```powershell
git clone https://github.com/sajeetharan/name-race-agent-workshop.git
Set-Location .\name-race-agent-workshop
npm ci
npm run check
npm run dev
```

Open http://127.0.0.1:18769. The local no-password host is loopback-only;
do not expose that configuration through a tunnel.

## Fourteen-minute read-aloud demo

**0-2 / Invite**

"Scan this code and choose a nickname. Your answers move your colored car.
There are five questions from today's workshop. This is not a random race."

Review the entries and type START.

**2-4 / Vibe coding**

"What is a good first step when building with AI? Explain the goal and review a
plan. Choose one answer on your phone. Once saved, it cannot change."

Wait for answers. Type CLOSE and show the correct answer and car progress.
Show a Skill as a recipe for reading, planning, changing and testing.

**4-6 / Antigravity**

Type NEXT.

"Antigravity helps build and review code. It does not make every answer true.
People still review the changes and run tests."

Wait and type CLOSE. Show a small reviewed edit and `npm run check`.

**6-8 / Skills**

Type NEXT.

"A Skill is a reusable recipe for a task. It is not a password or permission
to do anything. It guides a small, safe change."

Wait and type CLOSE. Show the real Skill file.

**8-10 / MCP**

Type NEXT.

"MCP connects apps and AI to real tools and data. Registration and answers use
real MCP calls. Here is the request and actual result. Private keys are omitted."

Show `submit_answer`, `read_room` and `host_control`. Explain that the coding
guide is a separate read-only connection. Wait and type CLOSE.

**10-12 / Human control**

Type NEXT.

"Only the host approves starting, closing, reopening or deleting the room.
Participants submit their own answers. The optional AI cannot grade or control it."

Wait and type CLOSE. Closing question five announces the named top-three podium.

**12-14 / Podium and agent recap**

"Each correct answer gives 100 points and moves the car 20% forward. Most correct
answers rank first. If scores match, faster correct answers break ties.
The server records time, including network and polling delay. Exact score/time
ties share a rank. Let us congratulate our top racers!"

Read the podium names. Show the scores and times.

"The coding agent helps build this app. The optional game agent reads anonymous
racer labels and chooses a small commentary style. It never receives nicknames.
Code supplies the facts."

If your live model was not rehearsed, say: "AI is off today. The MCP calls are real,
but they are not model reasoning." RESET keeps names and clears scores;
DELETE removes the room after the session.

Keep four minutes for Q&A. The slides, photo, notes, and animations remain
unchanged. Their ADK/Quest demo is a previous reference; use the current browser
and script. [Guess the Number](https://github.com/sajeetharan/guess-number-agent-workshop)
remains available as the previous single-player demo.
