# Data Governance Framework

This framework is written for the article and for RCC’s internal use. It answers a simple question: **who decides what about the data, and who is accountable when it is wrong?**

---

## 1. Principles

| Principle | Meaning for RCC |
|---|---|
| **Public value** | Data exists to improve services, planning, revenue administration, and accountability, not only to produce maps. |
| **Stewardship** | Every dataset has a named owner and a named steward. Data are maintained, not merely collected. |
| **Quality** | Accuracy, completeness, consistency, and timeliness are defined and measured. |
| **Openness** | Non-sensitive data are shared with the public in usable forms, subject to law and privacy. |
| **Privacy** | Personal, tax, complaint, and vulnerability data are protected. |
| **Security** | Access is role-based; backups are tested; incidents are managed. |
| **Equity** | The system does not assume universal digital access or English literacy. |
| **Sustainability** | Maintenance, training, and support are budgeted from the start. |
| **Legal compliance** | The system operates within Bangladeshi law and RCC’s administrative rules. |
| **Do no harm** | Data about informal settlements, vulnerable groups, and disputes are handled with care. |

---

## 2. Roles and responsibilities

| Role | Who | Responsibility |
|---|---|---|
| **Political owner** | Mayor / Chair | Champions the system; approves public-value priorities and publication policy. |
| **Executive owner** | Chief Executive Officer | Allocates budget, staff, and inter-departmental authority. |
| **Platform owner** | Head of ICT / GIS unit | Runs the geodatabase, standards, security, backups, and publishing. |
| **Data owner** | Department head | Accountable for the accuracy and fitness of a data domain (e.g., roads, drains, waste). |
| **Data steward** | Department focal point | Maintains the data, validates updates, and resolves quality issues. |
| **GIS editor** | GIS unit / trained staff | Creates and edits features, runs QA, and prepares publication views. |
| **Field officer** | Ward / engineering / conservancy staff | Captures field data and reports discrepancies. |
| **Data user** | Planners, engineers, revenue staff, management | Uses data for analysis, decisions, and services. |
| **Public** | Citizens, researchers, businesses | Uses published data and provides feedback. |
| **Legal / privacy officer** | RCC legal or designated officer | Reviews access, privacy, retention, and disclosure. |
| **IT security** | ICT / security | Manages accounts, network security, backups, and incident response. |

---

## 3. RACI matrix

R = Responsible, A = Accountable, C = Consulted, I = Informed.

| Activity | Mayor/Board | CEO | GIS Unit | Data Owner | Data Steward | Legal | IT Security |
|---|---|---|---|---|---|---|---|
| Approve data policy | A | R | C | C | I | C | I |
| Define layer standards | I | A | R | C | C | I | I |
| Capture/edit data | I | I | R | A | R | I | I |
| Validate data quality | I | I | R | A | R | I | I |
| Approve public release | A | R | C | C | C | C | C |
| Manage user access | I | I | R | C | I | C | A |
| Respond to data incident | I | A | R | C | C | C | R |
| Maintain metadata | I | I | R | A | R | I | I |
| Budget for maintenance | A | R | C | C | I | I | I |
| Train staff | I | A | R | C | C | I | I |

---

## 4. Policies

### 4.1 Data standards policy

- All layers use the approved schema, field names, and domains.
- All geometry uses EPSG:32645 (or the approved national grid).
- All features carry provenance and accuracy.
- All layers have metadata.
- Changes follow a versioned migration process.

### 4.2 Metadata policy

Every layer records:

- title and description;
- owner and steward;
- source and capture method;
- positional and attribute accuracy;
- update frequency;
- access classification;
- publication status;
- license and attribution;
- last update date.

### 4.3 Access classification

| Class | Description | Example |
|---|---|---|
| **Public** | Safe for open publication | wards, roads, parks, public facilities, flood extent |
| **Internal** | Staff-only | asset condition, work orders, inspections |
| **Restricted** | Named roles only | holding tax, owner names, complaints, vulnerable settlements |
| **Sensitive** | Case-by-case, legal review | disputes, personal data, security assets |

### 4.4 Privacy policy

- Collect only what is necessary.
- Do not publish owner names, tax amounts, arrears, personal contact details, or complaint narratives.
- Aggregate or generalise data where individual identification is possible.
- Apply retention rules and secure deletion.
- Conduct a privacy impact assessment before public release.

### 4.5 Open data policy

- Publish non-sensitive layers in open formats (GeoJSON, CSV, WMS/WFS).
- Use a clear license (e.g., CC BY 4.0) and attribution statement.
- Provide metadata and a data date.
- Maintain a public changelog.
- Remove or generalise fields that could identify individuals.

### 4.6 Retention and archiving

- Keep current operational data in production.
- Keep historical versions for audit and planning.
- Archive superseded layers with metadata.
- Define retention periods with legal advice.

### 4.7 Procurement policy

- Require open standards and data export.
- Avoid proprietary formats that cannot be migrated.
- Require source code or configuration documentation where custom work is procured.
- Include training and maintenance in contracts.
- Avoid vendor lock-in through data escrow and exit clauses.

### 4.8 Security policy

- Individual accounts; no shared administrator login.
- Role-based access; least privilege.
- Encryption in transit; secure backups.
- Patch management.
- Incident response and breach notification.
- Periodic access review.

---

## 5. Processes

### 5.1 Data request

1. Request received by GIS unit.
2. GIS unit checks access classification.
3. Data owner approves or rejects.
4. Legal reviews if personal or sensitive.
5. Data delivered with metadata and license.

### 5.2 Change request

1. User or department proposes a schema or data change.
2. GIS unit assesses impact.
3. Data governance group approves.
4. Migration script is tested on a copy.
5. Production change is applied and logged.
6. `meta_layer` and data dictionary are updated.

### 5.3 Quality assurance

1. Editor completes feature.
2. QGIS/ArcGIS validation rules run.
3. Steward reviews a sample.
4. QA status is recorded.
5. Failed records return to the editor with comments.

### 5.4 Publication approval

1. GIS unit prepares a `pub` view.
2. Privacy and accuracy checks pass.
3. Data owner signs off.
4. Legal reviews if required.
5. Layer is published with metadata, date, and disclaimer.
6. Public feedback is monitored.

### 5.5 Incident response

1. Report incident (data loss, breach, wrong publication).
2. Contain the incident.
3. Assess impact.
4. Notify affected parties and authorities if required.
5. Restore data.
6. Document lessons and update controls.

### 5.6 Audit

- Quarterly access review.
- Annual data quality audit.
- Annual backup restore test.
- Annual review of public layers.
- Post-implementation review after major projects.

---

## 6. Maturity model

| Level | Description | RCC characteristics |
|---|---|---|
| **1. Initial** | Ad hoc, paper/Excel, no standards | Data in departmental files; no shared address index |
| **2. Repeatable** | Some GIS use, repeated workflows | Pilot ward; QGIS projects; basic schema |
| **3. Defined** | Standards, roles, documented processes | Data dictionary, stewards, QA rules, internal map |
| **4. Managed** | Performance measured, maintenance funded | SLAs, dashboards, condition data, audit |
| **5. Optimised** | Continuous improvement, public value | Public map, open data, analytics, cross-agency sharing |

The goal is not to reach Level 5 quickly. The goal is to reach Level 3 reliably and then improve.

---

## 7. Legal and policy context

- **Local Government (City Corporation) Act, 2009** — defines RCC’s mandate and functions.
- **Right to Information Act, 2009** — supports proactive disclosure, subject to exemptions.
- **Smart Bangladesh Vision 2041** — national digital government agenda.
- **National Spatial Data Infrastructure (NSDI)** — national spatial data framework.
- **Applicable privacy, cyber-security, and data-protection rules** — to be confirmed with RCC legal counsel.
- **RCC budget and procurement rules** — govern hiring, software, and data acquisition.

The article should describe this as a **policy ecology**, not a single legal mandate. The system must be compatible with national frameworks while remaining usable at the ward level.

---

## 8. Financing and sustainability

### Cost categories

- staff time (largest);
- data capture and field verification;
- server, storage, and backup;
- training;
- support and maintenance;
- imagery and survey;
- public communication.

### Financing options

- RCC operating budget;
- development partner grants;
- municipal revenue improvements linked to the system;
- shared services with other city corporations;
- public-private partnerships with clear public-interest safeguards;
- academic partnerships for pilots and evaluation.

### Sustainability rules

- No system without a maintenance budget.
- No layer without a data steward.
- No public release without a review cycle.
- No procurement without an exit plan.
- No pilot without a scale-up decision.

---

## 9. Key performance indicators

| Dimension | Indicator |
|---|---|
| Completeness | % of wards with complete core layers |
| Accuracy | % of features within the declared accuracy tier |
| Currency | % of assets updated within the SLA |
| Consistency | % of geometry passing topology rules |
| Address matching | % of holding records matched to an address |
| Use | monthly active internal users |
| Public value | public map sessions, feedback, resolved queries |
| Governance | % of layers with a named steward and metadata |
| Sustainability | maintenance budget as % of total system cost |
| Trust | data-related complaints and correction requests |

---

## 10. What the article should emphasise

The governance framework is not a compliance appendix. It is the explanation for why the technical system can survive.

The article should make three points:

1. **Data governance is a precondition, not a postscript.** A geodatabase without stewards becomes a digital paper archive.
2. **Governance must fit RCC’s capacity.** A framework copied from a large Australian council will fail in a small GIS unit.
3. **Public value and privacy must be designed together.** The same address system that improves service delivery can expose vulnerable households if published carelessly.
