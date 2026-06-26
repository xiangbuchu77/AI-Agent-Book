from __future__ import annotations

import re
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
SUMMARY = ROOT / "SUMMARY.md"
OUTPUT = ROOT / "output" / "pdf" / "AI-Agent-Book-2026.pdf"
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
CJK_FONT = "AIHeiti"

TITLE = "AI Agent 开发圣经"
SUBTITLE = "从 LLM 到 Agent（2026）"
DESCRIPTION = "一本面向开发者的 AI Agent 工程实践书"

PRIMARY = colors.HexColor("#273469")
ACCENT = colors.HexColor("#16A085")
INK = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#6B7280")
LIGHT = colors.HexColor("#EEF2F7")
CODE_BG = colors.HexColor("#F4F7FA")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont(CJK_FONT, FONT_PATH, subfontIndex=0))


def clean_inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def read_summary_entries() -> list[tuple[int, str, Path]]:
    entries: list[tuple[int, str, Path]] = []
    pattern = re.compile(r"^(\s*)-\s+\[([^\]]+)\]\((docs/[^)]+\.md)\)")
    for line in SUMMARY.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if not match:
            continue
        level = 1 if len(match.group(1)) == 0 else 2
        title = match.group(2)
        path = ROOT / match.group(3)
        if path.exists():
            entries.append((level, title, path))
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
            spaceAfter=18,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            parent=base["Normal"],
            fontName=CJK_FONT,
            fontSize=20,
            leading=30,
            alignment=TA_CENTER,
            textColor=ACCENT,
            spaceAfter=32,
        ),
        "cover_desc": ParagraphStyle(
            "cover_desc",
            parent=base["Normal"],
            fontName=CJK_FONT,
            fontSize=12,
            leading=20,
            alignment=TA_CENTER,
            textColor=MUTED,
        ),
        "toc_title": ParagraphStyle(
            "toc_title",
            parent=base["Heading1"],
            fontName=CJK_FONT,
            fontSize=22,
            leading=30,
            textColor=PRIMARY,
            spaceAfter=14,
        ),
        "toc": ParagraphStyle(
            "toc",
            parent=base["Normal"],
            fontName=CJK_FONT,
            fontSize=10,
            leading=17,
            leftIndent=0,
            textColor=INK,
        ),
        "toc_sub": ParagraphStyle(
            "toc_sub",
            parent=base["Normal"],
            fontName=CJK_FONT,
            fontSize=9,
            leading=15,
            leftIndent=14,
            textColor=MUTED,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName=CJK_FONT,
            fontSize=22,
            leading=30,
            textColor=PRIMARY,
            spaceBefore=10,
            spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName=CJK_FONT,
            fontSize=15,
            leading=22,
            textColor=ACCENT,
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName=CJK_FONT,
            fontSize=12,
            leading=18,
            textColor=PRIMARY,
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName=CJK_FONT,
            fontSize=10.5,
            leading=18,
            alignment=TA_LEFT,
            textColor=INK,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontName=CJK_FONT,
            fontSize=10,
            leading=17,
            textColor=INK,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=8,
            leading=11,
            backColor=CODE_BG,
            borderColor=colors.HexColor("#D8DEE9"),
            borderWidth=0.5,
            borderPadding=6,
            textColor=colors.HexColor("#111827"),
        ),
    }


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
                ListItem(Paragraph(clean_inline(item), styles["bullet"]), leftIndent=8)
                for item in bullets
            ]
            flowables.append(
                ListFlowable(
                    items,
                    bulletType="bullet",
                    start="circle",
                    leftIndent=18,
                    bulletFontName=CJK_FONT,
                    bulletFontSize=8,
                    bulletColor=ACCENT,
                )
            )
            flowables.append(Spacer(1, 5))
            bullets = []

    def flush_code() -> None:
        nonlocal code
        if code:
            flowables.append(Preformatted("\n".join(code), styles["code"]))
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
        if line.startswith("# "):
            flush_paragraph()
            flush_bullets()
            flowables.append(Paragraph(clean_inline(line[2:]), styles["h1"]))
            flowables.append(HRFlowable(width="100%", thickness=1, color=LIGHT, spaceAfter=8))
        elif line.startswith("## "):
            flush_paragraph()
            flush_bullets()
            flowables.append(Paragraph(clean_inline(line[3:]), styles["h2"]))
        elif line.startswith("### "):
            flush_paragraph()
            flush_bullets()
            flowables.append(Paragraph(clean_inline(line[4:]), styles["h3"]))
        elif line.startswith("- "):
            flush_paragraph()
            bullets.append(line[2:])
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
        canvas.rect(0, height - 2.2 * cm, width, 2.2 * cm, stroke=0, fill=1)
        canvas.setFillColor(ACCENT)
        canvas.rect(0, 0, width, 0.45 * cm, stroke=0, fill=1)
    else:
        canvas.setStrokeColor(LIGHT)
        canvas.line(1.8 * cm, height - 1.45 * cm, width - 1.8 * cm, height - 1.45 * cm)
        canvas.setFillColor(MUTED)
        canvas.setFont(CJK_FONT, 8)
        canvas.drawString(1.8 * cm, height - 1.2 * cm, "AI Agent 开发圣经：从 LLM 到 Agent（2026）")
        canvas.drawRightString(width - 1.8 * cm, 1.1 * cm, str(page))
        canvas.setStrokeColor(LIGHT)
        canvas.line(1.8 * cm, 1.45 * cm, width - 1.8 * cm, 1.45 * cm)
    canvas.restoreState()


def build_pdf() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    entries = read_summary_entries()

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=1.9 * cm,
        rightMargin=1.9 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title=f"{TITLE}：{SUBTITLE}",
        author="AI-Agent-Book",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="book", frames=[frame], onPage=draw_page)])

    story = [
        Spacer(1, 4.8 * cm),
        Paragraph(TITLE, styles["cover_title"]),
        Paragraph(SUBTITLE, styles["cover_subtitle"]),
        Paragraph(DESCRIPTION, styles["cover_desc"]),
        Spacer(1, 1.2 * cm),
        HRFlowable(width="55%", thickness=1.2, color=ACCENT, hAlign="CENTER"),
        Spacer(1, 0.8 * cm),
        Paragraph("Generated from the AI-Agent-Book MkDocs source.", styles["cover_desc"]),
        PageBreak(),
        Paragraph("目录", styles["toc_title"]),
    ]

    for level, title, _ in entries:
        style = styles["toc"] if level == 1 else styles["toc_sub"]
        prefix = "" if level == 1 else "    "
        story.append(Paragraph(clean_inline(f"{prefix}{title}"), style))
    story.append(PageBreak())

    for index, (_, _, path) in enumerate(entries):
        if index > 0:
            story.append(PageBreak())
        story.extend(markdown_to_flowables(path, styles))

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
