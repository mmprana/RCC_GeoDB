# Implementation Roadmap

This roadmap translates the article’s proposal into a staged programme. It is designed for a resource-constrained city corporation that cannot stop normal operations while building a new system.

---

## 1. Design logic

The roadmap follows five rules:

1. **Build the container before filling it.** Establish the schema, standards, roles, and validation workflow first.
2. **Prove it in one ward.** A pilot ward exposes data, workflow, and governance problems at a manageable scale.
3. **Publish internally before publicly.** Staff trust must be built before public trust.
4. **Fund maintenance from the start.** A system without an update budget will fail.
5. **Evaluate before scaling.** Scale only what works.

---

## 2. Phases

### Phase 0 — Foundation (months 0–3)

**Purpose:** Create the institutional and technical conditions for the system.

**Activities:**

- establish a data governance group;
- appoint data owners and stewards;
- approve the data policy and access classification;
- finalise the geodatabase schema and data dictionary;
- install PostgreSQL/PostGIS, QGIS, QGIS Server, Lizmap, and backup;
- configure roles, authentication, and audit;
- select a pilot ward;
- inventory paper maps, Excel registers, CAD drawings, and orthophotos;
- define the first public-layer list;
- train the core GIS team.

**Outputs:**

- approved schema v1.0;
- empty geodatabase;
- QGIS project template;
- metadata template;
- pilot ward profile;
- data inventory;
- governance charter;
- backup and restore procedure.

**Exit test:**

- a test load of at least 50 features passes validation and appears in an internal map;
- one complete backup and restore has been performed;
- data owners and stewards have signed the charter.

---

### Phase 1 — Pilot ward (months 3–6)

**Purpose:** Prove the model in one ward.

**Activities:**

- georeference paper maps for the ward;
- digitise ward boundary, roads, buildings, and drains;
- import holding-tax addresses and match them to address points;
- capture waste bins, streetlights, parks, and public facilities with QField;
- create inspection and work-order forms;
- configure internal Lizmap;
- run QA and field verification;
- document problems and refine the schema.

**Outputs:**

- complete pilot ward dataset;
- address gazetteer for the ward;
- internal map;
- QA report;
- revised data dictionary;
- training materials.

**Exit test:**

- at least 80% of addresses in the pilot ward are geocoded;
- core layers pass geometry and domain checks;
- at least 10 internal users can search the map;
- data stewards can update records without GIS unit intervention.

---

### Phase 2 — City foundation (months 6–12)

**Purpose:** Extend the foundation city-wide.

**Activities:**

- complete city and ward boundaries;
- build the city-wide road centreline;
- complete the address gazetteer;
- digitise building footprints from orthophoto;
- capture public facilities, parks, and waste infrastructure;
- establish as-built data handover from engineering projects;
- train departmental stewards;
- publish internal dashboards;
- prepare public-layer views.

**Outputs:**

- city-wide address gazetteer;
- city-wide road and building base;
- facility and park layers;
- as-built workflow;
- internal dashboards;
- public release plan.

**Exit test:**

- 70% of city addresses matched;
- 80% of core layers complete;
- public-layer privacy review completed;
- maintenance budget approved.

---

### Phase 3 — Operations (months 12–18)

**Purpose:** Make the system part of daily work.

**Activities:**

- integrate inspections, work orders, and service requests;
- link holding tax to parcel/building;
- implement condition assessment for drains, roads, and facilities;
- introduce service-level dashboards;
- integrate waste routes and collection zones;
- add flood and water-quality layers;
- train ward and field staff;
- run data-quality audits.

**Outputs:**

- operational workflows;
- condition baseline;
- service dashboards;
- revenue linkage;
- training refresh;
- annual data-quality report.

**Exit test:**

- at least 50% of service requests linked to an asset;
- condition data available for priority assets;
- monthly active internal users exceed the target;
- data update lag within SLA.

---

### Phase 4 — Public (months 18–24)

**Purpose:** Publish selected layers and build public trust.

**Activities:**

- publish `pub` views;
- launch public map with address search;
- publish wards, roads, parks, facilities, waste zones, and flood layers;
- add Bangla/English interface;
- add print and mobile support;
- establish feedback and correction process;
- monitor use and complaints;
- review privacy and accuracy;
- publish metadata and data dates.

**Outputs:**

- public map;
- open data package;
- feedback log;
- public communication materials;
- annual public data report.

**Exit test:**

- at least five public layers maintained;
- public map passes mobile performance test;
- correction requests resolved within target;
- no privacy incidents.

---

### Phase 5 — Scale and optimise (months 24–36)

**Purpose:** Deepen the system and support replication.

**Activities:**

- extend to other city corporations;
- add analytics and modelling;
- integrate sensors and real-time data;
- develop 3D/digital-twin pilots;
- publish open data APIs;
- review governance maturity;
- update the schema and migration path;
- document lessons for national policy.

**Outputs:**

- replication toolkit;
- open API;
- maturity assessment;
- research publications;
- policy brief.

**Exit test:**

- another city corporation can adopt the model;
- open data is used by external users;
- governance maturity reaches Level 4;
- system is included in RCC’s recurring budget.

---

## 3. Milestone summary

| Milestone | Target |
|---|---|
| Schema v1.0 approved | Month 3 |
| Pilot ward complete | Month 6 |
| City-wide address gazetteer | Month 12 |
| Operations live | Month 18 |
| Public beta | Month 24 |
| Replication toolkit | Month 36 |

---

## 4. Workstreams

### 4.1 Governance and institutional

- data policy;
- RACI;
- data-sharing agreements;
- legal and privacy review;
- budget and procurement.

### 4.2 Data and schema

- schema design;
- domains and subtypes;
- data dictionary;
- metadata;
- migration and versioning.

### 4.3 Technology

- PostGIS/QGIS;
- QGIS Server/Lizmap;
- QField;
- backup and security;
- public map.

### 4.4 Data capture

- paper map conversion;
- Excel/address matching;
- CAD import;
- field capture;
- as-built handover.

### 4.5 Capacity and change

- training;
- SOPs;
- champions;
- communication;
- user feedback.

### 4.6 Evaluation

- data quality;
- user adoption;
- service impact;
- revenue impact;
- public value.

---

## 5. Quick wins

These can be delivered early and build confidence:

1. Ward boundary and road centreline map.
2. Address search for one ward.
3. Waste collection zone map.
4. Public facility map.
5. Drain complaint locator.
6. Streetlight inventory in one ward.
7. Park and tree map.
8. Internal dashboard of data completeness.

---

## 6. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Data capture takes longer than planned | High | High | Pilot first; phase rollout; realistic KPIs |
| No data ownership | High | High | RACI; stewards; executive mandate |
| Excel remains the shadow master | High | Medium | Templates; import workflow; show value |
| Paper maps are inaccurate | High | Medium | Accuracy flags; field verification; disclaimers |
| Staff turnover | Medium | High | Documentation; cross-training; champions |
| Budget cuts | Medium | High | Quick wins; revenue case; phased costs |
| Vendor lock-in | Medium | High | Open standards; exit clauses; data escrow |
| Privacy incident | Low | High | Classification; review; access control |
| Public map misuse | Medium | Medium | Selective publication; disclaimers; monitoring |
| Power/internet disruption | High | Medium | UPS; offline QField; local server |
| Political interference | Medium | Medium | Governance charter; transparency; audit |
| Over-customisation | Medium | Medium | Configure first; code only when necessary |

---

## 7. Cost categories

| Category | Notes |
|---|---|
| Staff time | Largest cost; includes GIS, stewards, field staff |
| Server and storage | Can be modest; cloud optional |
| Backup and disaster recovery | Must be funded |
| Training | Initial and refresher |
| Data capture | Paper conversion, field survey, imagery |
| Software support | Even open source needs support |
| Public communication | Accessibility, Bangla content, outreach |
| Evaluation | Internal or academic partnership |

The article should argue that **maintenance is the real cost**, not the initial software.

---

## 8. KPIs

| Area | KPI |
|---|---|
| Governance | % of layers with a named steward |
| Data completeness | % of core layers complete by ward |
| Address quality | % of holdings matched to an address point |
| Asset coverage | % of known assets captured |
| Geometry quality | % of features passing validity checks |
| Attribute quality | % of mandatory fields populated |
| Timeliness | days since last update by layer |
| Adoption | monthly active internal users |
| Service | % of service requests linked to an asset |
| Public value | public map sessions; feedback resolved |
| Sustainability | maintenance budget as % of total cost |

---

## 9. Decision gates

### Gate 1 — End of Phase 0
Proceed only if:

- schema approved;
- governance charter signed;
- pilot ward selected;
- backup tested.

### Gate 2 — End of Phase 1
Proceed only if:

- pilot ward data passes QA;
- internal users can use the map;
- stewards can update data;
- costs are understood.

### Gate 3 — End of Phase 2
Proceed only if:

- city-wide foundation is credible;
- privacy review passed;
- maintenance budget approved;
- public-layer list agreed.

### Gate 4 — End of Phase 3
Proceed only if:

- operational workflows are used;
- data updates are timely;
- service impact is visible;
- public release is safe.

### Gate 5 — End of Phase 4
Proceed only if:

- public map is maintained;
- feedback process works;
- no serious privacy incidents;
- scale-up case is proven.

---

## 10. What the article should emphasise

The roadmap is not a Gantt chart decoration. It is an argument about sequencing:

- governance before data;
- data before public map;
- pilot before scale;
- maintenance before expansion;
- evaluation before replication.

That sequencing is one of the article’s practical contributions.
