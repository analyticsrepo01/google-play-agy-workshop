"""Build the historical Quest deck, not the current Name Race presentation.

Dependencies: python-pptx, qrcode. Use update_demo_slides.py for the saved decks.
"""

from datetime import datetime, timedelta
from pathlib import Path
import os

import qrcode
from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.oxml.ns import qn
from pptx.util import Pt


ROOT = Path(__file__).parent
OUTPUT = ROOT / "DevFest_Quest_Legacy.pptx"
COUNT = 20
NAVY = "20344B"
BLUE = "4285F4"
GREEN = "34A853"
RED = "EA4335"
YELLOW = "FBBC04"
MUTED = "475569"
WHITE = "FFFFFF"
LINE = "D9E2EF"
BLACK = "000000"
MINT = "00FF94"
BODY = "2F4C6F"
FONT = "Google Sans"
GRADIENTS = {
    BLUE: ("1665E8", "58A6FF"),
    GREEN: ("009D62", "65CCD9"),
    RED: ("E94252", "FA85BE"),
}
prs = Presentation()
prs.slide_width = Pt(960)
prs.slide_height = Pt(540)
elapsed = 0
checks = []


def font_path(code=False, bold=False):
    if os.name == "nt":
        return Path(r"C:\Windows\Fonts") / (
            "consola.ttf" if code else "arialbd.ttf" if bold else "arial.ttf"
        )
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf") if code else
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") if bold else
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf") if bold else
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise RuntimeError("Install Arial/DejaVu fonts or adjust font_path() for this machine.")


def measure(value, size, bold=False, code=False):
    font = ImageFont.truetype(str(font_path(code, bold)), round(size * 4))
    return font.getlength(value) / 4


def rect(slide, x, y, w, h, fill, line=None, rounded=False):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Pt(x), Pt(y), Pt(w), Pt(h),
    )
    if rounded:
        shape.adjustments[0] = 0.12
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(fill)
    if line:
        shape.line.color.rgb = RGBColor.from_string(line)
        shape.line.width = Pt(1.1)
    else:
        shape.line.fill.background()
    shape._element.spPr.append(OxmlElement("a:effectLst"))
    return shape


def gradient(shape, colors):
    shape.fill.background()
    fill = OxmlElement("a:gradFill")
    fill.set("rotWithShape", "1")
    stops = OxmlElement("a:gsLst")
    for i, color in enumerate(colors):
        stop = OxmlElement("a:gs")
        stop.set("pos", str(round(i * 100000 / (len(colors) - 1))))
        rgb = OxmlElement("a:srgbClr")
        rgb.set("val", color)
        stop.append(rgb)
        stops.append(stop)
    fill.append(stops)
    direction = OxmlElement("a:lin")
    direction.set("ang", "0")
    direction.set("scaled", "1")
    fill.append(direction)
    shape._element.spPr.remove(shape._element.spPr.find(qn("a:noFill")))
    shape._element.spPr.insert(2, fill)


def panel(slide, x, y, w, h, fill=WHITE, line=NAVY, shadow=True):
    if shadow:
        rect(slide, x + 5, y + 6, w, h, NAVY, rounded=True)
    return rect(slide, x, y, w, h, fill, line, rounded=True)


def is_dark(slide):
    return slide.background.fill.fore_color.rgb == RGBColor.from_string(BLACK)


def pill(slide, label, x, y, w, h, accent=BLUE, dark=False):
    shape = rect(slide, x, y, w, h, BLACK if dark else accent,
                 MINT if dark else None, rounded=True)
    shape.adjustments[0] = 0.5
    if not dark:
        gradient(shape, GRADIENTS[accent])
    return text(slide, label, x + 10, y + 4, w - 20, h - 8,
                16, WHITE, True, minimum=12, align=PP_ALIGN.CENTER)


def handbook_qr(slide, x, y, size):
    code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4)
    code.add_data("https://g.dev/ai/build")
    code.make(fit=True)
    matrix = code.get_matrix()
    cell = size / len(matrix)
    rect(slide, x, y, size, size, WHITE)
    for row, modules in enumerate(matrix):
        start = None
        for column in range(len(modules) + 1):
            filled = column < len(modules) and modules[column]
            if filled and start is None:
                start = column
            elif not filled and start is not None:
                rect(slide, x + start * cell, y + row * cell,
                     (column - start) * cell, cell, BLACK)
                start = None


def lines_for(value, width, size, bold=False, code=False):
    if code:
        return value.split("\n")
    lines = []
    for paragraph in value.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}".strip()
            if line and measure(candidate, size, bold) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines


def text(slide, value, x, y, w, h, size=17, color=NAVY, bold=False, code=False,
         minimum=12, align=PP_ALIGN.LEFT):
    selected = size
    while selected >= minimum:
        lines = lines_for(value, w - 2, selected, bold, code)
        if len(lines) * selected * 1.22 <= h - 2 and all(
            measure(line, selected, bold, code) <= w - 2 for line in lines
        ):
            break
        selected -= 0.5
    if selected < minimum:
        raise ValueError(f"Slide {len(prs.slides)} text does not fit: {value[:80]}")
    shape = slide.shapes.add_textbox(Pt(x), Pt(y), Pt(w), Pt(h))
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = False
    frame.margin_top = frame.margin_bottom = frame.margin_left = frame.margin_right = Pt(0)
    for index, line in enumerate(lines):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.font.name = "Consolas" if code else FONT
        paragraph.font.size = Pt(selected)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = RGBColor.from_string(color)
        paragraph.line_spacing = Pt(selected * 1.22)
        paragraph.space_before = paragraph.space_after = Pt(0)
        paragraph.alignment = align
    checks.append((len(prs.slides), x, y, w, h, selected))
    return shape


def card(slide, heading, body, x, y, w, h, size=17, accent=BLUE):
    dark = is_dark(slide)
    panel(slide, x, y, w, h, BLACK if dark else WHITE,
          MINT if dark else NAVY, shadow=not dark)
    pill(slide, heading, x + 12, y + 15, w - 24, 45, accent, dark)
    text(slide, body, x + 19, y + 77, w - 38, h - 96, size, WHITE if dark else BODY)


def footer(slide, start, duration, inverted=False):
    clock = datetime(2026, 11, 21, 19, 30) + timedelta(minutes=start)
    end = clock + timedelta(minutes=duration)
    color = WHITE if inverted else MUTED
    if len(prs.slides) in (1, COUNT):
        gradient(rect(slide, 0, 534, 960, 6, BLUE), (BLUE, GREEN, YELLOW, RED))
    elif not inverted:
        rect(slide, 44, 505, 874, 0.7, LINE)
    text(slide, "GDG Kathmandu | Road to DevFest Nepal 2026", 44, 514, 435, 15, 10, color, minimum=10)
    text(slide, f"{clock:%H:%M}-{end:%H:%M} NPT | {start:03d}-{start+duration:03d} min",
         500, 514, 357, 15, 10, color, minimum=10)
    text(slide, f"{len(prs.slides):02d} / {COUNT}", 866, 514, 55, 15, 10, color, minimum=10)


def new(section, title, subtitle, duration, notes):
    global elapsed
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    dark = section in ("Antigravity overview", "Antigravity walkthrough", "Live walkthrough")
    phases = {"Think first": ("Think", BLUE), "Implement": ("Build", GREEN),
              "Permission boundary": ("Verify", RED)}
    phase = phases.get(section)
    slide.background.fill.fore_color.rgb = RGBColor.from_string(BLACK if dark else WHITE)
    if len(prs.slides) == 1:
        text(slide, "GDG Kathmandu | Road to DevFest Nepal 2026", 44, 35, 874, 35, 22, NAVY, True)
        panel(slide, 44, 107, 874, 387)
        pill(slide, section, 72, 131, 263, 33)
        text(slide, title, 72, 184, 565, 58, 36, NAVY, True, minimum=28)
        text(slide, subtitle, 72, 249, 565, 69, 22, BODY, minimum=17)
    elif phase:
        gradient(rect(slide, 0, 0, 960, 540, phase[1]), GRADIENTS[phase[1]])
        text(slide, section.upper(), 44, 26, 874, 22, 12, WHITE, True)
        text(slide, phase[0], 44, 61, 270, 101, 80, WHITE, True, minimum=64)
        text(slide, title, 337, 75, 581, 75, 29, WHITE, True, minimum=24)
        text(slide, subtitle, 44, 164, 874, 23, 15, WHITE, minimum=13)
    else:
        text(slide, section.upper(), 44, 26, 874, 22, 12, MINT if dark else BLUE, True)
        text(slide, title, 44, 57, 874, 76, 40, WHITE if dark else NAVY, True, minimum=28)
        text(slide, subtitle, 44, 141, 874, 37, 15, WHITE if dark else MUTED, minimum=13)
    footer(slide, elapsed, duration, dark or phase is not None)
    slide.notes_slide.notes_text_frame.text = notes
    elapsed += duration
    return slide


def split(slide, a, b, size=17):
    card(slide, a[0], a[1], 44, 190, 428, 302, size)
    card(slide, b[0], b[1], 490, 190, 428, 302, size, GREEN)


def three(slide, items, size=17):
    for i, (head, body) in enumerate(items):
        card(slide, head, body, 44 + i * 297, 190, 280, 302, size, [BLUE, GREEN, RED][i])


def code_slide(slide, code, aside, size=15):
    panel(slide, 44, 190, 574, 302, "071B13" if is_dark(slide) else NAVY,
          MINT if is_dark(slide) else NAVY, shadow=not is_dark(slide))
    for i, color in enumerate((RED, YELLOW, GREEN)):
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, Pt(62 + i * 17), Pt(201), Pt(8), Pt(8))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor.from_string(color)
        shape.line.fill.background()
    text(slide, code, 62, 224, 538, 251, size, WHITE, code=True, minimum=12)
    card(slide, "What to notice", aside, 636, 190, 282, 302, 16, GREEN)


s = new("Online Workshop Series #1", "Beyond AI-Assisted Coding",
        "From vibe coding to building agents | Antigravity + Google ADK for TypeScript", 1,
        "Welcome to Beyond AI-Assisted Coding: Understanding and Building AI Agents. "
        "I'm Sajeetharan Sinnathurai, a Principal Product Manager at Microsoft working on Azure Cosmos DB. "
        "It's great to be here with GDG Kathmandu.\n\n"
        "Our journey starts with vibe coding: turning an idea into software through natural language. "
        "Then we'll explore Antigravity and other tools, walk through setup, and understand Skills and MCP. "
        "Finally, we'll bring those ideas together by building and running an agent for DevFest Quest.\n\n"
        "The key distinction is simple: we can use an agent to build software, and we can also build "
        "an agent into that software. Today we'll understand both.")
text(s, "Idea -> tools -> agent", 72, 332, 565, 40, 27, BLUE, True)
text(s, "Vibe coding. Antigravity. Setup. Skills. MCP.\nFinish with the DevFest Quest agent demo.", 72, 379, 565, 58, 17, BODY)
text(s, "Sajeetharan Sinnathurai | Principal Product Manager, Microsoft (Azure Cosmos DB)",
     72, 441, 565, 32, 12, bold=True)
text(s, "GDG Kathmandu | 21 November 2026 | 7:30-8:30 PM NPT | Google Meet",
     72, 473, 818, 18, 12, MUTED)
text(s, "{ AI }", 682, 133, 201, 60, 36, BLUE, True, align=PP_ALIGN.CENTER)
text(s, "{ build }", 668, 268, 215, 68, 34, BLUE, True, align=PP_ALIGN.CENTER)
pill(s, "1 hour / 1 journey", 680, 370, 200, 35, GREEN)

s = new("Vibe coding", "Describe your idea. Iterate with AI.",
        "Adapted from the Build with AI Handbook: natural language becomes a working prototype.", 3,
        "Vibe coding starts with describing what you want to build in natural language. "
        "Instead of beginning with every implementation detail, you explain the problem, who the application "
        "is for, and what the experience should feel like. AI helps turn that intent into code and a prototype.\n\n"
        "The important word here is iterate. The first result is a starting point. You try it, notice what "
        "is missing, and give specific feedback. That might mean improving a layout, correcting a rule, "
        "or asking for a test that proves a feature works.\n\n"
        "This is useful for both developers and builders. Developers can accelerate implementation; "
        "people with less coding experience can explore ideas more directly. But faster generation does "
        "not remove responsibility. We still need to understand the result, validate its behavior, "
        "and recognize that a working preview is not the same as a production-ready application.")
three(s, [
    ("Describe", "Start with a real problem.\n\nUse natural language.\n\nExplain the user and outcome."),
    ("Iterate", "Preview what was built.\n\nGive focused feedback.\n\nReview code and changes."),
    ("Own the result", "Accessible to builders and developers.\n\nValidate behavior and risks.\n\nA demo is not production."),
])

s = new("Better prompts", "From 'build me a game' to a useful brief",
        "Handbook prompt anatomy: role, goal, context, AI need, style, and optional visual reference.", 3,
        "Compare these two prompts. 'Build me a cool DevFest game' communicates enthusiasm, but leaves "
        "almost every important decision open. Who plays it? What makes an answer correct? "
        "Does it need AI? What should happen when the player finishes?\n\n"
        "A useful brief gives the AI a role, a goal, and context. In our example, the role is a TypeScript "
        "app builder. The goal is a game with three fictional DevFest quests. The AI hosts the experience, "
        "but application code decides the score, and the player confirms badge publication locally.\n\n"
        "We also describe the experience: accessible A, B, and C choices, a clear score, and behavior "
        "that can be verified with tests. A visual reference can help communicate style when one is available.\n\n"
        "Better prompting is not about making every prompt longer. It is about removing ambiguity "
        "from the decisions that matter.")
split(s, ("Vague prompt", "Build me a cool DevFest game.\n\nMissing player, scope, rules, AI role, and success criteria."),
      ("Useful prompt", "Act as a TypeScript app builder.\n\nBuild three fictional DevFest quests with an ADK host.\n\nCode scores; humans publish locally.\n\nAccessible A/B/C UI; verify tests."))

s = new("Think first", "Fast iteration still needs verification",
        "Think -> Build -> Verify. Local badge publication is not cloud deployment.", 3,
        "A simple way to keep AI-assisted development reliable is Think, Build, Verify.\n\n"
        "Think means defining the user, the goal, the constraints, and what success looks like. "
        "For DevFest Quest, that includes three challenges, clear scoring, and a separate human decision "
        "before publishing a badge.\n\n"
        "Build means reviewing a short plan and making focused changes. We want changes that are small "
        "enough to understand, rather than a large collection of generated files that nobody has reviewed.\n\n"
        "Verify means running the relevant tests and checking the real experience. A model saying "
        "'done' is not proof. Test results, the actual code changes, and working browser behavior "
        "are much stronger evidence.\n\n"
        "We also need to be precise about publication. Publishing a badge to this local game does "
        "not deploy an application to the cloud. Those are different actions with different requirements.")
three(s, [
    ("Think", "Define the player and goal.\n\nState constraints.\n\nAgree on success criteria."),
    ("Build", "Review a short plan.\n\nMake focused changes.\n\nInspect code and the diff."),
    ("Verify", "Run relevant tests.\n\nInspect real UI behavior.\n\nKeep human approval separate."),
])

s = new("Tool landscape", "Choose your entry point, not a winner",
        "Other choices include GitHub Copilot, Cursor, and Claude Code; workflows and permissions vary.", 3,
        "There is no single starting point that is best for every project. Choose the environment "
        "that matches the kind of work you want to do.\n\n"
        "AI Studio is a useful entry point for browser-first prototypes and quick experiments. "
        "It helps you explore an idea and see a preview without starting with a full local workflow.\n\n"
        "Stitch focuses on interface design and visual intent. It can help you explore what an "
        "experience should look like, while implementation and behavior still need their own checks.\n\n"
        "Antigravity is our choice for project-level agentic coding. We want to work with files, "
        "review plans, run commands, and inspect evidence across a real application.\n\n"
        "GitHub Copilot, Cursor, and Claude Code are other choices in this space. Their workflows "
        "and permission models differ. The important question is not which product wins, but which "
        "environment supports your task and gives you the control you need.")
three(s, [
    ("AI Studio", "Browser-first prototyping.\n\nExplore an idea and preview.\n\nStarting point for quick experiments."),
    ("Stitch", "Explore interface design.\n\nCommunicate visual intent.\n\nDesign output still needs implementation checks."),
    ("Antigravity", "Work with project files.\n\nPlan, edit, run commands, and inspect evidence.\n\nOur workshop coding environment."),
])

s = new("Antigravity overview", "An agent-first development workspace",
        "Adapted from your Antigravity deck: project context, plans, terminal, browser, and review.", 3,
        "Antigravity is an agent-first development workspace. The agent can use project context "
        "to help plan work, edit files, run tests, and inspect results through the tools it is allowed to use.\n\n"
        "Project context matters because a useful change rarely depends on a prompt alone. "
        "The agent needs relevant files, requirements, existing patterns, and clear boundaries. "
        "Opening a trusted project and reviewing the plan gives that work a sensible starting point.\n\n"
        "The other half is action and evidence. We care about what actually changed, what commands ran, "
        "what the terminal reported, and whether the browser behaves correctly. Available controls "
        "depend on the App, CLI, or editor surface being used.\n\n"
        "Keep one distinction in mind throughout the workshop: Antigravity is the tool helping us "
        "develop the application. Google ADK is the framework we use for the agent running inside it.")
split(s, ("Project context", "Open a trusted folder.\n\nGive relevant files and requirements.\n\nReview plans and changes.\n\nUse only permitted tools."),
      ("Action and evidence", "Edit files and run tests.\n\nInspect terminal output.\n\nCheck the browser when supported.\n\nVerify, do not assume success."))

s = new("Antigravity walkthrough", "Clarify -> plan -> build -> verify",
        "Source deck slides 7-9 and 18: requirements, plan review, browser evidence, reusable instructions.", 4,
        "The workflow is clarify, plan, build, and verify. Before editing, ask the agent to identify "
        "missing decisions. For our game, those decisions include how hints affect points, who chooses "
        "answers, and who can publish a badge.\n\n"
        "Next, ask for a short implementation plan. Review the proposed files, changes, and checks. "
        "Approving a clear plan is easier than reviewing a large unexpected implementation later.\n\n"
        "During the build, keep the request focused and steer with specific feedback. "
        "For example, 'Keep the scoring logic unchanged and improve only the host's greeting' "
        "is much clearer than 'Make everything better.'\n\n"
        "Finally, inspect the actual diff, test output, and browser behavior. When a workflow proves "
        "useful, we can capture it as a reusable skill instead of repeating all the instructions.\n\n"
        "Some surfaces provide slash commands for parts of this loop. The command names can vary, "
        "but the underlying requests are straightforward: clarify first, plan before editing, "
        "make the approved change, and verify the result.")
three(s, [
    ("Clarify and plan", "Ask about missing decisions.\n\nReview a short implementation plan.\n\nApprove only the intended scope."),
    ("Build and steer", "Edit a small build copy.\n\nGive precise feedback.\n\nKeep permissions and reference safe."),
    ("Verify and reuse", "Inspect tests and browser evidence.\n\nReview the actual diff.\n\nCapture a reusable skill."),
])

s = new("Setup / Antigravity", "Install, sign in, open a trusted project",
        "Presenter walkthrough only: attendees can repeat these steps after the session.", 3,
        "There are three parts to setting up Antigravity: install it, sign in, and open a trusted project.\n\n"
        "Start with the official download and follow the instructions for your operating system "
        "and preferred surface. That might be the App, CLI, or a supported editor integration.\n\n"
        "Then sign in using an account you are permitted to use. Personal and business accounts "
        "can follow different authentication paths, and available models or quota can depend on "
        "the account. We should not assume everyone has the same access or free usage.\n\n"
        "Finally, open the demo build copy as the workspace and review its trust settings. "
        "This is the project the coding agent will be able to work with, so its files and instructions matter.\n\n"
        "Signing in to Antigravity is separate from configuring a Gemini API key for our ADK "
        "application. One authorizes the development environment; the other is used by the running "
        "application to make model requests.")
three(s, [
    ("Install", "Use the official download.\n\nChoose App, CLI, or supported editor surface.\n\nFollow current OS instructions."),
    ("Sign in", "Use a permitted account.\n\nCheck model availability.\n\nDo not assume shared/free quota."),
    ("Open and review", "Open the demo build copy.\n\nReview workspace trust.\n\nKeep credentials and unrelated files private."),
])

s = new("Setup / project", "Prepare TypeScript, ADK, and the demo",
        "Dependencies are restored before class. Screen sharing explains setup, not waiting on installs.", 4,
        "Our project uses TypeScript, Node version 24.13 or later, and npm version 11.8 or later. "
        "The dependencies include Google ADK and the MCP SDK, with a lockfile for reproducible installation.\n\n"
        "The first command moves into the demo folder. 'npm ci' restores the locked dependencies. "
        "'npm run check' builds the project and runs the thirteen reference tests. "
        "'npm run dev' starts the local browser game at the address shown here.\n\n"
        "That first mode is deliberately offline. The buttons use deterministic game functions, "
        "and model chat is disabled. It lets us explore the game without pretending that an AI model is running.\n\n"
        "For a real ADK host, the Gemini key is set privately on the server. Preflight checks the "
        "runtime versions and key presence, and 'npm run dev:live' starts live mode. "
        "Preflight does not prove model access, quota, or connectivity.\n\n"
        "Choose one server mode at a time, and keep a working reference separate from the build copy.")
code_slide(s, "Set-Location .\\workshop\\demo\nnpm ci\nnpm run check\nnpm run dev\n\n# Real ADK host: set key privately first\nnpm run preflight\nnpm run dev:live\n\nhttp://127.0.0.1:18767",
           "Use Node 24.13+ / npm 11.8+.\n\nChoose one server mode.\n\nOffline is not model reasoning.\n\nNo ADK devtools required.\n\nKeep a working reference.")

s = new("Setup / permissions", "Review access before giving the agent tools",
        "More context and automation do not grant unlimited permission.", 3,
        "Before adding more capabilities, we need to review access. More context and more automation "
        "do not mean the agent should have unlimited permission.\n\n"
        "At the workspace level, inspect instructions and scripts, use a separate build copy, "
        "and keep changes small enough to review. A project may contain commands or instructions "
        "that deserve inspection before execution.\n\n"
        "For credentials, keep account and key entry private. Never put secrets into prompts, "
        "source code, or shared screenshots. Use only accounts and quota you are authorized to use.\n\n"
        "For tools, review which server is being connected and exactly which operations it exposes. "
        "Honor the host's native approval prompts rather than enabling blanket auto-approval.\n\n"
        "These same principles will apply to Skills and MCP. A useful customization can guide work "
        "or connect a tool, but it does not replace the human decision about what access is appropriate.")
three(s, [
    ("Workspace", "Inspect instructions and scripts.\n\nUse a separate build copy.\n\nKeep changes reviewable."),
    ("Credentials", "Hide account/key entry.\n\nNever put keys in prompts or code.\n\nUse permitted access and quota."),
    ("Tool access", "Review server and tool scope.\n\nHonor native approval prompts.\n\nNo blanket auto-approval."),
])

s = new("Skills", "A reusable recipe for how the agent works",
        "A skill is a folder with SKILL.md metadata and task instructions; scripts/resources are optional.", 3,
        "A skill is a reusable recipe for a particular kind of task. It lives in a folder with "
        "a file named SKILL.md, and can include optional scripts, examples, or other resources.\n\n"
        "The name and description help the coding agent discover when the skill is relevant. "
        "The full instructions describe how to approach the work: what to read, which decisions "
        "to clarify, what checks to perform, and what evidence to report.\n\n"
        "A good skill is focused. Our DevFest skill is about building a bounded TypeScript ADK agent, "
        "not handling every possible development task. It captures a repeatable workflow: "
        "read the project, define the goal and capabilities, review a plan, make approved changes, "
        "and verify the result.\n\n"
        "A project rule gives broader guidance; a skill provides a task-specific procedure. "
        "Neither is an application tool or an authorization mechanism. "
        "Markdown instructions cannot grant permission to publish a badge or bypass host approvals.")
three(s, [
    ("Discover", "Name and description.\n\nSay when the skill is useful.\n\nKeep it focused."),
    ("Apply", "Read task instructions.\n\nReuse checks and examples.\n\nPlan -> approved edit -> evidence."),
    ("Still bounded", "Respect project rules.\n\nHonor host approvals.\n\nNo new permission from Markdown."),
])

s = new("Skills / walkthrough", "Show and use devfest-agent-builder",
        "Open the demo copy as the workspace so its .agents/skills folder is discoverable.", 3,
        "This is the structure of our devfest-agent-builder skill. The metadata gives it a name "
        "and a description of when it should be used. The instructions then define a simple, repeatable process.\n\n"
        "First, read the existing agent, tools, and tests. Next, define the agent's goal and allowed "
        "capabilities. Produce a plan and wait for human approval before making changes. "
        "Reuse typed handlers and schemas, then verify actual tests and tool results.\n\n"
        "The full skill is included under the demo workspace's .agents skills folder. "
        "Opening that demo copy as the workspace makes the skill available in the intended project context.\n\n"
        "In Antigravity App, it can be invoked by its name using the slash form shown here. "
        "Other surfaces may use a different supported invocation. "
        "A natural request is: 'Use devfest-agent-builder to plan our host, its four tools, "
        "and how we will verify it. Do not edit yet.'\n\n"
        "The result we want first is a plan we can review, not an unapproved implementation.")
code_slide(s, "---\nname: devfest-agent-builder\ndescription: Builds bounded TypeScript ADK agents.\n---\n\nRead existing agent, tools, and tests.\nDefine goal and allowed capabilities.\nPlan; wait for human approval.\nReuse typed handlers and schemas.\nVerify actual tests and tool results.",
           "Manifest/instruction excerpt.\n\nFull skill is bundled.\n\nApp: /devfest-agent-builder.\n\nOr name it in your prompt.\n\nDo not edit before approval.", size=16)

s = new("MCP", "A standard connection to tools and context",
        "Skill = how to work. MCP = how tools connect. ADK FunctionTool = an application capability.", 2,
        "MCP stands for Model Context Protocol. It provides a standard way for an AI application "
        "to connect to tools and context exposed by a server.\n\n"
        "The coding environment acts as an MCP client. A connected server describes its named tools "
        "and their input schemas. The client can request a tool call and receive its result. "
        "The connection might be a local process or a remote transport.\n\n"
        "Our example stays deliberately small. It provides a workshop outline and an agent-building "
        "checklist. It cannot read project files, contact external services, or change game state.\n\n"
        "Here is the distinction to remember: a skill describes how to work; MCP describes how "
        "tools connect; an ADK FunctionTool is a capability registered with our application agent. "
        "Connecting this MCP server to Antigravity does not automatically give those tools "
        "to the DevFest game host. They belong to different parts of the system.")
three(s, [
    ("Coding agent", "Requests a named tool.\n\nUses returned context.\n\nStill follows approvals."),
    ("MCP server", "Publishes tool schemas.\n\nExecutes scoped handlers.\n\nLocal stdio or remote transport."),
    ("Our example", "Workshop outline.\n\nAgent-building checklist.\n\nNo files, network, or game-state writes."),
])

s = new("MCP / setup", "Connect one reviewed local server",
        "Replace the example path; merge only this entry into your own MCP configuration.", 4,
        "This configuration connects one local MCP server named devfest-workshop. "
        "The command is Node, and the argument is the absolute path to the server's TypeScript file. "
        "The path on this slide is an example and must be replaced with the real path on your machine.\n\n"
        "In Antigravity App, MCP servers are managed through Customizations, Installed, and MCP Servers. "
        "The configuration location can be found through the host's configuration-path control. "
        "Merge this server entry into the existing configuration rather than replacing other servers.\n\n"
        "The enabled-tools list limits this connection to two tools: get_workshop_overview "
        "and get_agent_build_checklist. Node must be available to the host, and no Gemini key is "
        "needed for these static responses. Communication uses standard input and output, not a browser endpoint.\n\n"
        "The checklist tool takes empty arguments and returns a bounded agent-building workflow. "
        "Its actual discovery and calls are covered by the local protocol test. "
        "A successful protocol test and a successful connection in an editor are separate checks.\n\n"
        "Read-only labels are helpful descriptions, but reviewing what the server actually does "
        "is what establishes its scope.")
code_slide(s, '{\n  "mcpServers": {\n    "devfest-workshop": {\n      "command": "node",\n      "args": ["C:\\\\quest\\\\src\\\\mcp.ts"],\n      "enabledTools": [\n        "get_workshop_overview",\n        "get_agent_build_checklist"\n      ]\n    }\n  }\n}',
           "Use your real absolute path.\n\nNode must be on host PATH.\n\nReview before connecting.\n\nTwo read-only tools only.\n\nNo Gemini key required.", size=16)

s = new("Building agents", "Antigravity builds. Your ADK agent runs.",
        "The final demo is an application agent, not just a generated game page.", 2,
        "Now we can connect the development workflow to an application agent.\n\n"
        "On the left is Antigravity, helping us build software. It uses the skill as a workflow "
        "and can use the MCP checklist as development context. Its output is a reviewed change "
        "to the application, backed by tests and evidence.\n\n"
        "On the right is the agent we are building with Google ADK, the Agent Development Kit. "
        "This agent runs inside DevFest Quest. It has an identity, instructions, a model, "
        "and four allowed FunctionTools.\n\n"
        "The host can read a challenge, offer an agreed hint, check the player's answer, "
        "and propose a badge. Application code computes points, and the separate human flow publishes "
        "the badge locally. The model does not get to invent its own score or grant itself permission.\n\n"
        "That is the difference between using an agent to build an app and building an agent into an app.")
split(s, ("Development agent", "Antigravity uses the skill.\n\nMCP supplies a build checklist.\n\nReview a scoped agent change.\n\nRun tests and inspect evidence."),
      ("Application agent", "Google ADK LlmAgent.\n\nFour allowed FunctionTools.\n\nCode computes scores.\n\nHumans publish the badge locally."))

s = new("Implement", "Build the host from goal and typed tools",
        "Use existing tested handlers; do not rebuild storage or the whole website in four minutes.", 4,
        "The core construction is an LlmAgent. The name identifies our DevFest host, the model selects "
        "the configured language model, the instruction defines its behavior, and tools supplies the "
        "capabilities it is allowed to call.\n\n"
        "The code on this slide is a shortened example. The full agent instructions include player choice, "
        "hint consent, grounded progress, explicit errors, and the human-only publication boundary.\n\n"
        "Our focused change is to make the host a concise, encouraging coach without changing those "
        "constraints. A persona change should affect the experience, not expand permissions. "
        "We keep the same four tools and inspect the resulting code change and test output.\n\n"
        "The tools are get_challenge, get_hint, check_answer, and propose_badge. "
        "The answer checker accepts a challenge identifier and an A, B, or C choice through a strict schema. "
        "Its handler determines correctness and awards the points. There is no arbitrary score argument "
        "and no model tool that publishes a badge.\n\n"
        "Instructions guide the model, while schemas and application code enforce the important rules. "
        "Tests verify those rules; a live run separately evaluates how well the host follows its instructions.")
code_slide(s, "new LlmAgent({\n  name: 'devfest_quest_host',\n  model,\n  instruction: 'Use tools; never publish.',\n  tools: createQuestTools(store).tools,\n});\n\n// check_answer: strict challengeId + A/B/C\n// handler checks correctness and scores\n// propose_badge does not publish",
           "Construction excerpt.\n\nOpen the full agent source.\n\nApprove a small persona edit.\n\nKeep tested tools unchanged.\n\nVerify the actual result.", size=16)

s = new("Live walkthrough", "Run the agent. Inspect a real tool call.",
        "The MCP development connector and ADK game runtime are different evidence streams.", 3,
        "A running agent should be understood through its actual tool calls, not just its final wording. "
        "A useful first request is: 'Show my current quest and progress. Do not answer it for me.'\n\n"
        "The evidence chain is the function name, its arguments, the tool's actual result, and the "
        "model's final reply. The quest identifier and score in that reply should match the returned "
        "data and the game state. This is how we distinguish grounded behavior from a plausible guess.\n\n"
        "Entries labeled ADK runtime represent model-selected calls. The game buttons use the same "
        "underlying rules through local deterministic handlers, and their traces are labeled differently. "
        "The MCP checklist belongs to the development environment, not this application trace.\n\n"
        "Live mode needs a permitted key, model access, and connectivity. If a request fails, that "
        "failure must remain visible rather than becoming an invented success. "
        "Offline mode is a useful alternative for exploring the rules, but it is not model reasoning.")
code_slide(s, "npm run dev:live\n\nShow my current quest and progress.\nDo not answer it for me.\n\n# Inspect source: ADK runtime\n# function -> arguments -> result -> reply\n\n# Offline alternative: npm run dev",
           "Actual tool result.\n\nGrounded quest and score.\n\nErrors remain errors.\n\nNo invented live trace.\n\nUse your permitted key.")

s = new("Demo / play and confirm", "Play DevFest Quest. Review the badge.",
        "The agent hosts; code scores; the player confirms publication only to this local game.", 4,
        "DevFest Quest has three challenges: the Builder Bridge, the Tool Temple, and the Badge Vault. "
        "The player chooses A, B, or C. The host can guide the adventure, but it should not choose "
        "answers on the player's behalf.\n\n"
        "Each correct answer normally earns one hundred points. An agreed hint reduces the points "
        "available for that quest to seventy-five. A wrong answer earns zero, and repeating a correct "
        "answer cannot earn the points again. With one hint and three correct answers, the total is "
        "seventy-five plus one hundred plus one hundred: two hundred and seventy-five.\n\n"
        "After all three quests are complete, the agent can propose the earned badge. "
        "The proposal contains the computed score, but remains pending. 'Applied false' means "
        "publication has not happened. A request in chat is not approval.\n\n"
        "The final decision belongs to the player through a separate review flow. "
        "The player reviews the proposal, types PUBLISH, and confirms. The published badge and its "
        "score can then be checked again after refreshing the game.\n\n"
        "This publication exists only in the local game. It is not a cloud deployment or an official certificate.")
three(s, [
    ("Audience plays", "Builder Bridge -> Tool Temple -> Badge Vault.\n\nPlayer picks A/B/C.\n\nOne hint: 275 total."),
    ("Agent proposes", "Four scoped game tools.\n\nEarned score from code.\n\nPending / applied:false.\n\nChat is not approval."),
    ("Human confirms", "Review the real proposal.\n\nType PUBLISH separately.\n\nRefresh persisted state.\n\nNot an official certificate."),
])

s = new("Permission boundary", "Idea -> workflow -> connected tools -> agent",
        "Skills guide work. MCP connects tools. ADK runs the host. Code and humans own boundaries.", 1,
        "Our journey started with an idea and a useful prompt. We chose a development environment, "
        "reviewed setup and permissions, and used a skill to make the workflow reusable. "
        "MCP supplied a standard connection to bounded development tools. "
        "Google ADK gave our application agent a model, instructions, and typed capabilities.\n\n"
        "Remember the three distinctions: Skills guide how the coding agent works. "
        "MCP connects tools and context. ADK FunctionTools define what our game host can do.\n\n"
        "Across all three, evidence and boundaries still matter. Inspect actual results, "
        "let code enforce the rules, and keep the final human decision separate.")
three(s, [
    ("Start", "Describe intent.\n\nChoose the environment.\n\nSet up and review permissions."),
    ("Extend", "Reuse a focused skill.\n\nConnect reviewed MCP tools.\n\nKeep context and access bounded."),
    ("Build an agent", "Configure ADK and typed tools.\n\nInspect real calls/results.\n\nKeep human authority."),
])

s = new("Resources and Q&A", "Keep building after the one-hour session",
        "Take-home code and prompts are optional. The live session ends at 20:30 NPT.", 4,
        "The workshop resources let you repeat this journey at your own pace. "
        "The Build with AI Handbook provides more ideas, prompting examples, and starting points. "
        "The QR code and short link here lead to that public handbook.\n\n"
        "The Google ADK TypeScript quickstart is the next reference for building application agents. "
        "Antigravity's documentation covers setup, Skills, MCP, and the controls available in each surface.\n\n"
        "The workshop bundle includes DevFest Quest, its tests, the reusable skill, the local MCP server "
        "and configuration example, and the prompts and guides. "
        "Use the shared bundle for this version; local workshop changes do not mean a repository branch "
        "has already been published.\n\n"
        "A useful next step is to repeat the agent setup in your own build copy, inspect a real tool call, "
        "and make one small, verified improvement while keeping the capability boundaries intact.\n\n"
        "Thank you to GDG Kathmandu and to everyone who joined. "
        "What questions do you have about vibe coding, Antigravity, Skills, MCP, or building your own agents?")
panel(s, 44, 184, 620, 309)
text(s, "{  }", 710, 183, 194, 68, 52, BLUE, True, align=PP_ALIGN.CENTER)
text(s, "Scan the handbook", 698, 270, 210, 28, 18, BLUE, align=PP_ALIGN.CENTER)
handbook_qr(s, 721, 307, 166)
links = [
    ("Public Build with AI handbook", "https://g.dev/ai/build"),
    ("Google ADK TypeScript quickstart", "https://adk.dev/get-started/typescript/"),
    ("Antigravity documentation", "https://antigravity.google/docs/getting-started"),
    ("Workshop repository", "https://github.com/analyticsrepo01/google-play-agy-workshop"),
]
for i, (label, url) in enumerate(links):
    y = 192 + i * 66
    text(s, label, 62, y, 586, 28, 18, bold=True)
    shape = text(s, url, 62, y + 29, 586, 24, 14, BLUE)
    for paragraph in shape.text_frame.paragraphs:
        for run in paragraph.runs:
            run.hyperlink.address = url
text(s, "Use the shared source bundle; local changes are not a claim that the GitHub branch is published.",
     62, 461, 586, 30, 12, MUTED)

assert elapsed == 60, elapsed
assert len(prs.slides) == COUNT
for slide in prs.slides:
    assert slide.notes_slide.notes_text_frame.text.strip()
    for shape in slide.shapes:
        assert shape.left >= 0 and shape.top >= 0
        assert shape.left + shape.width <= prs.slide_width
        assert shape.top + shape.height <= prs.slide_height

# Preserve the handbook's page size while keeping the logical layout proportions.
scale = 0.75
for slide in prs.slides:
    for shape in slide.shapes:
        shape.left = round(shape.left * scale)
        shape.top = round(shape.top * scale)
        shape.width = round(shape.width * scale)
        shape.height = round(shape.height * scale)
        if shape.line.width is not None:
            shape.line.width = round(shape.line.width * scale)
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                if paragraph.font.size is not None:
                    paragraph.font.size = Pt(paragraph.font.size.pt * scale)
                if paragraph.line_spacing is not None:
                    paragraph.line_spacing = Pt(paragraph.line_spacing.pt * scale)
prs.slide_width = Pt(720)
prs.slide_height = Pt(405)
prs.core_properties.title = "Beyond AI-Assisted Coding: Understanding and Building AI Agents"
prs.core_properties.subject = "GDG Kathmandu | Vibe coding -> Antigravity -> setup -> skills -> MCP -> ADK agents"
prs.core_properties.author = "Sajeetharan Sinnathurai"
prs.core_properties.keywords = "Vibe coding, Antigravity, skills, MCP, Google ADK, TypeScript, DevFest Quest"
prs.save(OUTPUT)
assert len(Presentation(OUTPUT).slides) == COUNT
print(f"Created {OUTPUT}")
print(f"Verified {COUNT} slides, 60-minute timings, full notes, bounds, and {len(checks)} fitted text boxes.")
