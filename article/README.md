# Article Package

Working materials for:

**Making the City Legible: A Human-Centred Geodatabase for Urban Planning and Local Government in Bangladesh**

Case: Rajshahi City Corporation (RCC)
Method: scoping review + embedded case study + design science research
Target: *Transactions in GIS* (primary); *Cities*; *Habitat International*; *International Journal of Geographical Information Science*

---

## Files

| File | Purpose |
|---|---|
| `ARTICLE_PLAN.md` | Full article plan: abstract, research questions, theory, method, structure, figures, timeline |
| `JOURNAL_FIT_TRANSACTIONS_IN_GIS.md` | Journal fit, framing, data availability, reviewer concerns |
| `LITERATURE_MATRIX.csv` | 70-source literature matrix with themes, arguments, benefits, complexities, solutions, relevance |
| `LITERATURE_REVIEW_DRAFT.md` | Draft literature review (~2,700 words) |
| `REFERENCES_APA.md` | Working APA 7 reference list generated from Crossref metadata |
| `REFERENCES.bib` | BibTeX for reference management |
| `build_references.py` | Reproducible reference builder from `LITERATURE_MATRIX.csv` |
| `CASE_NOTES.md` | Notes on Perth, Wollongong, Camden, Wodonga and other comparators |
| `FIGURE_SPECS.md` | Mermaid drafts for research design, workflows, architecture, ERD, governance, roadmap |
| `DATA_DICTIONARY_EXCERPT.md` | Article-ready data dictionary for parcel, building, address, road, drain, bin, asset registry |
| `ERD.md` | Relational design, cardinalities, key decisions |
| `GOVERNANCE_FRAMEWORK.md` | Principles, roles, RACI, policies, processes, maturity, financing, KPIs |
| `IMPLEMENTATION_ROADMAP.md` | Phases, decision gates, risks, costs, KPIs |
| `MANUSCRIPT_DRAFT.md` | Working full draft (~8,900 words) |
| `RCC_GeoDB_Manuscript_TIG.docx` | Wiley-formatted manuscript for *Transactions in GIS* (tables after references; figures separate) |
| `RCC_GeoDB_Manuscript_TIG_Illustrated.docx` | Illustrated review copy with tables and figures placed inline |
| `build_docx.py` | Builds the submission-style Word manuscript |
| `build_docx_illustrated.py` | Builds the illustrated review copy |
| `make_figures.py` | Generates the six figures as high-resolution PNGs |
| `figures/` | Figure PNGs: workflow, architecture, ERD, lifecycle, governance, roadmap |
| `DOCX_COMPLIANCE_CHECK.md` | Requirement-by-requirement check against the journal guidelines |
| `interviews/` | Interview guide, question bank, consent script, response templates, coding frame |
| `interviews/FINDINGS_MEMO.md` | Anonymised empirical findings, quotes, limitations, and implications |
| `interviews/CODING_SUMMARY.csv` | 18-theme coding summary with participant codes and RQ mapping |

---

## Status

This is an **empirical working draft**, not a submission-ready manuscript.

Completed:

- article argument and structure;
- verified literature matrix and reference list;
- literature review draft;
- data model excerpt;
- ERD;
- governance framework;
- implementation roadmap;
- figure specifications;
- working manuscript draft with 11 interviews integrated;
- interview guide, response templates, findings memo, and coding summary;
- journal-fit note for *Transactions in GIS*.

Still needed:

1. Targeted interviews with revenue/holding tax, engineering (roads/drains), ICT/GIS, and WASA.
2. RCC document review: ward maps, holding-tax register, engineering drawings, budgets, organograms.
3. Expert review of the schema and governance framework.
4. RCC budget and revenue figures, verified.
5. Final figures drawn in a journal-compatible format.
6. Trim to the journal’s word limit.
7. Journal-specific formatting and cover letter.

---

## Working argument

The article argues that:

1. RCC’s binding constraint is not software but **stewardship**: ownership, maintenance, validation, and sharing.
2. The **address** is the foundational layer for property tax, waste, water, drainage, and service requests.
3. A **common asset registry** allows inspections and work orders to attach to any asset without schema changes.
4. **Governance must be designed with the system**, not added later.
5. **Public value and privacy must be designed together**: making the city legible should not make it surveilled.
6. Implementation must be **phased, pilot-led, and maintenance-funded**.

---

## Target contribution

A context-sensitive municipal spatial data infrastructure model for Bangladeshi city corporations, combining:

- a thematic geodatabase;
- an address gazetteer;
- a common asset registry;
- a staged automation pipeline;
- a governance framework;
- a phased implementation roadmap;
- a humanistic account of legibility, equity, and data justice.

---

## Notes

- All references should be checked against publisher records before submission.
- The literature matrix includes academic sources, legislation, standards, and grey literature.
- The manuscript uses `[empirical phase]` markers where RCC interviews and budget data should be inserted.
- The article does not claim a completed city-wide implementation.
