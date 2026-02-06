import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

ROOT = Path(__file__).parent

DOCS = [
    ("DOCUMENTACAO-USUARIO.md", "DOCUMENTACAO-USUARIO.pdf"),
    ("DOCUMENTACAO-TECNICA.md", "DOCUMENTACAO-TECNICA.pdf"),
    ("TECNOLOGIAS.md", "TECNOLOGIAS.pdf"),
]

def md_to_story(md_text):
    styles = getSampleStyleSheet()
    heading1 = styles["Heading1"]
    heading2 = styles["Heading2"]
    heading3 = styles["Heading3"]
    body = styles["BodyText"]
    code_style = ParagraphStyle(
        "Code",
        parent=body,
        fontName="Courier",
        fontSize=9,
        leading=11,
        alignment=TA_LEFT,
    )

    story = []
    in_code_block = False
    buffer_code = []

    for raw_line in md_text.splitlines():
        line = raw_line.rstrip()

        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                buffer_code = []
            else:
                in_code_block = False
                if buffer_code:
                    code_text = "<br/>".join(buffer_code)
                    story.append(Paragraph(code_text, code_style))
                    story.append(Spacer(1, 8))
                buffer_code = []
            continue

        if in_code_block:
            buffer_code.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue

        if not line.strip():
            story.append(Spacer(1, 8))
            continue

        if line.startswith("# "):
            story.append(Paragraph(line[2:], heading1))
            story.append(Spacer(1, 8))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], heading2))
            story.append(Spacer(1, 6))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], heading3))
            story.append(Spacer(1, 6))
        elif line.startswith("- "):
            story.append(Paragraph("• " + line[2:], body))
        else:
            story.append(Paragraph(line, body))

    return story

def export_markdown_to_pdf(md_path: Path, pdf_path: Path):
    with md_path.open("r", encoding="utf-8") as f:
        md_text = f.read()
    story = md_to_story(md_text)
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    doc.build(story)

def main():
    for md_name, pdf_name in DOCS:
        md_path = ROOT / md_name
        pdf_path = ROOT / pdf_name
        if not md_path.exists():
            print(f"[WARN] Arquivo Markdown não encontrado: {md_path}")
            continue
        export_markdown_to_pdf(md_path, pdf_path)
        print(f"[OK] Gerado: {pdf_path}")

if __name__ == "__main__":
    main()
