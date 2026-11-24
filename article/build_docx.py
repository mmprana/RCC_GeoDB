"""
Build a Transactions in GIS manuscript .docx from the working Markdown files.

Run with:
    /tmp/opencode/venv/bin/python build_docx.py

Requires python-docx.
"""

import os
import re
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
MANUSCRIPT = os.path.join(HERE, "MANUSCRIPT_DRAFT.md")
REFERENCES = os.path.join(HERE, "REFERENCES_APA.md")
OUT = os.path.join(HERE, "RCC_GeoDB_Manuscript_TIG.docx")

TITLE = "Making the City Legible: A Human-Centred Geodatabase for Urban Planning and Local Government in Bangladesh"
RUNNING_TITLE = "Making the City Legible in Rajshahi"

ABSTRACT = ("Bangladeshi city corporations hold spatial information in paper maps, Excel registers, "
            "and departmental files. This article asks how Rajshahi City Corporation can build a "
            "maintainable, human-centred geodatabase from that starting point. Drawing on a scoping "
            "review, 11 interviews, and a proof-of-concept schema, it proposes an address-centred data "
            "model, a common asset registry, a staged validation pipeline, a governance framework, and "
            "a phased roadmap. The interviews reveal departmental silos, an address gap, a "
            "cadastral–holding tax disconnect, the absence of a shared asset register, and strong demand "
            "for a Spatial Services Unit and selective publication. The article argues that the binding "
            "constraint is stewardship, not software, and that making the city legible need not make it "
            "surveilled. It contributes a context-sensitive municipal spatial data infrastructure model "
            "for Bangladesh and a humanistic account of GIS as public infrastructure.")

KEYWORDS = "municipal GIS; spatial data infrastructure; geodatabase; data governance; urban planning; Bangladesh"


def set_run_font(run, name="Times New Roman", size=12, bold=None, italic=None):
    run.font.name = name
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:eastAsia"), name)


def add_runs(paragraph, text, size=12):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("`", "")
    parts = re.split(r"(\*\*.*?\*\*|\*.*?\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            set_run_font(run, size=size, bold=True)
        elif part.startswith("*") and part.endswith("*"):
            run = paragraph.add_run(part[1:-1])
            set_run_font(run, size=size, italic=True)
        else:
            run = paragraph.add_run(part)
            set_run_font(run, size=size)


def style_document(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 2.0
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.space_before = Pt(0)

    for style_name in ("Heading 1", "Heading 2", "Heading 3"):
        style = doc.styles[style_name]
        style.font.name = "Times New Roman"
        style.font.size = Pt(12)
        style.font.bold = True
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.keep_with_next = True

    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        section.different_first_page_header_footer = True

        # Continuous line numbering
        sectPr = section._sectPr
        ln = OxmlElement("w:lnNumType")
        ln.set(qn("w:countBy"), "1")
        ln.set(qn("w:restart"), "continuous")
        sectPr.append(ln)

        # Page number in footer
        footer_p = section.footer.paragraphs[0]
        footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = footer_p.add_run()
        fld = OxmlElement("w:fldSimple")
        fld.set(qn("w:instr"), "PAGE")
        run._r.append(fld)
        set_run_font(run, size=10)

        # Running title in header (not first page)
        header_p = section.header.paragraphs[0]
        header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = header_p.add_run(RUNNING_TITLE)
        set_run_font(run, size=9, italic=True)


def add_title_page(doc, main_word_count):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_runs(p, TITLE, size=14)
    for run in p.runs:
        run.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_runs(p, "Manuscript prepared for Transactions in GIS", size=12)

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
        ("Tables and figures: ", "2 tables; 6 figures (supplied separately)"),
    ]
    for label, value in lines:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        run = p.add_run(label)
        set_run_font(run, bold=True)
        add_runs(p, value)

    doc.add_page_break()


def add_abstract_page(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_runs(p, TITLE, size=14)
    for run in p.runs:
        run.bold = True

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.add_run("Abstract").bold = True
    for run in p.runs:
        set_run_font(run, size=12, bold=True)

    p = doc.add_paragraph()
    add_runs(p, ABSTRACT, size=12)

    p = doc.add_paragraph()
    run = p.add_run("Keywords: ")
    set_run_font(run, bold=True)
    add_runs(p, KEYWORDS, size=12)

    doc.add_page_break()


def add_table_from_lines(doc, caption, table_lines, note=None):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(caption)
    set_run_font(run, size=10, bold=True)

    rows = []
    for line in table_lines:
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        rows.append(cells)
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.style = "Table Grid"
    table.autofit = True
    for i, row in enumerate(rows):
        for j in range(ncols):
            cell = table.cell(i, j)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(0)
            text = row[j] if j < len(row) else ""
            add_runs(p, text, size=9)
            if i == 0:
                for run in p.runs:
                    run.bold = True

    if note:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(3)
        add_runs(p, note, size=9)


def extract_table(md, caption_start):
    lines = md.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith(caption_start):
            start = i
            break
    if start is None:
        return []
    out = []
    in_table = False
    for line in lines[start + 1:]:
        if line.strip().startswith("|"):
            in_table = True
            out.append(line)
        elif in_table:
            break
    return out


def add_main_text(doc, md):
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
                    add_runs(p, "The architecture is summarised in Figure 2.", size=12)
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

        # Skip Markdown tables; they are placed after the references.
        if stripped.startswith("|"):
            while i < len(lines) and lines[i].strip().startswith("|"):
                i += 1
            continue

        # Skip figure placeholders; legends are placed at the end.
        if stripped.startswith("!["):
            i += 1
            continue

        if stripped.startswith("### "):
            p = doc.add_paragraph(style="Heading 2")
            add_runs(p, stripped[4:], size=12)
            i += 1
            continue

        if stripped.startswith("## "):
            p = doc.add_paragraph(style="Heading 1")
            add_runs(p, stripped[3:], size=12)
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
            add_runs(p, " ".join(quote), size=11)
            for run in p.runs:
                run.italic = True
            continue

        if re.match(r"^[-*]\s+", stripped):
            p = doc.add_paragraph(style="List Bullet")
            add_runs(p, re.sub(r"^[-*]\s+", "", stripped), size=12)
            i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            p = doc.add_paragraph(style="List Number")
            add_runs(p, re.sub(r"^\d+\.\s+", "", stripped), size=12)
            i += 1
            continue

        # Ordinary paragraph: collect until blank or a structural marker.
        para = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (not nxt or nxt.startswith("#") or nxt.startswith("|") or
                nxt.startswith(">") or nxt.startswith("![") or
                nxt.startswith("```") or re.match(r"^[-*]\s+", nxt) or
                re.match(r"^\d+\.\s+", nxt)):
                break
            para.append(nxt)
            i += 1
        p = doc.add_paragraph()
        add_runs(p, " ".join(para), size=12)


def add_references(doc):
    doc.add_page_break()
    p = doc.add_paragraph(style="Heading 1")
    add_runs(p, "References", size=12)

    entries = []
    with open(REFERENCES, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line.startswith("- "):
                entries.append(line[2:].strip())
    entries.sort(key=lambda s: s.lower())

    for entry in entries:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        add_runs(p, entry, size=12)


def add_tables(doc, md):
    doc.add_page_break()
    p = doc.add_paragraph(style="Heading 1")
    add_runs(p, "Tables", size=12)

    table1 = extract_table(md, "**Table 1.")
    add_table_from_lines(
        doc,
        "Table 1. Interview sample",
        table1,
        "Note. Purposive sample. P01 and P02 are paired planner perspectives; P03 and P05 are paired councillor perspectives. P10 is used only as a public-perspective illustration."
    )

    doc.add_page_break()
    table2 = extract_table(md, "**Table 2.")
    add_table_from_lines(
        doc,
        "Table 2. From interview findings to design responses",
        table2,
        "Note. Design responses derived from the themes reported in Section 6."
    )


def add_figure_legends(doc):
    doc.add_page_break()
    p = doc.add_paragraph(style="Heading 1")
    add_runs(p, "Figure Legends", size=12)

    legends = [
        "Figure 1. Current paper/Excel workflow versus proposed digital workflow.",
        "Figure 2. System architecture: capture, staging, validation, production geodatabase, and publication.",
        "Figure 3. Simplified entity-relationship diagram for the core municipal data model.",
        "Figure 4. Data lifecycle and validation pipeline.",
        "Figure 5. Data governance framework.",
        "Figure 6. Phased implementation roadmap.",
    ]
    for legend in legends:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        add_runs(p, legend, size=12)

    p = doc.add_paragraph()
    add_runs(p, "Figures are supplied as separate files in the highest available resolution.", size=12)


def add_appendices(doc):
    doc.add_page_break()
    p = doc.add_paragraph(style="Heading 1")
    add_runs(p, "Appendices", size=12)

    items = [
        ("Appendix A. Layer catalogue.", "Provided as a supplementary file (RCC_Layer_Summary.csv and README.md)."),
        ("Appendix B. Data dictionary excerpt.", "Provided as a supplementary file (DATA_DICTIONARY_EXCERPT.md)."),
        ("Appendix C. Relational database design.", "Provided as a supplementary file (ERD.md)."),
        ("Appendix D. Data governance framework.", "Provided as a supplementary file (GOVERNANCE_FRAMEWORK.md)."),
        ("Appendix E. Implementation roadmap.", "Provided as a supplementary file (IMPLEMENTATION_ROADMAP.md)."),
        ("Appendix F. Interview guide and coding frame.", "Provided as supplementary files (INTERVIEW_GUIDE.md and CODING_FRAME.md)."),
        ("Appendix G. Literature matrix.", "Provided as a supplementary file (LITERATURE_MATRIX.csv)."),
    ]
    for label, value in items:
        p = doc.add_paragraph()
        run = p.add_run(label + " ")
        set_run_font(run, bold=True)
        add_runs(p, value, size=12)


def main():
    md = open(MANUSCRIPT, encoding="utf-8").read()
    main_start = md.index("## 1. Introduction")
    main_end = md.index("## References")
    main_word_count = len(re.findall(r"\b\w+\b", md[main_start:main_end]))

    doc = Document()
    style_document(doc)
    doc.core_properties.title = TITLE
    doc.core_properties.subject = "Transactions in GIS manuscript"
    doc.core_properties.author = "[Author One]; [Author Two]"

    add_title_page(doc, main_word_count)
    add_abstract_page(doc)
    add_main_text(doc, md)
    add_references(doc)
    add_tables(doc, md)
    add_figure_legends(doc)
    add_appendices(doc)

    doc.save(OUT)
    print(f"Wrote {OUT}")
    print(f"Abstract words: {len(ABSTRACT.split())}")
    print(f"Main text words: {main_word_count}")


if __name__ == "__main__":
    main()
