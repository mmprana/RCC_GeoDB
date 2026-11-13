"""
RCC geodatabase schema definition.

This module is deliberately pure Python so it can be:
  * imported by ArcPy (create_rcc_gdb.py)
  * imported by QGIS/GDAL scripts
  * used to generate an Excel/CSV data dictionary without ArcGIS

Coordinate system: WGS 84 / UTM zone 45N (EPSG:32645)
Vertical datum: to be confirmed by RCC (commonly PWD in Bangladesh)

Naming rules:
  * snake_case
  * units are explicit: _m, _mm, _sqm, _m3, _lps, _bdt
  * _code fields are controlled by domains where possible
  * IDs are stable text UUIDs; business keys are separate
"""

SRID = 32645
GDB_NAME = "RCC.gdb"

DATASETS = [
    "REF",      # reference / boundaries
    "CAD",      # cadastre, buildings, addresses
    "TRANS",    # roads and transport
    "WATER",    # water supply
    "SEWER",    # sewerage
    "DRAIN",    # storm drainage
    "WASTE",    # solid waste
    "PARK",     # parks, trees, recreation
    "FAC",      # community facilities
    "PLAN",     # planning and development
    "ENV",      # environment and flood
    "OPS",      # inspections, work orders, requests
    "CIVIC",    # points of interest
]


# ---------------------------------------------------------------------------
# Field helpers
# ---------------------------------------------------------------------------

def F(name, ftype, length=None, precision=None, scale=None,
      alias=None, domain=None, nullable=True, default=None):
    """Create a field specification."""
    return {
        "name": name,
        "type": ftype,
        "length": length,
        "precision": precision,
        "scale": scale,
        "alias": alias or name.replace("_", " ").title(),
        "domain": domain,
        "nullable": nullable,
        "default": default,
    }


def audit_fields():
    """Provenance, QA and audit fields shared by almost every layer."""
    return [
        F("source_code", "TEXT", 30, domain="dom_source"),
        F("source_date", "DATE"),
        F("accuracy_m", "DOUBLE", precision=8, scale=2),
        F("capture_method_code", "TEXT", 30, domain="dom_capture_method"),
        F("qa_status_code", "TEXT", 20, domain="dom_qa_status", default="pending"),
        F("is_active", "SHORT", domain="dom_yes_no", default="1"),
        F("created_at", "DATE"),
        F("created_by", "TEXT", 50),
        F("updated_at", "DATE"),
        F("updated_by", "TEXT", 50),
        F("notes", "TEXT", 255),
    ]


def asset_fields():
    """Common block for asset-like feature classes."""
    return [
        F("asset_id", "TEXT", 38, alias="Asset ID"),
        F("asset_no", "TEXT", 40, alias="Asset Number", nullable=False),
        F("asset_class", "TEXT", 30, domain="dom_asset_class"),
        F("asset_type", "TEXT", 60),
        F("subtype", "TEXT", 40),
        F("name_en", "TEXT", 120, alias="Name (English)"),
        F("name_bn", "TEXT", 120, alias="Name (Bangla)"),
        F("status_code", "TEXT", 20, domain="dom_status", default="operational"),
        F("owner_org_code", "TEXT", 20, domain="dom_owner_org"),
        F("custodian_org_code", "TEXT", 20, domain="dom_owner_org"),
        F("operator_org_code", "TEXT", 20, domain="dom_owner_org"),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("address_id", "TEXT", 38),
        F("install_date", "DATE"),
        F("commission_date", "DATE"),
        F("decommission_date", "DATE"),
        F("condition_code", "SHORT", domain="dom_condition"),
        F("condition_date", "DATE"),
        F("criticality_code", "SHORT", domain="dom_criticality"),
        F("replacement_value_bdt", "DOUBLE", precision=18, scale=2),
        F("expected_life_yrs", "SHORT"),
        F("maintenance_code", "TEXT", 30, domain="dom_maintenance"),
    ]


def FC(dataset, name, alias, geometry, fields, key,
       subtype_field=None, subtypes=None):
    """Create a feature class specification."""
    return {
        "dataset": dataset,
        "name": name,
        "alias": alias,
        "geometry": geometry,
        "fields": fields,
        "key": key,
        "subtype_field": subtype_field,
        "subtypes": subtypes or [],
    }


def T(name, alias, fields, key):
    """Create a standalone table specification."""
    return {
        "name": name,
        "alias": alias,
        "fields": fields,
        "key": key,
    }


# ---------------------------------------------------------------------------
# Domains (coded value lists)
# ---------------------------------------------------------------------------

def C(ftype, description, values):
    return {
        "type": ftype,
        "description": description,
        "domain_type": "CODED",
        "values": values,
    }


DOMAINS = {
    "dom_yes_no": C("SHORT", "Yes / No", [(1, "Yes"), (0, "No")]),
    "dom_ward": C("TEXT", "RCC ward (01-30)",
                  [(f"{i:02d}", f"Ward {i:02d}") for i in range(1, 31)]),
    "dom_status": C("TEXT", "Asset lifecycle status", [
        ("planned", "Planned"),
        ("design", "Design"),
        ("under_construction", "Under construction"),
        ("operational", "Operational"),
        ("maintenance", "Under maintenance"),
        ("decommissioned", "Decommissioned"),
        ("unknown", "Unknown"),
    ]),
    "dom_condition": C("SHORT", "Condition rating (IIMM-style 0-5)", [
        (0, "Unknown"),
        (1, "Very poor"),
        (2, "Poor"),
        (3, "Fair"),
        (4, "Good"),
        (5, "Excellent"),
    ]),
    "dom_criticality": C("SHORT", "Criticality", [
        (1, "Low"),
        (2, "Moderate"),
        (3, "High"),
        (4, "Very high"),
        (5, "Critical"),
    ]),
    "dom_priority": C("SHORT", "Work priority", [
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
        (4, "Urgent"),
        (5, "Emergency"),
    ]),
    "dom_owner_org": C("TEXT", "Owner / custodian / operator", [
        ("RCC", "Rajshahi City Corporation"),
        ("RWASA", "Rajshahi WASA"),
        ("LGED", "LGED"),
        ("RHD", "Roads and Highways Department"),
        ("BBA", "Bangladesh Bridge Authority"),
        ("DPHE", "DPHE"),
        ("PRIVATE", "Private"),
        ("COMMUNITY", "Community"),
        ("OTHER", "Other"),
    ]),
    "dom_asset_class": C("TEXT", "Asset class", [
        ("WATER", "Water"),
        ("SEWER", "Sewer"),
        ("DRAIN", "Drainage"),
        ("WASTE", "Waste"),
        ("TRANSPORT", "Transport"),
        ("PARK", "Park"),
        ("FACILITY", "Facility"),
        ("BUILDING", "Building"),
        ("OTHER", "Other"),
    ]),
    "dom_source": C("TEXT", "Data source", [
        ("DGPS", "DGPS"),
        ("GNSS", "GNSS"),
        ("TOTAL_STATION", "Total station"),
        ("UAV", "UAV / drone"),
        ("MOBILE_GPS", "Mobile GPS"),
        ("ORTHO", "Digitised orthophoto"),
        ("CAD", "CAD as-built"),
        ("PAPER", "Paper map"),
        ("FIELD", "Field sketch"),
        ("THIRD_PARTY", "Third party"),
        ("UNKNOWN", "Unknown"),
    ]),
    "dom_capture_method": C("TEXT", "Capture method", [
        ("SURVEY", "Survey"),
        ("GNSS", "GNSS"),
        ("TOTAL_STATION", "Total station"),
        ("UAV", "UAV"),
        ("DIGITISED", "Digitised"),
        ("CAD", "CAD"),
        ("PAPER", "Paper"),
        ("FIELD", "Field"),
        ("THIRD_PARTY", "Third party"),
        ("UNKNOWN", "Unknown"),
    ]),
    "dom_qa_status": C("TEXT", "QA status", [
        ("pending", "Pending"),
        ("passed", "Passed"),
        ("failed", "Failed"),
        ("not_checked", "Not checked"),
    ]),
    "dom_maintenance": C("TEXT", "Maintenance responsibility", [
        ("RCC", "RCC"),
        ("CONTRACTOR", "Contractor"),
        ("COMMUNITY", "Community"),
        ("PRIVATE", "Private"),
        ("NONE", "None"),
    ]),
    "dom_road_class": C("TEXT", "Road class", [
        ("NATIONAL", "National highway"),
        ("REGIONAL", "Regional road"),
        ("ZILA", "Zila road"),
        ("CITY_PRIMARY", "City primary"),
        ("CITY_SECONDARY", "City secondary"),
        ("COLLECTOR", "Collector"),
        ("LOCAL", "Local"),
        ("LANE", "Lane"),
        ("SERVICE", "Service"),
        ("PEDESTRIAN", "Pedestrian"),
    ]),
    "dom_surface": C("TEXT", "Surface type", [
        ("ASPHALT", "Asphalt"),
        ("CONCRETE", "Concrete"),
        ("BRICK", "Brick"),
        ("PAVER", "Paver"),
        ("GRAVEL", "Gravel"),
        ("EARTHEN", "Earthen"),
        ("OTHER", "Other"),
    ]),
    "dom_land_use": C("TEXT", "Land use", [
        ("RESIDENTIAL", "Residential"),
        ("COMMERCIAL", "Commercial"),
        ("MIXED", "Mixed"),
        ("INDUSTRIAL", "Industrial"),
        ("INSTITUTIONAL", "Institutional"),
        ("OPEN_SPACE", "Open space"),
        ("RECREATION", "Recreation"),
        ("WATER", "Water"),
        ("TRANSPORT", "Transport"),
        ("UTILITY", "Utility"),
        ("VACANT", "Vacant"),
        ("AGRICULTURAL", "Agricultural"),
        ("SLUM", "Slum / low-income"),
        ("OTHER", "Other"),
    ]),
    "dom_tenure": C("TEXT", "Land tenure", [
        ("PRIVATE", "Private"),
        ("GOVERNMENT", "Government"),
        ("KHAS", "Khas"),
        ("WAQF", "Waqf"),
        ("LEASE", "Lease"),
        ("TRUST", "Trust"),
        ("DISPUTED", "Disputed"),
        ("UNKNOWN", "Unknown"),
    ]),
    "dom_owner_type": C("TEXT", "Owner type", [
        ("PRIVATE", "Private"),
        ("GOVT", "Government"),
        ("KHAS", "Khas"),
        ("WAQF", "Waqf"),
        ("TRUST", "Trust"),
        ("DISPUTED", "Disputed"),
        ("UNKNOWN", "Unknown"),
    ]),
    "dom_survey_type": C("TEXT", "Survey type", [
        ("CS", "CS"),
        ("SA", "SA"),
        ("RS", "RS"),
        ("BS", "BS"),
        ("CITY", "City survey"),
        ("OTHER", "Other"),
    ]),
    "dom_occupancy": C("TEXT", "Occupancy", [
        ("RESIDENTIAL", "Residential"),
        ("COMMERCIAL", "Commercial"),
        ("MIXED", "Mixed"),
        ("INSTITUTIONAL", "Institutional"),
        ("INDUSTRIAL", "Industrial"),
        ("VACANT", "Vacant"),
        ("OTHER", "Other"),
    ]),
    "dom_construction": C("TEXT", "Construction type", [
        ("RCC", "RCC"),
        ("BRICK", "Brick"),
        ("STEEL", "Steel"),
        ("TIMBER", "Timber"),
        ("MUD", "Mud"),
        ("MIXED", "Mixed"),
        ("OTHER", "Other"),
    ]),
    "dom_address_status": C("TEXT", "Address status", [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("duplicate", "Duplicate"),
        ("unverified", "Unverified"),
    ]),
    "dom_side": C("TEXT", "Road side", [
        ("LEFT", "Left"),
        ("RIGHT", "Right"),
        ("BOTH", "Both"),
    ]),
    "dom_waste_stream": C("TEXT", "Waste stream", [
        ("MIXED", "Mixed"),
        ("ORGANIC", "Organic"),
        ("RECYCLABLE", "Recyclable"),
        ("HAZARDOUS", "Hazardous"),
        ("CONSTRUCTION", "Construction"),
        ("E_WASTE", "E-waste"),
    ]),
    "dom_frequency": C("TEXT", "Collection frequency", [
        ("DAILY", "Daily"),
        ("ALTERNATE_DAY", "Alternate day"),
        ("TWICE_WEEKLY", "Twice weekly"),
        ("WEEKLY", "Weekly"),
        ("FORTNIGHTLY", "Fortnightly"),
        ("ON_CALL", "On call"),
    ]),
    "dom_material": C("TEXT", "Material", [
        ("AC", "Asbestos cement"),
        ("DI", "Ductile iron"),
        ("CI", "Cast iron"),
        ("PVC", "PVC"),
        ("HDPE", "HDPE"),
        ("CONCRETE", "Concrete"),
        ("BRICK", "Brick"),
        ("STEEL", "Steel"),
        ("OTHER", "Other"),
    ]),
    "dom_network_role": C("TEXT", "Water network role", [
        ("TRUNK", "Trunk"),
        ("DISTRIBUTION", "Distribution"),
        ("SERVICE", "Service"),
    ]),
    "dom_valve_type": C("TEXT", "Valve type", [
        ("GATE", "Gate"),
        ("BUTTERFLY", "Butterfly"),
        ("AIR", "Air"),
        ("PRESSURE_REDUCING", "Pressure reducing"),
        ("OTHER", "Other"),
    ]),
    "dom_valve_status": C("TEXT", "Valve operating status", [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
        ("PARTLY_OPEN", "Partly open"),
        ("UNKNOWN", "Unknown"),
    ]),
    "dom_hydrant_type": C("TEXT", "Hydrant type", [
        ("PILLAR", "Pillar"),
        ("UNDERGROUND", "Underground"),
        ("OTHER", "Other"),
    ]),
    "dom_meter_type": C("TEXT", "Meter type", [
        ("MECHANICAL", "Mechanical"),
        ("SMART", "Smart"),
        ("OTHER", "Other"),
    ]),
    "dom_reservoir_type": C("TEXT", "Reservoir type", [
        ("GROUND", "Ground"),
        ("ELEVATED", "Elevated"),
        ("UNDERGROUND", "Underground"),
        ("OTHER", "Other"),
    ]),
    "dom_pump_type": C("TEXT", "Pump type", [
        ("CENTRIFUGAL", "Centrifugal"),
        ("SUBMERSIBLE", "Submersible"),
        ("AXIAL", "Axial"),
        ("OTHER", "Other"),
    ]),
    "dom_fuel": C("TEXT", "Fuel / power source", [
        ("ELECTRIC", "Electric"),
        ("DIESEL", "Diesel"),
        ("GAS", "Gas"),
        ("SOLAR", "Solar"),
        ("OTHER", "Other"),
    ]),
    "dom_sewer_type": C("TEXT", "Sewer type", [
        ("GRAVITY", "Gravity"),
        ("PRESSURE", "Pressure"),
        ("COMBINED", "Combined"),
    ]),
    "dom_manhole_type": C("TEXT", "Manhole type", [
        ("STRAIGHT", "Straight"),
        ("JUNCTION", "Junction"),
        ("DROP", "Drop"),
        ("FLUSH", "Flush"),
        ("OTHER", "Other"),
    ]),
    "dom_cover_type": C("TEXT", "Cover type", [
        ("RCC", "RCC"),
        ("CI", "Cast iron"),
        ("STEEL", "Steel"),
        ("COMPOSITE", "Composite"),
        ("OTHER", "Other"),
    ]),
    "dom_drain_type": C("TEXT", "Drain type", [
        ("STORM", "Storm"),
        ("FOUL", "Foul"),
        ("COMBINED", "Combined"),
    ]),
    "dom_shape": C("TEXT", "Cross-section shape", [
        ("CIRCULAR", "Circular"),
        ("RECTANGULAR", "Rectangular"),
        ("TRAPEZOIDAL", "Trapezoidal"),
        ("OVAL", "Oval"),
        ("OTHER", "Other"),
    ]),
    "dom_catchpit_type": C("TEXT", "Catchpit type", [
        ("ROAD", "Road"),
        ("FOOTPATH", "Footpath"),
        ("YARD", "Yard"),
        ("OTHER", "Other"),
    ]),
    "dom_culvert_type": C("TEXT", "Culvert type", [
        ("PIPE", "Pipe"),
        ("BOX", "Box"),
        ("ARCH", "Arch"),
        ("OTHER", "Other"),
    ]),
    "dom_outfall_type": C("TEXT", "Outfall type", [
        ("RIVER", "River"),
        ("CANAL", "Canal"),
        ("POND", "Pond"),
        ("OTHER", "Other"),
    ]),
    "dom_gate_type": C("TEXT", "Sluice gate type", [
        ("FLAP", "Flap"),
        ("SLUICE", "Sluice"),
        ("PENSTOCK", "Penstock"),
        ("OTHER", "Other"),
    ]),
    "dom_bin_type": C("TEXT", "Bin type", [
        ("COMMUNAL", "Communal"),
        ("INDIVIDUAL", "Individual"),
        ("SKIP", "Skip"),
        ("SMART", "Smart"),
    ]),
    "dom_location_type": C("TEXT", "Location type", [
        ("ROADSIDE", "Roadside"),
        ("MARKET", "Market"),
        ("RESIDENTIAL", "Residential"),
        ("SCHOOL", "School"),
        ("HOSPITAL", "Hospital"),
        ("PARK", "Park"),
        ("OTHER", "Other"),
    ]),
    "dom_park_class": C("TEXT", "Park classification", [
        ("REGIONAL", "Regional"),
        ("CITY", "City"),
        ("NEIGHBOURHOOD", "Neighbourhood"),
        ("POCKET", "Pocket"),
        ("PLAYGROUND", "Playground"),
        ("OTHER", "Other"),
    ]),
    "dom_maintenance_grade": C("TEXT", "Maintenance grade", [
        ("A", "A - high"),
        ("B", "B - medium"),
        ("C", "C - low"),
    ]),
    "dom_health": C("TEXT", "Tree health", [
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
        ("POOR", "Poor"),
        ("DEAD", "Dead"),
        ("UNKNOWN", "Unknown"),
    ]),
    "dom_risk": C("TEXT", "Risk rating", [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]),
    "dom_facility_type": C("SHORT", "Public facility type", [
        (1, "Market"),
        (2, "Public toilet"),
        (3, "Community centre"),
        (4, "School"),
        (5, "Hospital"),
        (6, "Mosque"),
        (7, "Cemetery"),
        (8, "Cyclone shelter"),
        (9, "Other"),
    ]),
    "dom_zone_type": C("TEXT", "Zoning type", [
        ("RESIDENTIAL", "Residential"),
        ("COMMERCIAL", "Commercial"),
        ("MIXED", "Mixed"),
        ("INDUSTRIAL", "Industrial"),
        ("INSTITUTIONAL", "Institutional"),
        ("OPEN", "Open space"),
        ("AGRICULTURAL", "Agricultural"),
        ("WATER", "Water"),
        ("OTHER", "Other"),
    ]),
    "dom_application_status": C("TEXT", "Application status", [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("UNDER_REVIEW", "Under review"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("WITHDRAWN", "Withdrawn"),
    ]),
    "dom_permit_type": C("TEXT", "Permit type", [
        ("BUILDING", "Building"),
        ("TRADE", "Trade"),
        ("SIGN", "Sign"),
        ("DEMOLITION", "Demolition"),
        ("OTHER", "Other"),
    ]),
    "dom_heritage_type": C("TEXT", "Heritage type", [
        ("BUILDING", "Building"),
        ("SITE", "Site"),
        ("MONUMENT", "Monument"),
        ("PRECINCT", "Precinct"),
        ("OTHER", "Other"),
    ]),
    "dom_flood_type": C("TEXT", "Flood type", [
        ("RIVER", "River flood"),
        ("RAINFALL", "Rainfall flood"),
        ("TIDAL", "Tidal"),
        ("DRAINAGE", "Drainage"),
        ("OTHER", "Other"),
    ]),
    "dom_inspection_type": C("TEXT", "Inspection type", [
        ("ROUTINE", "Routine"),
        ("CONDITION", "Condition"),
        ("DEFECT", "Defect"),
        ("SAFETY", "Safety"),
        ("OTHER", "Other"),
    ]),
    "dom_method": C("TEXT", "Assessment method", [
        ("VISUAL", "Visual"),
        ("CCTV", "CCTV"),
        ("ACOUSTIC", "Acoustic"),
        ("HYDRAULIC", "Hydraulic"),
        ("LIDAR", "LiDAR"),
        ("OTHER", "Other"),
    ]),
    "dom_action": C("TEXT", "Recommended action", [
        ("NONE", "None"),
        ("MONITOR", "Monitor"),
        ("REPAIR", "Repair"),
        ("REPLACE", "Replace"),
        ("INVESTIGATE", "Investigate"),
    ]),
    "dom_wo_type": C("TEXT", "Work order type", [
        ("REPAIR", "Repair"),
        ("MAINTENANCE", "Maintenance"),
        ("INSPECTION", "Inspection"),
        ("CLEANING", "Cleaning"),
        ("INSTALLATION", "Installation"),
        ("OTHER", "Other"),
    ]),
    "dom_wo_status": C("TEXT", "Work order status", [
        ("OPEN", "Open"),
        ("ASSIGNED", "Assigned"),
        ("IN_PROGRESS", "In progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]),
    "dom_request_channel": C("TEXT", "Request channel", [
        ("PHONE", "Phone"),
        ("EMAIL", "Email"),
        ("WEB", "Web"),
        ("WALK_IN", "Walk-in"),
        ("SOCIAL", "Social media"),
        ("FIELD", "Field staff"),
    ]),
    "dom_request_status": C("TEXT", "Request status", [
        ("NEW", "New"),
        ("ASSIGNED", "Assigned"),
        ("IN_PROGRESS", "In progress"),
        ("RESOLVED", "Resolved"),
        ("CLOSED", "Closed"),
    ]),
    "dom_poi_category": C("TEXT", "Point of interest category", [
        ("TOURISM", "Tourism"),
        ("EDUCATION", "Education"),
        ("HEALTH", "Health"),
        ("RELIGION", "Religion"),
        ("MARKET", "Market"),
        ("TRANSPORT", "Transport"),
        ("OTHER", "Other"),
    ]),
    "dom_waterbody_type": C("TEXT", "Waterbody type", [
        ("RIVER", "River"),
        ("CANAL", "Canal"),
        ("POND", "Pond"),
        ("LAKE", "Lake"),
        ("DRAIN", "Drain"),
        ("OTHER", "Other"),
    ]),
    "dom_structure_type": C("TEXT", "Structure type", [
        ("BRIDGE", "Bridge"),
        ("CULVERT", "Culvert"),
        ("FOOTBRIDGE", "Footbridge"),
        ("OTHER", "Other"),
    ]),
    "dom_signal_type": C("TEXT", "Traffic signal type", [
        ("VEHICLE", "Vehicle"),
        ("PEDESTRIAN", "Pedestrian"),
        ("COMBINED", "Combined"),
    ]),
    "dom_parking_type": C("TEXT", "Parking type", [
        ("ON_STREET", "On-street"),
        ("OFF_STREET", "Off-street"),
        ("MULTI_LEVEL", "Multi-level"),
    ]),
    "dom_energy_source": C("TEXT", "Energy source", [
        ("GRID", "Grid"),
        ("SOLAR", "Solar"),
        ("GENERATOR", "Generator"),
        ("OTHER", "Other"),
    ]),
}


# ---------------------------------------------------------------------------
# Feature classes
# ---------------------------------------------------------------------------

FEATURE_CLASSES = [

    # -----------------------------------------------------------------------
    # REFERENCE / BOUNDARIES
    # -----------------------------------------------------------------------
    FC("REF", "city_boundary", "City Boundary", "POLYGON", [
        F("city_code", "TEXT", 20, nullable=False),
        F("city_name_en", "TEXT", 120, alias="City Name (English)"),
        F("city_name_bn", "TEXT", 120, alias="City Name (Bangla)"),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
        F("population", "LONG"),
        F("established_date", "DATE"),
    ] + audit_fields(), "city_code"),

    FC("REF", "ward_boundary", "Ward Boundary", "POLYGON", [
        F("ward_code", "TEXT", 4, domain="dom_ward", nullable=False),
        F("ward_no", "SHORT"),
        F("ward_name_en", "TEXT", 120, alias="Ward Name (English)"),
        F("ward_name_bn", "TEXT", 120, alias="Ward Name (Bangla)"),
        F("thana_code", "TEXT", 20),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
        F("population", "LONG"),
        F("councillor_name", "TEXT", 120),
        F("office_address", "TEXT", 255),
    ] + audit_fields(), "ward_code"),

    FC("REF", "thana_boundary", "Thana Boundary", "POLYGON", [
        F("thana_code", "TEXT", 20, nullable=False),
        F("thana_name_en", "TEXT", 120, alias="Thana Name (English)"),
        F("thana_name_bn", "TEXT", 120, alias="Thana Name (Bangla)"),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
    ] + audit_fields(), "thana_code"),

    FC("REF", "mouza_boundary", "Mouza / JL Boundary", "POLYGON", [
        F("mouza_code", "TEXT", 20, nullable=False),
        F("mouza_name", "TEXT", 120),
        F("jl_no", "TEXT", 20),
        F("thana_code", "TEXT", 20),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
    ] + audit_fields(), "mouza_code"),

    FC("REF", "mahalla_boundary", "Mahalla Boundary", "POLYGON", [
        F("mahalla_code", "TEXT", 20, nullable=False),
        F("mahalla_name_en", "TEXT", 120, alias="Mahalla Name (English)"),
        F("mahalla_name_bn", "TEXT", 120, alias="Mahalla Name (Bangla)"),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
    ] + audit_fields(), "mahalla_code"),

    FC("REF", "waterbody", "Waterbody", "POLYGON", [
        F("waterbody_id", "TEXT", 38, nullable=False),
        F("waterbody_name", "TEXT", 120),
        F("waterbody_type_code", "TEXT", 20, domain="dom_waterbody_type"),
        F("owner_org_code", "TEXT", 20, domain="dom_owner_org"),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
    ] + audit_fields(), "waterbody_id"),

    # -----------------------------------------------------------------------
    # CADASTRE / ADDRESSES / BUILDINGS
    # -----------------------------------------------------------------------
    FC("CAD", "parcel", "Parcel", "POLYGON", [
        F("parcel_id", "TEXT", 38, nullable=False),
        F("parcel_no", "TEXT", 40),
        F("survey_type", "TEXT", 20, domain="dom_survey_type"),
        F("khatian_no", "TEXT", 40),
        F("dag_no", "TEXT", 40),
        F("mouza_code", "TEXT", 20),
        F("jl_no", "TEXT", 20),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("holding_no", "TEXT", 40),
        F("address_id", "TEXT", 38),
        F("land_use_code", "TEXT", 30, domain="dom_land_use"),
        F("tenure_code", "TEXT", 20, domain="dom_tenure"),
        F("owner_type_code", "TEXT", 20, domain="dom_owner_type"),
        F("owner_name", "TEXT", 120),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
        F("area_katha", "DOUBLE", precision=10, scale=2),
        F("assessed_value_bdt", "DOUBLE", precision=18, scale=2),
        F("annual_tax_bdt", "DOUBLE", precision=18, scale=2),
        F("arrears_bdt", "DOUBLE", precision=18, scale=2),
        F("building_id", "TEXT", 38),
    ] + audit_fields(), "parcel_id"),

    FC("CAD", "building", "Building", "POLYGON", [
        F("building_id", "TEXT", 38, nullable=False),
        F("holding_no", "TEXT", 40),
        F("name_en", "TEXT", 120, alias="Name (English)"),
        F("name_bn", "TEXT", 120, alias="Name (Bangla)"),
        F("use_code", "TEXT", 30, domain="dom_land_use"),
        F("occupancy_code", "TEXT", 30, domain="dom_occupancy"),
        F("floors", "SHORT"),
        F("height_m", "DOUBLE", precision=8, scale=2),
        F("footprint_sqm", "DOUBLE", precision=18, scale=2),
        F("gross_floor_area_sqm", "DOUBLE", precision=18, scale=2),
        F("construction_type_code", "TEXT", 20, domain="dom_construction"),
        F("year_built", "SHORT"),
        F("condition_code", "SHORT", domain="dom_condition"),
        F("approval_no", "TEXT", 40),
        F("permit_date", "DATE"),
        F("occupancy_cert_no", "TEXT", 40),
        F("water_connection_no", "TEXT", 40),
        F("sewer_connection_no", "TEXT", 40),
        F("bin_asset_no", "TEXT", 40),
        F("occupants", "LONG"),
        F("accessible", "SHORT", domain="dom_yes_no"),
        F("heritage_flag", "SHORT", domain="dom_yes_no"),
        F("parcel_id", "TEXT", 38),
        F("address_id", "TEXT", 38),
    ] + audit_fields(), "building_id"),

    FC("CAD", "address_point", "Address Point", "POINT", [
        F("address_id", "TEXT", 38, nullable=False),
        F("full_address_en", "TEXT", 255, alias="Full Address (English)"),
        F("full_address_bn", "TEXT", 255, alias="Full Address (Bangla)"),
        F("holding_no", "TEXT", 40),
        F("road_id", "TEXT", 38),
        F("building_id", "TEXT", 38),
        F("parcel_id", "TEXT", 38),
        F("floor", "TEXT", 20),
        F("unit", "TEXT", 20),
        F("block", "TEXT", 20),
        F("section", "TEXT", 20),
        F("mohalla", "TEXT", 80),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("postcode", "TEXT", 10),
        F("latitude", "DOUBLE", precision=10, scale=7),
        F("longitude", "DOUBLE", precision=10, scale=7),
        F("entrance_type", "TEXT", 30),
        F("occupancy_code", "TEXT", 30, domain="dom_occupancy"),
        F("status_code", "TEXT", 20, domain="dom_address_status", default="unverified"),
    ] + audit_fields(), "address_id"),

    FC("CAD", "address_range", "Address Range", "POLYLINE", [
        F("range_id", "TEXT", 38, nullable=False),
        F("road_id", "TEXT", 38),
        F("side_code", "TEXT", 10, domain="dom_side"),
        F("from_no", "TEXT", 20),
        F("to_no", "TEXT", 20),
        F("from_measure", "DOUBLE", precision=12, scale=2),
        F("to_measure", "DOUBLE", precision=12, scale=2),
        F("odd_even", "TEXT", 10),
        F("postcode", "TEXT", 10),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
    ] + audit_fields(), "range_id"),

    # -----------------------------------------------------------------------
    # TRANSPORT
    # -----------------------------------------------------------------------
    FC("TRANS", "road_centerline", "Road Centreline", "POLYLINE", [
        F("road_id", "TEXT", 38, nullable=False),
        F("road_no", "TEXT", 40),
        F("name_en", "TEXT", 120, alias="Road Name (English)"),
        F("name_bn", "TEXT", 120, alias="Road Name (Bangla)"),
        F("road_class_code", "TEXT", 30, domain="dom_road_class"),
        F("surface_code", "TEXT", 20, domain="dom_surface"),
        F("carriageway_width_m", "DOUBLE", precision=8, scale=2),
        F("row_width_m", "DOUBLE", precision=8, scale=2),
        F("lanes", "SHORT"),
        F("one_way", "SHORT", domain="dom_yes_no"),
        F("speed_limit_kmh", "SHORT"),
        F("from_node_id", "TEXT", 38),
        F("to_node_id", "TEXT", 38),
        F("address_left_from", "TEXT", 20),
        F("address_left_to", "TEXT", 20),
        F("address_right_from", "TEXT", 20),
        F("address_right_to", "TEXT", 20),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("maintainer_code", "TEXT", 20, domain="dom_owner_org"),
        F("condition_code", "SHORT", domain="dom_condition"),
        F("pci", "DOUBLE", precision=5, scale=2),
        F("last_rehab_date", "DATE"),
        F("drain_present", "SHORT", domain="dom_yes_no"),
        F("footpath_present", "SHORT", domain="dom_yes_no"),
        F("lighting_present", "SHORT", domain="dom_yes_no"),
    ] + audit_fields(), "road_id"),

    FC("TRANS", "pavement_segment", "Pavement Segment", "POLYLINE", [
        F("pavement_id", "TEXT", 38, nullable=False),
        F("road_id", "TEXT", 38),
        F("from_measure", "DOUBLE", precision=12, scale=2),
        F("to_measure", "DOUBLE", precision=12, scale=2),
        F("surface_code", "TEXT", 20, domain="dom_surface"),
        F("width_m", "DOUBLE", precision=8, scale=2),
        F("thickness_mm", "SHORT"),
        F("construction_date", "DATE"),
        F("condition_code", "SHORT", domain="dom_condition"),
        F("pci", "DOUBLE", precision=5, scale=2),
        F("last_rehab_date", "DATE"),
    ] + audit_fields(), "pavement_id"),

    FC("TRANS", "footpath", "Footpath", "POLYLINE", [
        F("footpath_id", "TEXT", 38, nullable=False),
        F("road_id", "TEXT", 38),
        F("side_code", "TEXT", 10, domain="dom_side"),
        F("width_m", "DOUBLE", precision=8, scale=2),
        F("surface_code", "TEXT", 20, domain="dom_surface"),
        F("length_m", "DOUBLE", precision=12, scale=2),
        F("condition_code", "SHORT", domain="dom_condition"),
    ] + audit_fields(), "footpath_id"),

    FC("TRANS", "bridge_culvert", "Bridge / Culvert", "POINT", [
        F("structure_id", "TEXT", 38, nullable=False),
        F("structure_type_code", "TEXT", 20, domain="dom_structure_type"),
        F("road_id", "TEXT", 38),
        F("name", "TEXT", 120),
        F("length_m", "DOUBLE", precision=10, scale=2),
        F("width_m", "DOUBLE", precision=8, scale=2),
        F("span_m", "DOUBLE", precision=8, scale=2),
        F("material_code", "TEXT", 20, domain="dom_material"),
        F("year_built", "SHORT"),
        F("condition_code", "SHORT", domain="dom_condition"),
        F("load_limit_t", "DOUBLE", precision=8, scale=2),
    ] + audit_fields(), "structure_id"),

    FC("TRANS", "streetlight", "Streetlight", "POINT",
       asset_fields() + [
        F("pole_no", "TEXT", 40),
        F("pole_type", "TEXT", 30),
        F("height_m", "DOUBLE", precision=6, scale=2),
        F("luminaire_type", "TEXT", 40),
        F("wattage", "SHORT"),
        F("mounting_code", "TEXT", 30),
        F("circuit_id", "TEXT", 40),
        F("control_panel_id", "TEXT", 40),
        F("energy_source_code", "TEXT", 20, domain="dom_energy_source"),
        F("last_relamp_date", "DATE"),
    ], "asset_no"),

    FC("TRANS", "traffic_signal", "Traffic Signal", "POINT",
       asset_fields() + [
        F("signal_type_code", "TEXT", 20, domain="dom_signal_type"),
        F("intersection", "TEXT", 120),
        F("controller_id", "TEXT", 40),
        F("phases", "SHORT"),
        F("power_source_code", "TEXT", 20, domain="dom_energy_source"),
    ], "asset_no"),

    FC("TRANS", "road_sign", "Road Sign", "POINT",
       asset_fields() + [
        F("sign_type", "TEXT", 40),
        F("sign_text", "TEXT", 120),
        F("road_id", "TEXT", 38),
        F("direction", "TEXT", 20),
        F("height_m", "DOUBLE", precision=6, scale=2),
    ], "asset_no"),

    FC("TRANS", "road_marking", "Road Marking", "POLYLINE", [
        F("marking_id", "TEXT", 38, nullable=False),
        F("road_id", "TEXT", 38),
        F("marking_type", "TEXT", 40),
        F("colour", "TEXT", 20),
        F("width_mm", "SHORT"),
        F("length_m", "DOUBLE", precision=10, scale=2),
        F("condition_code", "SHORT", domain="dom_condition"),
    ] + audit_fields(), "marking_id"),

    FC("TRANS", "bus_stop", "Bus Stop", "POINT",
       asset_fields() + [
        F("stop_name", "TEXT", 120),
        F("routes", "TEXT", 255),
        F("shelter", "SHORT", domain="dom_yes_no"),
        F("bench", "SHORT", domain="dom_yes_no"),
        F("lighting", "SHORT", domain="dom_yes_no"),
    ], "asset_no"),

    FC("TRANS", "parking", "Parking", "POINT",
       asset_fields() + [
        F("parking_type_code", "TEXT", 20, domain="dom_parking_type"),
        F("capacity", "LONG"),
        F("operator", "TEXT", 120),
        F("fee_bdt", "DOUBLE", precision=10, scale=2),
        F("opening_hours", "TEXT", 80),
    ], "asset_no"),

    # -----------------------------------------------------------------------
    # WATER SUPPLY
    # -----------------------------------------------------------------------
    FC("WATER", "water_main", "Water Main", "POLYLINE",
       asset_fields() + [
        F("diameter_mm", "LONG"),
        F("material_code", "TEXT", 20, domain="dom_material"),
        F("pressure_class", "TEXT", 20),
        F("network_role_code", "TEXT", 20, domain="dom_network_role"),
        F("from_node_id", "TEXT", 38),
        F("to_node_id", "TEXT", 38),
        F("depth_m", "DOUBLE", precision=6, scale=2),
        F("flow_direction", "TEXT", 20),
        F("leak_count", "LONG"),
    ], "asset_no"),

    FC("WATER", "water_service", "Water Service Line", "POLYLINE",
       asset_fields() + [
        F("connected_holding_no", "TEXT", 40),
        F("parent_asset_no", "TEXT", 40),
        F("diameter_mm", "LONG"),
        F("material_code", "TEXT", 20, domain="dom_material"),
        F("depth_m", "DOUBLE", precision=6, scale=2),
        F("connection_date", "DATE"),
        F("meter_no", "TEXT", 40),
    ], "asset_no"),

    FC("WATER", "valve", "Water Valve", "POINT",
       asset_fields() + [
        F("valve_type_code", "TEXT", 30, domain="dom_valve_type"),
        F("diameter_mm", "LONG"),
        F("turns", "SHORT"),
        F("operating_status_code", "TEXT", 20, domain="dom_valve_status"),
        F("parent_asset_no", "TEXT", 40),
    ], "asset_no"),

    FC("WATER", "hydrant", "Hydrant", "POINT",
       asset_fields() + [
        F("hydrant_type_code", "TEXT", 20, domain="dom_hydrant_type"),
        F("diameter_mm", "LONG"),
        F("pressure_bar", "DOUBLE", precision=6, scale=2),
        F("flow_lps", "DOUBLE", precision=10, scale=2),
        F("parent_asset_no", "TEXT", 40),
    ], "asset_no"),

    FC("WATER", "water_meter", "Water Meter", "POINT",
       asset_fields() + [
        F("meter_no", "TEXT", 40),
        F("meter_type_code", "TEXT", 20, domain="dom_meter_type"),
        F("size_mm", "LONG"),
        F("last_reading_date", "DATE"),
        F("last_reading_m3", "DOUBLE", precision=12, scale=2),
    ], "asset_no"),

    FC("WATER", "reservoir", "Reservoir", "POLYGON",
       asset_fields() + [
        F("reservoir_type_code", "TEXT", 20, domain="dom_reservoir_type"),
        F("capacity_m3", "DOUBLE", precision=14, scale=2),
        F("material_code", "TEXT", 20, domain="dom_material"),
        F("height_m", "DOUBLE", precision=8, scale=2),
        F("overflow_level_m", "DOUBLE", precision=8, scale=2),
    ], "asset_no"),

    FC("WATER", "pump_station", "Water Pump Station", "POINT",
       asset_fields() + [
        F("pump_type_code", "TEXT", 30, domain="dom_pump_type"),
        F("capacity_lps", "DOUBLE", precision=12, scale=2),
        F("head_m", "DOUBLE", precision=8, scale=2),
        F("power_kw", "DOUBLE", precision=10, scale=2),
        F("fuel_type_code", "TEXT", 20, domain="dom_fuel"),
        F("number_of_pumps", "SHORT"),
    ], "asset_no"),

    FC("WATER", "treatment_plant", "Water Treatment Plant", "POLYGON",
       asset_fields() + [
        F("capacity_mld", "DOUBLE", precision=10, scale=2),
        F("treatment_type", "TEXT", 80),
        F("process_description", "TEXT", 255),
        F("outfall_asset_no", "TEXT", 40),
    ], "asset_no"),

    # -----------------------------------------------------------------------
    # SEWERAGE
    # -----------------------------------------------------------------------
    FC("SEWER", "sewer_main", "Sewer Main", "POLYLINE",
       asset_fields() + [
        F("diameter_mm", "LONG"),
        F("material_code", "TEXT", 20, domain="dom_material"),
        F("sewer_type_code", "TEXT", 20, domain="dom_sewer_type"),
        F("from_manhole_no", "TEXT", 40),
        F("to_manhole_no", "TEXT", 40),
        F("depth_up_m", "DOUBLE", precision=8, scale=2),
        F("depth_down_m", "DOUBLE", precision=8, scale=2),
        F("slope_pct", "DOUBLE", precision=6, scale=3),
        F("capacity_lps", "DOUBLE", precision=12, scale=2),
    ], "asset_no"),

    FC("SEWER", "sewer_manhole", "Sewer Manhole", "POINT",
       asset_fields() + [
        F("manhole_no", "TEXT", 40),
        F("manhole_type_code", "TEXT", 20, domain="dom_manhole_type"),
        F("cover_level_m", "DOUBLE", precision=8, scale=3),
        F("invert_level_m", "DOUBLE", precision=8, scale=3),
        F("depth_m", "DOUBLE", precision=8, scale=2),
        F("chamber_diameter_mm", "LONG"),
        F("cover_type_code", "TEXT", 20, domain="dom_cover_type"),
        F("blockage_risk_code", "TEXT", 20, domain="dom_risk"),
        F("parent_asset_no", "TEXT", 40),
    ], "asset_no"),

    FC("SEWER", "lift_station", "Sewer Lift Station", "POINT",
       asset_fields() + [
        F("capacity_lps", "DOUBLE", precision=12, scale=2),
        F("number_of_pumps", "SHORT"),
        F("power_kw", "DOUBLE", precision=10, scale=2),
        F("emergency_generator", "SHORT", domain="dom_yes_no"),
    ], "asset_no"),

    FC("SEWER", "sewage_treatment_plant", "Sewage Treatment Plant", "POLYGON",
       asset_fields() + [
        F("capacity_mld", "DOUBLE", precision=10, scale=2),
        F("treatment_type", "TEXT", 80),
        F("discharge_point", "TEXT", 120),
    ], "asset_no"),

    # -----------------------------------------------------------------------
    # STORM DRAINAGE
    # -----------------------------------------------------------------------
    FC("DRAIN", "storm_drain", "Storm Drain", "POLYLINE",
       asset_fields() + [
        F("drain_type_code", "TEXT", 20, domain="dom_drain_type"),
        F("shape_code", "TEXT", 20, domain="dom_shape"),
        F("diameter_mm", "LONG"),
        F("width_mm", "LONG"),
        F("height_mm", "LONG"),
        F("material_code", "TEXT", 20, domain="dom_material"),
        F("slope_pct", "DOUBLE", precision=6, scale=3),
        F("invert_up_m", "DOUBLE", precision=8, scale=3),
        F("invert_down_m", "DOUBLE", precision=8, scale=3),
        F("capacity_m3s", "DOUBLE", precision=12, scale=3),
        F("catchment_id", "TEXT", 40),
        F("outfall_id", "TEXT", 38),
        F("blockage_risk_code", "TEXT", 20, domain="dom_risk"),
    ], "asset_no"),

    FC("DRAIN", "drain_manhole", "Drain Manhole", "POINT",
       asset_fields() + [
        F("manhole_no", "TEXT", 40),
        F("manhole_type_code", "TEXT", 20, domain="dom_manhole_type"),
        F("cover_level_m", "DOUBLE", precision=8, scale=3),
        F("invert_level_m", "DOUBLE", precision=8, scale=3),
        F("depth_m", "DOUBLE", precision=8, scale=2),
        F("chamber_diameter_mm", "LONG"),
        F("cover_type_code", "TEXT", 20, domain="dom_cover_type"),
        F("blockage_risk_code", "TEXT", 20, domain="dom_risk"),
        F("parent_asset_no", "TEXT", 40),
    ], "asset_no"),

    FC("DRAIN", "catchpit", "Catchpit", "POINT",
       asset_fields() + [
        F("catchpit_type_code", "TEXT", 20, domain="dom_catchpit_type"),
        F("depth_m", "DOUBLE", precision=6, scale=2),
        F("grate_type", "TEXT", 40),
        F("parent_asset_no", "TEXT", 40),
    ], "asset_no"),

    FC("DRAIN", "culvert", "Culvert", "POINT",
       asset_fields() + [
        F("culvert_type_code", "TEXT", 20, domain="dom_culvert_type"),
        F("shape_code", "TEXT", 20, domain="dom_shape"),
        F("diameter_mm", "LONG"),
        F("width_mm", "LONG"),
        F("height_mm", "LONG"),
        F("length_m", "DOUBLE", precision=10, scale=2),
        F("material_code", "TEXT", 20, domain="dom_material"),
        F("road_id", "TEXT", 38),
        F("watercourse", "TEXT", 120),
    ], "asset_no"),

    FC("DRAIN", "outfall", "Drain Outfall", "POINT",
       asset_fields() + [
        F("outfall_type_code", "TEXT", 20, domain="dom_outfall_type"),
        F("diameter_mm", "LONG"),
        F("waterbody", "TEXT", 120),
        F("flap_gate", "SHORT", domain="dom_yes_no"),
    ], "asset_no"),

    FC("DRAIN", "sluice_gate", "Sluice Gate", "POINT",
       asset_fields() + [
        F("gate_type_code", "TEXT", 20, domain="dom_gate_type"),
        F("width_m", "DOUBLE", precision=8, scale=2),
        F("height_m", "DOUBLE", precision=8, scale=2),
        F("operation_type", "TEXT", 40),
        F("waterbody", "TEXT", 120),
    ], "asset_no"),

    FC("DRAIN", "drainage_pump", "Drainage Pump", "POINT",
       asset_fields() + [
        F("pump_type_code", "TEXT", 30, domain="dom_pump_type"),
        F("capacity_lps", "DOUBLE", precision=12, scale=2),
        F("head_m", "DOUBLE", precision=8, scale=2),
        F("power_kw", "DOUBLE", precision=10, scale=2),
        F("number_of_pumps", "SHORT"),
    ], "asset_no"),

    # -----------------------------------------------------------------------
    # SOLID WASTE
    # -----------------------------------------------------------------------
    FC("WASTE", "waste_bin", "Waste Bin", "POINT",
       asset_fields() + [
        F("bin_type_code", "TEXT", 20, domain="dom_bin_type"),
        F("size_l", "LONG"),
        F("waste_stream_code", "TEXT", 20, domain="dom_waste_stream"),
        F("collection_zone", "TEXT", 40),
        F("zone_id", "TEXT", 38),
        F("route_id", "TEXT", 38),
        F("collection_days", "TEXT", 40),
        F("frequency_code", "TEXT", 20, domain="dom_frequency"),
        F("location_type_code", "TEXT", 20, domain="dom_location_type"),
    ], "asset_no"),

    FC("WASTE", "collection_zone", "Waste Collection Zone", "POLYGON", [
        F("zone_id", "TEXT", 38, nullable=False),
        F("zone_name", "TEXT", 120),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("frequency_code", "TEXT", 20, domain="dom_frequency"),
        F("collection_days", "TEXT", 40),
        F("contractor", "TEXT", 120),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
    ] + audit_fields(), "zone_id"),

    FC("WASTE", "collection_route", "Waste Collection Route", "POLYLINE", [
        F("route_id", "TEXT", 38, nullable=False),
        F("route_no", "TEXT", 40),
        F("route_name", "TEXT", 120),
        F("zone", "TEXT", 40),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("vehicle_no", "TEXT", 40),
        F("collection_days", "TEXT", 40),
        F("start_time", "TEXT", 10),
        F("end_time", "TEXT", 10),
        F("frequency_code", "TEXT", 20, domain="dom_frequency"),
        F("length_km", "DOUBLE", precision=10, scale=2),
    ] + audit_fields(), "route_id"),

    FC("WASTE", "transfer_station", "Waste Transfer Station", "POINT",
       asset_fields() + [
        F("capacity_tpd", "DOUBLE", precision=10, scale=2),
        F("station_type", "TEXT", 40),
        F("operating_hours", "TEXT", 80),
    ], "asset_no"),

    FC("WASTE", "landfill", "Landfill", "POLYGON",
       asset_fields() + [
        F("landfill_type", "TEXT", 40),
        F("area_ha", "DOUBLE", precision=10, scale=2),
        F("capacity_m3", "DOUBLE", precision=14, scale=2),
        F("start_date", "DATE"),
        F("closure_date", "DATE"),
        F("leachate_system", "SHORT", domain="dom_yes_no"),
        F("gas_system", "SHORT", domain="dom_yes_no"),
    ], "asset_no"),

    # -----------------------------------------------------------------------
    # PARKS / TREES / RECREATION
    # -----------------------------------------------------------------------
    FC("PARK", "park", "Park", "POLYGON", [
        F("park_id", "TEXT", 38, nullable=False),
        F("park_no", "TEXT", 40),
        F("name_en", "TEXT", 120, alias="Park Name (English)"),
        F("name_bn", "TEXT", 120, alias="Park Name (Bangla)"),
        F("classification_code", "TEXT", 30, domain="dom_park_class"),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("owner_org_code", "TEXT", 20, domain="dom_owner_org"),
        F("manager", "TEXT", 120),
        F("facilities", "TEXT", 255),
        F("lighting", "SHORT", domain="dom_yes_no"),
        F("irrigation", "SHORT", domain="dom_yes_no"),
        F("toilets", "SHORT", domain="dom_yes_no"),
        F("playground", "SHORT", domain="dom_yes_no"),
        F("booking", "SHORT", domain="dom_yes_no"),
        F("maintenance_grade_code", "TEXT", 10, domain="dom_maintenance_grade"),
        F("condition_code", "SHORT", domain="dom_condition"),
    ] + audit_fields(), "park_id"),

    FC("PARK", "playground", "Playground", "POLYGON",
       asset_fields() + [
        F("park_id", "TEXT", 38),
        F("surface_code", "TEXT", 20, domain="dom_surface"),
        F("equipment", "TEXT", 255),
        F("age_group", "TEXT", 40),
    ], "asset_no"),

    FC("PARK", "sports_facility", "Sports Facility", "POLYGON",
       asset_fields() + [
        F("park_id", "TEXT", 38),
        F("sport_type", "TEXT", 60),
        F("surface_code", "TEXT", 20, domain="dom_surface"),
        F("lighting", "SHORT", domain="dom_yes_no"),
        F("capacity", "LONG"),
    ], "asset_no"),

    FC("PARK", "tree", "Tree", "POINT", [
        F("tree_id", "TEXT", 38, nullable=False),
        F("tree_no", "TEXT", 40),
        F("species_en", "TEXT", 120, alias="Species (English)"),
        F("species_bn", "TEXT", 120, alias="Species (Bangla)"),
        F("common_name", "TEXT", 120),
        F("height_m", "DOUBLE", precision=6, scale=2),
        F("dbh_cm", "DOUBLE", precision=8, scale=2),
        F("canopy_diameter_m", "DOUBLE", precision=8, scale=2),
        F("health_code", "TEXT", 20, domain="dom_health"),
        F("risk_code", "TEXT", 20, domain="dom_risk"),
        F("planting_date", "DATE"),
        F("location_type_code", "TEXT", 20, domain="dom_location_type"),
        F("park_id", "TEXT", 38),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
    ] + audit_fields(), "tree_id"),

    FC("PARK", "irrigation_asset", "Irrigation Asset", "POINT",
       asset_fields() + [
        F("park_id", "TEXT", 38),
        F("irrigation_type", "TEXT", 40),
        F("water_source", "TEXT", 60),
        F("coverage_sqm", "DOUBLE", precision=18, scale=2),
        F("pump_asset_no", "TEXT", 40),
    ], "asset_no"),

    # -----------------------------------------------------------------------
    # COMMUNITY FACILITIES
    # -----------------------------------------------------------------------
    FC("FAC", "public_facility", "Public Facility", "POINT",
       asset_fields() + [
        F("facility_type_code", "SHORT", domain="dom_facility_type"),
        F("capacity", "LONG"),
        F("opening_hours", "TEXT", 80),
        F("accessible", "SHORT", domain="dom_yes_no"),
        F("public_toilet", "SHORT", domain="dom_yes_no"),
        F("water_supply", "SHORT", domain="dom_yes_no"),
        F("power_supply", "SHORT", domain="dom_yes_no"),
    ], "asset_no",
       subtype_field="facility_type_code",
       subtypes=[(1, "Market"), (2, "Public toilet"), (3, "Community centre"),
                 (4, "School"), (5, "Hospital"), (6, "Mosque"),
                 (7, "Cemetery"), (8, "Cyclone shelter"), (9, "Other")]),

    FC("FAC", "facility_site", "Facility Site", "POLYGON", [
        F("site_id", "TEXT", 38, nullable=False),
        F("facility_type_code", "SHORT", domain="dom_facility_type"),
        F("name_en", "TEXT", 120, alias="Name (English)"),
        F("name_bn", "TEXT", 120, alias="Name (Bangla)"),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("owner_org_code", "TEXT", 20, domain="dom_owner_org"),
        F("address_id", "TEXT", 38),
    ] + audit_fields(), "site_id",
       subtype_field="facility_type_code",
       subtypes=[(1, "Market"), (2, "Public toilet"), (3, "Community centre"),
                 (4, "School"), (5, "Hospital"), (6, "Mosque"),
                 (7, "Cemetery"), (8, "Cyclone shelter"), (9, "Other")]),

    # -----------------------------------------------------------------------
    # PLANNING
    # -----------------------------------------------------------------------
    FC("PLAN", "zoning", "Zoning", "POLYGON", [
        F("zone_id", "TEXT", 38, nullable=False),
        F("zone_code", "TEXT", 20),
        F("zone_name", "TEXT", 120),
        F("zone_type_code", "TEXT", 30, domain="dom_zone_type"),
        F("authority", "TEXT", 120),
        F("gazette_date", "DATE"),
        F("max_far", "DOUBLE", precision=6, scale=2),
        F("max_height_m", "DOUBLE", precision=8, scale=2),
        F("land_use_code", "TEXT", 30, domain="dom_land_use"),
    ] + audit_fields(), "zone_id"),

    FC("PLAN", "land_use", "Land Use", "POLYGON", [
        F("landuse_id", "TEXT", 38, nullable=False),
        F("landuse_code", "TEXT", 20),
        F("landuse_name", "TEXT", 120),
        F("category_code", "TEXT", 30, domain="dom_land_use"),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
    ] + audit_fields(), "landuse_id"),

    FC("PLAN", "growth_area", "Growth Area", "POLYGON", [
        F("growth_id", "TEXT", 38, nullable=False),
        F("growth_name", "TEXT", 120),
        F("growth_type", "TEXT", 40),
        F("authority", "TEXT", 120),
        F("gazette_date", "DATE"),
        F("area_sqm", "DOUBLE", precision=18, scale=2),
        F("status_code", "TEXT", 20, domain="dom_status"),
    ] + audit_fields(), "growth_id"),

    FC("PLAN", "development_application", "Development Application", "POINT", [
        F("da_id", "TEXT", 38, nullable=False),
        F("da_no", "TEXT", 40),
        F("application_type", "TEXT", 60),
        F("applicant", "TEXT", 120),
        F("address_id", "TEXT", 38),
        F("parcel_id", "TEXT", 38),
        F("status_code", "TEXT", 20, domain="dom_application_status"),
        F("submitted_date", "DATE"),
        F("decision_date", "DATE"),
        F("decision", "TEXT", 120),
        F("conditions", "TEXT", 500),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
    ] + audit_fields(), "da_id"),

    FC("PLAN", "building_permit", "Building Permit", "POINT", [
        F("permit_id", "TEXT", 38, nullable=False),
        F("permit_no", "TEXT", 40),
        F("application_no", "TEXT", 40),
        F("permit_type_code", "TEXT", 20, domain="dom_permit_type"),
        F("applicant", "TEXT", 120),
        F("address_id", "TEXT", 38),
        F("parcel_id", "TEXT", 38),
        F("building_id", "TEXT", 38),
        F("status_code", "TEXT", 20, domain="dom_application_status"),
        F("submitted_date", "DATE"),
        F("approved_date", "DATE"),
        F("expiry_date", "DATE"),
        F("conditions", "TEXT", 500),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
    ] + audit_fields(), "permit_id"),

    FC("PLAN", "heritage_site", "Heritage Site", "POINT", [
        F("heritage_id", "TEXT", 38, nullable=False),
        F("heritage_name", "TEXT", 120),
        F("heritage_type_code", "TEXT", 20, domain="dom_heritage_type"),
        F("grade", "TEXT", 20),
        F("listed_date", "DATE"),
        F("address_id", "TEXT", 38),
        F("parcel_id", "TEXT", 38),
        F("description", "TEXT", 500),
    ] + audit_fields(), "heritage_id"),

    # -----------------------------------------------------------------------
    # ENVIRONMENT / FLOOD
    # -----------------------------------------------------------------------
    FC("ENV", "flood_extent", "Flood Extent", "POLYGON", [
        F("flood_id", "TEXT", 38, nullable=False),
        F("flood_type_code", "TEXT", 20, domain="dom_flood_type"),
        F("return_period_yrs", "SHORT"),
        F("event_date", "DATE"),
        F("depth_m", "DOUBLE", precision=6, scale=2),
    ] + audit_fields(), "flood_id"),

    FC("ENV", "water_quality_site", "Water Quality Site", "POINT", [
        F("site_id", "TEXT", 38, nullable=False),
        F("site_name", "TEXT", 120),
        F("waterbody", "TEXT", 120),
        F("parameter", "TEXT", 80),
        F("measurement_value", "DOUBLE", precision=12, scale=3),
        F("unit", "TEXT", 20),
        F("sample_date", "DATE"),
    ] + audit_fields(), "site_id"),

    FC("ENV", "air_quality_site", "Air Quality Site", "POINT", [
        F("site_id", "TEXT", 38, nullable=False),
        F("site_name", "TEXT", 120),
        F("parameter", "TEXT", 80),
        F("measurement_value", "DOUBLE", precision=12, scale=3),
        F("unit", "TEXT", 20),
        F("sample_date", "DATE"),
    ] + audit_fields(), "site_id"),

    # -----------------------------------------------------------------------
    # OPERATIONS
    # -----------------------------------------------------------------------
    FC("OPS", "inspection", "Inspection", "POINT", [
        F("inspection_id", "TEXT", 38, nullable=False),
        F("asset_no", "TEXT", 40),
        F("inspection_type_code", "TEXT", 20, domain="dom_inspection_type"),
        F("inspection_date", "DATE"),
        F("inspector", "TEXT", 80),
        F("method_code", "TEXT", 20, domain="dom_method"),
        F("condition_score", "SHORT", domain="dom_condition"),
        F("defects", "TEXT", 500),
        F("action_code", "TEXT", 20, domain="dom_action"),
        F("next_inspection_date", "DATE"),
        F("cost_bdt", "DOUBLE", precision=18, scale=2),
        F("photo_path", "TEXT", 255),
    ] + audit_fields(), "inspection_id"),

    FC("OPS", "work_order", "Work Order", "POINT", [
        F("wo_id", "TEXT", 38, nullable=False),
        F("wo_no", "TEXT", 40),
        F("asset_no", "TEXT", 40),
        F("wo_type_code", "TEXT", 20, domain="dom_wo_type"),
        F("priority_code", "SHORT", domain="dom_priority"),
        F("status_code", "TEXT", 20, domain="dom_wo_status"),
        F("reported_by", "TEXT", 80),
        F("reported_date", "DATE"),
        F("assigned_team", "TEXT", 80),
        F("scheduled_date", "DATE"),
        F("completed_date", "DATE"),
        F("defect_code", "TEXT", 40),
        F("labour_hours", "DOUBLE", precision=10, scale=2),
        F("material_cost_bdt", "DOUBLE", precision=18, scale=2),
        F("total_cost_bdt", "DOUBLE", precision=18, scale=2),
    ] + audit_fields(), "wo_id"),

    FC("OPS", "service_request", "Service Request / Complaint", "POINT", [
        F("request_id", "TEXT", 38, nullable=False),
        F("request_no", "TEXT", 40),
        F("channel_code", "TEXT", 20, domain="dom_request_channel"),
        F("category", "TEXT", 80),
        F("description", "TEXT", 500),
        F("address_id", "TEXT", 38),
        F("asset_no", "TEXT", 40),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("reported_date", "DATE"),
        F("status_code", "TEXT", 20, domain="dom_request_status"),
        F("assigned_to", "TEXT", 80),
        F("resolved_date", "DATE"),
        F("sla_days", "SHORT"),
        F("satisfaction", "SHORT"),
    ] + audit_fields(), "request_id"),

    # -----------------------------------------------------------------------
    # CIVIC
    # -----------------------------------------------------------------------
    FC("CIVIC", "point_of_interest", "Point of Interest", "POINT", [
        F("poi_id", "TEXT", 38, nullable=False),
        F("name_en", "TEXT", 120, alias="Name (English)"),
        F("name_bn", "TEXT", 120, alias="Name (Bangla)"),
        F("category_code", "TEXT", 20, domain="dom_poi_category"),
        F("address_id", "TEXT", 38),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("description", "TEXT", 500),
        F("opening_hours", "TEXT", 80),
        F("website", "TEXT", 255),
        F("phone", "TEXT", 40),
    ] + audit_fields(), "poi_id"),

    FC("CIVIC", "event", "Event", "POINT", [
        F("event_id", "TEXT", 38, nullable=False),
        F("event_name", "TEXT", 120),
        F("category", "TEXT", 40),
        F("venue", "TEXT", 120),
        F("address_id", "TEXT", 38),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("start_date", "DATE"),
        F("end_date", "DATE"),
        F("organizer", "TEXT", 120),
        F("public_event", "SHORT", domain="dom_yes_no"),
    ] + audit_fields(), "event_id"),
]


# ---------------------------------------------------------------------------
# Standalone tables
# ---------------------------------------------------------------------------

TABLES = [
    T("asset_registry", "Asset Registry", [
        F("asset_no", "TEXT", 40, nullable=False),
        F("asset_id", "TEXT", 38),
        F("asset_class", "TEXT", 30, domain="dom_asset_class"),
        F("asset_type", "TEXT", 60),
        F("theme_schema", "TEXT", 20),
        F("theme_table", "TEXT", 60),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("status_code", "TEXT", 20, domain="dom_status"),
        F("condition_code", "SHORT", domain="dom_condition"),
        F("owner_org_code", "TEXT", 20, domain="dom_owner_org"),
    ] + audit_fields(), "asset_no"),

    T("holding", "Holding / Property Tax", [
        F("holding_id", "TEXT", 38, nullable=False),
        F("holding_no", "TEXT", 40, nullable=False),
        F("owner_name", "TEXT", 120),
        F("occupant_name", "TEXT", 120),
        F("address_id", "TEXT", 38),
        F("parcel_id", "TEXT", 38),
        F("building_id", "TEXT", 38),
        F("ward_code", "TEXT", 4, domain="dom_ward"),
        F("holding_category", "TEXT", 40),
        F("annual_value_bdt", "DOUBLE", precision=18, scale=2),
        F("annual_tax_bdt", "DOUBLE", precision=18, scale=2),
        F("arrears_bdt", "DOUBLE", precision=18, scale=2),
        F("last_payment_date", "DATE"),
        F("water_connection_no", "TEXT", 40),
        F("sewer_connection_no", "TEXT", 40),
    ] + audit_fields(), "holding_id"),

    T("condition_assessment", "Condition Assessment", [
        F("assessment_id", "TEXT", 38, nullable=False),
        F("asset_no", "TEXT", 40),
        F("assessment_date", "DATE"),
        F("assessor", "TEXT", 80),
        F("method_code", "TEXT", 20, domain="dom_method"),
        F("condition_score", "SHORT", domain="dom_condition"),
        F("defects", "TEXT", 500),
        F("action_code", "TEXT", 20, domain="dom_action"),
        F("next_assessment_date", "DATE"),
        F("cost_bdt", "DOUBLE", precision=18, scale=2),
        F("photo_path", "TEXT", 255),
    ] + audit_fields(), "assessment_id"),

    T("route_bin", "Route-Bin Assignment", [
        F("route_bin_id", "TEXT", 38, nullable=False),
        F("route_id", "TEXT", 38),
        F("bin_asset_no", "TEXT", 40),
        F("sequence_no", "SHORT"),
        F("collection_day", "TEXT", 20),
    ] + audit_fields(), "route_bin_id"),

    T("waste_vehicle", "Waste Vehicle", [
        F("vehicle_id", "TEXT", 38, nullable=False),
        F("vehicle_no", "TEXT", 40),
        F("vehicle_type", "TEXT", 40),
        F("capacity_m3", "DOUBLE", precision=10, scale=2),
        F("registration_no", "TEXT", 40),
        F("status_code", "TEXT", 20, domain="dom_status"),
        F("assigned_route_id", "TEXT", 38),
        F("last_service_date", "DATE"),
    ] + audit_fields(), "vehicle_id"),

    T("notice", "Public Notice", [
        F("notice_id", "TEXT", 38, nullable=False),
        F("title", "TEXT", 200),
        F("category", "TEXT", 40),
        F("issued_date", "DATE"),
        F("effective_date", "DATE"),
        F("expiry_date", "DATE"),
        F("description", "TEXT", 500),
        F("url", "TEXT", 255),
    ] + audit_fields(), "notice_id"),

    T("raster_catalogue", "Raster Catalogue", [
        F("raster_id", "TEXT", 38, nullable=False),
        F("raster_name", "TEXT", 120),
        F("raster_type", "TEXT", 30),
        F("file_path", "TEXT", 255),
        F("acquisition_date", "DATE"),
        F("resolution_m", "DOUBLE", precision=8, scale=3),
    ] + audit_fields(), "raster_id"),

    T("meta_layer", "Layer Catalogue", [
        F("layer_name", "TEXT", 80, nullable=False),
        F("title_en", "TEXT", 120),
        F("title_bn", "TEXT", 120),
        F("theme", "TEXT", 20),
        F("geometry_type", "TEXT", 20),
        F("srid", "LONG"),
        F("is_public", "SHORT", domain="dom_yes_no", default="0"),
        F("min_zoom", "SHORT"),
        F("searchable", "SHORT", domain="dom_yes_no", default="0"),
        F("editable", "SHORT", domain="dom_yes_no", default="1"),
        F("metadata_url", "TEXT", 255),
    ] + audit_fields(), "layer_name"),

    T("meta_load_log", "Data Load Log", [
        F("load_id", "TEXT", 38, nullable=False),
        F("layer_name", "TEXT", 80),
        F("source_file", "TEXT", 255),
        F("loaded_at", "DATE"),
        F("loaded_by", "TEXT", 80),
        F("row_count", "LONG"),
        F("status", "TEXT", 20),
        F("error_file", "TEXT", 255),
    ] + audit_fields(), "load_id"),
]


# ---------------------------------------------------------------------------
# Relationship classes
# ---------------------------------------------------------------------------

RELATIONSHIPS = [
    {"name": "REL_PARCEL_BUILDING", "origin": "CAD/parcel", "destination": "CAD/building",
     "forward": "contains building", "backward": "is in parcel",
     "cardinality": "ONE_TO_MANY", "origin_key": "parcel_id", "foreign_key": "parcel_id"},
    {"name": "REL_PARCEL_ADDRESS", "origin": "CAD/parcel", "destination": "CAD/address_point",
     "forward": "contains address", "backward": "is in parcel",
     "cardinality": "ONE_TO_MANY", "origin_key": "parcel_id", "foreign_key": "parcel_id"},
    {"name": "REL_BUILDING_ADDRESS", "origin": "CAD/building", "destination": "CAD/address_point",
     "forward": "contains address", "backward": "is in building",
     "cardinality": "ONE_TO_MANY", "origin_key": "building_id", "foreign_key": "building_id"},
    {"name": "REL_ROAD_ADDRESS", "origin": "TRANS/road_centerline", "destination": "CAD/address_point",
     "forward": "has address", "backward": "is on road",
     "cardinality": "ONE_TO_MANY", "origin_key": "road_id", "foreign_key": "road_id"},
    {"name": "REL_ROAD_ADDRESS_RANGE", "origin": "TRANS/road_centerline", "destination": "CAD/address_range",
     "forward": "has address range", "backward": "is on road",
     "cardinality": "ONE_TO_MANY", "origin_key": "road_id", "foreign_key": "road_id"},
    {"name": "REL_ROAD_PAVEMENT", "origin": "TRANS/road_centerline", "destination": "TRANS/pavement_segment",
     "forward": "has pavement", "backward": "is on road",
     "cardinality": "ONE_TO_MANY", "origin_key": "road_id", "foreign_key": "road_id"},
    {"name": "REL_ROAD_FOOTPATH", "origin": "TRANS/road_centerline", "destination": "TRANS/footpath",
     "forward": "has footpath", "backward": "is on road",
     "cardinality": "ONE_TO_MANY", "origin_key": "road_id", "foreign_key": "road_id"},
    {"name": "REL_ROAD_BRIDGE", "origin": "TRANS/road_centerline", "destination": "TRANS/bridge_culvert",
     "forward": "has bridge/culvert", "backward": "is on road",
     "cardinality": "ONE_TO_MANY", "origin_key": "road_id", "foreign_key": "road_id"},
    {"name": "REL_ROAD_SIGN", "origin": "TRANS/road_centerline", "destination": "TRANS/road_sign",
     "forward": "has sign", "backward": "is on road",
     "cardinality": "ONE_TO_MANY", "origin_key": "road_id", "foreign_key": "road_id"},
    {"name": "REL_WARD_ROAD", "origin": "REF/ward_boundary", "destination": "TRANS/road_centerline",
     "forward": "contains road", "backward": "is in ward",
     "cardinality": "ONE_TO_MANY", "origin_key": "ward_code", "foreign_key": "ward_code"},
    {"name": "REL_WARD_PARCEL", "origin": "REF/ward_boundary", "destination": "CAD/parcel",
     "forward": "contains parcel", "backward": "is in ward",
     "cardinality": "ONE_TO_MANY", "origin_key": "ward_code", "foreign_key": "ward_code"},
    {"name": "REL_PARK_TREE", "origin": "PARK/park", "destination": "PARK/tree",
     "forward": "contains tree", "backward": "is in park",
     "cardinality": "ONE_TO_MANY", "origin_key": "park_id", "foreign_key": "park_id"},
    {"name": "REL_PARK_PLAYGROUND", "origin": "PARK/park", "destination": "PARK/playground",
     "forward": "contains playground", "backward": "is in park",
     "cardinality": "ONE_TO_MANY", "origin_key": "park_id", "foreign_key": "park_id"},
    {"name": "REL_PARK_SPORTS", "origin": "PARK/park", "destination": "PARK/sports_facility",
     "forward": "contains sports facility", "backward": "is in park",
     "cardinality": "ONE_TO_MANY", "origin_key": "park_id", "foreign_key": "park_id"},
    {"name": "REL_ASSET_INSPECTION", "origin": "asset_registry", "destination": "OPS/inspection",
     "forward": "has inspection", "backward": "is inspection of asset",
     "cardinality": "ONE_TO_MANY", "origin_key": "asset_no", "foreign_key": "asset_no"},
    {"name": "REL_ASSET_WORK_ORDER", "origin": "asset_registry", "destination": "OPS/work_order",
     "forward": "has work order", "backward": "is work order for asset",
     "cardinality": "ONE_TO_MANY", "origin_key": "asset_no", "foreign_key": "asset_no"},
    {"name": "REL_ASSET_REQUEST", "origin": "asset_registry", "destination": "OPS/service_request",
     "forward": "has service request", "backward": "is request for asset",
     "cardinality": "ONE_TO_MANY", "origin_key": "asset_no", "foreign_key": "asset_no"},
    {"name": "REL_ROUTE_ROUTE_BIN", "origin": "WASTE/collection_route", "destination": "route_bin",
     "forward": "has bin assignment", "backward": "is on route",
     "cardinality": "ONE_TO_MANY", "origin_key": "route_id", "foreign_key": "route_id"},
    {"name": "REL_BIN_ROUTE_BIN", "origin": "WASTE/waste_bin", "destination": "route_bin",
     "forward": "has route assignment", "backward": "is assigned bin",
     "cardinality": "ONE_TO_MANY", "origin_key": "asset_no", "foreign_key": "bin_asset_no"},
    {"name": "REL_PARCEL_DA", "origin": "CAD/parcel", "destination": "PLAN/development_application",
     "forward": "has development application", "backward": "is on parcel",
     "cardinality": "ONE_TO_MANY", "origin_key": "parcel_id", "foreign_key": "parcel_id"},
    {"name": "REL_PARCEL_PERMIT", "origin": "CAD/parcel", "destination": "PLAN/building_permit",
     "forward": "has building permit", "backward": "is on parcel",
     "cardinality": "ONE_TO_MANY", "origin_key": "parcel_id", "foreign_key": "parcel_id"},
    {"name": "REL_PARCEL_HERITAGE", "origin": "CAD/parcel", "destination": "PLAN/heritage_site",
     "forward": "has heritage site", "backward": "is on parcel",
     "cardinality": "ONE_TO_MANY", "origin_key": "parcel_id", "foreign_key": "parcel_id"},
    {"name": "REL_ROAD_MARKING", "origin": "TRANS/road_centerline", "destination": "TRANS/road_marking",
     "forward": "has road marking", "backward": "is on road",
     "cardinality": "ONE_TO_MANY", "origin_key": "road_id", "foreign_key": "road_id"},
    {"name": "REL_WARD_COLLECTION_ZONE", "origin": "REF/ward_boundary", "destination": "WASTE/collection_zone",
     "forward": "contains collection zone", "backward": "is in ward",
     "cardinality": "ONE_TO_MANY", "origin_key": "ward_code", "foreign_key": "ward_code"},
    {"name": "REL_ZONE_BIN", "origin": "WASTE/collection_zone", "destination": "WASTE/waste_bin",
     "forward": "contains bin", "backward": "is in collection zone",
     "cardinality": "ONE_TO_MANY", "origin_key": "zone_id", "foreign_key": "zone_id"},
    {"name": "REL_ROUTE_VEHICLE", "origin": "WASTE/collection_route", "destination": "waste_vehicle",
     "forward": "uses vehicle", "backward": "is assigned to route",
     "cardinality": "ONE_TO_MANY", "origin_key": "route_id", "foreign_key": "assigned_route_id"},
    {"name": "REL_ADDRESS_EVENT", "origin": "CAD/address_point", "destination": "CIVIC/event",
     "forward": "hosts event", "backward": "is at address",
     "cardinality": "ONE_TO_MANY", "origin_key": "address_id", "foreign_key": "address_id"},
]


# ---------------------------------------------------------------------------
# Publication hints used to seed meta_layer
# ---------------------------------------------------------------------------

PUBLIC_LAYERS = {
    "REF.city_boundary",
    "REF.ward_boundary",
    "REF.waterbody",
    "TRANS.road_centerline",
    "PARK.park",
    "FAC.public_facility",
    "WASTE.waste_bin",
    "WASTE.collection_zone",
    "WASTE.collection_route",
    "ENV.flood_extent",
    "CIVIC.point_of_interest",
    "CIVIC.event",
}

SEARCHABLE_LAYERS = {
    "CAD.address_point",
    "TRANS.road_centerline",
    "PARK.park",
    "FAC.public_facility",
    "WASTE.waste_bin",
    "CIVIC.point_of_interest",
    "REF.city_boundary",
    "REF.ward_boundary",
}


def min_zoom_for(layer_name):
    """Suggested minimum web-map zoom for a layer."""
    if layer_name in ("REF.city_boundary", "REF.ward_boundary", "ENV.flood_extent"):
        return 8
    if layer_name.startswith("PLAN.") or layer_name.startswith("PARK."):
        return 12
    if layer_name.startswith("TRANS.") or layer_name.startswith("WATER.") \
            or layer_name.startswith("SEWER.") or layer_name.startswith("DRAIN."):
        return 13
    if layer_name.startswith("CAD.") or layer_name.startswith("WASTE.") \
            or layer_name.startswith("FAC.") or layer_name.startswith("OPS."):
        return 15
    return 12
