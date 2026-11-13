# Figure Specifications and Draft Mermaid Diagrams

These diagrams are working figures. Redraw them in a journal-compatible tool (draw.io, Inkscape, Adobe Illustrator, or QGIS layout) before submission. Keep the source text in this file so the figures remain reproducible.

---

## Figure 1 — Research design

```mermaid
flowchart TD
    A[Problem identification<br/>paper and Excel municipal data] --> B[Scoping literature review]
    B --> C[Conceptual framework<br/>socio-technical systems, public value, data governance]
    C --> D[Embedded case study<br/>Rajshahi City Corporation]
    D --> E[Design science artifact<br/>geodatabase, workflow, governance, roadmap]
    E --> F[Expert validation<br/>GIS, planning, municipal practice]
    F --> G[Evaluation<br/>technical, organisational, economic, public value]
    G --> H[Contribution<br/>context-sensitive implementation model]
    H --> B
```

**Caption:** Research design combining a scoping review, an embedded case study, and design science research.

---

## Figure 2 — Current and proposed workflows

```mermaid
flowchart LR
    subgraph Current["Current paper/Excel workflow"]
        A1[Paper maps] --> A2[Departmental files]
        A3[Excel registers] --> A2
        A4[Cad drawings] --> A2
        A2 --> A5[Duplication and inconsistency]
        A5 --> A6[Slow reporting and weak accountability]
    end

    subgraph Proposed["Proposed digital workflow"]
        B1[Capture<br/>QGIS, QField, Excel templates, CAD] --> B2[Staging<br/>load ID, source, accuracy]
        B2 --> B3[Validation<br/>CRS, domains, geometry, keys]
        B3 --> B4[Production geodatabase<br/>PostGIS or file geodatabase]
        B4 --> B5[Analysis and editing<br/>QGIS Desktop]
        B4 --> B6[Internal map<br/>QGIS Server + Lizmap]
        B4 --> B7[Public views<br/>selective layers and fields]
        B5 --> B8[Feedback and maintenance]
        B6 --> B8
        B7 --> B8
        B8 --> B2
    end
```

**Caption:** The shift from distributed paper records to a staged, validated, and maintained municipal data workflow.

---

## Figure 3 — System architecture

```mermaid
flowchart TB
    subgraph Sources
        S1[Paper maps and scans]
        S2[Excel and CSV]
        S3[Cadastral and engineering CAD]
        S4[Field capture with QField]
        S5[Partner agency data]
    end

    subgraph DataPlatform["Data platform"]
        ST[Staging schema]
        V[Validation and QA]
        DB[(PostgreSQL + PostGIS<br/>or file geodatabase)]
        META[Meta catalogue<br/>layers, fields, domains, contracts]
        AUD[Audit and history]
    end

    subgraph Users
        Q[QGIS Desktop<br/>editing and analysis]
        QS[QGIS Server]
        LZ[Lizmap<br/>internal map]
        PUB[Public views and API]
        LP[Lizmap / MapLibre<br/>public map]
    end

    S1 --> ST
    S2 --> ST
    S3 --> ST
    S4 --> ST
    S5 --> ST
    ST --> V
    V --> DB
    META --> V
    DB --> AUD
    DB --> Q
    Q --> DB
    DB --> QS
    QS --> LZ
    DB --> PUB
    PUB --> LP
    Q --> S4
```

**Caption:** A socio-technical architecture in which the geodatabase, metadata, and validation layer are more durable than any single front-end.

---

## Figure 4 — Data lifecycle and automation

```mermaid
flowchart LR
    A[Capture] --> B[Stage]
    B --> C[Validate]
    C -->|fail| D[Error report]
    D --> A
    C -->|pass| E[Approve]
    E --> F[Publish to production]
    F --> G[Use and analyse]
    G --> H[Feedback and corrections]
    H --> A
    F --> I[Audit and history]
    I --> G
```

**Caption:** The data lifecycle. Automation is concentrated in staging, validation, publication, and audit, not in replacing professional judgement.

---

## Figure 5 — Data governance framework

```mermaid
flowchart TD
    P[Principles<br/>public value, stewardship, quality,<br/>openness, privacy, security, equity]
    R[Roles<br/>mayor/board, CEO, GIS unit,<br/>data owners, data stewards, users, public]
    POL[Policies<br/>standards, metadata, access, privacy,<br/>retention, sharing, procurement]
    PR[Processes<br/>data request, change request, QA,<br/>publication approval, incident response]
    E[Evaluation<br/>maturity, completeness, timeliness,<br/>use, trust, public value]

    P --> R
    R --> POL
    POL --> PR
    PR --> E
    E --> P
```

**Caption:** A five-layer governance framework for RCC’s spatial data system.

---

## Figure 6 — Implementation roadmap

```mermaid
gantt
    title RCC geodatabase implementation roadmap
    dateFormat  YYYY-MM-DD
    axisFormat  %b %Y

    section Phase 0 — Foundation
    Governance, schema, stack, pilot selection :a1, 2026-01-01, 90d

    section Phase 1 — Pilot ward
    Boundaries, roads, addresses, buildings, drains :a2, after a1, 90d

    section Phase 2 — City foundation
    Address gazetteer, roads, buildings, facilities :a3, after a2, 180d

    section Phase 3 — Operations
    Inspections, work orders, requests, dashboards :a4, after a3, 180d

    section Phase 4 — Public
    Public layers, search, print, feedback :a5, after a4, 180d

    section Phase 5 — Scale
    Other city corporations, open data, analytics :a6, after a5, 365d
```

**Caption:** A phased roadmap. The dates are illustrative and should be adjusted to RCC’s budget and procurement cycle.

---

## Figure 7 — Simplified relational database ERD

```mermaid
erDiagram
    WARD ||--o{ PARCEL : contains
    WARD ||--o{ ROAD : contains
    WARD ||--o{ ASSET_REGISTRY : contains

    PARCEL ||--o{ BUILDING : contains
    PARCEL ||--o{ ADDRESS : has
    BUILDING ||--o{ ADDRESS : has
    ROAD ||--o{ ADDRESS : serves
    ROAD ||--o{ ROAD_ASSET : has

    ASSET_REGISTRY ||--o{ INSPECTION : has
    ASSET_REGISTRY ||--o{ WORK_ORDER : has
    ASSET_REGISTRY ||--o{ SERVICE_REQUEST : has

    DRAIN ||--o{ MANHOLE : has
    COLLECTION_ZONE ||--o{ BIN : contains
    COLLECTION_ROUTE ||--o{ BIN : collects

    ASSET_REGISTRY {
        text asset_no PK
        text asset_class
        text asset_type
        text ward_code
        text status_code
    }
    PARCEL {
        text parcel_id PK
        text khatian_no
        text dag_no
        text ward_code
        text land_use_code
        double area_sqm
    }
    BUILDING {
        text building_id PK
        text parcel_id FK
        text holding_no
        text use_code
        int floors
    }
    ADDRESS {
        text address_id PK
        text road_id FK
        text building_id FK
        text parcel_id FK
        text full_address_en
        text full_address_bn
    }
    ROAD {
        text road_id PK
        text name_en
        text name_bn
        text road_class_code
        text ward_code
    }
```

**Caption:** Simplified entity-relationship model. The full schema contains 65 feature classes and 9 tables; the article shows only the core relationships.

---

## Figure 8 — Evaluation framework

```mermaid
flowchart LR
    T[Technical validity<br/>schema, geometry, completeness] --> E[Evaluation]
    O[Organisational fit<br/>workflow, roles, capacity] --> E
    F[Financial value<br/>revenue, maintenance, cost avoidance] --> E
    P[Public value<br/>access, trust, equity, accountability] --> E
    S[Sustainability<br/>ownership, financing, update cadence] --> E
    E --> R[Refined design and roadmap]
```

**Caption:** Multi-dimensional evaluation framework for the proposed system.

---

## Table specifications

### Table 1 — Literature matrix
Use `LITERATURE_MATRIX.csv`. In the article, reduce to 12–15 rows of the most important sources and put the full matrix in supplementary material.

### Table 2 — Benefits, complexities, and solutions
Summarise the literature review in three columns:
- Benefit;
- Complexity;
- Response.

### Table 3 — Layer catalogue
Use the dataset table from the geodatabase README. Include 13 datasets and representative layers, not all 65 feature classes.

### Table 4 — Data dictionary excerpt
Use `DATA_DICTIONARY_EXCERPT.md`. Show 5–6 entities, not the full 1,788-row dictionary.

### Table 5 — RACI matrix
Use the matrix in `GOVERNANCE_FRAMEWORK.md`.

### Table 6 — Risks and mitigations
Use the risk table in `IMPLEMENTATION_ROADMAP.md`.

### Table 7 — Implementation phases and KPIs
Use the phase table in `IMPLEMENTATION_ROADMAP.md`.

### Table 8 — Evaluation criteria
Use the evaluation section in `ARTICLE_PLAN.md`.
