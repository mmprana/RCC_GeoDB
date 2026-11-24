"""
Build an illustrated review copy of the Transactions in GIS manuscript.

This version places tables and figures inline so they are visible when the
document is opened. The journal submission version keeps tables after the
reference list and figures as separate files.

Run with:
    /tmp/opencode/venv/bin/python build_docx_illustrated.py
"""

import os
import re

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

import build_docx as base

HERE = os.path.dirname(os.path.abspath(__file__))
MANUSCRIPT = os.path.join(HERE, "MANUSCRIPT_DRAFT.md")
FIGDIR = os.path.join(HERE, "figures")
OUT = os.path.join(HERE, "RCC_GeoDB_Manuscript_TIG_Illustrated.docx")

TITLE = base.TITLE
RUNNING_TITLE = base.RUNNING_TITLE
ABSTRACT = base.ABSTRACT
KEYWORDS = base.KEYWORDS


def add_illustrated_title_page(doc, main_word_count):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    base.add_runs(p, TITLE, size=14)
    for run in p.runs:
        run.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    base.add_runs(p, "Illustrated review copy — Transactions in GIS", size=12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    base.add_runs(
        p,
        "Tables and figures are placed inline for review. The journal submission "
        "version follows the separate-file and end-of-manuscript table requirements.",
        size=10,
    )
    for run in p.runs:
        run.italic = True

    doc.add_paragraph()
    lines = [
        ("Running title: ", RUNNING_TITLE),
        ("Manuscript type: ", "Original research article"),
        ("Authors: ", "[Author One], [Author Two]"),
        ("Affiliations: ", "[Department, University, City, Country]"),
        ("Corresponding author: ", "[Name, email address, ORCID]"),
        ("Conflict of interest: ", "The authors declare no conflict of interest."),
        ("Funding: ", "[Funding statement to be inserted]"),
        ("Acknowledgements: ", "[Acknowledgements to be inserted]"),
        ("Ethics statement: ", "[Ethics approval body and approval number to be inserted]"),
        ("Data availability: ", "The geodatabase schema, data dictionary, and build scripts are available at https://github.com/mprgesru/RCC_GeoDB and https://github.com/mmprana/RCC_GeoDB. RCC operational data and interview data are not publicly available because of confidentiality and privacy commitments. Anonymised excerpts are included in the article."),
        ("Abstract word count: ", f"{len(ABSTRACT.split())} words"),
        ("Main text word count: ", f"approximately {main_word_count:,} words"),
        ("Tables and figures: ", "3 tables; 6 figures (embedded in this review copy)"),
    ]
    for label, value in lines:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(label)
        base.set_run_font(run, bold=True)
        base.add_runs(p, value)

    doc.add_page_break()


def add_abstract_page(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    base.add_runs(p, TITLE, size=14)
    for run in p.runs:
        run.bold = True

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    run = p.add_run("Abstract")
    base.set_run_font(run, size=12, bold=True)

    p = doc.add_paragraph()
    base.add_runs(p, ABSTRACT, size=12)

    p = doc.add_paragraph()
    run = p.add_run("Keywords: ")
    base.set_run_font(run, bold=True)
    base.add_runs(p, KEYWORDS, size=12)

    doc.add_page_break()


def add_figure(doc, filename, caption, width=6.1):
    path = os.path.join(FIGDIR, filename)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    run = p.add_run()
    run.add_picture(path, width=Inches(width))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(caption)
    base.set_run_font(run, size=9, italic=True)


def add_table_block(doc, lines, caption, note):
    base.add_table_from_lines(doc, caption, lines, note)
    doc.add_paragraph()


def add_illustrated_main_text(doc, md):
    start = md.index("## 1. Introduction")
    end = md.index("## References")
    text = md[start:end]
    lines = text.splitlines()

    i = 0
    in_code = False
    code_lines = []
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                if code_lines and code_lines[0].startswith("Paper maps"):
                    p = doc.add_paragraph()
                    base.add_runs(p, "The architecture is summarised in Figure 2.", size=12)
            i += 1
            continue
        if in_code:
            code_lines.append(stripped)
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        if stripped in ("---", "***", "___"):
            i += 1
            continue

        # Insert figures before selected headings.
        if stripped == "### 7.4 Data model":
            add_figure(doc, "fig2_architecture.png",
                       "Figure 2. System architecture: capture, staging, validation, production geodatabase, and publication.")
        if stripped == "### 7.5 Address gazetteer":
            add_figure(doc, "fig3_erd.png",
                       "Figure 3. Simplified entity-relationship diagram for the core municipal data model.")
        if stripped == "### 7.8 Governance":
            add_figure(doc, "fig4_lifecycle.png",
                       "Figure 4. Data lifecycle and validation pipeline.")
        if stripped == "### 7.9 Implementation roadmap":
            add_figure(doc, "fig5_governance.png",
                       "Figure 5. Data governance framework.")
        if stripped == "## 8. Discussion":
            add_figure(doc, "fig6_roadmap.png",
                       "Figure 6. Phased implementation roadmap.")

        # Figure 1 placeholder.
        if stripped.startswith("![Figure 1"):
            add_figure(doc, "fig1_workflow.png",
                       "Figure 1. Current paper/Excel workflow versus proposed digital workflow.")
            i += 1
            continue

        # Table 1 and Table 2 captions + tables.
        if stripped.startswith("**Table 1."):
            caption = stripped.strip("*")
            table_lines = []
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("|"):
                j += 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                table_lines.append(lines[j])
                j += 1
            add_table_block(
                doc, table_lines, caption,
                "Note. Purposive sample. P01 and P02 are paired planner perspectives; P03 and P05 are paired councillor perspectives. P10 is used only as a public-perspective illustration."
            )
            i = j
            continue

        if stripped.startswith("**Table 2."):
            caption = stripped.strip("*")
            table_lines = []
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("|"):
                j += 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                table_lines.append(lines[j])
                j += 1
            add_table_block(
                doc, table_lines, caption,
                "Note. Design responses derived from the themes reported in Section 6."
            )
            i = j
            continue

        # Unnumbered roadmap table.
        if stripped.startswith("|"):
            table_lines = []
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                table_lines.append(lines[j])
                j += 1
            add_table_block(
                doc, table_lines, "Table 3. Implementation roadmap",
                "Note. Decision gates G1–G5 are shown in Figure 6."
            )
            i = j
            continue

        if stripped.startswith("### "):
            p = doc.add_paragraph(style="Heading 2")
            base.add_runs(p, stripped[4:], size=12)
            i += 1
            continue

        if stripped.startswith("## "):
            p = doc.add_paragraph(style="Heading 1")
            base.add_runs(p, stripped[3:], size=12)
            i += 1
            continue

        if stripped.startswith("> "):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.right_indent = Inches(0.5)
            base.add_runs(p, " ".join(quote), size=11)
            for run in p.runs:
                run.italic = True
            continue

        if re.match(r"^[-*]\s+", stripped):
            p = doc.add_paragraph(style="List Bullet")
            base.add_runs(p, re.sub(r"^[-*]\s+", "", stripped), size=12)
            i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            p = doc.add_paragraph(style="List Number")
            base.add_runs(p, re.sub(r"^\d+\.\s+", "", stripped), size=12)
            i += 1
            continue

        para = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith("#") or nxt.startswith("|") or
                nxt.startswith(">") or nxt.startswith("![") or
                nxt.startswith("```") or nxt.startswith("**Table") or
                re.match(r"^[-*]\s+", nxt) or re.match(r"^\d+\.\s+", nxt)):
                break
            para.append(nxt)
            i += 1
        p = doc.add_paragraph()
        base.add_runs(p, " ".join(para), size=12)


def main():
    md = open(MANUSCRIPT, encoding="utf-8").read()
    main_start = md.index("## 1. Introduction")
    main_end = md.index("## References")
    main_word_count = len(re.findall(r"\b\w+\b", md[main_start:main_end]))

    doc = Document()
    base.style_document(doc)
    doc.core_properties.title = TITLE
    doc.core_properties.subject = "Transactions in GIS illustrated review copy"
    doc.core_properties.author = "[Author One]; [Author Two]"

    add_illustrated_title_page(doc, main_word_count)
    add_abstract_page(doc)
    add_illustrated_main_text(doc, md)
    base.add_references(doc)
    base.add_figure_legends(doc)
    base.add_appendices(doc)

    doc.save(OUT)
    print(f"Wrote {OUT}")
    print(f"Abstract words: {len(ABSTRACT.split())}")
    print(f"Main text words: {main_word_count}")


if __name__ == "__main__":
    main()
