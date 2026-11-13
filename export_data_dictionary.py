"""
Generate CSV data-dictionary files from rcc_schema.py.

This script does not require ArcGIS Pro. It can be run with any Python 3:

    python export_data_dictionary.py

Outputs:
    RCC_Data_Dictionary.csv
    RCC_Layer_Summary.csv
    RCC_Domains.csv
    RCC_Relationships.csv
"""

import csv
import os
import sys

from rcc_schema import (
    DATASETS,
    DOMAINS,
    FEATURE_CLASSES,
    RELATIONSHIPS,
    SRID,
    TABLES,
)


OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def write_csv(filename, headers, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows)")


def main():
    dictionary_rows = []

    for spec in FEATURE_CLASSES:
        layer_name = f"{spec['dataset']}.{spec['name']}"
        for field in spec["fields"]:
            dictionary_rows.append([
                spec["dataset"],
                layer_name,
                spec["alias"],
                spec["geometry"],
                field["name"],
                field["alias"],
                field["type"],
                field["length"] or "",
                field["precision"] or "",
                field["scale"] or "",
                field["domain"] or "",
                "NULLABLE" if field["nullable"] else "NON_NULLABLE",
                field["default"] or "",
            ])

    for spec in TABLES:
        for field in spec["fields"]:
            dictionary_rows.append([
                "ROOT",
                spec["name"],
                spec["alias"],
                "TABLE",
                field["name"],
                field["alias"],
                field["type"],
                field["length"] or "",
                field["precision"] or "",
                field["scale"] or "",
                field["domain"] or "",
                "NULLABLE" if field["nullable"] else "NON_NULLABLE",
                field["default"] or "",
            ])

    write_csv(
        "RCC_Data_Dictionary.csv",
        [
            "dataset", "layer_name", "layer_alias", "geometry",
            "field_name", "field_alias", "field_type",
            "length", "precision", "scale", "domain",
            "nullable", "default",
        ],
        dictionary_rows,
    )

    layer_rows = []
    for spec in FEATURE_CLASSES:
        layer_name = f"{spec['dataset']}.{spec['name']}"
        layer_rows.append([
            spec["dataset"], layer_name, spec["alias"], spec["geometry"],
            spec["key"], len(spec["fields"]),
            ", ".join(sorted({f["domain"] for f in spec["fields"] if f["domain"]})),
        ])

    for spec in TABLES:
        layer_rows.append([
            "ROOT", spec["name"], spec["alias"], "TABLE",
            spec["key"], len(spec["fields"]),
            ", ".join(sorted({f["domain"] for f in spec["fields"] if f["domain"]})),
        ])

    write_csv(
        "RCC_Layer_Summary.csv",
        ["dataset", "layer_name", "layer_alias", "geometry", "key_field",
         "field_count", "domains_used"],
        layer_rows,
    )

    domain_rows = []
    for name, spec in DOMAINS.items():
        for code, description in spec["values"]:
            domain_rows.append([
                name, spec["type"], spec["domain_type"],
                code, description,
            ])

    write_csv(
        "RCC_Domains.csv",
        ["domain", "field_type", "domain_type", "code", "description"],
        domain_rows,
    )

    relationship_rows = []
    for rel in RELATIONSHIPS:
        relationship_rows.append([
            rel["name"], rel["origin"], rel["destination"],
            rel["cardinality"], rel["origin_key"], rel["foreign_key"],
            rel["forward"], rel["backward"],
        ])

    write_csv(
        "RCC_Relationships.csv",
        ["relationship", "origin", "destination", "cardinality",
         "origin_key", "foreign_key", "forward_label", "backward_label"],
        relationship_rows,
    )

    print("")
    print(f"Schema summary: {len(FEATURE_CLASSES)} feature classes, "
          f"{len(TABLES)} tables, {len(DOMAINS)} domains, "
          f"{len(RELATIONSHIPS)} relationship classes, EPSG:{SRID}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
