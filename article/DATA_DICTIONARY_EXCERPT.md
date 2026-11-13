# Data Dictionary Excerpt

This excerpt is designed for the article. The full geodatabase dictionary contains 1,788 field definitions; the article should show only the core entities and the design logic.

---

## 1. `CAD.parcel`

| Field | Type | Domain / key | Purpose |
|---|---|---|---|
| `parcel_id` | TEXT(38) | Primary key | Stable parcel identifier |
| `parcel_no` | TEXT(40) | | Survey or holding parcel number |
| `survey_type` | TEXT(20) | `dom_survey_type` | CS, SA, RS, BS, city survey |
| `khatian_no` | TEXT(40) | | Record-of-rights number |
| `dag_no` | TEXT(40) | | Plot number |
| `mouza_code` | TEXT(20) | | Mouza / revenue village |
| `jl_no` | TEXT(20) | | Jurisdiction list number |
| `ward_code` | TEXT(4) | `dom_ward` | RCC ward |
| `holding_no` | TEXT(40) | | Link to holding-tax register |
| `address_id` | TEXT(38) | FK | Primary address |
| `land_use_code` | TEXT(30) | `dom_land_use` | Residential, commercial, mixed, etc. |
| `tenure_code` | TEXT(20) | `dom_tenure` | Private, government, khas, waqf, lease |
| `owner_type_code` | TEXT(20) | `dom_owner_type` | Owner category |
| `area_sqm` | DOUBLE | | Area in square metres |
| `area_katha` | DOUBLE | | Display value in katha |
| `assessed_value_bdt` | DOUBLE | | Assessed value |
| `annual_tax_bdt` | DOUBLE | | Annual tax |
| `arrears_bdt` | DOUBLE | | Arrears |
| `source_code` | TEXT(30) | `dom_source` | Survey, orthophoto, paper map, etc. |
| `accuracy_m` | DOUBLE | | Positional accuracy |
| `geom` | POLYGON | EPSG:32645 | Parcel geometry |

**Design note:** `parcel_id` is stable; `parcel_no`, `khatian_no`, and `dag_no` are business references that may change across survey systems. The parcel is linked to the holding-tax register through `holding_no` and to the address gazetteer through `address_id`.

---

## 2. `CAD.building`

| Field | Type | Domain / key | Purpose |
|---|---|---|---|
| `building_id` | TEXT(38) | Primary key | Stable building identifier |
| `holding_no` | TEXT(40) | | Holding number |
| `name_en` | TEXT(120) | | Building name in English |
| `name_bn` | TEXT(120) | | Building name in Bangla |
| `use_code` | TEXT(30) | `dom_land_use` | Building use |
| `occupancy_code` | TEXT(30) | `dom_occupancy` | Occupancy type |
| `floors` | SHORT | | Number of floors |
| `height_m` | DOUBLE | | Height |
| `footprint_sqm` | DOUBLE | | Footprint area |
| `gross_floor_area_sqm` | DOUBLE | | Gross floor area |
| `construction_type_code` | TEXT(20) | `dom_construction` | RCC, brick, steel, etc. |
| `year_built` | SHORT | | Year of construction |
| `condition_code` | SHORT | `dom_condition` | 0–5 condition rating |
| `parcel_id` | TEXT(38) | FK | Parent parcel |
| `address_id` | TEXT(38) | FK | Address point |
| `bin_asset_no` | TEXT(40) | FK | Waste bin serving the building |

**Design note:** The building is the bridge between the parcel, the address, the holding tax, and service connections. It is also the unit for occupancy, condition, and emergency planning.

---

## 3. `CAD.address_point`

| Field | Type | Domain / key | Purpose |
|---|---|---|---|
| `address_id` | TEXT(38) | Primary key | Stable address identifier |
| `full_address_en` | TEXT(255) | | Full address in English |
| `full_address_bn` | TEXT(255) | | Full address in Bangla |
| `holding_no` | TEXT(40) | | Holding number |
| `road_id` | TEXT(38) | FK | Road |
| `building_id` | TEXT(38) | FK | Building |
| `parcel_id` | TEXT(38) | FK | Parcel |
| `floor` | TEXT(20) | | Floor |
| `unit` | TEXT(20) | | Unit |
| `block` | TEXT(20) | | Block |
| `section` | TEXT(20) | | Section |
| `mohalla` | TEXT(80) | | Mahalla / neighbourhood |
| `ward_code` | TEXT(4) | `dom_ward` | Ward |
| `postcode` | TEXT(10) | | Postcode |
| `latitude` | DOUBLE | | WGS 84 latitude |
| `longitude` | DOUBLE | | WGS 84 longitude |
| `occupancy_code` | TEXT(30) | `dom_occupancy` | Occupancy |
| `status_code` | TEXT(20) | `dom_address_status` | Active, inactive, duplicate, unverified |
| `accuracy_m` | DOUBLE | | Positional accuracy |

**Design note:** The address is the front door to the system. It must support both “house–road–block–section” and “mahalla–holding” address styles. The address gazetteer is built from this table plus `address_range` and place names.

---

## 4. `TRANS.road_centerline`

| Field | Type | Domain / key | Purpose |
|---|---|---|---|
| `road_id` | TEXT(38) | Primary key | Stable road identifier |
| `road_no` | TEXT(40) | | Road number |
| `name_en` | TEXT(120) | | Road name in English |
| `name_bn` | TEXT(120) | | Road name in Bangla |
| `road_class_code` | TEXT(30) | `dom_road_class` | National, regional, city primary, local, lane |
| `surface_code` | TEXT(20) | `dom_surface` | Asphalt, concrete, brick, earthen |
| `carriageway_width_m` | DOUBLE | | Carriageway width |
| `row_width_m` | DOUBLE | | Right-of-way width |
| `lanes` | SHORT | | Number of lanes |
| `one_way` | SHORT | `dom_yes_no` | One-way status |
| `speed_limit_kmh` | SHORT | | Speed limit |
| `from_node_id` / `to_node_id` | TEXT(38) | | Network nodes |
| `address_left_from` / `address_left_to` | TEXT(20) | | Address range, left side |
| `address_right_from` / `address_right_to` | TEXT(20) | | Address range, right side |
| `ward_code` | TEXT(4) | `dom_ward` | Ward |
| `maintainer_code` | TEXT(20) | `dom_owner_org` | RCC, LGED, RHD, etc. |
| `condition_code` | SHORT | `dom_condition` | 0–5 condition |
| `pci` | DOUBLE | | Pavement condition index |
| `last_rehab_date` | DATE | | Last rehabilitation |
| `geom` | POLYLINE | EPSG:32645 | Road centreline |

**Design note:** The road centreline is both a transport layer and an address-range carrier. Address interpolation uses `address_left_from/to` and `address_right_from/to`, which is why the road network must be topologically clean.

---

## 5. `DRAIN.storm_drain`

| Field | Type | Domain / key | Purpose |
|---|---|---|---|
| `asset_no` | TEXT(40) | Primary key | Asset number |
| `asset_class` | TEXT(30) | `dom_asset_class` | DRAIN |
| `asset_type` | TEXT(60) | | Pipe, box drain, open channel |
| `drain_type_code` | TEXT(20) | `dom_drain_type` | Storm, foul, combined |
| `shape_code` | TEXT(20) | `dom_shape` | Circular, rectangular, trapezoidal |
| `diameter_mm` | LONG | | Diameter |
| `width_mm` / `height_mm` | LONG | | Rectangular dimensions |
| `material_code` | TEXT(20) | `dom_material` | Concrete, brick, PVC, etc. |
| `slope_pct` | DOUBLE | | Slope |
| `invert_up_m` | DOUBLE | | Upstream invert level |
| `invert_down_m` | DOUBLE | | Downstream invert level |
| `capacity_m3s` | DOUBLE | | Hydraulic capacity |
| `catchment_id` | TEXT(40) | | Drainage catchment |
| `outfall_id` | TEXT(38) | FK | Outfall |
| `blockage_risk_code` | TEXT(20) | `dom_risk` | Low, medium, high, critical |
| `condition_code` | SHORT | `dom_condition` | 0–5 condition |
| `geom` | POLYLINE | EPSG:32645 | Drain alignment |

**Design note:** Invert levels and flow direction turn a set of lines into a gravity network. The schema stores both geometric and hydraulic information so that RCC can move from “where is the drain?” to “will it drain?”

---

## 6. `WASTE.waste_bin`

| Field | Type | Domain / key | Purpose |
|---|---|---|---|
| `asset_no` | TEXT(40) | Primary key | Bin asset number |
| `asset_class` | TEXT(30) | `dom_asset_class` | WASTE |
| `bin_type_code` | TEXT(20) | `dom_bin_type` | Communal, individual, skip, smart |
| `size_l` | LONG | | Capacity in litres |
| `waste_stream_code` | TEXT(20) | `dom_waste_stream` | Mixed, organic, recyclable, hazardous |
| `collection_zone` | TEXT(40) | | Collection zone name |
| `zone_id` | TEXT(38) | FK | Collection zone |
| `route_id` | TEXT(38) | FK | Collection route |
| `collection_days` | TEXT(40) | | Collection days |
| `frequency_code` | TEXT(20) | `dom_frequency` | Daily, weekly, etc. |
| `location_type_code` | TEXT(20) | `dom_location_type` | Roadside, market, residential, school |
| `ward_code` | TEXT(4) | `dom_ward` | Ward |
| `condition_code` | SHORT | `dom_condition` | 0–5 condition |
| `geom` | POINT | EPSG:32645 | Bin location |

**Design note:** The bin is a small asset with large operational value. Linking bins to zones and routes enables collection planning, missed-bin analysis, and public “when is my collection day?” services.

---

## 7. `asset_registry` table

| Field | Type | Domain / key | Purpose |
|---|---|---|---|
| `asset_no` | TEXT(40) | Primary key | Cross-theme asset number |
| `asset_id` | TEXT(38) | | UUID for future migration |
| `asset_class` | TEXT(30) | `dom_asset_class` | Water, sewer, drain, waste, transport, park, facility |
| `asset_type` | TEXT(60) | | Specific type |
| `theme_schema` | TEXT(20) | | Source dataset |
| `theme_table` | TEXT(60) | | Source table |
| `ward_code` | TEXT(4) | `dom_ward` | Ward |
| `status_code` | TEXT(20) | `dom_status` | Lifecycle status |
| `condition_code` | SHORT | `dom_condition` | 0–5 condition |
| `owner_org_code` | TEXT(20) | `dom_owner_org` | Owner |
| `is_active` | SHORT | `dom_yes_no` | Active record |

**Design note:** The registry is the “thin index” that lets inspections, work orders, and service requests attach to any asset without a new relationship table for every asset type. In a file geodatabase, it must be populated by the editing workflow; in PostGIS, it can be maintained by a trigger or scheduled job.

---

## 8. Domain examples

| Domain | Example values |
|---|---|
| `dom_status` | planned, design, under construction, operational, maintenance, decommissioned, unknown |
| `dom_condition` | 0 unknown, 1 very poor, 2 poor, 3 fair, 4 good, 5 excellent |
| `dom_owner_org` | RCC, RWASA, LGED, RHD, BBA, DPHE, private, community, other |
| `dom_source` | DGPS, GNSS, total station, UAV, mobile GPS, orthophoto, CAD, paper map, field sketch, third party, unknown |
| `dom_road_class` | national, regional, zila, city primary, city secondary, collector, local, lane, service, pedestrian |
| `dom_land_use` | residential, commercial, mixed, industrial, institutional, open space, recreation, water, transport, utility, vacant, agricultural, slum, other |
| `dom_ward` | 01–30 |

---

## Design logic in one paragraph

The dictionary is deliberately repetitive. Every asset-like table carries the same identity, ownership, condition, provenance, and audit block. This repetition is a feature, not a flaw: it allows staff to move between layers without relearning the schema, and it allows the system to append new data without redesigning the database. The differences between layers are confined to the physical and operational attributes that make each asset type distinct.
