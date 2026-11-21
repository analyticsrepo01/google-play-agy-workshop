"""Align the saved decks with Name Race without regenerating their artwork.

Requires the existing slide-tool dependencies: python-pptx, Pillow, and qrcode.
Run from any directory; export fresh PDFs with PowerPoint afterward.
"""

from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
import json
import os
import posixpath
import zipfile

import qrcode
from lxml import etree
from PIL import ImageFont
from pptx import Presentation
from pptx.util import Pt


ROOT = Path(__file__).parent
DEMO_REPO = "https://github.com/sajeetharan/name-race-agent-workshop"
WEBSITE = "https://sajeetharan.dev/"
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
CONFIG = {
    "mcpServers": {
        "name-race-guide": {
            "command": "node",
            "args": [r"C:\name-race-agent-workshop\src\mcp.ts", "--guide"],
        }
    }
}
TEXT = {
    1: {
        8: "From vibe coding to building agents | Antigravity +\nTypeScript + MCP + optional Gemini",
        14: "Vibe coding. Antigravity. Setup. Skills. MCP.\nFinish with the live Name Race quiz.",
    },
    4: {
        13: "Build me a cool quiz.\n\nMissing players, rules, AI role,\nand success criteria.",
        18: "Act as a TypeScript app builder.\n\nBuild Name Race: 120 nicknames,\nfive questions, colored cars.\n\nCode ranks; humans control.\n\nOptional AI; verify both screens.",
    },
    5: {6: "Think -> Build -> Verify. Test the quiz before deploying it."},
    10: {
        3: "Prepare TypeScript, MCP, and Name Race",
        14: "git clone `\n  https://github.com/sajeetharan/name-race-agent-workshop\nSet-Location .\\name-race-agent-workshop\nnpm ci\nnpm run check\nnpm run dev\n\n# Local rehearsal\nhttp://127.0.0.1:18769",
        19: "Node 24.13+ / npm 11+.\n\nTen tests + strict build.\n\nNo ADK or key needed.\n\nAI OFF is honest.\n\nKeep a working reference.",
    },
    13: {
        3: "Show and use name-race-builder",
        4: "Open the Name Race repo as the workspace; verify actual Skill discovery.",
        14: "---\nname: name-race-builder\ndescription: Build and verify Name Race.\n---\n\nRead AGENTS.md; review a short plan.\nKeep scoring and host controls in code.\nMake the smallest approved change.\nRun npm run check.\nVerify host, phone, and MCP results.",
        19: "Instruction excerpt.\n\nFull Skill is in the repo.\n\nAsk for name-race-builder.\n\nCheck host discovery.\n\nReview before edits.",
    },
    14: {
        4: "Skill = how to work. MCP = how tools connect. Agent = a bounded model loop.",
        22: "Guide vs runtime",
        23: "Guide: static build steps.\n\nRuntime: real room calls.\n\nDifferent tool scopes.\n\nReview each connection.",
    },
    15: {
        14: json.dumps(CONFIG, indent=2),
        19: "Replace the absolute path.\n\nKeep --guide in args.\n\nMerge; do not overwrite.\n\nget_game_rules +\nget_build_steps.\n\nNo key or room access.",
    },
    16: {
        3: "Antigravity builds. Gemini comments.",
        4: "The quiz works without AI. Optional commentary uses a bounded application agent.",
        18: "Optional Gemini loop.\n\nOne anonymous MCP read.\n\nCode scores and ranks.\n\nOnly the host controls rooms.",
    },
    17: {
        5: "Build a bounded commentator",
        6: "Actual agent.ts excerpts; retain the read-only tool and validate the model result.",
        15: "export function createCommentator(connection, provider)\nconst tool = connection.tools.find(\n  t => t.name === 'read_race_summary');\n\n// Model gets only this tool, once.\n// Output: actual phase + calm/excited style.\n// Code validates phase and fresh facts.\n// Code renders all factual words.\n// No names, answers, or host controls.",
        20: "Excerpts, not a full function.\n\nInspect src/agent.ts.\n\nModel chooses style only.\n\nNo scores or winners by AI.\n\nRun npm run check.",
    },
    18: {
        3: "Inspect real MCP calls and commentary",
        4: "Guide calls, HTTP -> MCP, and optional Agent -> MCP are different evidence streams.",
        12: "npm run dev\n\n# Host/phone actions -> real MCP\njoin_room -> submit_answer -> read_room\nhost_control: START / CLOSE / NEXT\n\n# Optional AI: set key privately; restart\nread_race_summary -> phase + style\n\n# Inspect actual call / result trace",
        16: "Real MCP without a key.\n\nAI OFF is not reasoning.\n\nAnonymous facts only.\n\nFailures stay visible.\n\nRehearse Gemini privately.",
    },
    19: {
        2: "DEMO / PLAY AND REVEAL",
        3: "Play Name Race. Reveal the podium.",
        4: "Phones answer; code scores and ranks; the human host opens and closes questions.",
        13: "Scan QR; use a nickname.\n\nUp to 120 entries.\n\nFive workshop questions.\n\nOne final answer each.\n\nCorrect: 100 points / 20%.",
        17: "Code ranks",
        18: "Wrong or missing: zero.\n\nScore first; faster correct\nanswers break ties.\n\nExact ties share rank.\n\nNamed top-three podium.",
        23: "Review START.\n\nCLOSE: reveal results.\n\nNEXT: open a question.\n\nRESET: replay; keep names.\n\nDELETE: remove the room.",
    },
    20: {
        6: "Skills guide work. MCP connects tools. Gemini comments. Code and humans own boundaries.",
        24: "Bound the model loop.\n\nInspect real MCP results.\n\nKeep human authority.",
    },
    21: {
        12: "Scan the demo repo",
        175: "Name Race repository",
        176: DEMO_REPO,
        177: "Numbered build guide and prompts",
        178: DEMO_REPO + "/blob/main/BUILD_GUIDE.md",
        183: "Clone Name Race for the current demo; workshop slides and guides are in the workshop repository.",
    },
}

NOTES = {
    1: "Welcome to Beyond AI-Assisted Coding: Understanding and Building AI Agents. Today we move from vibe coding to tools, setup, Skills, MCP, and a bounded application agent. Our demo is Name Race: a live five-question quiz with colored cars and a named podium. Antigravity helps build the software. Optional Gemini commentary runs inside it. The quiz works without a model or ADK.",
    4: "A vague request leaves important choices open. A useful brief names the players, rules, AI role, and evidence of success. Build Name Race for up to 120 nickname entries answering five workshop questions. Correct answers earn 100 points and move cars 20 percent. Code ranks by score and then total correct-answer time. People control the room. AI commentary is optional and receives no names. Verify both host and phone screens.",
    5: "Think, Build, Verify keeps fast iteration reliable. Define the quiz rules, privacy, and host controls. Review a short plan and make focused changes. Run the tests and inspect the real host and phone experience. A model saying done is not proof. Deployment is a separate step: verify the HTTPS app, private host login, QR joining, answers, and podium. Do not deploy during a live race.",
    7: "Antigravity uses project context to help plan, edit, test, and inspect evidence. Open the trusted Name Race workspace and review relevant files and requirements. Use only permitted tools and inspect actual changes. Antigravity is the development agent; the optional Gemini commentator is the application agent. Neither replaces tested quiz rules or human host control.",
    8: "Clarify, plan, build, verify. For Name Race, clarify how answers score, who controls questions, and what data reaches AI. Review the files and checks before editing. Make one small wording change in a build copy while keeping scoring and permissions unchanged. Inspect the diff, tests, and browser. Capture the repeatable process as a Skill. Invocation controls differ across coding surfaces.",
    9: "Install Antigravity from the official source, sign in using a permitted account, and open the Name Race build copy as a trusted workspace. Review account access and native permissions. Antigravity sign-in is separate from the optional server-side Gemini API key. The quiz and real MCP calls need no model key. Never show credential entry while screen sharing.",
    10: "Clone github.com/sajeetharan/name-race-agent-workshop, then enter that folder. Use Node 24.13 or later and npm 11 or later. npm ci restores locked dependencies. npm run check performs the strict TypeScript build, ten tests, and browser JavaScript syntax check. npm run dev opens local rehearsal at 127.0.0.1 port 18769. The quiz uses real MCP even with AI OFF. No ADK or model key is required. Optional commentary uses a privately configured Gemini key and the same startup command.",
    12: "A Skill is a focused reusable recipe with SKILL.md metadata and instructions. Name and description help discovery; the body says what to read, plan, change, and verify. Our name-race-builder Skill keeps scoring and time tie-breaks in code, grades private until CLOSE, and host permissions in the HTTP adapter. It asks for the smallest approved change and actual checks. A Skill grants no permissions and cannot bypass native approvals.",
    13: "Open the Name Race repo as its own coding workspace and inspect .agents/skills/name-race-builder/SKILL.md. Ask the installed host to use name-race-builder for one small change. Verify discovery rather than assuming a file was loaded. Read AGENTS.md, state the expected behavior, review a short plan, preserve the quiz and privacy rules, make the approved change, run npm run check, and inspect host, participant, and actual MCP results. First request a plan, not an unapproved implementation.",
    14: "MCP is a standard connection to named tools and their schemas. Name Race has two distinct scopes. Guide mode exposes get_game_rules and get_build_steps with static context and no running-room access. The runtime broker exposes real registration, answers, reads, and reviewed host actions. The HTTP adapter validates callers and supplies private authority and timestamps. The optional model receives only read_race_summary with anonymous labels. A Skill guides work; MCP connects tools; the agent is a bounded model loop.",
    15: "Review the Name Race MCP example. Replace the absolute source path and retain --guide. Merge only name-race-guide into the installed host's configuration without overwriting other servers. Node must be on its PATH. Guide mode exposes get_game_rules and get_build_steps and needs no Gemini key. Call get_build_steps with empty arguments and inspect the real result. This guide cannot inspect or mutate a running room. Editor discovery and a protocol test are separate evidence. Respect native permissions.",
    16: "Antigravity is the development agent: it uses the Skill and guide MCP to produce reviewed changes. The optional application agent uses Gemini and a small loop in src/agent.ts. It receives only the read_race_summary tool, once for the selected room, with anonymous labels. It chooses calm or excited style and reports the actual phase. Code validates the response and renders factual words. Code determines scores and ranks. The authenticated host alone controls the room. The quiz works without AI.",
    17: "Open createCommentator in src/agent.ts. These are excerpts, not a complete runnable function. The model receives only read_race_summary and may call it once with the selected room code. The application validates the returned phase and calm or excited style, rereads the summary to reject stale commentary, and renders every factual word from real data. No names, answers, scoring, or host-control tools reach Gemini. Inspect a small approved wording change and run npm run check. Live model access still requires private rehearsal.",
    18: "Inspect the actual runtime call and result trace. Phone registration calls join_room; answers call submit_answer; views call read_room. Reviewed START, CLOSE, and NEXT reach host_control through the authorized HTTP adapter. These are real MCP calls without a model key, not AI reasoning. Guide MCP is a separate development connection. If optional Gemini is enabled privately, its trace reads Agent to MCP using read_race_summary. The model chooses style, not facts or winners. Errors stay visible; do not invent a successful model call.",
    19: "Scan the room QR code and choose a nickname you consent to display. Up to 120 entries answer five questions about vibe coding, Antigravity, Skills, MCP, and human control. Each answer is final. Review and type START; after answers type CLOSE to reveal; type NEXT to open the next question. Each correct answer earns 100 points and moves the car 20 percent. Wrong or missing answers earn zero. Scores rank first and faster total correct-answer receipt times break ties, including network and polling delay. Exact ties share a rank; the leading three entries appear on the named podium after question five closes. RESET retains names for another round. DELETE removes the room. Rooms expire two hours after creation.",
    20: "We started with a clear idea, chose Antigravity, reviewed setup and permissions, reused a Skill, connected real MCP tools, and built a bounded optional commentator. Skills guide how to work. MCP connects scoped tools. Gemini chooses a commentary style while code owns facts, scores, and ranking. Human host controls remain outside the model. Test, inspect actual results, and verify deployment separately. This is a teaching demo, not an abuse-proof exam or multi-instance production backend.",
    21: "The QR code and first link lead to the Name Race repository. Clone it for the current quiz, Skill, MCP configuration, optional agent, tests, and deployment instructions. The next link opens the numbered build guide and prompts. Antigravity documentation helps with setup. The workshop repository contains these slides and session guides; its bundled Quest demo is a historical reference, not today's quiz. Make one small verified change in your own copy and keep the capability boundaries. Thank you to GDG Kathmandu and everyone joining.",
}

QUESTIONS = {
    "SPOT IT | Offline handlers or live model?": "SPOT IT | Real MCP or optional AI?",
    "QUICK CHECK | Skill, MCP, or FunctionTool?": "QUICK CHECK | Skill, MCP, or agent?",
    "VOTE A/B/C | You choose; the host guides.": "PLAY | Answer on your phone; code ranks.",
}
STALE = (
    "devfest quest", "devfest-agent-builder", "devfest-workshop", "adk",
    "badge", "18767", "dev:live", "preflight", "get_workshop_overview",
    "get_agent_build_checklist", "275", "llmagent", "functiontool",
)


def tag(name):
    prefix, local = name.split(":")
    return f"{{{NS[prefix]}}}{local}"


def fitted_lines(value, shape):
    paragraph = shape.text_frame.paragraphs[0]
    size = paragraph.font.size
    if size is None and paragraph.runs:
        size = paragraph.runs[0].font.size
    size = size.pt if size is not None else 12.75
    minimum = min(9, size)
    code = shape.shape_id in (14, 15, 12) and (
        "npm " in value or "mcpServers" in value or "export function" in value or "---" in value
    )
    font_file = Path(os.environ["WINDIR"]) / "Fonts" / (
        "consola.ttf" if code else "arialbd.ttf" if paragraph.font.bold else "arial.ttf"
    )
    width = shape.width.pt - shape.text_frame.margin_left.pt - shape.text_frame.margin_right.pt
    height = shape.height.pt - shape.text_frame.margin_top.pt - shape.text_frame.margin_bottom.pt
    while size >= minimum:
        font = ImageFont.truetype(str(font_file), round(size * 4))
        measure = lambda text: font.getlength(text) / 4
        lines = []
        for source_line in value.split("\n"):
            if code or not source_line:
                lines.append(source_line)
                continue
            line = ""
            for word in source_line.split():
                candidate = f"{line} {word}".strip()
                if line and measure(candidate) > width - 3:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
        leading = 1.15 if height < 15 else 1.22
        padding = 0 if height < 15 else 3
        if len(lines) * size * leading <= height - padding and all(measure(line) <= width - 3 for line in lines):
            return lines, size, leading
        size -= 0.25
    raise ValueError(f"Text does not fit shape {shape.shape_id}: {value}")


def replace_body(body, lines, size=None, hyperlink=None, leading=1.22):
    original = body.find(tag("a:p"))
    ppr = original.find(tag("a:pPr"))
    rpr = original.find(f".//{tag('a:rPr')}")
    if rpr is None and ppr is not None:
        rpr = ppr.find(tag("a:defRPr"))
    for paragraph in list(body.findall(tag("a:p"))):
        body.remove(paragraph)
    for line in lines:
        paragraph = etree.SubElement(body, tag("a:p"))
        properties = deepcopy(ppr) if ppr is not None else etree.Element(tag("a:pPr"))
        if size is not None:
            spacing = properties.find(tag("a:lnSpc"))
            if spacing is not None:
                properties.remove(spacing)
            spacing = etree.Element(tag("a:lnSpc"))
            etree.SubElement(spacing, tag("a:spcPts"), val=str(round(size * leading * 100)))
            properties.insert(0, spacing)
        paragraph.append(properties)
        run = etree.SubElement(paragraph, tag("a:r"))
        style = deepcopy(rpr) if rpr is not None else etree.Element(tag("a:rPr"))
        style.tag = tag("a:rPr")
        if size is not None:
            style.set("sz", str(round(size * 100)))
        for link in list(style.findall(tag("a:hlinkClick"))):
            style.remove(link)
        if hyperlink:
            etree.SubElement(style, tag("a:hlinkClick"), {tag("r:id"): hyperlink})
        run.append(style)
        etree.SubElement(run, tag("a:t")).text = line


def serialize(root):
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def relationships(entries, name):
    rel_name = posixpath.join(posixpath.dirname(name), "_rels", posixpath.basename(name) + ".rels")
    return rel_name, etree.fromstring(entries[rel_name])


def resolve_part(source, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(source), target)).lstrip("/")


def add_cover_website(root, entries, name, changed):
    body = root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@id="15"]/p:txBody', namespaces=NS)[0]
    if WEBSITE in body.xpath(".//a:t/text()", namespaces=NS):
        return
    rel_name, rels = relationships(entries, name)
    link_id = f"rId{max(int(rel.get('Id')[3:]) for rel in rels) + 1}"
    etree.SubElement(rels, "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship",
                     Id=link_id, Type=NS["r"] + "/hyperlink", Target=WEBSITE, TargetMode="External")
    changed[rel_name] = serialize(rels)
    website_body = deepcopy(body)
    replace_body(website_body, [WEBSITE], size=9, hyperlink=link_id, leading=1.15)
    paragraph = website_body.find(tag("a:p"))
    style = paragraph.find(".//" + tag("a:rPr"))
    style.set("b", "0")
    style.set("u", "sng")
    style.find(".//" + tag("a:srgbClr")).set("val", "4285F4")
    body.append(paragraph)


def qr_modules(root):
    shapes = root.xpath(".//p:sp", namespaces=NS)
    named = [shape for shape in shapes
             if shape.find(".//" + tag("p:cNvPr")).get("name", "").startswith("Name Race QR module ")]
    if named:
        return named
    return [shape for shape in shapes
            if 14 <= int(shape.find(".//" + tag("p:cNvPr")).get("id")) <= 174]


def update_closing_qr(root):
    modules = qr_modules(root)
    if modules[0].find(".//" + tag("p:cNvPr")).get("name", "").startswith("Name Race QR module "):
        return
    ids = {shape.find(".//" + tag("p:cNvPr")).get("id") for shape in modules}
    assert not ids.intersection(root.xpath(".//p:spTgt/@spid", namespaces=NS)), "QR modules must remain static."
    tree = modules[0].getparent()
    template = deepcopy(modules[0])
    index = tree.index(modules[0])
    next_id = max(int(value) for value in root.xpath(".//p:cNvPr/@id", namespaces=NS)) + 1
    for module in modules:
        tree.remove(module)
    background = root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@id="13"]/p:spPr/a:xfrm', namespaces=NS)[0]
    offset, extent = background.find(tag("a:off")), background.find(tag("a:ext"))
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4)
    qr.add_data(DEMO_REPO)
    qr.make(fit=True)
    matrix = qr.get_matrix()
    size = len(matrix)
    number = 0
    for row, cells in enumerate(matrix):
        start = None
        for column in range(size + 1):
            filled = column < size and cells[column]
            if filled and start is None:
                start = column
            elif not filled and start is not None:
                shape = deepcopy(template)
                identity = shape.find(".//" + tag("p:cNvPr"))
                identity.set("id", str(next_id + number))
                identity.set("name", f"Name Race QR module {number + 1}")
                transform = shape.find(".//" + tag("a:xfrm"))
                x = round(start * int(extent.get("cx")) / size)
                y = round(row * int(extent.get("cy")) / size)
                right = round(column * int(extent.get("cx")) / size)
                bottom = round((row + 1) * int(extent.get("cy")) / size)
                transform.find(tag("a:off")).set("x", str(int(offset.get("x")) + x))
                transform.find(tag("a:off")).set("y", str(int(offset.get("y")) + y))
                transform.find(tag("a:ext")).set("cx", str(right - x))
                transform.find(tag("a:ext")).set("cy", str(bottom - y))
                tree.insert(index + number, shape)
                number += 1
                start = None


def update(path):
    presentation = Presentation(path)
    if len(presentation.slides) != 21:
        raise ValueError("Expected the saved 21-slide deck.")
    with zipfile.ZipFile(path) as archive:
        entries = {info.filename: archive.read(info.filename) for info in archive.infolist()}
        infos = archive.infolist()
    _, presentation_rels = relationships(entries, "ppt/presentation.xml")
    targets = {rel.get("Id"): resolve_part("ppt/presentation.xml", rel.get("Target"))
               for rel in presentation_rels}
    ordered_parts = [targets[node.get(tag("r:id"))]
                     for node in etree.fromstring(entries["ppt/presentation.xml"]).findall(".//" + tag("p:sldId"))]
    changed = {}
    for number, slide in enumerate(presentation.slides, 1):
        # python-pptx renumbers part names when slides are enumerated.
        # The saved package's relationship order remains authoritative.
        name = ordered_parts[number - 1]
        root = etree.fromstring(entries[name])
        replacements = dict(TEXT.get(number, {}))
        for shape in slide.shapes:
            if shape.has_text_frame and shape.text in QUESTIONS:
                replacements[shape.shape_id] = QUESTIONS[shape.text]
        for shape_id, value in replacements.items():
            shape = next(shape for shape in slide.shapes if shape.shape_id == shape_id)
            nodes = root.xpath(f'.//p:sp[p:nvSpPr/p:cNvPr/@id="{shape_id}"]/p:txBody', namespaces=NS)
            if len(nodes) != 1:
                raise ValueError(f"Missing text shape {number}/{shape_id}")
            lines, size, leading = fitted_lines(value, shape)
            link_id = None
            if number == 21 and shape_id in (176, 178):
                link_id = nodes[0].xpath(".//a:hlinkClick/@r:id", namespaces=NS)[0]
                rel_name, rels = relationships(entries, name)
                if rel_name in changed:
                    rels = etree.fromstring(changed[rel_name])
                for relationship in rels:
                    if relationship.get("Id") == link_id:
                        relationship.set("Target", value)
                changed[rel_name] = serialize(rels)
            replace_body(nodes[0], lines, size, link_id, leading)
        if number == 1:
            add_cover_website(root, entries, name, changed)
            title = root.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@id="13"]', namespaces=NS)[0]
            title.find(".//" + tag("a:ext")).set("cy", str(Pt(33.5)))
            replace_body(title.find(tag("p:txBody")), ["Idea -> tools -> agent"], size=27, leading=1.1)
        if number == 21:
            update_closing_qr(root)
        if replacements or number == 1:
            changed[name] = serialize(root)
        if number in NOTES:
            _, slide_rels = relationships(entries, name)
            note_name = next(resolve_part(name, rel.get("Target")) for rel in slide_rels
                             if rel.get("Type").endswith("/notesSlide"))
            note_root = etree.fromstring(entries[note_name])
            body = note_root.xpath('.//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]/p:txBody', namespaces=NS)
            if len(body) != 1:
                raise ValueError(f"Missing speaker notes for slide {number}")
            replace_body(body[0], NOTES[number].split("\n"))
            changed[note_name] = serialize(note_root)
    core = etree.fromstring(entries["docProps/core.xml"])
    for element in core:
        if etree.QName(element).localname in ("subject", "keywords"):
            element.text = "Name Race | Vibe coding, Antigravity, Skills, MCP, TypeScript, optional Gemini"
    changed["docProps/core.xml"] = serialize(core)
    with NamedTemporaryFile(dir=path.parent, suffix=".pptx", delete=False) as handle:
        temporary = Path(handle.name)
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            for info in infos:
                archive.writestr(info, changed.get(info.filename, entries[info.filename]))
        verify(temporary, entries)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Updated and verified {path.name}: 21 slides, notes, artwork, links, and timelines.")


def verify(path, before):
    deck = Presentation(path)
    assert len(deck.slides) == 21
    assert any(
        shape.has_text_frame and WEBSITE in shape.text for shape in deck.slides[0].shapes
    )
    with zipfile.ZipFile(path) as archive:
        assert set(archive.namelist()) == set(before)
        for name, original in before.items():
            current = archive.read(name)
            if name.startswith("ppt/media/"):
                assert current == original, name
            if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
                left, right = etree.fromstring(original), etree.fromstring(current)
                if name == "ppt/slides/slide1.xml":
                    left.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@id="13"]/p:spPr/a:xfrm/a:ext', namespaces=NS)[0].set("cy", str(Pt(33.5)))
                if left.xpath('.//p:sp[p:nvSpPr/p:cNvPr/@id="175"]', namespaces=NS):
                    for root in (left, right):
                        for module in qr_modules(root):
                            module.getparent().remove(module)
                for expression in (".//p:cNvPr/@id", ".//a:xfrm", ".//p:timing", ".//p:transition", ".//p:pic"):
                    def values(root):
                        return [etree.tostring(node) if not isinstance(node, str) else node
                                for node in root.xpath(expression, namespaces=NS)]
                    assert values(left) == values(right), (name, expression)
    for slide in deck.slides:
        content = "\n".join(shape.text for shape in slide.shapes if shape.has_text_frame)
        content += "\n" + slide.notes_slide.notes_text_frame.text
        for token in STALE:
            # "No ADK" explicitly describes the new demo's dependency boundary.
            cleaned = content.lower().replace("no adk", "").replace("without a model or adk", "")
            assert token not in cleaned, (token, content[:100])
        assert slide.notes_slide.notes_text_frame.text.strip()


if __name__ == "__main__":
    for filename in ("Beyond_AI_Assisted_Coding.pptx", "Beyond_AI_Assisted_Coding_Animated.pptx"):
        update(ROOT / filename)
