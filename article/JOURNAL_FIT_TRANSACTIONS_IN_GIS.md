# Journal Fit: Transactions in GIS

## 1. Why this journal

*Transactions in GIS* publishes research on spatial data infrastructures, standardization and interoperability, spatial data structures and databases, and GIS and society. The RCC article fits all four:

- **Spatial data infrastructure:** a municipal SDI for a resource-constrained city corporation.
- **Standardization and interoperability:** domains, metadata, stable identifiers, open formats, QGIS/PostGIS.
- **Spatial data structures and databases:** a 65-feature-class geodatabase, address gazetteer, asset registry, relationship model.
- **GIS and society:** legibility, privacy, equity, public value, local-government capacity.

The article should therefore be positioned as a **GIScience contribution**, not only a planning case study. The planning and policy material is the context and justification; the schema, workflow, and governance model are the contribution.

---

## 2. What to foreground

### 2.1 The artifact

- The municipal geodatabase schema.
- The address-centred data model.
- The common asset registry.
- The staged validation and publication pipeline.
- The data dictionary and domain model.
- The reproducible build package (ArcPy + QGIS-compatible schema).

### 2.2 The method

- Design science research.
- Scoping review.
- Embedded case study.
- Expert review and proof-of-concept validation.
- Technical evaluation: schema consistency, geometry validity, domain coverage, completeness.

### 2.3 The GIScience questions

- How can a municipal SDI be designed for paper/Excel starting conditions?
- What data structures make address, parcel, building, and asset data interoperable?
- How should provenance and accuracy be encoded so that public maps do not imply false precision?
- What governance arrangements make a municipal SDI maintainable?
- How can a GIS be designed for public value without becoming a surveillance tool?

### 2.4 The humanistic thread

Keep the legibility argument, but make it serve the GIScience argument. The point is not only that the city can be mapped, but that the **data model encodes choices about visibility, privacy, and accountability**. That is a GIS and society contribution.

---

## 3. What to trim or subordinate

- Long generic descriptions of smart cities.
- Broad planning theory that is not connected to the artifact.
- Excessive detail on Australian council websites.
- General e-government history without a GIS link.
- Policy recommendations that are not grounded in the data model or governance framework.

The article should still be readable for planners and policymakers, but the technical contribution must be visible within the first two pages.

---

## 4. Suggested structure for Transactions in GIS

| Section | Emphasis |
|---|---|
| 1. Introduction | Problem, GIScience gap, RCC context, contribution |
| 2. Related work | Municipal GIS, SDI, spatial databases, data governance, GIS and society |
| 3. Conceptual framework | Socio-technical systems, public value, data governance, legibility |
| 4. Methodology | Design science, scoping review, case study, expert review |
| 5. Case context | RCC, paper/Excel baseline, institutional ecology |
| 6. The RCC municipal geodatabase | Architecture, schema, address gazetteer, asset registry, automation |
| 7. Evaluation | Technical validation, expert review, public-value assessment |
| 8. Governance and implementation | RACI, policies, roadmap, financing |
| 9. Discussion | GIScience implications, planning/economic significance, limitations |
| 10. Conclusion | Contribution and research agenda |

The current draft has most of this. The main change is to add a stronger **evaluation/results** section and to move some planning discussion later.

---

## 5. Data and code availability

*Transactions in GIS* expects data supporting the results to be archived in an appropriate public repository. For this article:

- Publish the schema definition and build scripts on GitHub.
- Archive a version on Zenodo with a DOI.
- Provide a **synthetic sample dataset** or empty schema; do not publish personal tax, owner, or complaint data.
- Provide the data dictionary as a supplementary CSV.
- Provide the ERD and figure-generation files.
- Provide a README with reproduction steps.

Suggested data availability statement:

> The geodatabase schema, data dictionary, and build scripts are available at [repository URL]. A versioned archive is deposited at [Zenodo DOI]. The RCC operational data are not publicly available because they contain personal and commercially sensitive information. Synthetic sample records are provided to demonstrate the schema.

---

## 6. Figures and tables for this journal

### Figures

1. Research design.
2. Current paper/Excel workflow versus proposed digital workflow.
3. System architecture.
4. Simplified ERD.
5. Data lifecycle and validation pipeline.
6. Governance framework.
7. Implementation roadmap.

### Tables

1. Literature matrix (short version; full matrix as supplement).
2. Layer catalogue.
3. Data dictionary excerpt.
4. Domain examples.
5. RACI matrix.
6. Evaluation criteria and results.
7. Risks and mitigations.

Transactions in GIS reviewers will look for clarity in the schema and reproducibility. The ERD and data dictionary excerpt are central, not decorative.

---

## 7. Anticipated reviewer concerns

| Concern | Response |
|---|---|
| “This is a case study, not a general contribution.” | The contribution is a reusable design pattern for paper/Excel municipal SDIs, not a universal schema. The case specifies the pattern. |
| “The system is not fully implemented.” | The article is explicit about being design-phase. It reports a proof-of-concept schema and expert validation, not long-term outcomes. |
| “The schema is too broad.” | The breadth is intentional for a municipal platform; the article shows the core entities and explains the extension logic. The full dictionary is supplementary. |
| “Why QGIS/PostGIS rather than Esri?” | The choice is justified by cost, openness, interoperability, and local capacity. The schema is portable to Esri file geodatabases. |
| “Where is the empirical evaluation?” | The article includes technical validation and expert review; the interview programme and pilot evaluation are the next phase. |
| “How is this GIScience?” | It contributes to municipal SDI design, spatial data quality, address infrastructure, interoperability, and GIS and society. |
| “Privacy and surveillance are underdeveloped.” | The governance framework includes access classification, publication gates, and data-justice principles. |

---

## 8. Citation style

Check the current Wiley author guidelines at submission. The working manuscript uses APA 7. If *Transactions in GIS* requires a different style, convert the reference list at the final stage.

---

## 9. What to do next

1. Add an explicit “GIScience contribution” paragraph to the introduction.
2. Add an evaluation/results section with:
   - schema validation results;
   - expert-review themes;
   - address-matching test results;
   - data-quality metrics from the pilot.
3. Move the data dictionary excerpt and ERD into the main text.
4. Archive the schema and build scripts on Zenodo.
5. Trim the planning discussion by 20–30%.
6. Confirm the word limit and reference style.
