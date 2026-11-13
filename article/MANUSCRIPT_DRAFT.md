# Making the City Legible
## A Human-Centred Geodatabase for Urban Planning and Local Government in Bangladesh

**Working manuscript draft — not for submission**
**Case:** Rajshahi City Corporation (RCC)
**Method:** Design science research, scoping review, embedded case study
**Target:** *Habitat International* (primary); *Cities*; *Land Use Policy*; *Information Technology for Development*

> **Note to co-authors:** This is a design-phase manuscript. It reports the proposed artifact and the documentary/technical analysis, not completed interviews. Sections marked `[empirical phase]` should be completed after RCC interviews and expert review. Budget figures, ward-level statistics, and quotations must be verified before submission.

---

## Abstract

Bangladeshi city corporations hold a great deal of information that is fundamentally spatial: parcels, roads, drains, buildings, waste collection points, streetlights, taxes, and public facilities. Yet much of this information is kept in paper maps, Excel registers, departmental files, and the memory of experienced staff. The result is not simply a data problem. It is a planning problem, a revenue problem, and a problem of public trust.

This article asks how a resource-constrained city corporation can build a maintainable, human-centred geospatial data infrastructure from a paper-and-Excel starting point. Drawing on a scoping review of municipal GIS, spatial data infrastructure, e-government, and data governance, and using Rajshahi City Corporation as an embedded case, the article proposes a design-science artifact: a thematic geodatabase, an address-centred data model, an automation pipeline, a governance framework, and a phased implementation roadmap. The proposal is assessed against technical, institutional, economic, and public-value criteria.

The article argues that the binding constraint is not software. It is stewardship: who owns, maintains, validates, and shares the data. It also argues that making a city legible need not mean making it surveilled. A municipal geodatabase can be designed to make citizens more visible to planners and service providers while protecting privacy, respecting language and local knowledge, and strengthening public accountability. The article contributes a context-sensitive implementation model for Bangladeshi city corporations and a humanistic account of spatial data infrastructure as public infrastructure.

**Keywords:** municipal GIS; spatial data infrastructure; geodatabase; data governance; urban planning; local government; Bangladesh; Rajshahi City Corporation

---

## 1. Introduction

A ward office in Rajshahi keeps a map on the wall. It may be a printed ward map, a hand-drawn drainage sketch, or a photocopy annotated by a field officer. Nearby, a register records holdings, taxes, and complaints. An engineer keeps drainage drawings in a file. A conservancy officer knows which bins are collected on which day, but that knowledge may not be written down in a form that anyone else can use. The city is, in practice, mapped many times over — in paper, in Excel, and in memory — but rarely in one place that can be trusted across departments.

This is not a failure of individual effort. It is the predictable outcome of under-investment in data infrastructure. The consequences are practical. A drainage complaint cannot be linked to the drain that caused it. A holding-tax record cannot be matched to a building. A ward councillor cannot see which streets are unserved. A planner cannot compare population growth with service capacity. A citizen cannot find out when the waste truck will arrive. The city is visible in fragments, but not legible as a system.

The idea of legibility is central here. Scott (1998) argued that states simplify complex social reality to govern it. That simplification can enable planning, but it can also erase local knowledge, informal settlements, and the messy realities of everyday life. A municipal geodatabase is a legibility project in this sense. It makes the city readable to the administration. The question is whether it also makes the city more governable *for* its citizens, or merely more controllable.

Bangladesh’s policy environment is favourable to digital government. Smart Bangladesh Vision 2041 emphasises a smart citizen, smart government, smart economy, and smart society (Pal & Sarker, 2023). The country has a national spatial data infrastructure effort (Rahman & Szabó, 2023). City corporations have a broad legal mandate over urban services (Local Government (City Corporation) Act, 2009). The Right to Information Act, 2009 creates a basis for public access to information. Yet these national ambitions do not automatically produce municipal data systems. The local work of building addresses, asset registers, and stewardship routines remains.

The international literature offers useful lessons. Municipal GIS has moved from isolated mapping projects to spatial data infrastructure (Bishop et al., 2000; Jacoby et al., 2002). Local governments have used GIS for planning, engineering, asset management, revenue, and public services (Budić, 1994; Kaganova & Telgarsky, 2018; Singh et al., 2022; Ventura, 1995; Venigalla & Baik, 2007). Australian councils such as Perth, Wollongong, Camden, and Wodonga provide visible examples of address-centred public maps that combine property, planning, transport, waste, parks, and open data. But these systems sit on decades of investment in addresses, cadastre, asset registers, metadata, and governance. They cannot simply be copied.

The literature on Bangladeshi local government is rich on e-services, citizen satisfaction, and digital governance, but thin on municipal spatial data infrastructure. Studies of RCC tend to focus on e-governance, waste, sanitation, water, or climate rather than on the geodatabase that would connect them. There is little work that starts from paper and Excel and proposes a full data model, automation pipeline, governance framework, and implementation roadmap. There is even less work that asks who is made visible, who is missing, and who is protected in municipal spatial data.

This article addresses that gap. It asks:

1. What do international municipal GIS and geoportal cases reveal about the benefits, complexities, and governance requirements of city-level spatial data systems?
2. What data model, system architecture, and automation workflow are appropriate for a resource-constrained city corporation starting from paper and Excel records?
3. What governance, capacity, and financing arrangements are needed to sustain such a system?
4. How can an RCC geodatabase create public value in planning, revenue mobilisation, service delivery, and accountability?
5. What phased implementation roadmap can guide other Bangladeshi city corporations?

The article makes four contributions. First, it proposes a context-sensitive municipal data model with a common asset registry, address gazetteer, and thematic layers. Second, it describes a paper-to-digital workflow that records provenance and accuracy rather than pretending the starting data are better than they are. Third, it connects the technical artifact to a governance and implementation model. Fourth, it offers a humanistic argument: the geodatabase is public infrastructure, and its design must be judged by who it serves, who it exposes, and who it leaves out.

The article proceeds in seven parts. Section 2 reviews the literature. Section 3 sets out the conceptual framework. Section 4 describes the methodology. Section 5 introduces the RCC context. Section 6 presents the proposed system. Section 7 discusses planning, economic, governance, and humanistic implications. Section 8 concludes.

---

## 2. Literature review

### 2.1 From municipal mapping to spatial data infrastructure

Early work on GIS in local government focused on adoption, efficiency, and the cost of technology. Ventura (1995) described GIS as a practical tool for routine municipal administration, but warned that its value depended on organisational capacity and sustained data maintenance. Budić (1994) showed that GIS could improve local planning analysis, but its effectiveness was mediated by data quality, staff skills, and the organisation of planning work. Campbell (1994) found that GIS use in British local government did not automatically change decision-making. Worrall (1994) argued that investment cases had to account for indirect benefits, maintenance, and organisational costs, not only software acquisition.

These studies established a durable theme: **a municipal GIS is a socio-technical system, not a software installation**. Nedović-Budić and Godschalk (1996) emphasised human factors, organisational culture, and leadership. Nedović-Budić and Pinto (1999) extended the argument to inter-organisational settings, where data sharing depends on trust, standards, and clear custodianship. Ramasubramanian (1999), writing about developing countries, argued that GIS implementation must be understood through organisational theory and reflective practice rather than imported technical models.

More recent work has shifted the unit of analysis from the individual GIS project to the **spatial data infrastructure** that supports a city or region. Bishop et al. (2000) argued that cities in developing countries need SDIs appropriate to local capacity, data quality, and institutional realities. Jacoby et al. (2002) showed how a common SDI between state and local government in Australia could reduce duplication and improve access to authoritative data, but only with governance, standards, and coordination. Giff and Crompvoets (2008) and Grus et al. (2011) developed performance indicators and assessment frameworks, making the point that infrastructure must be evaluated, not merely built.

This shift matters for RCC. The question is not whether RCC should have a web map. The question is whether it can build and sustain a **municipal spatial data infrastructure**: a shared, governed, maintained system of addresses, parcels, buildings, roads, drains, assets, and operational records that many departments can use and that citizens can eventually trust.

### 2.2 What cities gain

The literature identifies several benefits.

**Operational efficiency and record integration.** Ventura (1995) and Venigalla and Baik (2007) show that GIS can take municipal governments beyond mapping into engineering management, maintenance planning, and service functions. When asset information is linked to location, departments can reduce duplicate records, locate assets faster, and coordinate work across teams.

**Planning and evidence-based decision-making.** Budić (1994) and more recent Bangladeshi studies show that GIS can support plan analysis, land-use assessment, and spatial monitoring. Tanvir and Haque (2023) use remote sensing and GIS to assess development plans in small urban areas of Bangladesh. Rahman et al. (2022) use GIS to measure urban form and compactness in Dhaka. These studies demonstrate that spatial data can inform planning decisions, but they also depend on reliable municipal data.

**Asset management and maintenance.** Dawidowicz et al. (2019) show how GIS can support sustainable management of municipal housing stock. Kaganova and Telgarsky (2018) argue that local governments need systematic asset information and lifecycle management to make sound capital decisions. ISO 55000 and the International Infrastructure Management Manual (IIMM) provide the broader asset-management logic: condition, criticality, lifecycle cost, and service level. For RCC, this translates into drains, roads, streetlights, waste bins, parks, and public buildings.

**Revenue mobilisation.** Property tax is one of the most important own-source revenues for urban local governments. Norregaard (2013) shows that immovable property tax has substantial revenue potential but requires cadastral information, valuation capacity, and enforcement. Singh et al. (2022) demonstrate a GIS-based property tax assessment model in India. Namangaya (2018) shows how secondary cities in Tanzania institutionalised GIS for revenue mobilisation. Tanny (2022) situates Bangladesh’s urban local government finance in a context of limited own-source revenue and dependence on transfers. An address and parcel geodatabase is therefore not only a planning tool; it is a fiscal tool.

**Service delivery and transparency.** Mukherjee (2018) shows how an Indian urban local body used GIS as part of e-governance. Conradie and Choenni (2014) and Wilson and Cong (2021) show that local governments can release open data, but that supply alone is not enough: use, usability, and intermediaries matter. For RCC, a public map could improve access to information about wards, roads, parks, facilities, waste collection, and flood risk, but only if it is designed for actual public use.

**Disaster response and climate planning.** Faridatul et al. (2024) show that greenery and waterbodies have a measurable cooling effect in Rajshahi. Habib et al. (2021) examine municipal solid waste and waste-to-energy potential in RCC. Sultana et al. (2025) assess the reliability of open-source spatial data for urban sanitation planning in Rajshahi. These studies show that spatial data can support climate, waste, and sanitation planning, but also that data quality is a serious constraint.

**Public participation.** Obermeyer (1998) and Kar et al. (2016) trace the evolution of public participation GIS and the GeoWeb. GIS can support deliberation and inclusion, but access is uneven and data politics are real. A public map is not automatically participatory; it becomes participatory only when citizens can understand it, use it, and see their feedback reflected in decisions.

### 2.3 What makes it difficult

**Data quality and legacy systems.** Municipal data are often incomplete, inconsistent, and spatially inaccurate. Sultana et al. (2025) show that open-source spatial data for sanitation infrastructure in Rajshahi can be useful but requires field validation. Goodchild and Hill (2008) explain why gazetteers and place-name systems are difficult to maintain: names change, boundaries overlap, and authority is contested. Yıldırım et al. (2014) show that street addressing and geocoding are challenging where street naming and numbering are inconsistent. RCC’s paper and Excel legacy is therefore not a trivial starting point; it is the central design problem.

**Institutional fragmentation.** Nedović-Budić and Pinto (1999) and Mukherjee (2020) show that GIS use is shaped by networks of actors and inter-organisational relationships. In RCC’s case, responsibilities overlap with Rajshahi WASA, LGED, RHD, BBS, and the Survey of Bangladesh. A geodatabase that ignores these relationships will duplicate data or fail to become authoritative. Rahman and Szabó (2023) show that Bangladesh’s national SDI has developed but still faces coordination, standards, and uptake challenges. Local systems must connect to national frameworks without waiting for them to be perfect.

**Capacity and organisational change.** Campbell (1994), Ramasubramanian (1999), and Hijazi et al. (2025) all point to capacity, leadership, and organisational learning as critical success factors. A GIS unit with one or two staff cannot maintain a city-wide system without departmental data stewards. Training is necessary but not sufficient; workload, incentives, and career paths matter.

**Financing and maintenance.** Worrall (1994) and Kaganova and Telgarsky (2018) show that the real cost of GIS is not acquisition but maintenance. Municipal budgets often fund hardware and software but not data updates, training, or support. This is a particular risk in Bangladesh, where local governments have limited fiscal space (Tanny, 2022). A system that cannot be maintained will become a costly static map.

**Procurement and vendor lock-in.** Hollands (2014), Paskaleva et al. (2017), and the OECD (2023) warn that smart-city and data-platform projects can become vendor-driven. Proprietary formats, restrictive licences, and opaque algorithms can lock municipalities into costly dependencies. Open standards and open-source tools reduce this risk, but they require in-house capacity and support arrangements (Graser et al., 2025; Steiniger & Hunter, 2013).

**Privacy, surveillance, and data justice.** Kitchin (2014) warns that real-time urban data can enable surveillance and technocratic control. Dencik et al. (2019) argue that data systems must be evaluated for fairness, power, and the distribution of benefits and harms. A municipal geodatabase contains sensitive information about property, tax, complaints, and vulnerable settlements. Public release must be selective, lawful, and ethically framed.

**The digital divide.** Cavallo et al. (2014) show that citizen-initiated digital contacts are unevenly distributed across places and social groups. Obermeyer (1998) and Kar et al. (2016) make a similar point about participation. A public map cannot become the only channel for services; it must sit alongside ward offices, phone lines, and face-to-face support.

**Design-reality gaps.** Heeks (2002) provides the most useful diagnostic: information systems in developing countries often fail because the design assumes conditions that do not exist. Dada (2006), Ndou (2004), Schuppan (2009), and Walsham (2017) extend this argument to e-government and ICT4D. RCC cannot simply import a municipal GIS model from Perth or Wodonga. It must design for paper maps, Excel registers, intermittent connectivity, thin capacity, and political change.

### 2.4 How the literature says to respond

**Data governance and stewardship.** Khatri and Brown (2010) argue that data governance must define decision rights and accountability for data quality, access, and use. Janssen et al. (2020) extend this to trustworthy data reuse, and the OECD (2023) provides a smart-city governance framework covering access, sharing, privacy, procurement, and public value. For RCC, this means naming data owners and stewards, defining quality rules, and deciding who can publish what.

**Standards, metadata, and assessment.** Giff and Crompvoets (2008), Grus et al. (2011), and Goodchild and Hill (2008) emphasise standards, metadata, and performance indicators. A geodatabase without metadata is a black box. A public map without accuracy statements is misleading. RCC’s system should record source, date, accuracy, and capture method on every feature.

**Fit-for-purpose accuracy.** Williamson (1986) and Enemark et al. (2021) argue that land information systems should be designed for the purpose and context, not for an abstract ideal of precision. RCC should distinguish survey-grade, GPS-grade, orthophoto-digitised, paper-map, and interpolated data. “Fit for purpose” is both a technical and a political principle: it allows progress without pretending to a precision that does not exist.

**Open source and open standards.** Graser et al. (2025) and Steiniger and Hunter (2013) show that the open-source GIS stack is mature enough for serious municipal work. QGIS, PostGIS, QGIS Server, Lizmap, and QField offer a low-licence-cost path that is widely used in resource-constrained settings. The trade-off is the need for training and support.

**Phased implementation and piloting.** Heeks (2002), Ramasubramanian (1999), and Hijazi et al. (2025) imply that incremental, pilot-based implementation is more realistic than a big-bang rollout. A single ward can be used to test the data model, workflows, and governance before city-wide scale-up.

**Public participation and transparency.** Obermeyer (1998), Kar et al. (2016), Conradie and Choenni (2014), and Wilson and Cong (2021) show that public access can create value, but only with usability, documentation, and engagement. RCC should publish selectively, starting with layers that are accurate, non-sensitive, and useful.

**Public value.** Moore (1995) and Benington (2009) provide the normative test: does the system create value that citizens can recognise? Panagiotopoulos et al. (2019) apply this to digital government. For RCC, public value includes fair service delivery, transparent planning, improved revenue administration, and trust that data will not be used against citizens.

### 2.5 Global cases and the Australian example

The public-facing municipal geoportals of cities such as Perth, Wollongong, Camden, and Wodonga illustrate what a mature system can look like. The City of Perth’s GeoHub provides property, planning, transport, security-camera, events, and 3D views through a single interface. Wodonga Council publishes open spatial resources, including property, school crossings, and parking. Camden Council’s interactive mapping tool provides land information, flood, heritage, and other layers. Wollongong City Council offers online maps and property information through its website.

These are not merely technical achievements. They reflect decades of investment in address systems, cadastral data, asset registers, metadata, web services, and governance. Jacoby et al. (2002) show that Australian state–local SDI arrangements were built through coordination and standards, not through a single software purchase. The lesson for RCC is not to copy the layer list. It is to copy the **architecture of stewardship**: authoritative addresses, shared data, clear custodians, and a publication pipeline.

European and North American cases add further lessons. London, Amsterdam, and New York have invested in open data, urban platforms, and digital twins, but the literature also warns about vendor capture, data inequality, and the gap between platform rhetoric and public value (Barns, 2018; Deng et al., 2021; Haraguchi et al., 2024; Hollands, 2014; Kitchin, 2014; OECD, 2023). Asian cases such as Singapore’s OneMap and Indian urban local body initiatives show that strong central coordination can accelerate progress, but local capacity and institutional networks still matter (Mukherjee, 2018, 2020).

The Australian example is especially relevant because it combines local government autonomy with state-level spatial data infrastructure. RCC operates in a more centralised system, but the principle is similar: local systems must connect to national datasets and standards while remaining useful at the ward level.

### 2.6 The Bangladesh context and the gap

Bangladesh has a rich policy environment for digital government. Smart Bangladesh Vision 2041 emphasises digital government, a smart citizen, a smart economy, and a smart society (Pal & Sarker, 2023). The country has a national NSDI effort, although its maturity and local uptake remain uneven (Rahman & Szabó, 2023). The Local Government (City Corporation) Act, 2009 gives city corporations a broad mandate over urban services, and the Right to Information Act, 2009 provides a legal basis for public access to information, subject to exemptions.

The academic literature on Bangladeshi local government, however, is dominated by studies of e-services, citizen satisfaction, and digital governance rather than municipal spatial data infrastructure. Ferdous (2024) examines local government in Bangladesh within a centralised administrative and fiscal framework. Islam et al. (2026) study digital transformation in municipalities and find uneven capacity and leadership. Chowdhury (2018) examines government web portals and citizen engagement in rural local government. These studies are valuable, but they do not address the geodatabase, address system, asset register, or spatial data governance that would make a municipal map authoritative.

RCC-specific studies tend to focus on e-governance, waste, sanitation, water, and climate rather than on an integrated spatial data system. Habib et al. (2021) examine solid waste and waste-to-energy potential. Sultana et al. (2025) assess open spatial data for sanitation planning. Faridatul et al. (2024) examine greenery and cooling. These studies show the demand for spatial evidence, but they do not provide a municipal data model or governance framework.

The gap is therefore both empirical and conceptual: there is little research on municipal GIS in Bangladeshi city corporations; almost no work starts from paper/Excel and proposes a full data model, automation pipeline, governance framework, and implementation roadmap; and there is little humanistic reflection on who is made visible, who is missing, and who is protected in municipal spatial data.

---

## 3. Conceptual framework

The article combines three lenses.

### 3.1 Socio-technical systems

A municipal geodatabase is not a neutral technical object. It is a bundle of people, processes, standards, incentives, and technologies. Failure is often organisational rather than technical (Campbell, 1994; Nedović-Budić & Godschalk, 1996; Ramasubramanian, 1999). This lens explains why a technically sound schema can still fail if departments do not trust it, if staff are not trained, or if no one owns the data.

### 3.2 Public value

Public value theory asks what the system adds to citizens’ lives, not just what it adds to the administration’s toolkit (Benington, 2009; Moore, 1995; Panagiotopoulos et al., 2019). For RCC, public value includes fair and reliable service delivery; improved revenue without arbitrary enforcement; transparent planning decisions; faster response to drainage, waste, and road problems; accessible information in Bangla and English; and trust that data will not be used to surveil or exclude.

### 3.3 Data governance and stewardship

Data governance defines who can make what decisions about data, under what conditions, and with what accountability (Khatri & Brown, 2010; Janssen et al., 2020). For a city corporation, governance must cover ownership and custodianship; standards and metadata; quality assurance; access classification; privacy and security; retention and archiving; sharing and pricing; and public publication.

Design science research provides the methodological frame for building and evaluating the artifact (Gregor & Hevner, 2013; Hevner et al., 2004; Peffers et al., 2007). The article does not claim a full implementation. It presents an **ex-ante design** validated through documentary analysis, expert review, and a proof-of-concept geodatabase.

---

## 4. Methodology

### 4.1 Research design

A three-part design:

1. **Scoping literature review** — to identify global patterns in municipal GIS, benefits, complexities, and solutions.
2. **Embedded single-case study** — to understand RCC’s current data practices, institutional arrangements, and constraints.
3. **Design science research** — to build and evaluate the proposed geodatabase, workflow, governance framework, and roadmap.

### 4.2 Scoping review

The review follows PRISMA-ScR (Tricco et al., 2018). It is exploratory and thematic, not a meta-analysis.

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

**Synthesis:** thematic analysis (Braun & Clarke, 2006), organised around benefits; complexities; governance and capacity; financing and procurement; public access and equity; and implementation strategies.

### 4.3 Case study

RCC is the embedded case. Data collection for the empirical phase:

- **Documents:** ward maps, holding-tax registers, engineering drawings, annual budgets, organograms, service records, project documents.
- **Interviews:** 8–12 key informants across ICT, engineering, revenue, conservancy, town planning, ward offices, and partner agencies. Semi-structured, 45–60 minutes, anonymised.
- **Observation:** how paper maps and Excel files are used in daily work; where data are duplicated; where handovers fail.
- **Technical artifact:** the geodatabase schema, data dictionary, validation rules, and prototype workflows.
- **Expert review:** a small panel of GIS professionals, urban planners, and municipal practitioners.

### 4.4 Analysis

- Thematic analysis of interviews and documents.
- Comparative case matrix from the literature.
- Design-science evaluation against technical validity, organisational fit, economic value, public value, and sustainability.

### 4.5 Ethics

- University ethics approval before interviews.
- Informed consent and anonymisation.
- No publication of personal tax, owner, or complaint data.
- Careful handling of informal settlements and vulnerable groups.
- Data stored securely and destroyed according to protocol.

### 4.6 Scope of this article

This article reports the design phase. It proposes the artifact and evaluates its internal consistency, feasibility, and public-value logic. It does not claim that the system has been fully implemented or that interviews have been completed. `[empirical phase]` markers indicate where subsequent RCC evidence should be integrated.

---

## 5. Context: Rajshahi City Corporation

Rajshahi City Corporation is one of Bangladesh’s major urban local governments. It covers roughly 96.7 square kilometres, is divided into 30 wards, and spans the Boalia, Motihar, Rajpara, and Shah Makhdum thanas. The city sits on the north bank of the Padma River and faces recurrent drainage, waste, heat, and flood-related challenges (Faridatul et al., 2024; Habib et al., 2021; Rajshahi City Corporation, n.d.).

RCC’s responsibilities include roads, drains, streetlights, waste management, public health, markets, parks, and a range of civic services. It also maintains a holding-tax register, which is one of the most valuable—and least spatially integrated—data assets in the city.

The current information environment is best described as **distributed paper**:

- ward maps and engineering drawings in files;
- holding-tax records in Excel and paper registers;
- asset information in departmental notebooks and procurement files;
- address descriptions that vary by ward and by officer;
- limited shared standards for naming, coding, or geometry;
- no single authoritative address or asset index.

This is not a failure of individual staff. It is the predictable outcome of under-investment in data infrastructure, fragmented mandates, and the absence of a stewardship model.

The wider policy context is favourable. Smart Bangladesh Vision 2041 emphasises digital government and citizen-centred services (Pal & Sarker, 2023). Bangladesh has a national NSDI effort, although its maturity and local uptake remain limited (Rahman & Szabó, 2023). The Local Government (City Corporation) Act, 2009 gives city corporations a broad mandate over urban services and local development. The Right to Information Act, 2009 creates a legal basis for proactive disclosure, subject to privacy and public-interest exceptions.

The institutional ecology is more complicated. Water and sewerage may involve Rajshahi WASA; roads may involve LGED and RHD; land records involve the Survey of Bangladesh and the revenue administration; population and socio-economic data involve BBS. RCC cannot build a municipal geodatabase in isolation. It must decide what it owns, what it shares, and what it references from other agencies.

![Figure 1: Current paper/Excel workflow versus proposed digital workflow](FIGURE_SPECS.md#figure-2--current-and-proposed-workflows)

---

## 6. The proposed system

### 6.1 Design principles

1. **Address first.** The address is the common key for property, tax, waste, water, drainage, and citizen requests.
2. **One system of record.** Excel and paper become sources, not masters.
3. **Stable identifiers.** Every asset and address has a persistent ID.
4. **Provenance on every feature.** Source, date, accuracy, and capture method are mandatory.
5. **Fit for purpose.** Accuracy should match the decision, not an abstract ideal.
6. **Open standards.** QGIS, PostGIS, GeoPackage, OGC services, and portable formats.
7. **Selective publication.** Internal data first; public layers only when ready.
8. **Human-centred.** Bangla/English labels, low-bandwidth design, privacy, and accessibility.

### 6.2 Architecture

The proposed architecture is deliberately modest:

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

The stack is replaceable. The data model, standards, and governance are not. This is a socio-technical architecture, not a software brand.

### 6.3 Data model

The geodatabase contains 13 thematic datasets:

- `REF` — city, ward, thana, mouza, mahalla boundaries; waterbodies.
- `CAD` — parcels, buildings, addresses, address ranges.
- `TRANS` — roads, pavements, footpaths, bridges, streetlights, signals, signs, markings, bus stops, parking.
- `WATER` — mains, service lines, valves, hydrants, meters, reservoirs, pump stations, treatment plants.
- `SEWER` — sewer mains, manholes, lift stations, treatment plants.
- `DRAIN` — storm drains, manholes, catchpits, culverts, outfalls, sluice gates, drainage pumps.
- `WASTE` — bins, collection zones, routes, transfer stations, landfill.
- `PARK` — parks, playgrounds, sports facilities, trees, irrigation assets.
- `FAC` — public facilities and facility sites.
- `PLAN` — zoning, land use, growth areas, development applications, permits, heritage.
- `ENV` — flood extent, water-quality and air-quality sites.
- `OPS` — inspections, work orders, service requests.
- `CIVIC` — points of interest and events.

The full schema contains 65 feature classes, 9 tables, 67 domains, and 27 relationship classes. The article does not reproduce the full dictionary. It shows the design logic and a representative excerpt (Table 4).

A common asset block includes:

```text
asset_id, asset_no, asset_class, asset_type, subtype,
name_en, name_bn, status_code, owner_org_code,
custodian_org_code, operator_org_code, ward_code,
address_id, install_date, commission_date,
decommission_date, condition_code, condition_date,
criticality_code, replacement_value_bdt,
expected_life_yrs, maintenance_code,
source_code, source_date, accuracy_m,
capture_method_code, qa_status_code,
created_at, created_by, updated_at, updated_by, notes
```

### 6.4 Address gazetteer

The address gazetteer is the most important early deliverable. It combines:

- address points;
- address ranges on roads;
- road names;
- ward and mahalla names;
- facility and park names.

It should support both “house–road–block–section” and “mahalla–holding” address styles. It should be searchable in Bangla and English, with fuzzy matching for inconsistent spellings. The gazetteer is the front door to property tax, waste collection, water connections, drainage complaints, and public services.

The literature supports this emphasis. Goodchild and Hill (2008) show that gazetteers are foundational for search and interoperability. Yıldırım et al. (2014) show that street addressing and geocoding are difficult where naming and numbering are inconsistent. Australia’s G-NAF is a national asset that RCC does not have; RCC must build the equivalent locally.

### 6.5 Asset registry

A separate `asset_registry` table indexes every asset across themes. It allows inspections, work orders, and service requests to attach to any asset without schema changes. In a file geodatabase, the registry must be populated by the editing workflow. In PostGIS, it can be maintained by a trigger or scheduled job.

The registry is a pragmatic alternative to a full utility-network model. It does not replace network topology for water and sewer, but it provides a common operational index for a small GIS team.

### 6.6 Automation

The automation model has five stages:

1. **Capture** — QGIS, QField, Excel templates, CAD, paper maps.
2. **Stage** — raw data loaded into a staging table with load metadata.
3. **Validate** — CRS, domains, geometry, uniqueness, parent keys, accuracy.
4. **Publish** — approved records move to production; history is retained.
5. **Share** — internal views, public views, print layouts, and later APIs.

Automation is not only technical. It includes address matching and geocoding; asset-registry updates; duplicate detection; metadata generation; scheduled backups; audit logs; and publication approval.

### 6.7 Governance

The governance framework has five layers:

1. **Principles** — public value, stewardship, quality, openness, privacy, security, equity.
2. **Roles** — mayor/board, CEO, GIS unit, data owners, data stewards, users, public.
3. **Policies** — standards, metadata, access, privacy, retention, sharing, procurement.
4. **Processes** — data request, change request, QA, publication, incident response.
5. **Evaluation** — maturity, completeness, timeliness, use, trust.

A RACI matrix clarifies who is responsible, accountable, consulted, and informed for each data domain (Table 5).

### 6.8 Implementation roadmap

| Phase | Time | Focus | Exit test |
|---|---|---|---|
| 0. Foundation | Months 0–3 | Governance, schema, stack, pilot ward selection | Test load and internal map |
| 1. Pilot ward | Months 3–6 | Boundaries, roads, addresses, buildings, drains, bins, lights, parks | One ward complete |
| 2. City foundation | Months 6–12 | Address gazetteer, roads, buildings, facilities, orthophoto | City-wide foundation |
| 3. Operations | Months 12–18 | Inspections, work orders, requests, dashboards | Daily operational use |
| 4. Public | Months 18–24 | Public layers, search, print, feedback | Public beta |
| 5. Scale | Months 24–36 | Other city corporations, open data, analytics | Replicable model |

The sequencing is deliberate: governance before data; data before public map; pilot before scale; maintenance before expansion.

---

## 7. Discussion

### 7.1 Planning significance

A maintained geodatabase changes the quality of planning conversation. It allows RCC to ask:

- Which wards have the lowest road and drain coverage?
- Where do waste collection routes overlap or leave gaps?
- Which schools, clinics, and markets are inaccessible during floods?
- Where is new development outpacing drainage capacity?
- Which parks and trees serve the hottest neighbourhoods?
- How do service levels differ between wards?

These are not abstract questions. They are the daily substance of urban planning. The geodatabase makes them answerable with evidence rather than anecdote.

The literature supports this planning value (Budić, 1994; Rahman et al., 2022; Tanvir & Haque, 2023). But it also warns that GIS does not automatically change decisions (Campbell, 1994). The system must be embedded in planning routines, budget cycles, and ward meetings.

### 7.2 Economic significance

The economic case rests on four channels.

**Property tax coverage.** An address and parcel geodatabase can identify properties that are missing from the tax register, improve valuation, and reduce leakage (Norregaard, 2013; Singh et al., 2022). Even a modest improvement in coverage can generate significant revenue for a city corporation with limited fiscal space (Tanny, 2022).

**Asset management.** A condition-rated asset register supports maintenance prioritisation, lifecycle costing, and capital planning (Kaganova & Telgarsky, 2018; ISO 55000; IIMM). It helps RCC avoid premature replacement and repeated emergency repairs.

**Operational efficiency.** A shared address and asset index reduces duplicate data collection, time spent searching for records, and repeated site visits. The literature on municipal GIS consistently reports efficiency gains (Ventura, 1995; Venigalla & Baik, 2007).

**Investment and donor confidence.** A credible data system strengthens project proposals, procurement, and reporting. It also reduces the risk of failed investments caused by poor asset information.

The economic argument should be made carefully. A geodatabase is not a revenue guarantee. It is an enabling infrastructure whose value depends on how it is used.

### 7.3 Governance and public value

The governance framework is the condition for sustainability. Data without a steward becomes stale. A public map without a publication gate becomes a privacy risk. A system without a maintenance budget becomes a ruin.

The public-value argument is equally important. A geodatabase can make the city more legible to the administration, but legibility is not automatically good (Scott, 1998). It can make informal settlements more visible for upgrading, or more visible for eviction. It can improve service delivery, or it can become a tool of surveillance. The difference is governance.

Dencik et al. (2019) and Kitchin (2014) remind us that data systems distribute benefits and harms unevenly. RCC should therefore ask:

- Who is counted?
- Who is missing?
- Who is exposed?
- Who can access the map?
- Who can challenge the data?

These questions should be built into the design, not added as an ethics afterthought.

### 7.4 Humanistic considerations

The article’s humanistic argument is simple: a geodatabase is made of people as much as polygons.

Field officers, ward staff, and department clerks are the ones who know where the drains are, which addresses are wrong, and which buildings are missing. Lipsky (1980) shows that street-level bureaucrats shape policy through discretion and daily practice. If the system ignores their knowledge, it will fail. If it captures and respects their knowledge, it can succeed.

The system should also respect language. Bangla labels, Bangla search, and Bangla training materials are not optional. A public map that only works in English is not a public map.

Finally, the system should be modest. It should not promise to solve urban governance. It should help RCC see the city a little more clearly, act a little more consistently, and explain itself a little more openly.

### 7.5 Limitations

This article has several limitations.

First, it is a design proposal, not a completed implementation. The artifact has been specified and technically validated, but it has not been evaluated in routine RCC use.

Second, the empirical evidence from RCC interviews and operational data is not yet integrated. `[empirical phase]`

Third, the schema is intentionally broad. It may be simplified or extended after pilot use.

Fourth, the economic estimates are indicative. They require RCC budget and tax data.

Fifth, the article does not resolve the legal and privacy questions around public release. These require RCC legal review and public consultation.

### 7.6 Research agenda

Future research should:

1. Evaluate the geodatabase in a pilot ward.
2. Measure data capture effort and cost.
3. Test address-matching rates against holding-tax records.
4. Assess the effect on service request resolution.
5. Estimate revenue impact.
6. Study public use and trust.
7. Compare implementation across city corporations.
8. Develop a maturity model for Bangladeshi municipalities.

---

## 8. Conclusion

This article began with a simple observation: RCC already knows a great deal about its city, but that knowledge is scattered across paper, Excel, and memory. The proposed geodatabase is an attempt to make that knowledge shared, maintainable, and useful.

The article argued that the binding constraint is not software. QGIS, PostGIS, and open web services are mature and affordable. The binding constraints are data quality, stewardship, capacity, and institutional coordination.

It also argued that making the city legible need not mean making it surveilled. A municipal geodatabase can be designed to serve citizens, protect privacy, respect language and local knowledge, and strengthen accountability. That is a design choice, not a technical inevitability.

The contribution is a context-sensitive model: an address-centred data model, a common asset registry, a staged automation pipeline, a governance framework, and a phased roadmap. The model is not a universal template. It is a starting point for RCC and for other Bangladeshi city corporations that face similar conditions.

The next step is implementation in a pilot ward. The city does not need a perfect map. It needs a map that can be trusted, corrected, and maintained.

---

## References

The full working reference list is maintained in [`REFERENCES_APA.md`](REFERENCES_APA.md). The BibTeX file is [`REFERENCES.bib`](REFERENCES.bib). Every entry should be checked against the publisher record before submission.

Key sources cited in this draft:

- Benington (2009)
- Bishop et al. (2000)
- Budić (1994)
- Campbell (1994)
- Cavallo et al. (2014)
- Chowdhury (2018)
- Conradie & Choenni (2014)
- Dada (2006)
- Dawidowicz et al. (2019)
- Dencik et al. (2019)
- Deng et al. (2021)
- Enemark et al. (2021)
- Faridatul et al. (2024)
- Ferdous (2024)
- Giff & Crompvoets (2008)
- Goodchild & Hill (2008)
- Graser et al. (2025)
- Gregor & Hevner (2013)
- Grus et al. (2011)
- Habib et al. (2021)
- Haraguchi et al. (2024)
- Heeks (2002)
- Hevner et al. (2004)
- Hijazi et al. (2025)
- Hollands (2014)
- Islam et al. (2026)
- Jacoby et al. (2002)
- Janssen et al. (2020)
- Kaganova & Telgarsky (2018)
- Kar et al. (2016)
- Khatri & Brown (2010)
- Kitchin (2014)
- Lipsky (1980)
- Local Government (City Corporation) Act, 2009
- Moore (1995)
- Mukherjee (2018, 2020)
- Namangaya (2018)
- Nedović-Budić & Godschalk (1996)
- Nedović-Budić & Pinto (1999)
- Ndou (2004)
- Norregaard (2013)
- Obermeyer (1998)
- OECD (2023)
- Pal & Sarker (2023)
- Panagiotopoulos et al. (2019)
- Paskaleva et al. (2017)
- Peffers et al. (2007)
- Rahman & Szabó (2023)
- Rahman et al. (2022)
- Rajshahi City Corporation (n.d.)
- Ramasubramanian (1999)
- Right to Information Act, 2009
- Schuppan (2009)
- Scott (1998)
- Singh et al. (2022)
- Steiniger & Hunter (2013)
- Sultana et al. (2025)
- Tanvir & Haque (2023)
- Tanny (2022)
- Tricco et al. (2018)
- Ventura (1995)
- Venigalla & Baik (2007)
- Walsham (2017)
- Williamson (1986)
- Wilson & Cong (2021)
- Worrall (1994)
- Yıldırım et al. (2014)

---

## Appendices

- Appendix A: Layer catalogue — see `../README.md`.
- Appendix B: Data dictionary excerpt — see `DATA_DICTIONARY_EXCERPT.md`.
- Appendix C: Relational database design — see `ERD.md`.
- Appendix D: Data governance framework — see `GOVERNANCE_FRAMEWORK.md`.
- Appendix E: Implementation roadmap — see `IMPLEMENTATION_ROADMAP.md`.
- Appendix F: Figure specifications — see `FIGURE_SPECS.md`.
- Appendix G: Literature matrix — see `LITERATURE_MATRIX.csv`.
