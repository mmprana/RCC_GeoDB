"""
Create the RCC file geodatabase in ArcGIS Pro.

Run from the ArcGIS Pro Python window:

    import sys
    sys.path.append(r"C:\\RCC_Geodatabase")
    import create_rcc_gdb
    create_rcc_gdb.main(r"C:\\RCC_GIS")

Or from the ArcGIS Pro Python command prompt:

    python create_rcc_gdb.py --out C:\\RCC_GIS --name RCC.gdb

Requirements:
  * ArcGIS Pro 2.9 or later (3.x recommended)
  * The script and rcc_schema.py in the same folder

The script creates:
  * a file geodatabase
  * thematic feature datasets
  * feature classes and standalone tables
  * coded-value domains
  * subtypes for public facilities
  * attribute indexes and unique keys
  * relationship classes
  * optional editor tracking
  * a seeded meta_layer catalogue
"""

import argparse
import datetime
import os
import sys
import traceback

import arcpy

from rcc_schema import (
    DATASETS,
    DOMAINS,
    FEATURE_CLASSES,
    GDB_NAME,
    PUBLIC_LAYERS,
    RELATIONSHIPS,
    SEARCHABLE_LAYERS,
    SRID,
    TABLES,
    min_zoom_for,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(message):
    print(message)
    sys.stdout.flush()


def resolve_path(gdb, reference):
    """Resolve 'DATASET/layer' or 'table' to a full geodatabase path."""
    if "/" in reference:
        dataset, name = reference.split("/", 1)
        return os.path.join(gdb, dataset, name)
    return os.path.join(gdb, reference)


def field_names(path):
    return {f.name.lower() for f in arcpy.ListFields(path)}


def create_domains(gdb):
    log("Creating domains ...")
    existing = {d.name for d in arcpy.da.ListDomains(gdb)}

    for name, spec in DOMAINS.items():
        if name in existing:
            log(f"  - skip existing domain: {name}")
            continue

        arcpy.management.CreateDomain(
            gdb,
            name,
            spec["description"],
            spec["type"],
            spec["domain_type"],
        )

        for code, description in spec["values"]:
            arcpy.management.AddCodedValueToDomain(
                gdb, name, code, description
            )

        log(f"  - {name}: {len(spec['values'])} values")


def add_fields(target, fields):
    existing = field_names(target)

    for spec in fields:
        if spec["name"].lower() in existing:
            continue

        kwargs = {
            "in_table": target,
            "field_name": spec["name"],
            "field_type": spec["type"],
            "field_alias": spec["alias"],
            "field_is_nullable": "NULLABLE" if spec["nullable"] else "NON_NULLABLE",
        }

        if spec["length"] is not None:
            kwargs["field_length"] = spec["length"]
        if spec["precision"] is not None:
            kwargs["field_precision"] = spec["precision"]
        if spec["scale"] is not None:
            kwargs["field_scale"] = spec["scale"]
        if spec["domain"]:
            kwargs["field_domain"] = spec["domain"]
        if spec["default"] is not None:
            kwargs["default_value"] = spec["default"]

        arcpy.management.AddField(**kwargs)


def create_indexes(target, spec):
    flds = field_names(target)
    key = spec["key"].lower()
    created = set()

    def add(field, unique=False):
        field_lower = field.lower()
        if field_lower not in flds or field_lower in created:
            return
        index_name = f"idx_{spec['name']}_{field}"[:64]
        try:
            arcpy.management.AddIndex(
                target,
                [field],
                index_name,
                "UNIQUE" if unique else "NON_UNIQUE",
                "ASCENDING",
            )
            created.add(field_lower)
        except Exception as exc:
            log(f"    ! index {index_name}: {exc}")

    # Primary / business key
    add(spec["key"], unique=True)

    # Asset number is a second business key on asset layers
    if "asset_no" in flds and key != "asset_no":
        add("asset_no", unique=True)

    # Holding number is the business key of the property tax register
    if spec["name"] == "holding":
        add("holding_no", unique=True)

    # Common foreign keys and filters
    for field in (
        "ward_code", "road_id", "parcel_id", "building_id", "address_id",
        "park_id", "route_id", "zone_id", "assigned_route_id",
        "parent_asset_no", "bin_asset_no",
        "catchment_id", "outfall_id", "asset_no", "holding_no",
    ):
        if field.lower() in flds and field.lower() != key:
            add(field, unique=False)


def create_subtypes(path, spec):
    subtype_field = spec.get("subtype_field")
    if not subtype_field:
        return

    try:
        arcpy.management.SetSubtypeField(path, subtype_field)
        for code, name in spec.get("subtypes", []):
            arcpy.management.AddSubtype(path, subtype_field, code, name)
        log(f"    - subtypes on {spec['name']}: {len(spec.get('subtypes', []))}")
    except Exception as exc:
        log(f"    ! subtypes on {spec['name']}: {exc}")


def create_relationships(gdb):
    log("Creating relationship classes ...")

    for rel in RELATIONSHIPS:
        out_path = os.path.join(gdb, rel["name"])
        if arcpy.Exists(out_path):
            log(f"  - skip existing relationship: {rel['name']}")
            continue

        try:
            arcpy.management.CreateRelationshipClass(
                resolve_path(gdb, rel["origin"]),
                resolve_path(gdb, rel["destination"]),
                out_path,
                "SIMPLE",
                rel["forward"],
                rel["backward"],
                "NONE",
                rel["cardinality"],
                "NONE",
                rel["origin_key"],
                rel["foreign_key"],
            )
            log(f"  - {rel['name']}")
        except Exception as exc:
            log(f"  ! {rel['name']}: {exc}")


def enable_editor_tracking(path):
    try:
        arcpy.management.EnableEditorTracking(
            path,
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "UTC",
            "NO_ADD_FIELDS",
        )
    except Exception as exc:
        log(f"    ! editor tracking on {os.path.basename(path)}: {exc}")


def seed_meta_layer(gdb):
    log("Seeding meta_layer ...")

    table = os.path.join(gdb, "meta_layer")
    fields = [
        "layer_name", "title_en", "title_bn", "theme", "geometry_type",
        "srid", "is_public", "min_zoom", "searchable", "editable",
        "metadata_url", "source_code", "source_date", "accuracy_m",
        "capture_method_code", "qa_status_code", "is_active",
        "created_at", "created_by", "updated_at", "updated_by", "notes",
    ]

    now = datetime.datetime.utcnow()
    rows = []

    for spec in FEATURE_CLASSES:
        layer_name = f"{spec['dataset']}.{spec['name']}"
        rows.append((
            layer_name,
            spec["alias"],
            "",
            spec["dataset"],
            spec["geometry"],
            SRID,
            1 if layer_name in PUBLIC_LAYERS else 0,
            min_zoom_for(layer_name),
            1 if layer_name in SEARCHABLE_LAYERS else 0,
            1,
            "",
            "UNKNOWN",
            None,
            None,
            "UNKNOWN",
            "pending",
            1,
            now,
            "system",
            now,
            "system",
            "Seeded by create_rcc_gdb.py",
        ))

    for spec in TABLES:
        rows.append((
            spec["name"],
            spec["alias"],
            "",
            "ROOT",
            "TABLE",
            0,
            0,
            0,
            0,
            1,
            "",
            "UNKNOWN",
            None,
            None,
            "UNKNOWN",
            "pending",
            1,
            now,
            "system",
            now,
            "system",
            "Seeded by create_rcc_gdb.py",
        ))

    with arcpy.da.InsertCursor(table, fields) as cursor:
        for row in rows:
            cursor.insertRow(row)

    log(f"  - {len(rows)} catalogue rows")


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------

def main(out_folder, gdb_name=GDB_NAME, overwrite=False, editor_tracking=True):
    out_folder = os.path.abspath(out_folder)
    gdb = os.path.join(out_folder, gdb_name)

    if not os.path.isdir(out_folder):
        os.makedirs(out_folder)

    if arcpy.Exists(gdb):
        if overwrite:
            log(f"Deleting existing geodatabase: {gdb}")
            arcpy.management.Delete(gdb)
        else:
            raise RuntimeError(
                f"Geodatabase already exists: {gdb}\n"
                "Use overwrite=True only on a test copy."
            )

    arcpy.env.overwriteOutput = True

    log(f"Creating file geodatabase: {gdb}")
    arcpy.management.CreateFileGDB(out_folder, gdb_name)

    create_domains(gdb)

    sr = arcpy.SpatialReference(SRID)
    log(f"Creating feature datasets (EPSG:{SRID}) ...")
    for dataset in DATASETS:
        arcpy.management.CreateFeatureDataset(gdb, dataset, sr)
        log(f"  - {dataset}")

    log("Creating feature classes ...")
    for spec in FEATURE_CLASSES:
        dataset_path = os.path.join(gdb, spec["dataset"])
        path = os.path.join(dataset_path, spec["name"])

        arcpy.management.CreateFeatureclass(
            out_path=dataset_path,
            out_name=spec["name"],
            geometry_type=spec["geometry"],
            spatial_reference=sr,
            has_m="DISABLED",
            has_z="DISABLED",
        )
        add_fields(path, spec["fields"])
        arcpy.management.AlterAliasName(path, spec["alias"])
        log(f"  - {spec['dataset']}/{spec['name']} ({len(spec['fields']) + 2} fields)")

    log("Creating standalone tables ...")
    for spec in TABLES:
        path = os.path.join(gdb, spec["name"])
        arcpy.management.CreateTable(gdb, spec["name"])
        add_fields(path, spec["fields"])
        arcpy.management.AlterAliasName(path, spec["alias"])
        log(f"  - {spec['name']} ({len(spec['fields']) + 1} fields)")

    log("Creating subtypes and indexes ...")
    for spec in FEATURE_CLASSES:
        path = os.path.join(gdb, spec["dataset"], spec["name"])
        create_subtypes(path, spec)
        create_indexes(path, spec)

    for spec in TABLES:
        path = os.path.join(gdb, spec["name"])
        create_indexes(path, spec)

    create_relationships(gdb)
    seed_meta_layer(gdb)

    if editor_tracking:
        log("Enabling editor tracking ...")
        for spec in FEATURE_CLASSES:
            enable_editor_tracking(os.path.join(gdb, spec["dataset"], spec["name"]))
        for spec in TABLES:
            enable_editor_tracking(os.path.join(gdb, spec["name"]))

    log("")
    log("Build complete.")
    log(f"  Geodatabase : {gdb}")
    log(f"  Datasets    : {len(DATASETS)}")
    log(f"  Feature classes: {len(FEATURE_CLASSES)}")
    log(f"  Tables      : {len(TABLES)}")
    log(f"  Domains     : {len(DOMAINS)}")
    log(f"  Relationships: {len(RELATIONSHIPS)}")
    log("")
    log("Open the geodatabase in ArcGIS Pro Catalog, or add it in QGIS Browser.")
    log("Review meta_layer for publication hints.")

    return gdb


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create the RCC file geodatabase in ArcGIS Pro."
    )
    parser.add_argument(
        "--out",
        default=os.path.join(os.path.expanduser("~"), "RCC_GIS"),
        help="Folder where the .gdb will be created.",
    )
    parser.add_argument(
        "--name",
        default=GDB_NAME,
        help="Geodatabase name, e.g. RCC.gdb.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Delete and recreate the geodatabase. Use only on a test copy.",
    )
    parser.add_argument(
        "--no-editor-tracking",
        action="store_true",
        help="Do not enable editor tracking.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        main(
            out_folder=args.out,
            gdb_name=args.name,
            overwrite=args.overwrite,
            editor_tracking=not args.no_editor_tracking,
        )
    except Exception:
        traceback.print_exc()
        sys.exit(1)
