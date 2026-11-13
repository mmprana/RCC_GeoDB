"""
Validate the RCC schema before running ArcPy.

    python validate_schema.py

Checks:
  * duplicate field names
  * missing keys
  * missing domains
  * domain/field type mismatches
  * text fields without a length
  * subtype fields and codes
  * relationship origins, destinations and key fields
  * public/searchable layer names
"""

import sys
from collections import Counter

import rcc_schema as s


def main():
    errors = []
    feature_index = {}
    table_index = {t["name"]: t for t in s.TABLES}

    for fc in s.FEATURE_CLASSES:
        full = f"{fc['dataset']}/{fc['name']}"
        feature_index[full] = fc
        names = [f["name"].lower() for f in fc["fields"]]

        duplicates = [n for n, count in Counter(names).items() if count > 1]
        if duplicates:
            errors.append(f"duplicate fields in {full}: {duplicates}")

        if fc["dataset"] not in s.DATASETS:
            errors.append(f"unknown dataset for {full}: {fc['dataset']}")

        if fc["key"].lower() not in names:
            errors.append(f"missing key in {full}: {fc['key']}")

        for field in fc["fields"]:
            if field["type"] == "TEXT" and not field["length"]:
                errors.append(f"TEXT field without length: {full}.{field['name']}")
            if field["domain"]:
                domain = s.DOMAINS.get(field["domain"])
                if not domain:
                    errors.append(f"missing domain {field['domain']} for {full}.{field['name']}")
                elif field["type"] != domain["type"]:
                    errors.append(
                        f"domain type mismatch {full}.{field['name']}: "
                        f"{field['type']} != {domain['type']}"
                    )

        subtype_field = fc.get("subtype_field")
        if subtype_field:
            if subtype_field.lower() not in names:
                errors.append(f"missing subtype field in {full}: {subtype_field}")
            else:
                domain_name = next(
                    (f["domain"] for f in fc["fields"]
                     if f["name"].lower() == subtype_field.lower()),
                    None,
                )
                if domain_name:
                    domain_codes = {code for code, _ in s.DOMAINS[domain_name]["values"]}
                    for code, _ in fc.get("subtypes", []):
                        if code not in domain_codes:
                            errors.append(
                                f"subtype code {code} not in {domain_name} for {full}"
                            )

    for table in s.TABLES:
        names = [f["name"].lower() for f in table["fields"]]
        duplicates = [n for n, count in Counter(names).items() if count > 1]
        if duplicates:
            errors.append(f"duplicate fields in {table['name']}: {duplicates}")
        if table["key"].lower() not in names:
            errors.append(f"missing key in {table['name']}: {table['key']}")

        for field in table["fields"]:
            if field["type"] == "TEXT" and not field["length"]:
                errors.append(f"TEXT field without length: {table['name']}.{field['name']}")
            if field["domain"]:
                domain = s.DOMAINS.get(field["domain"])
                if not domain:
                    errors.append(f"missing domain {field['domain']} for {table['name']}.{field['name']}")
                elif field["type"] != domain["type"]:
                    errors.append(
                        f"domain type mismatch {table['name']}.{field['name']}: "
                        f"{field['type']} != {domain['type']}"
                    )

    def resolve(reference):
        if "/" in reference:
            return feature_index.get(reference)
        return table_index.get(reference)

    def field_type(spec, field_name):
        return next(
            (f["type"] for f in spec["fields"]
             if f["name"].lower() == field_name.lower()),
            None,
        )

    for rel in s.RELATIONSHIPS:
        origin = resolve(rel["origin"])
        destination = resolve(rel["destination"])

        if not origin:
            errors.append(f"cannot resolve relationship origin: {rel['name']} -> {rel['origin']}")
            continue
        if not destination:
            errors.append(f"cannot resolve relationship destination: {rel['name']} -> {rel['destination']}")
            continue

        origin_type = field_type(origin, rel["origin_key"])
        destination_type = field_type(destination, rel["foreign_key"])

        if origin_type is None:
            errors.append(f"missing relationship origin key: {rel['name']}.{rel['origin_key']}")
        if destination_type is None:
            errors.append(f"missing relationship foreign key: {rel['name']}.{rel['foreign_key']}")
        if origin_type and destination_type and origin_type != destination_type:
            errors.append(
                f"relationship key type mismatch {rel['name']}: "
                f"{origin_type} != {destination_type}"
            )

    all_layers = {f"{fc['dataset']}.{fc['name']}" for fc in s.FEATURE_CLASSES}
    for layer in sorted(s.PUBLIC_LAYERS):
        if layer not in all_layers:
            errors.append(f"public layer not found: {layer}")
    for layer in sorted(s.SEARCHABLE_LAYERS):
        if layer not in all_layers:
            errors.append(f"searchable layer not found: {layer}")

    print(f"Feature classes : {len(s.FEATURE_CLASSES)}")
    print(f"Tables          : {len(s.TABLES)}")
    print(f"Domains         : {len(s.DOMAINS)}")
    print(f"Relationships   : {len(s.RELATIONSHIPS)}")
    print(f"CRS             : EPSG:{s.SRID}")
    print("")

    if errors:
        print(f"Validation failed: {len(errors)} issue(s)")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Schema validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
