from __future__ import annotations

import re
import textwrap
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
)
from reportlab.platypus.flowables import HRFlowable


ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "book"
SUMMARY = BOOK_DIR / "SUMMARY.md"
OUTPUT = ROOT / "output" / "pdf" / "AI-Agent-Book-2026.pdf"
SITE_PDF = ROOT / "docs" / "assets" / "pdf" / "AI-Agent-Book-2026.pdf"

FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
CJK_FONT = "AIHeiti"

TITLE = "AI Agent 开发圣经"
SUBTITLE = "从 LLM 到 Agent（2026）"
DESCRIPTION = "完整版教材工程版｜LLM · Prompt · RAG · Agent · Tools · LangGraph · MCP"

PRIMARY = colors.HexColor("#1F2A5A")
ACCENT = colors.HexColor("#0F9F8F")
ACCENT_DARK = colors.HexColor("#087C70")
INK = colors.HexColor("#111827")
MUTED = colors.HexColor("#64748B")
LIGHT = colors.HexColor("#E6ECF4")
SOFT = colors.HexColor("#F7FAFC")
CODE_BG = colors.HexColor("#F1F5F9")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont(CJK_FONT, FONT_PATH, subfontIndex=0))


def strip_emoji(text: str) -> str:
    # Keep PDF rendering stable with the bundled macOS CJK font.
    return re.sub(
        r"[\U0001F300-\U0001FAFF\u2600-\u27BF]",
        "",
        text,
    ).strip()


def clean_inline(text: str) -> str:
    text = strip_emoji(text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("❌", "x").replace("✔", "OK").replace("👉", "=>")
    return text


def read_summary_entries() -> list[tuple[str, Path]]:
    entries: list[tuple[str, Path]] = []
    pattern = re.compile(r"^-\s+\[([^\]]+)\]\(([^)]+/index\.md)\)")
    in_archive = False
    for line in SUMMARY.read_text(encoding="utf-8").splitlines():
        if line.strip() == "## Archive":
            in_archive = True
            continue
        if in_archive:
            continue
        match = pattern.match(line)
        if not match:
            continue
        title = match.group(1)
        path = BOOK_DIR / match.group(2)
        if path.exists():
            entries.append((title, path))
    return entries


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "cover_title",
            parent=base["Title"],
            fontName=CJK_FONT,
            fontSize=34,
            leading=44,
            alignment=TA_CENTER,
            textColor=PRIMARY,
            spaceAfter=16,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            parent=base["Normal"],
            fontName=CJK_FONT,
            fontSize=18,
            leading=28,
            alignment=TA_CENTER,
            textColor=ACCENT_DARK,
            spaceAfter=28,
        ),
        "cover_desc": ParagraphStyle(
            "cover_desc",
            parent=base["Normal"],
            fontName=CJK_FONT,
            fontSize=10.5,
            leading=18,
            alignment=TA_CENTER,
            textColor=MUTED,
        ),
        "toc_title": ParagraphStyle(
            "toc_title",
            parent=base["Heading1"],
            fontName=CJK_FONT,
            fontSize=24,
            leading=32,
            textColor=PRIMARY,
            spaceAfter=18,
        ),
        "toc": ParagraphStyle(
            "toc",
            parent=base["Normal"],
            fontName=CJK_FONT,
            fontSize=11,
            leading=19,
            textColor=INK,
            leftIndent=2,
            spaceAfter=4,
        ),
        "chapter_kicker": ParagraphStyle(
            "chapter_kicker",
            parent=base["Normal"],
            fontName=CJK_FONT,
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=ACCENT_DARK,
            spaceAfter=16,
        ),
        "chapter_title": ParagraphStyle(
            "chapter_title",
            parent=base["Title"],
            fontName=CJK_FONT,
            fontSize=26,
            leading=36,
            alignment=TA_CENTER,
            textColor=PRIMARY,
            spaceAfter=16,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName=CJK_FONT,
            fontSize=21,
            leading=29,
            textColor=PRIMARY,
            spaceBefore=8,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName=CJK_FONT,
            fontSize=14.5,
            leading=22,
            textColor=ACCENT_DARK,
            spaceBefore=13,
            spaceAfter=7,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName=CJK_FONT,
            fontSize=12,
            leading=18,
            textColor=PRIMARY,
            spaceBefore=9,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName=CJK_FONT,
            fontSize=10.2,
            leading=17.2,
            alignment=TA_LEFT,
            textColor=INK,
            spaceAfter=6,
        ),
        "quote": ParagraphStyle(
            "quote",
            parent=base["BodyText"],
            fontName=CJK_FONT,
            fontSize=11,
            leading=18,
            leftIndent=14,
            rightIndent=10,
            borderColor=ACCENT,
            borderWidth=1,
            borderPadding=7,
            backColor=SOFT,
            textColor=PRIMARY,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontName=CJK_FONT,
            fontSize=10,
            leading=16.5,
            textColor=INK,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName=CJK_FONT,
            fontSize=7.8,
            leading=10.5,
            backColor=CODE_BG,
            borderColor=colors.HexColor("#CBD5E1"),
            borderWidth=0.4,
            borderPadding=6,
            textColor=colors.HexColor("#0F172A"),
        ),
    }


def wrapped_code(lines: list[str]) -> str:
    wrapped: list[str] = []
    for line in lines:
        if len(line) <= 92:
            wrapped.append(line)
            continue
        wrapped.extend(textwrap.wrap(line, width=92, subsequent_indent="    ", replace_whitespace=False))
    return "\n".join(wrapped)


def markdown_to_flowables(path: Path, styles: dict[str, ParagraphStyle]) -> list:
    flowables = []
    lines = path.read_text(encoding="utf-8").splitlines()
    paragraph: list[str] = []
    bullets: list[str] = []
    code: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            flowables.append(Paragraph(clean_inline(" ".join(paragraph)), styles["body"]))
            paragraph = []

    def flush_bullets() -> None:
        nonlocal bullets
        if bullets:
            items = [
                ListItem(Paragraph(clean_inline(item), styles["bullet"]), leftIndent=7)
                for item in bullets
            ]
            flowables.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                    start="circle",
                    leftIndent=18,
                    bulletFontName=CJK_FONT,
                    bulletFontSize=7,
                    bulletColor=ACCENT,
                )
            )
            flowables.append(Spacer(1, 4))
            bullets = []

    def flush_code() -> None:
        nonlocal code
        if code:
            flowables.append(Preformatted(wrapped_code(code), styles["code"]))
            flowables.append(Spacer(1, 7))
            code = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_paragraph()
                flush_bullets()
                in_code = True
            continue
        if in_code:
            code.append(line)
            continue
        if not line.strip():
            flush_paragraph()
            flush_bullets()
            continue
        if line.strip() == "---":
            flush_paragraph()
            flush_bullets()
            flowables.append(HRFlowable(width="100%", thickness=0.6, color=LIGHT, spaceBefore=6, spaceAfter=8))
        elif line.startswith("# "):
            flush_paragraph()
            flush_bullets()
            flowables.append(Paragraph(clean_inline(line[2:]), styles["h1"]))
            flowables.append(HRFlowable(width="100%", thickness=1, color=LIGHT, spaceAfter=7))
        elif line.startswith("## "):
            flush_paragraph()
            flush_bullets()
            flowables.append(Paragraph(clean_inline(line[3:]), styles["h2"]))
        elif line.startswith("### "):
            flush_paragraph()
            flush_bullets()
            flowables.append(Paragraph(clean_inline(line[4:]), styles["h3"]))
        elif line.startswith("> "):
            flush_paragraph()
            flush_bullets()
            flowables.append(Paragraph(clean_inline(line[2:]), styles["quote"]))
        elif line.startswith("- "):
            flush_paragraph()
            bullets.append(line[2:])
        elif re.match(r"^\d+\.\s+", line):
            flush_paragraph()
            bullets.append(re.sub(r"^\d+\.\s+", "", line))
        elif line.startswith("|"):
            flush_paragraph()
            flush_bullets()
            if set(line.replace("|", "").strip()) <= {"-", " "}:
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            flowables.append(Paragraph(clean_inline(" / ".join(cells)), styles["body"]))
        else:
            paragraph.append(line)
    flush_paragraph()
    flush_bullets()
    flush_code()
    return flowables


def draw_page(canvas, doc) -> None:
    page = canvas.getPageNumber()
    width, height = A4
    canvas.saveState()
    if page == 1:
        canvas.setFillColor(PRIMARY)
        canvas.rect(0, height - 2.35 * cm, width, 2.35 * cm, stroke=0, fill=1)
        canvas.setFillColor(ACCENT)
        canvas.rect(0, 0, width, 0.5 * cm, stroke=0, fill=1)
        canvas.setFillColor(colors.HexColor("#EAF7F5"))
        canvas.circle(width - 2.4 * cm, height - 1.15 * cm, 0.35 * cm, stroke=0, fill=1)
    else:
        canvas.setStrokeColor(LIGHT)
        canvas.line(1.65 * cm, height - 1.45 * cm, width - 1.65 * cm, height - 1.45 * cm)
        canvas.setFillColor(MUTED)
        canvas.setFont(CJK_FONT, 8)
        canvas.drawString(1.65 * cm, height - 1.18 * cm, "AI Agent 开发圣经：从 LLM 到 Agent（2026）")
        canvas.drawRightString(width - 1.65 * cm, height - 1.18 * cm, "AI-Agent-Book")
        canvas.setFillColor(PRIMARY)
        canvas.drawCentredString(width / 2, 1.0 * cm, str(page))
        canvas.setStrokeColor(LIGHT)
        canvas.line(1.65 * cm, 1.42 * cm, width - 1.65 * cm, 1.42 * cm)
    canvas.restoreState()


def chapter_divider(title: str, index: int, styles: dict[str, ParagraphStyle]) -> list:
    return [
        Spacer(1, 5.2 * cm),
        Paragraph(f"Chapter {index:02d}", styles["chapter_kicker"]),
        Paragraph(clean_inline(title), styles["chapter_title"]),
        HRFlowable(width="42%", thickness=1.2, color=ACCENT, hAlign="CENTER", spaceBefore=4, spaceAfter=10),
        Paragraph("Story · Technical · Diagram · Code · Engineering · Interview", styles["cover_desc"]),
        PageBreak(),
    ]


def build_pdf() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    SITE_PDF.parent.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    entries = read_summary_entries()

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=1.65 * cm,
        rightMargin=1.65 * cm,
        topMargin=1.75 * cm,
        bottomMargin=1.65 * cm,
        title=f"{TITLE}：{SUBTITLE}",
        author="AI-Agent-Book",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="book", frames=[frame], onPage=draw_page)])

    story = [
        Spacer(1, 4.9 * cm),
        Paragraph(TITLE, styles["cover_title"]),
        Paragraph(SUBTITLE, styles["cover_subtitle"]),
        Paragraph(DESCRIPTION, styles["cover_desc"]),
        Spacer(1, 1.0 * cm),
        HRFlowable(width="58%", thickness=1.3, color=ACCENT, hAlign="CENTER"),
        Spacer(1, 0.7 * cm),
        Paragraph("Generated from the latest book/ source.", styles["cover_desc"]),
        PageBreak(),
        Paragraph("目录", styles["toc_title"]),
    ]

    for index, (title, _) in enumerate(entries, 1):
        story.append(Paragraph(f"{index:02d}. {clean_inline(title)}", styles["toc"]))
    story.append(PageBreak())

    for index, (title, path) in enumerate(entries, 1):
        story.extend(chapter_divider(title, index, styles))
        story.extend(markdown_to_flowables(path, styles))
        story.append(PageBreak())

    doc.build(story)
    SITE_PDF.write_bytes(OUTPUT.read_bytes())
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
