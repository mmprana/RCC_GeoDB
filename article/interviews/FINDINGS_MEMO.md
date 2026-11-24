# Interview Findings Memo

**Study:** Making the City Legible: A Human-Centred Geodatabase for Urban Planning and Local Government in Bangladesh

**Case:** Rajshahi City Corporation (RCC)

**Data:** 11 semi-structured interviews conducted 16–24 November 2026.

**Quote permission:** Yes for all participants.

**Status:** Anonymised working analysis. Raw response files are kept outside the public repository.

---

## 1. Sample

| Code | Role category | Broad department | Date | Substantive responses | Quote permission |
|---|---|---|---|---|---|
| P01 | RCC Planner | Planning | 2026-11-18 | 39/40 | Yes |
| P02 | RCC Planner | Planning | 2026-11-17 | 40/40 | Yes |
| P03 | Local Councillor | Councillor office | 2026-11-16 | 40/40 | Yes |
| P04 | Health Services | Health services | 2026-11-17 | 30/40 | Yes |
| P05 | Local Councillor | Councillor office | 2026-11-18 | 40/40 | Yes |
| P06 | Field Staff | Waste management | 2026-11-17 | 26/40 | Yes |
| P07 | Field Staff | Field inspection | 2026-11-17 | 30/40 | Yes |
| P08 | Partner Agency | RDA | 2026-11-17 | 22/40 | Yes |
| P09 | Academic | Geography and environment studies | 2026-11-17 | 39/40 | Yes |
| P10 | Local Resident | Resident | 2026-11-17 | 22/40 | Yes |
| P11 | Cleaning Department | Cleaning | 2026-11-24 | 35/40 | Yes |

**Total:** 440 question rows; 4 blanks; 77 blank or “NA” responses. Many “NA” responses are role-appropriate (for example, a partner agency cannot describe RCC’s internal file movement).

### Data-quality notes

- P01 and P02 (both planners) gave closely similar accounts. P03 and P05 (both councillors) also gave closely similar accounts. They may reflect shared departmental positions or joint briefing. They are treated as **paired perspectives**, not as fully independent interviews.
- P10 (local resident) has 18 blank/NA responses and several answers that drift from the question. Use P10 only as a public-perspective illustration, not as a core informant.
- P04 (health services) is relevant for birth registration, vaccination, and health service location, but many questions fall outside their role.
- P08 (partner agency) is strong on data sharing, custodianship, and metadata, but cannot describe RCC’s internal workflows.
- No email addresses or Bangladeshi mobile numbers were detected in the response text. A manual anonymisation check is still required before quotation.

### Coverage gap

The sample does **not** include:

- revenue / holding-tax staff;
- engineering staff responsible for roads and drains;
- ICT / GIS focal point;
- Rajshahi WASA or LGED/RHD.

This matters for claims about property tax, drainage asset management, technical architecture, and inter-agency water/sewer data. The findings below are therefore strongest on **organisational practice, address problems, governance expectations, public access, and implementation sequencing**, and weaker on departmental asset and revenue workflows.

---

## 2. Key findings

### 2.1 The paper/Excel baseline is pervasive

Most participants described a working environment built on paper files, registers, Excel, Word, and in-person communication. There is no integrated RCC spatial data system.

> “There is no digital way to cooperate with each other. We follow the traditional way.” — P01, RCC Planner

> “Records are kept in hard-copy format and, at times, in Excel files.” — P02, RCC Planner

> “Most information is kept in hard-copy forms, registers, and files. Some records may be kept in Excel.” — P03, Local Councillor

This is not simply a technology gap. It shapes how work is coordinated, how progress is tracked, and how citizens experience services.

### 2.2 Departmental silos and file-based coordination

Departments keep their own records. Coordination happens through files, phone calls, and direct contact. There is no shared case-tracking or spatial platform.

> “Each department manages its own data. There is no centralized system for departments to collaborate and develop a shared database.” — P02, RCC Planner

> “We share information through hard-copy files and direct contact with other departments.” — P03, Local Councillor

> “RDA and RCC do share planning information when needed. This supports individual requests, but the process is not automated and there is no common database or platform.” — P08, Partner Agency

### 2.3 The address is the missing infrastructure

Addresses are recorded manually and inconsistently. Staff use National ID cards to verify identity, but identity verification is not the same as a location index. Incomplete or inconsistent addresses make it difficult to find residents, route services, or link records.

> “We have no digital way to locate clients; we verify their identity using their National ID.” — P02, RCC Planner

> “Addresses are recorded manually in applications and other paper records. An address is easier to use when it clearly identifies the resident’s location. It can be difficult to find a place when address details are incomplete or inconsistent, especially without a shared address or mapping system.” — P03, Local Councillor

> “RCC should adopt a standard address structure, including administrative area, locality, road or landmark, building or holding reference where available, and a unique address identifier.” — P09, Academic

This directly supports the proposed **address gazetteer** and the decision to make the address the front door of the system.

### 2.4 Holding tax and cadastral records are disconnected

Participants who could speak to this issue were clear: RCC does not have a cadastral database and cannot reliably link holding or tax records to buildings or parcels.

> “RCC does not have a cadastral database, so we cannot reliably link a holding or tax record to a building or parcel using a shared spatial record.” — P03, Local Councillor

> “We cannot reliably connect a holding or tax record to a building or parcel because RCC does not have a cadastral database.” — P05, Local Councillor

> “RCC cannot reliably link holding-tax records to buildings or parcels without cadastral data. The recommended approach is to establish authoritative parcel and building identifiers, then link records through those identifiers and documented relationships.” — P09, Academic

This is a major finding for the economic argument. It also explains why the geodatabase design separates `holding_no`, `parcel_id`, `building_id`, and `address_id` while allowing them to be linked.

### 2.5 Assets are repaired, but not registered spatially

Drains, bins, streetlights, parks, and facilities are handled by departments, but there is no shared spatial asset register. As-built drawings and contractor data are filed in project files or the records room, not linked to a mapped asset.

> “RCC does not have a shared spatial asset register for features such as drains, manholes, bins, streetlights, parks, and public facilities. Information about these assets is handled manually by the relevant departments.” — P05, Local Councillor

> “There is no automatic process for updating a central map or database.” — P05, Local Councillor

> “Final project documents are kept in files and stored in the records room. We do not have a central system that links as-built drawings or contractor information to a mapped project record.” — P03, Local Councillor

This supports the **asset registry**, `asset_no`, condition fields, and as-built handover workflow.

### 2.6 Field data capture is paper-based

Field staff receive paper instructions, record work on paper, and return information in person or on paper. They do not use digital forms, GPS, or mobile data collection.

> “I provide field information on paper or in person. I have not used a digital method to collect it.” — P06, Field Staff

> “Field information is handled through hard-copy records and in-person communication. We have not been provided with a digital field data collection system.” — P07, Field Staff

> “There is no digital system for collecting field data.” — P02, RCC Planner

This supports **QField**, mobile forms, offline capture, photo attachments, and GPS accuracy fields.

### 2.7 Capacity and training are weak

Most participants had no GIS, Excel, or data-management training. Some learned GIS informally. IT support exists but is limited.

> “No. RCC does not have a system for organizing workshops of this kind.” — P02, RCC Planner

> “GIS is used but self learned without any institutional training; RCC does not provide any training on GIS, Excel to anyone here.” — P04, Health Services

> “I have never received training in GIS or digital field data collection. I would like training if a system is introduced.” — P06, Field Staff

This supports the training and change-management component of the roadmap.

### 2.8 Governance demand: a Spatial Services Unit and departmental custodians

There is a strong, repeated preference for a central spatial unit, departmental data custodians, clear standards, and a data governance policy.

> “There should be a Spatial Services Unit at RCC, who can develop and manage spatial database.” — P01, RCC Planner

> “RCC should establish a Spatial Services Unit to manage the city-wide spatial database. Departments should maintain and update the information related to their work, with the Spatial Services Unit coordinating standards and the IT section supporting the technology.” — P03, Local Councillor

> “RCC should establish a Spatial Services Unit and assign data custodians in each department. A central spatial database should have documented schemas, stable identifiers, backups, and controlled editing.” — P09, Academic

> “RCC should lead the database for its municipal operational data, while RDA should remain custodian of its planning datasets. The agencies should agree on a shared catalogue, data standards, access rules, and update responsibilities.” — P08, Partner Agency

This is one of the clearest findings in the dataset. It maps directly onto the proposed governance framework.

### 2.9 Privacy and selective publication

Participants consistently distinguished public information from personal, tax, identity, and complaint data. They wanted role-based access, approval, audit trails, and a public map limited to reviewed layers.

> “General information about services, roads, public facilities, and service locations could be made public after it is checked. Personal, tax, identity, and complaint information should remain internal or restricted.” — P03, Local Councillor

> “Sensitive client data should be restricted to internal use. Access should also be limited among internal users according to their roles.” — P02, RCC Planner

> “Each agency should share only the personal information necessary for an agreed purpose. Personal identifiers and sensitive records should be access-controlled, logged, and excluded from public maps.” — P08, Partner Agency

This supports the `pub` views, access classification, publication gate, and privacy framework.

### 2.10 Public map expectations and risks

Participants saw value in a public map of services, roads, facilities, waste areas, and approved planning information. They also warned about inaccurate, outdated, or sensitive data.

> “A public map showing waste service areas, relevant service locations, and how to report a problem could be useful.” — P07, Field Staff

> “A public map could show approved planning information and suitable public layers, such as roads and public facilities. It should clearly distinguish adopted plans from proposals and show the source and update date.” — P08, Partner Agency

> “Risks include exposing personal or tax information, publishing sensitive locations, and misleading residents if map data is inaccurate or out of date.” — P09, Academic

> “People may not be sufficiently aware of or familiar with maps.” — P11, Cleaning Department

The last quote is a reminder that a public map cannot be the only channel. It must sit alongside ward offices, phone lines, and printed materials.

### 2.11 Trust requires provenance and maintenance

Trust was linked to accuracy, regular updates, visible dates, recorded responsibilities, and a way to report errors.

> “Trust would improve if both agencies documented data sources, dates, scale, accuracy, coordinate reference system, custodian, and update frequency.” — P08, Partner Agency

> “Citizens are more likely to trust the map if the information is accurate, kept up to date, and clearly shows when it was last verified.” — P03, Local Councillor

> “Trustworthy data needs clear custodianship, consistent definitions, source and date information, routine validation, and a recorded history of changes.” — P09, Academic

This supports the provenance fields, metadata, QA status, audit log, and data-date statement.

### 2.12 Implementation sequencing

Participants prioritised governance, a central database, an address layer, training, workflow integration, and a public website.

> “First, establish data governance, assign clear responsibilities, and identify the data RCC needs. Second, create a central database and GIS system, starting with accurate addresses and cadastral information. Third, train staff and connect the system to service workflows and the RCC website.” — P03, Local Councillor

> “Database, GIS-based system, and finally an automated version. The GIS-based system should be linked to the website like an IntraMap services.” — P01, RCC Planner

> “First, inventory each agency’s datasets and agree on custodianship, sharing rights, standards, and privacy rules. Second, prepare priority data with common formats, identifiers, metadata, and quality checks. Third, establish a secure shared catalogue or platform, pilot data updates between the agencies, and publish only approved open datasets.” — P08, Partner Agency

This maps closely onto the proposed roadmap: Phase 0 governance and schema; Phase 1 pilot ward and address layer; Phase 2 city foundation; Phase 3 operations; Phase 4 public; Phase 5 scale.

### 2.13 Risks and success measures

Participants identified failure risks: inaccurate data, no updates, unclear responsibilities, no training, weak privacy, no funding or support, political influence, and limited public awareness.

> “The system could fail if data is not maintained, departments do not take responsibility, staff are not trained, privacy safeguards are weak, or ongoing funding and technical support are missing.” — P09, Academic

> “The main difficulty may be getting staff across departments to use and maintain the shared system consistently.” — P05, Local Councillor

Success measures included data accuracy and update frequency, departmental use, service coordination, resident feedback, training, and request turnaround.

---

## 3. What the findings change in the article

### 3.1 The argument is stronger, not weaker

The interviews confirm the core argument: the binding constraint is **stewardship and institutional coordination**, not software. Every major design choice in the geodatabase is reflected in a participant concern:

| Design choice | Interview evidence |
|---|---|
| Address gazetteer | Addresses are manual, inconsistent, and not linked to a location index |
| Parcel–building–holding keys | No cadastral database; holding tax cannot be reliably linked |
| Asset registry | No shared asset register; as-built data filed but not linked |
| Provenance and QA | Trust depends on source, date, accuracy, and maintenance |
| Governance framework | Repeated demand for a Spatial Services Unit and departmental custodians |
| Selective publication | Clear distinction between public layers and personal/tax/complaint data |
| Phased roadmap | Participants prioritised governance, address data, training, then public map |

### 3.2 Claims to soften

The sample does not include revenue, engineering, ICT/GIS, or WASA. Therefore:

- Do not claim that RCC’s holding-tax office has no linking process at all; say that **planners and councillors reported** no reliable parcel–holding link, and that the issue requires validation with revenue staff.
- Do not claim that no asset register exists anywhere; say that **participants did not identify a shared spatial asset register**.
- Do not make strong technical claims about server capacity, security, or integration; these require ICT/GIS interviews.
- Treat P10 as a public-perspective illustration, not as representative of residents.

### 3.3 Claims to strengthen

- The demand for a **Spatial Services Unit** is strong and repeated.
- The demand for **data governance before technology** is strong.
- The **address layer** is the most frequently prioritised first step.
- **Privacy and selective publication** are widely understood.
- **Training and maintenance** are seen as conditions for success.

---

## 4. Selected quotes for the manuscript

Use quotes sparingly and with the participant code and broad role. Suggested selection:

1. P01: “There is no digital way to cooperate with each other. We follow the traditional way.”
2. P02: “We have no digital way to locate clients; we verify their identity using their National ID.”
3. P03: “RCC does not have a cadastral database, so we cannot reliably link a holding or tax record to a building or parcel using a shared spatial record.”
4. P05: “There is no automatic process for updating a central map or database.”
5. P07: “A public map showing waste service areas, relevant service locations, and how to report a problem could be useful.”
6. P08: “Trust would improve if both agencies documented data sources, dates, scale, accuracy, coordinate reference system, custodian, and update frequency.”
7. P09: “The system could fail if data is not maintained, departments do not take responsibility, staff are not trained, privacy safeguards are weak, or ongoing funding and technical support are missing.”
8. P03: “General information about services, roads, public facilities, and service locations could be made public after it is checked. Personal, tax, identity, and complaint information should remain internal or restricted.”
9. P03: “First, establish data governance, assign clear responsibilities, and identify the data RCC needs.”
10. P11: “People may not be sufficiently aware of or familiar with maps.”

---

## 5. Limitations of the interview evidence

- 11 participants, not the full 12–15 target.
- No revenue, engineering, ICT/GIS, or WASA respondents.
- Two planner accounts and two councillor accounts are closely similar; treat as paired perspectives.
- P10 is thin and partly off-topic.
- Some responses are short or role-limited.
- The sample supports **contextual and design requirements**, not statistical generalization.
- The findings should be triangulated with documents and field observation.

---

## 6. Next analytic steps

1. Code all responses against the coding frame.
2. Build a theme–evidence table with participant counts.
3. Select 12–15 quotes for the manuscript.
4. Integrate findings into Sections 5–8.
5. Add a sample table and a limitations paragraph.
6. Revise the abstract to state the empirical basis.
7. Update the article for *Transactions in GIS*: emphasise schema, address infrastructure, interoperability, provenance, and reproducibility.
