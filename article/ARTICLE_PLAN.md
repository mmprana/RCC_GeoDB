# Making the City Legible
## A Human-Centred Geodatabase for Urban Planning and Local Government in Bangladesh

**Working article plan — version 1.0**
**Case:** Rajshahi City Corporation (RCC), Bangladesh
**Method:** Design science research + scoping review + embedded single-case study
**Target length:** 8,000–9,000 words (excluding references and appendices)
**Citation style:** APA 7
**Primary target:** *Transactions in GIS*
**Alternative targets:** *Cities*; *Habitat International*; *International Journal of Geographical Information Science*; *Government Information Quarterly*

---

## 1. Working abstract

Bangladeshi city corporations hold a great deal of information that is fundamentally spatial: parcels, roads, drains, buildings, waste collection points, streetlights, taxes, and public facilities. Yet much of this information is kept in paper maps, Excel registers, departmental files, and the memory of experienced staff. The result is not simply a data problem. It is a planning problem, a revenue problem, and a problem of public trust.

This article asks how a resource-constrained city corporation can build a maintainable, human-centred geospatial data infrastructure from a paper-and-Excel starting point. Drawing on a scoping review of municipal GIS, spatial data infrastructure, e-government, and data governance, and using Rajshahi City Corporation as an embedded case, the article proposes a design-science artifact: a thematic geodatabase, an address-centred data model, an automation pipeline, a governance framework, and a phased implementation roadmap. The proposal is assessed against technical, institutional, economic, and public-value criteria.

The article argues that the binding constraint is not software. It is stewardship: who owns, maintains, validates, and shares the data. It also argues that making a city legible need not mean making it surveilled. A municipal geodatabase can be designed to make citizens more visible to planners and service providers while protecting privacy, respecting language and local knowledge, and strengthening public accountability. The article contributes a context-sensitive implementation model for Bangladeshi city corporations and a humanistic account of spatial data infrastructure as public infrastructure.

**Keywords:** municipal GIS; spatial data infrastructure; geodatabase; data governance; urban planning; local government; Bangladesh; Rajshahi City Corporation

---

## 2. Problem statement

Most research on municipal GIS and urban spatial data infrastructure comes from high-income countries with mature address systems, digital cadastres, stable budgets, and specialised GIS teams. Bangladeshi city corporations operate under different conditions:

- data are held in paper maps, Excel sheets, and departmental files;
- addresses are inconsistent and often lack a unique identifier;
- cadastral records are fragmented across survey and revenue systems;
- asset registers are incomplete or maintained only for procurement;
- GIS capacity is thin and often concentrated in one person or unit;
- budgets are tight and procurement is complex;
- responsibilities overlap with WASA, LGED, RHD, BBS, and other agencies;
- public access to spatial data is limited;
- the political and administrative environment changes frequently.

These conditions are not temporary. They are the design context. A municipal geodatabase for RCC must therefore be:

- **incremental** — useful before it is complete;
- **address-centred** — because the address is the common key across services;
- **asset-aware** — because infrastructure management is the daily work of the corporation;
- **governance-led** — because data without stewardship becomes stale;
- **human-centred** — because the system exists for citizens and staff, not for the technology;
- **financially realistic** — because maintenance, not acquisition, is the real cost.

The article addresses this gap: how to move from a paper/Excel municipal administration to a maintained, shared, and public-facing spatial data system, in a way that is academically defensible and practically actionable.

---

## 3. Research questions

1. **RQ1:** What do international municipal GIS and geoportal cases reveal about the benefits, complexities, and governance requirements of city-level spatial data systems?
2. **RQ2:** What data model, system architecture, and automation workflow are appropriate for a resource-constrained city corporation starting from paper and Excel records?
3. **RQ3:** What governance, capacity, and financing arrangements are needed to sustain such a system beyond its initial implementation?
4. **RQ4:** How can an RCC geodatabase create public value in planning, revenue mobilisation, service delivery, and accountability?
5. **RQ5:** What phased implementation roadmap can guide other Bangladeshi city corporations?

---

## 4. Contribution

The article makes four contributions.

### 4.1 A context-sensitive municipal data model

It proposes a thematic geodatabase for a Bangladeshi city corporation, with:

- a common asset registry;
- an address gazetteer;
- parcel, building, road, drainage, waste, park, facility, planning, and operations layers;
- coded domains and stable identifiers;
- a data dictionary that can be implemented in ArcGIS Pro and QGIS.

### 4.2 A paper-to-digital workflow

It shows how to convert paper maps, Excel registers, CAD drawings, and field observations into a validated geodatabase without pretending that the starting data are better than they are. Accuracy, source, and confidence are recorded on every feature.

### 4.3 A governance and implementation model

It connects the technical artifact to the institutional conditions that determine whether it survives:

- data owners and stewards;
- quality rules and publication gates;
- procurement and financing;
- training and change management;
- privacy and public access;
- phased rollout and evaluation.

### 4.4 A humanistic argument

It reframes the geodatabase as public infrastructure. The question is not only “Can the city map itself?” but “Who is made visible, who is made legible, who is protected, and who gets to use the map?”

---

## 5. Theoretical framework

The article combines three lenses.

### 5.1 Socio-technical systems

A municipal geodatabase is not a neutral technical object. It is a bundle of people, processes, standards, incentives, and technologies. Failure is often organisational rather than technical (Campbell, 1994; Nedović-Budić & Godschalk, 1996; Ramasubramanian, 1999). This lens explains why a technically sound schema can still fail if departments do not trust it, if staff are not trained, or if no one owns the data.

### 5.2 Public value

Public value theory asks what the system adds to citizens’ lives, not just what it adds to the administration’s toolkit (Benington, 2009; Moore, 1995; Panagiotopoulos et al., 2019). For RCC, public value includes:

- fair and reliable service delivery;
- improved revenue without arbitrary enforcement;
- transparent planning decisions;
- faster response to drainage, waste, and road problems;
- accessible information in Bangla and English;
- trust that data will not be used to surveil or exclude.

### 5.3 Data governance and stewardship

Data governance defines who can make what decisions about data, under what conditions, and with what accountability (Khatri & Brown, 2010; Janssen et al., 2020). For a city corporation, governance must cover:

- ownership and custodianship;
- standards and metadata;
- quality assurance;
- access classification;
- privacy and security;
- retention and archiving;
- sharing and pricing;
- public publication.

Design science research provides the methodological frame for building and evaluating the artifact (Gregor & Hevner, 2013; Hevner et al., 2004; Peffers et al., 2007). The article does not claim a full implementation. It presents an **ex-ante design** validated through documentary analysis, expert review, and a proof-of-concept geodatabase.

---

## 6. Methodology

### 6.1 Research design

A three-part design:

1. **Scoping literature review** — to identify global patterns in municipal GIS, benefits, complexities, and solutions.
2. **Embedded single-case study** — to understand RCC’s current data practices, institutional arrangements, and constraints.
3. **Design science research** — to build and evaluate the proposed geodatabase, workflow, governance framework, and roadmap.

### 6.2 Scoping review

Use the PRISMA-ScR checklist (Tricco et al., 2018). The review is exploratory and thematic, not a meta-analysis.

**Databases:** Scopus, Web of Science, Google Scholar, ScienceDirect, Taylor & Francis, SpringerLink, IEEE Xplore, and selected grey literature.

**Search strings (example):**

```text
("municipal GIS" OR "local government GIS" OR "city GIS" OR "urban GIS")
AND (planning OR governance OR asset management OR revenue OR services)

("spatial data infrastructure" OR "urban spatial data infrastructure")
AND (developing countries OR Bangladesh OR South Asia)

("e-government" OR "digital government" OR "smart city")
AND ("local government" OR municipality)
AND (developing countries OR Bangladesh)

("data governance" OR "data stewardship")
AND ("local government" OR municipality OR "public sector")
```

**Inclusion:** peer-reviewed articles, books, and high-quality grey literature; English; 1990–2026; municipal/local government focus; explicit attention to GIS, spatial data, e-government, or data governance.

**Exclusion:** purely technical remote-sensing papers with no governance or municipal relevance; commercial product descriptions; studies with no identifiable local-government context.

**Synthesis:** thematic analysis (Braun & Clarke, 2006), organised around:

1. benefits;
2. complexities;
3. governance and capacity;
4. financing and procurement;
5. public access and equity;
6. implementation strategies.

### 6.3 Case study

RCC is the embedded case. Data collection:

- **Documents:** ward maps, holding-tax registers, engineering drawings, annual budgets, organograms, service records, project documents.
- **Interviews:** 12–15 key informants across ICT, engineering, revenue, conservancy, town planning, ward offices, partner agencies, and public users. Semi-structured, 45–60 minutes, anonymised. The protocol is in `interviews/INTERVIEW_GUIDE.md`.
- **Observation:** how paper maps and Excel files are used in daily work; where data are duplicated; where handovers fail.
- **Technical artifact:** the geodatabase schema, data dictionary, validation rules, and prototype workflows.
- **Expert review:** a small panel of GIS professionals, urban planners, and municipal practitioners.

### 6.4 Analysis

- Thematic analysis of interviews and documents.
- Comparative case matrix from the literature.
- Design-science evaluation against:
  - **technical validity** — schema consistency, geometry rules, completeness;
  - **organisational fit** — workflow, roles, capacity;
  - **economic value** — revenue, maintenance, cost avoidance;
  - **public value** — access, trust, equity, accountability;
  - **sustainability** — financing, ownership, update cadence.

### 6.5 Ethics

- University ethics approval before interviews.
- Informed consent and anonymisation.
- No publication of personal tax, owner, or complaint data.
- Careful handling of informal settlements and vulnerable groups.
- Data stored securely and destroyed according to protocol.

---

## 7. Case context: Rajshahi City Corporation

Rajshahi City Corporation is one of Bangladesh’s major urban local governments. It covers roughly 96.7 square kilometres, is divided into 30 wards, and spans the Boalia, Motihar, Rajpara, and Shah Makhdum thanas. The city sits on the north bank of the Padma River and faces recurrent drainage, waste, heat, and flood-related challenges.

RCC’s responsibilities include roads, drains, streetlights, waste management, public health, markets, parks, and a range of civic services. It also maintains a holding-tax register, which is one of the most valuable—and least spatially integrated—data assets in the city.

The current information environment is best described as **distributed paper**:

- ward maps and engineering drawings in files;
- holding-tax records in Excel and paper registers;
- asset information in departmental notebooks and procurement files;
- address descriptions that vary by ward and by officer;
- limited shared standards for naming, coding, or geometry;
- no single authoritative address or asset index.

This is not a failure of individual staff. It is the predictable outcome of under-investment in data infrastructure, fragmented mandates, and the absence of a stewardship model.

The wider policy context is favourable:

- **Smart Bangladesh Vision 2041** emphasises digital government and citizen-centred services (Pal & Sarker, 2023).
- Bangladesh has a national **NSDI** effort, although its maturity and local uptake remain limited (Rahman & Szabó, 2023).
- The **Local Government (City Corporation) Act, 2009** gives city corporations a broad mandate over urban services and local development.
- The **Right to Information Act, 2009** creates a legal basis for proactive disclosure, subject to privacy and public-interest exceptions.

The article treats these policies as opportunities, not guarantees. A policy vision does not build a geodatabase. Stewardship does.

---

## 8. Proposed system

### 8.1 Design principles

1. **Address first.** The address is the common key for property, tax, waste, water, drainage, and citizen requests.
2. **One system of record.** Excel and paper become sources, not masters.
3. **Stable identifiers.** Every asset and address has a persistent ID.
4. **Provenance on every feature.** Source, date, accuracy, and capture method are mandatory.
5. **Fit for purpose.** Accuracy should match the decision, not an abstract ideal.
6. **Open standards.** QGIS, PostGIS, GeoPackage, OGC services, and portable formats.
7. **Selective publication.** Internal data first; public layers only when ready.
8. **Human-centred.** Bangla/English labels, low-bandwidth design, privacy, and accessibility.

### 8.2 Architecture

```text
Paper maps / Excel / CAD / field observation
                    │
                    ▼
             Staging schema
        (validation, error reports)
                    │
                    ▼
     PostgreSQL + PostGIS / file geodatabase
     (reference, cadastre, transport, water,
      drainage, waste, parks, facilities,
      planning, environment, operations)
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
  QGIS Desktop             QGIS Server + Lizmap
  (editing, analysis)      (internal map, later public)
        │
        ▼
  QField (field capture)
```

The article presents this as a **socio-technical architecture**, not a software stack. The stack is replaceable. The data model, standards, and governance are not.

### 8.3 Data model

The geodatabase contains:

- reference boundaries and waterbodies;
- parcels, buildings, addresses, and address ranges;
- roads, footpaths, bridges, streetlights, signs, markings, parking;
- water, sewer, and storm-drainage assets;
- waste bins, collection zones, routes, transfer stations, landfill;
- parks, playgrounds, sports facilities, trees, irrigation;
- public facilities and facility sites;
- zoning, land use, growth areas, permits, development applications, heritage;
- flood extent, water-quality and air-quality sites;
- inspections, work orders, service requests;
- points of interest and events.

A common asset block includes:

```text
asset_id, asset_no, asset_class, asset_type, subtype,
name_en, name_bn, status_code, owner_org_code,
custodian_org_code, operator_org_code, ward_code,
install_date, condition_code, condition_date,
criticality_code, replacement_value_bdt,
source_code, source_date, accuracy_m,
capture_method_code, qa_status_code,
created_at, created_by, updated_at, updated_by
```

A separate `asset_registry` table indexes every asset so that inspections, work orders, and service requests can attach to any asset without schema changes.

### 8.4 Data dictionary excerpt

The article will include a compact table for five entities:

1. `parcel`
2. `building`
3. `road_centerline`
4. `storm_drain`
5. `waste_bin`
6. `asset_registry`

Each table shows field name, type, domain, and purpose. The full dictionary is provided as a supplementary file.

### 8.5 Automation

The automation model has five stages:

1. **Capture** — QGIS, QField, Excel templates, CAD, paper maps.
2. **Stage** — raw data loaded into a staging table with load metadata.
3. **Validate** — CRS, domains, geometry, uniqueness, parent keys, accuracy.
4. **Publish** — approved records move to production; history is retained.
5. **Share** — internal views, public views, print layouts, and later APIs.

Automation is not only technical. It includes:

- address matching and geocoding;
- asset-registry updates;
- duplicate detection;
- metadata generation;
- scheduled backups;
- audit logs;
- publication approval.

### 8.6 Governance

The governance framework has five layers:

1. **Principles** — public value, stewardship, quality, openness, privacy, security, equity.
2. **Roles** — mayor/board, CEO, GIS unit, data owners, data stewards, users, public.
3. **Policies** — standards, metadata, access, privacy, retention, sharing, procurement.
4. **Processes** — data request, change request, QA, publication, incident response.
5. **Evaluation** — maturity, completeness, timeliness, use, trust.

A RACI matrix clarifies who is responsible, accountable, consulted, and informed for each data domain.

### 8.7 Implementation roadmap

| Phase | Time | Focus | Exit test |
|---|---|---|---|
| 0. Foundation | Months 0–3 | Governance, schema, stack, pilot ward selection | Test load and internal map |
| 1. Pilot ward | Months 3–6 | Boundaries, roads, addresses, buildings, drains, bins, lights, parks | One ward complete |
| 2. City foundation | Months 6–12 | Address gazetteer, roads, buildings, facilities, orthophoto | City-wide foundation |
| 3. Operations | Months 12–18 | Inspections, work orders, requests, dashboards | Daily operational use |
| 4. Public | Months 18–24 | Public layers, search, print, feedback | Public beta |
| 5. Scale | Months 24–36 | Other city corporations, open data, analytics | Replicable model |

---

## 9. Article structure

| Section | Content | Words |
|---|---|---|
| 1. Introduction | Problem, context, gap, questions, contribution | 900 |
| 2. Literature review | Global municipal GIS, benefits, complexities, solutions | 1,800 |
| 3. Conceptual framework | Socio-technical systems, public value, data governance | 700 |
| 4. Methodology | Scoping review, case study, design science, ethics | 800 |
| 5. Context | RCC, Bangladesh local government, current data practices | 900 |
| 6. Proposed system | Architecture, data model, automation, dictionary | 2,000 |
| 7. Governance and roadmap | Roles, policies, financing, phased implementation | 1,200 |
| 8. Discussion | Planning, economy, equity, limitations | 1,200 |
| 9. Conclusion | Argument, contribution, future research | 400 |

**Total:** approximately 9,900 words. Trim to 8,000–9,000 for submission.

---

## 10. Figures and tables

### Figures

1. Research design.
2. Current paper/Excel workflow versus proposed digital workflow.
3. System architecture.
4. Simplified relational database ERD.
5. Data lifecycle and automation pipeline.
6. Data governance framework.
7. Phased implementation roadmap.
8. Evaluation framework.

### Tables

1. Literature matrix.
2. Municipal GIS benefits, complexities, and solutions.
3. Layer catalogue.
4. Data dictionary excerpt.
5. RACI matrix.
6. Risks and mitigations.
7. Implementation phases and KPIs.
8. Evaluation criteria.

---

## 11. Literature review strategy

### 11.1 Purpose

The review is not a catalogue of every municipal GIS project. It is an argument about what the global literature can and cannot teach a Bangladeshi city corporation.

### 11.2 Structure

1. **From mapping to infrastructure** — the shift from isolated GIS projects to shared spatial data infrastructure.
2. **What cities gain** — efficiency, planning, revenue, service delivery, transparency, disaster response.
3. **What makes it difficult** — data quality, institutional fragmentation, capacity, financing, procurement, privacy, politics, digital divide.
4. **How the literature says to respond** — standards, governance, phased implementation, open source, training, public participation.
5. **What the Global South adds** — informality, paper legacies, donor dependence, weak address systems, contested land records.
6. **The Bangladesh gap** — few municipal GIS studies; almost none starting from paper/Excel and connecting data model, automation, governance, and public value.

### 11.3 Case matrix

The article will compare:

- **Australia:** Perth, Wollongong, Camden, Wodonga.
- **Europe/North America:** London, Amsterdam, New York.
- **Asia:** Singapore, Seoul, Bhubaneswar, Pune, Jakarta, Quezon City.
- **Bangladesh:** RCC, Dhaka, Khulna, Chattogram, Sylhet.

For each case: population, system scope, data layers, public services, governance, financing, benefits, challenges, lessons.

### 11.4 Gap statement

The literature is rich on:

- why GIS matters;
- how local governments adopt it;
- what smart cities promise;
- how data governance should work in principle.

It is thin on:

- municipal GIS in Bangladeshi city corporations;
- implementation from paper/Excel;
- the relationship between address systems, asset registers, and revenue;
- governance models that fit low-capacity municipalities;
- the humanistic question of who is made visible by the map.

This article addresses that gap.

---

## 12. Target journals

| Journal | Fit | Notes |
|---|---|---|
| *Transactions in GIS* | GIScience, spatial data infrastructure, databases, interoperability, GIS and society | **Primary target**; strongest fit for the data model, schema, SDI, and reproducibility contribution |
| *Cities* | Urban policy, governance, planning | Broad international reach |
| *Habitat International* | Urban planning/development in the Global South | Strong fit for the planning and policy dimension |
| *International Journal of Geographical Information Science* | GIScience theory and methods | More demanding theoretically; requires a sharper GIScience contribution |
| *Government Information Quarterly* | Digital government, public value, data governance | Good if the governance contribution is foregrounded |
| *Transactions in GIS* technical note | Shorter, schema-focused paper | Possible if the article is trimmed to the data model and reproducibility artifact |
| *Journal of Bangladesh Institute of Planners* | Local planning audience | Good for policy uptake in Bangladesh |

**Primary recommendation:** *Transactions in GIS*.
**Fallback:** *Cities*, then *Habitat International*.

---

## 13. Timeline

| Week | Work |
|---|---|
| 1–2 | Finalise argument, research questions, target journal |
| 3–5 | Scoping review and literature matrix |
| 6–8 | RCC document review and interviews |
| 9–11 | Artifact design, diagrams, data dictionary |
| 12–13 | Expert review and refinement |
| 14–16 | Full draft |
| 17–18 | Internal review, language editing, references |
| 19–20 | Journal formatting and submission |

---

## 14. Writing style

The article should be academically rigorous but human to read.

- Open with a concrete RCC scene: a ward map on a wall, an Excel register, a drainage complaint, a citizen looking for a holding number.
- Define technical terms in plain language.
- Avoid “smart city” hype. Use “municipal spatial data infrastructure” and “geodatabase” precisely.
- Treat data as social and political, not only technical.
- Use interviews as evidence, not decoration.
- Be explicit about what is proposed, what is tested, and what remains uncertain.
- Keep the human question visible: who is counted, who is missing, who is served, who is protected.

---

## 15. What the article does not claim

- It does not claim that RCC has already implemented the full system.
- It does not claim that a geodatabase alone will solve revenue, planning, or service problems.
- It does not claim that open data is always good or that technology is neutral.
- It does not claim that the model is generalisable to every city corporation without adaptation.
- It does not treat the schema as final. The schema is a starting point, designed to be extended.

---

## 16. Next writing tasks

1. Finalise literature matrix and references.
2. Draft the literature review.
3. Draft the RCC context section.
4. Draft the proposed system section with figures and data dictionary excerpt.
5. Draft governance and roadmap.
6. Draft discussion and conclusion.
7. Edit for length, argument, and humanistic voice.
