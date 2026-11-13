# RCC Geodatabase Starter Package

A complete, empty geodatabase schema for Rajshahi City Corporation, built to be
created in **ArcGIS Pro** with ArcPy and opened in **QGIS**.

The schema is deliberately data-free. You build the container first, then load
paper maps, Excel registers, CAD drawings, and field data into it.

- Coordinate system: **WGS 84 / UTM zone 45N (EPSG:32645)**
- Format: **Esri file geodatabase (`RCC.gdb`)**
- 65 feature classes
- 9 standalone tables
- 67 coded-value domains
- 27 relationship classes
- 13 thematic feature datasets
- Metadata catalogue seeded in `meta_layer`

---

## 1. Files

| File | Purpose |
|---|---|
| `rcc_schema.py` | Pure-Python schema definition: layers, fields, domains, relationships |
| `create_rcc_gdb.py` | ArcPy script that builds `RCC.gdb` in ArcGIS Pro |
| `export_data_dictionary.py` | Generates CSV documentation without ArcGIS |
| `validate_schema.py` | Checks the schema for duplicate fields, missing domains, and broken relationships |
| `RCC_Data_Dictionary.csv` | Every layer and field |
| `RCC_Layer_Summary.csv` | One row per layer |
| `RCC_Domains.csv` | Every domain code |
| `RCC_Relationships.csv` | Every relationship class |

---

## 2. Create the geodatabase in ArcGIS Pro

### Option A — ArcGIS Pro Python window

1. Copy the `RCC_Geodatabase` folder to Windows, for example:
   `C:\RCC_Geodatabase`
2. Open ArcGIS Pro.
3. Open **Analysis → Python**.
4. Run:

```python
import sys
sys.path.append(r"C:\RCC_Geodatabase")
import create_rcc_gdb
create_rcc_gdb.main(r"C:\RCC_GIS")
```

The result is:

```text
C:\RCC_GIS\RCC.gdb
```

### Option B — ArcGIS Pro Python command prompt

```bat
"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" ^
  "C:\RCC_Geodatabase\create_rcc_gdb.py" ^
  --out "C:\RCC_GIS" ^
  --name "RCC.gdb"
```

### Options

```bat
--out "C:\RCC_GIS"          Folder for the .gdb
--name "RCC.gdb"            Geodatabase name
--overwrite                 Delete and recreate the .gdb
--no-editor-tracking        Do not enable editor tracking
```

> Use `--overwrite` only on a test copy. It deletes the existing geodatabase.

### If ArcPy is not found

Run the script inside ArcGIS Pro, not in a normal Windows Python installation.
ArcPy is installed with ArcGIS Pro.

### Before you run

You can validate the schema without ArcGIS:

```bash
python validate_schema.py
```

You should see `Schema validation passed.`

---

## 3. Open the geodatabase in QGIS

QGIS reads Esri file geodatabases through the **OpenFileGDB** driver.

1. Open QGIS.
2. In the **Browser** panel, find **OpenFileGDB** or use
   **Layer → Add Layer → Add Vector Layer → Directory**.
3. Select `RCC.gdb`.
4. Add the layers you need.

### Important: editing in QGIS

The OpenFileGDB driver is generally **read-only** in QGIS. You can:

- view and query the data,
- style it,
- export it,
- use it as a basemap/analysis source.

To edit in QGIS, use one of these:

1. **GeoPackage working copy** — export the layers to `RCC.gpkg` and edit there.
2. **PostGIS** — move the schema to PostgreSQL/PostGIS later for multi-user
   editing and web publishing.

Export the whole geodatabase to GeoPackage with OSGeo4W Shell:

```bat
ogr2ogr -f GPKG C:\RCC_GIS\RCC.gpkg C:\RCC_GIS\RCC.gdb
```

Or in QGIS: right-click a layer → **Export → Save Features As → GeoPackage**.

Domains, subtypes, and relationship classes are fully honoured in ArcGIS Pro.
QGIS may show the coded values but will not enforce ArcGIS subtypes or
relationship-class behaviour. That is why PostGIS is the recommended long-term
editing platform.

---

## 4. What gets created

### Feature datasets

| Dataset | Theme | Feature classes |
|---|---|---|
| `REF` | Boundaries and waterbodies | 6 |
| `CAD` | Parcels, buildings, addresses | 4 |
| `TRANS` | Roads, footpaths, streetlights, signs, markings, parking | 10 |
| `WATER` | Water mains, services, valves, hydrants, meters, reservoirs, pumps | 8 |
| `SEWER` | Sewer mains, manholes, lift stations, treatment | 4 |
| `DRAIN` | Storm drains, manholes, catchpits, culverts, outfalls, gates, pumps | 7 |
| `WASTE` | Bins, zones, routes, transfer stations, landfill | 5 |
| `PARK` | Parks, playgrounds, sports, trees, irrigation | 5 |
| `FAC` | Public facilities and facility sites | 2 |
| `PLAN` | Zoning, land use, growth areas, development applications, permits, heritage | 6 |
| `ENV` | Flood extent, water quality, air quality | 3 |
| `OPS` | Inspections, work orders, service requests | 3 |
| `CIVIC` | Points of interest and events | 2 |

### Standalone tables

- `asset_registry` — one row per asset across all themes
- `holding` — holding/property-tax link
- `condition_assessment` — condition history
- `route_bin` — waste route/bin assignment
- `waste_vehicle` — waste fleet
- `notice` — public notices
- `raster_catalogue` — orthophoto, DEM, and other raster registry
- `meta_layer` — layer catalogue and publication hints
- `meta_load_log` — data-load audit

Orthophotos, DEMs, and contour sources are registered in `raster_catalogue` rather
than embedded as raster datasets. This keeps the geodatabase light and lets you
store imagery as COG/TIFF files on disk or a server.

### Relationship classes

Examples:

- parcel → building
- parcel → address
- building → address
- road → address range
- road → pavement, footpath, bridge, sign
- ward → road, parcel
- park → tree, playground, sports facility
- asset registry → inspection, work order, service request
- collection route → route/bin assignment
- waste bin → route/bin assignment
- collection zone → bin
- collection route → vehicle
- address → event
- parcel → development application, building permit, heritage site

### Domains

Every coded field has a domain where practical, including:

- status, condition, criticality, priority
- owner organisation (RCC, RWASA, LGED, RHD, BBA, DPHE, private, community)
- source and capture method
- road class, surface, land use, tenure, survey type
- water/sewer/drain material, shape, type
- waste stream, collection frequency, bin type
- facility type, zone type, permit type, flood type
- inspection method, action, work-order type and status
- ward codes `01`–`30`

---

## 5. Design rules

### Stable IDs

- `asset_no` is the business key, for example `RCC-DRN-000123`.
- `asset_id` is a text UUID for future database migration.
- Do not encode ward or asset type in `asset_no`.
- Never reuse an `asset_no`.

### Provenance

Every layer carries:

```text
source_code, source_date, accuracy_m, capture_method_code,
qa_status_code, is_active, created_at, created_by,
updated_at, updated_by, notes
```

This is how you distinguish survey-grade data from digitised paper maps.

### Asset registry

The `asset_registry` table is the cross-theme index. Inspections, work orders,
and service requests relate to it through `asset_no`.

When you create an asset, add a matching row to `asset_registry`. Later we can
automate this with a Python script, ArcGIS Pro attribute rules, or PostGIS
triggers.

### File geodatabase limits

A file geodatabase is excellent for a single office and ArcGIS Pro editing.
It does not provide multi-user versioning, web services, or robust QGIS editing.
Those come later with PostgreSQL/PostGIS.

---

## 6. Loading data later

Recommended order:

1. **Reference** — city, ward, thana, mouza, mahalla boundaries; waterbodies.
2. **Transport** — road centreline, footpaths, bridges, streetlights.
3. **Addresses** — import the holding-tax Excel register, clean, geocode, verify.
4. **Buildings** — digitise from orthophoto or paper maps; link to addresses.
5. **Drainage** — storm drains, manholes, catchpits, outfalls.
6. **Waste** — bins and collection routes.
7. **Water/sewer** — only if RCC owns those assets; confirm the role of Rajshahi WASA.
8. **Parks and facilities** — digitise and verify.
9. **Planning/environment** — zoning, land use, flood.
10. **Operations** — inspections, work orders, service requests.

### Minimum first load

Do not wait for every layer. A useful first internal map needs only:

- ward boundary
- road centreline
- address point
- building footprint
- public facility
- waste bin
- streetlight
- drain/manhole

---

## 7. Coordinate system

The schema uses **EPSG:32645** because Rajshahi is around 88.6°E, inside UTM
zone 45N.

If RCC engineering requires the national **Bangladesh Transverse Mercator**
grid, change this line in `rcc_schema.py` before creating the geodatabase:

```python
SRID = 3106
```

Do not mix EPSG:32645 and EPSG:3106 in one feature dataset. Pick one storage
CRS and document it.

Vertical datum is not encoded in the geometry. Record it in layer metadata;
RCC engineers commonly use the **PWD** datum.

---

## 8. Update the schema later

The schema is code. To add a field or layer:

1. Edit `rcc_schema.py`.
2. Test on a new geodatabase:
   `create_rcc_gdb.main(r"C:\RCC_GIS_TEST", overwrite=True)`.
3. Review the change in ArcGIS Pro and QGIS.
4. Apply the same change to production with a migration script — do not
   overwrite production.

For production, create a small migration script that uses
`arcpy.management.AddField` and updates `meta_layer`. Keep every migration in
version control.

---

## 9. Regenerate the data dictionary

Any Python 3 installation can run:

```bash
python export_data_dictionary.py
```

This rewrites the four CSV files. Open them in Excel to review the schema
before building.

---

## 10. Next steps

1. Run the script on a test machine.
2. Open `RCC.gdb` in ArcGIS Pro and QGIS.
3. Review `meta_layer` and the CSV data dictionary.
4. Choose the pilot ward.
5. Load the first eight layers.
6. Then build the QGIS project template, forms, and internal Lizmap map.

The database is intentionally empty. The next milestone is not more schema —
it is the first complete pilot ward.
