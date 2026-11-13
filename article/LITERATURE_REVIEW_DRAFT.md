# Literature Review — Working Draft

## Making the City Legible: Municipal GIS, Spatial Data Infrastructure, and the Governance of Urban Data

### 1. Introduction: from maps to infrastructure

The literature on geographic information systems in local government has moved a long way from the simple question of whether councils should make maps. The early debates were about adoption, efficiency, and the cost of technology. Ventura (1995), for example, described GIS as a practical tool for routine municipal administration, but also warned that its value depended on organisational capacity and sustained data maintenance. Budić (1994) showed that GIS could improve local planning analysis, yet its effectiveness was mediated by data quality, staff skills, and the way planning work was organised. Campbell (1994) found that GIS use in British local government did not automatically change decision-making, and Worrall (1994) argued that investment cases had to account for indirect benefits, maintenance, and organisational costs, not only software acquisition.

Those early studies established a theme that still runs through the literature: **a municipal GIS is a socio-technical system, not a software installation**. Nedović-Budić and Godschalk (1996) emphasised human factors, organisational culture, and leadership in GIS adoption. Nedović-Budić and Pinto (1999) extended the argument to inter-organisational settings, where data sharing depends on trust, standards, and clear custodianship. Ramasubramanian (1999), writing about developing countries, argued that GIS implementation must be understood through organisational theory and reflective practice rather than through imported technical models.

More recent work has shifted the unit of analysis from the individual GIS project to the **spatial data infrastructure** (SDI) that supports a city or a region. Bishop et al. (2000) argued that cities in developing countries need SDIs appropriate to local capacity, data quality, and institutional realities, rather than ambitious systems copied from high-income contexts. Jacoby et al. (2002) showed how a common SDI between state and local government in Australia could reduce duplication and improve access to authoritative data, but only with governance, standards, and coordination. Giff and Crompvoets (2008) and Grus et al. (2011) developed performance indicators and assessment frameworks for SDIs, making the point that infrastructure must be evaluated, not merely built.

This shift matters for Rajshahi City Corporation (RCC). The question is not whether RCC should have a web map. The question is whether it can build and sustain a **municipal spatial data infrastructure**: a shared, governed, maintained system of addresses, parcels, buildings, roads, drains, assets, and operational records that many departments can use and that citizens can eventually trust.

### 2. What cities gain

The literature identifies several benefits of municipal GIS and spatial data infrastructure.

**Operational efficiency and record integration.** Ventura (1995) and Venigalla and Baik (2007) show that GIS can take municipal governments beyond mapping into engineering management, maintenance planning, and service functions. When asset information is linked to location, departments can reduce duplicate records, locate assets faster, and coordinate work across teams.

**Planning and evidence-based decision-making.** Budić (1994) and more recent Bangladeshi studies show that GIS can support plan analysis, land-use assessment, and spatial monitoring. Tanvir and Haque (2023) use remote sensing and GIS to assess development plans in small urban areas of Bangladesh, while Rahman et al. (2022) use GIS to measure urban form and compactness in Dhaka. These studies demonstrate that spatial data can inform planning decisions, but they also depend on reliable municipal data.

**Asset management and maintenance.** Dawidowicz et al. (2019) show how GIS can support sustainable management of municipal housing stock. Kaganova and Telgarsky (2018) argue that local governments need systematic asset information and lifecycle management to make sound capital decisions. ISO 55000 and the International Infrastructure Management Manual (IIMM) provide the broader asset-management logic: condition, criticality, lifecycle cost, and service level. For RCC, this translates into drains, roads, streetlights, waste bins, parks, and public buildings.

**Revenue mobilisation.** Property tax is one of the most important own-source revenues for urban local governments. Norregaard (2013) shows that immovable property tax has substantial revenue potential but requires cadastral information, valuation capacity, and enforcement. Singh et al. (2022) demonstrate a GIS-based property tax assessment model in India, and Namangaya (2018) shows how secondary cities in Tanzania institutionalised GIS for revenue mobilisation. Tanny (2022) situates Bangladesh’s urban local government finance in a context of limited own-source revenue and dependence on transfers. An address and parcel geodatabase is therefore not only a planning tool; it is a fiscal tool.

**Service delivery and transparency.** Mukherjee (2018) shows how an Indian urban local body used GIS as part of e-governance. Conradie and Choenni (2014) and Wilson and Cong (2021) show that local governments can release open data, but that supply alone is not enough: use, usability, and intermediaries matter. For RCC, a public map could improve access to information about wards, roads, parks, facilities, waste collection, and flood risk, but only if it is designed for actual public use.

**Disaster response and climate planning.** Faridatul et al. (2024) show that greenery and waterbodies have a measurable cooling effect in Rajshahi. Habib et al. (2021) examine municipal solid waste and waste-to-energy potential in RCC. Sultana et al. (2025) assess the reliability of open-source spatial data for urban sanitation planning in Rajshahi. These studies show that spatial data can support climate, waste, and sanitation planning, but also that data quality is a serious constraint.

**Public participation.** Obermeyer (1998) and Kar et al. (2016) trace the evolution of public participation GIS and the GeoWeb. GIS can support deliberation and inclusion, but access is uneven and data politics are real. A public map is not automatically participatory; it becomes participatory only when citizens can understand it, use it, and see their feedback reflected in decisions.

### 3. What makes it difficult

The same literature is candid about complexity.

**Data quality and legacy systems.** Municipal data are often incomplete, inconsistent, and spatially inaccurate. Sultana et al. (2025) show that open-source spatial data for sanitation infrastructure in Rajshahi can be useful but requires field validation. Goodchild and Hill (2008) explain why gazetteers and place-name systems are difficult to maintain: names change, boundaries overlap, and authority is contested. Yıldırım et al. (2014) show that street addressing and geocoding are challenging where street naming and numbering are inconsistent. RCC’s paper and Excel legacy is therefore not a trivial starting point; it is the central design problem.

**Institutional fragmentation.** Nedović-Budić and Pinto (1999) and Mukherjee (2020) show that GIS use is shaped by networks of actors and inter-organisational relationships. In RCC’s case, responsibilities overlap with Rajshahi WASA, LGED, RHD, BBS, and the Survey of Bangladesh. A geodatabase that ignores these relationships will duplicate data or fail to become authoritative. Rahman and Szabó (2023) show that Bangladesh’s national SDI has developed but still faces coordination, standards, and uptake challenges. Local systems must connect to national frameworks without waiting for them to be perfect.

**Capacity and organisational change.** Campbell (1994), Ramasubramanian (1999), and Hijazi et al. (2025) all point to capacity, leadership, and organisational learning as critical success factors. A GIS unit with one or two staff cannot maintain a city-wide system without departmental data stewards. Training is necessary but not sufficient; workload, incentives, and career paths matter.

**Financing and maintenance.** Worrall (1994) and Kaganova and Telgarsky (2018) show that the real cost of GIS is not acquisition but maintenance. Municipal budgets often fund hardware and software but not data updates, training, or support. This is a particular risk in Bangladesh, where local governments have limited fiscal space (Tanny, 2022). A system that cannot be maintained will become a costly static map.

**Procurement and vendor lock-in.** Hollands (2014), Paskaleva et al. (2017), and the OECD (2023) warn that smart-city and data-platform projects can become vendor-driven. Proprietary formats, restrictive licences, and opaque algorithms can lock municipalities into costly dependencies. Open standards and open-source tools reduce this risk, but they require in-house capacity and support arrangements (Graser et al., 2025; Steiniger & Hunter, 2013).

**Privacy, surveillance, and data justice.** Kitchin (2014) warns that real-time urban data can enable surveillance and technocratic control. Dencik et al. (2019) argue that data systems must be evaluated for fairness, power, and the distribution of benefits and harms. A municipal geodatabase contains sensitive information about property, tax, complaints, and vulnerable settlements. Public release must be selective, lawful, and ethically framed.

**The digital divide.** Cavallo et al. (2014) show that citizen-initiated digital contacts are unevenly distributed across places and social groups. Obermeyer (1998) and Kar et al. (2016) make a similar point about participation. A public map cannot become the only channel for services; it must sit alongside ward offices, phone lines, and face-to-face support.

**Design-reality gaps.** Heeks (2002) provides the most useful diagnostic: information systems in developing countries often fail because the design assumes conditions that do not exist. Dada (2006), Ndou (2004), Schuppan (2009), and Walsham (2017) extend this argument to e-government and ICT4D. RCC cannot simply import a municipal GIS model from Perth or Wodonga. It must design for paper maps, Excel registers, intermittent connectivity, thin capacity, and political change.

### 4. How the literature says to respond

The literature does not offer a single template, but it converges on several responses.

**Data governance and stewardship.** Khatri and Brown (2010) argue that data governance must define decision rights and accountability for data quality, access, and use. Janssen et al. (2020) extend this to trustworthy data reuse, and the OECD (2023) provides a smart-city governance framework covering access, sharing, privacy, procurement, and public value. For RCC, this means naming data owners and stewards, defining quality rules, and deciding who can publish what.

**Standards, metadata, and assessment.** Giff and Crompvoets (2008), Grus et al. (2011), and Goodchild and Hill (2008) emphasise standards, metadata, and performance indicators. A geodatabase without metadata is a black box. A public map without accuracy statements is misleading. RCC’s system should record source, date, accuracy, and capture method on every feature.

**Fit-for-purpose accuracy.** Williamson (1986) and Enemark et al. (2021) argue that land information systems should be designed for the purpose and context, not for an abstract ideal of precision. RCC should distinguish survey-grade, GPS-grade, orthophoto-digitised, paper-map, and interpolated data. “Fit for purpose” is both a technical and a political principle: it allows progress without pretending to a precision that does not exist.

**Open source and open standards.** Graser et al. (2025) and Steiniger and Hunter (2013) show that the open-source GIS stack is mature enough for serious municipal work. QGIS, PostGIS, QGIS Server, Lizmap, and QField offer a low-licence-cost path that is widely used in resource-constrained settings. The trade-off is the need for training and support.

**Phased implementation and piloting.** Heeks (2002), Ramasubramanian (1999), and Hijazi et al. (2025) imply that incremental, pilot-based implementation is more realistic than a big-bang rollout. A single ward can be used to test the data model, workflows, and governance before city-wide scale-up.

**Public participation and transparency.** Obermeyer (1998), Kar et al. (2016), Conradie and Choenni (2014), and Wilson and Cong (2021) show that public access can create value, but only with usability, documentation, and engagement. RCC should publish selectively, starting with layers that are accurate, non-sensitive, and useful.

**Public value.** Moore (1995) and Benington (2009) provide the normative test: does the system create value that citizens can recognise? Panagiotopoulos et al. (2019) apply this to digital government. For RCC, public value includes fair service delivery, transparent planning, improved revenue administration, and trust that data will not be used against citizens.

### 5. Global cases and the Australian example

The public-facing municipal geoportals of cities such as Perth, Wollongong, Camden, and Wodonga are useful illustrations of what a mature system can look like. The City of Perth’s GeoHub, for example, provides property, planning, transport, security-camera, events, and 3D views through a single interface. Wodonga Council publishes open spatial resources, including property, school crossings, and parking. Camden Council’s interactive mapping tool provides land information, flood, heritage, and other layers. Wollongong City Council offers online maps and property information through its website.

These are not merely technical achievements. They reflect decades of investment in address systems, cadastral data, asset registers, metadata, web services, and governance. Jacoby et al. (2002) show that Australian state–local SDI arrangements were built through coordination and standards, not through a single software purchase. The lesson for RCC is not to copy the layer list. It is to copy the **architecture of stewardship**: authoritative addresses, shared data, clear custodians, and a publication pipeline.

European and North American cases add further lessons. London, Amsterdam, and New York have invested in open data, urban platforms, and digital twins, but the literature also warns about vendor capture, data inequality, and the gap between platform rhetoric and public value (Barns, 2018; Deng et al., 2021; Haraguchi et al., 2024; Hollands, 2014; Kitchin, 2014; OECD, 2023). Asian cases such as Singapore’s OneMap and Indian urban local body initiatives show that strong central coordination can accelerate progress, but local capacity and institutional networks still matter (Mukherjee, 2018, 2020).

The Australian example is especially relevant because it combines local government autonomy with state-level spatial data infrastructure. RCC operates in a more centralised system, but the principle is similar: local systems must connect to national datasets and standards while remaining useful at the ward level.

### 6. The Bangladesh context and the gap

Bangladesh has a rich policy environment for digital government. Smart Bangladesh Vision 2041 emphasises digital government, a smart citizen, a smart economy, and a smart society (Pal & Sarker, 2023). The country has a national NSDI effort, although its maturity and local uptake remain uneven (Rahman & Szabó, 2023). The Local Government (City Corporation) Act, 2009 gives city corporations a broad mandate over urban services, and the Right to Information Act, 2009 provides a legal basis for public access to information, subject to exemptions.

The academic literature on Bangladeshi local government, however, is dominated by studies of e-services, citizen satisfaction, and digital governance rather than municipal spatial data infrastructure. Ferdous (2024) examines local government in Bangladesh within a centralised administrative and fiscal framework. Islam et al. (2026) study digital transformation in municipalities and find uneven capacity and leadership. Chowdhury (2018) examines government web portals and citizen engagement in rural local government. These studies are valuable, but they do not address the geodatabase, address system, asset register, or spatial data governance that would make a municipal map authoritative.

RCC-specific studies tend to focus on e-governance, waste, sanitation, water, and climate rather than on an integrated spatial data system. Habib et al. (2021) examine solid waste and waste-to-energy potential. Sultana et al. (2025) assess open spatial data for sanitation planning. Faridatul et al. (2024) examine greenery and cooling. These studies show the demand for spatial evidence, but they do not provide a municipal data model or governance framework.

The gap is therefore both empirical and conceptual:

- there is little research on municipal GIS in Bangladeshi city corporations;
- there is almost no work that starts from paper/Excel and proposes a full data model, automation pipeline, governance framework, and implementation roadmap;
- there is little connection between address systems, asset registers, property tax, and public value in the Bangladeshi context;
- there is little humanistic reflection on who is made visible, who is missing, and who is protected in municipal spatial data.

This article addresses that gap.

### 7. Conclusion: what the literature implies for RCC

The literature supports four conclusions.

First, **the technology is not the binding constraint**. QGIS, PostGIS, and open web services are mature and affordable. The binding constraints are data quality, stewardship, capacity, and institutional coordination.

Second, **the address is the foundational layer**. Without a consistent address and parcel system, property tax, waste collection, water connections, drainage complaints, and service requests cannot be reliably linked.

Third, **governance must be designed with the system**. Data ownership, quality rules, privacy, access, and publication cannot be added later as an afterthought. They are part of the architecture.

Fourth, **public value must be explicit**. A municipal geodatabase can improve planning and revenue, but it can also surveillance, exclude, or misrepresent. The humanistic question is not decorative. It is a design requirement.

These conclusions frame the proposed RCC geodatabase and the implementation roadmap that follow.
