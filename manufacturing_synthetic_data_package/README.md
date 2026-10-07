
# Synthetic Manufacturing Data Package

This package generates a realistic, internally consistent manufacturing data environment for three portfolio projects:

1. **Manufacturing Operations Intelligence**
2. **Manufacturing Data Pipeline & Analytics Engineering**
3. **Multi-Plant KPI Standardization**

## Why this is more realistic than random fake data

The generator does **not** independently sample dashboard columns. Instead, it simulates operational relationships:

- Production volume is constrained by scheduled minutes, downtime, product cycle time, line capability, plant effects, shift effects, and speed loss.
- Good units + scrap units always reconcile to total production.
- Quality events reconcile back to work-order scrap quantities.
- Unplanned downtime is influenced by machine health and time since maintenance.
- Corrective maintenance work orders are triggered by mechanical, electrical, or control failures.
- Sensor temperature and vibration increase with machine load and poor health and can spike around failures.
- Night shifts are slightly less productive and have higher scrap risk than day shifts.
- Products have different standard cycle times and target scrap rates.
- Plants have persistent but modest operating differences.
- Project 3 includes deliberate differences in local plant schemas, units, date formats, shift codes, and downtime reason codes so you can demonstrate standardization rather than merely filtering one clean table.
- A separate QA exercise set includes known bad records so you can demonstrate validation logic without corrupting the main dataset.

## Source-system simulation

The generator creates folders resembling common enterprise systems:

- **ERP:** product master and work orders
- **MES:** production runs and downtime events
- **QMS:** quality events
- **CMMS:** maintenance work orders
- **SCADA/IIoT:** hourly machine telemetry

These are **simulated source-system extracts**, not claims that they reproduce any specific vendor's proprietary schema.

## Default scale

With the default 180-day configuration:

- 3 plants
- 3 lines per plant
- 4 machines per line
- 8 products
- 3 shifts
- thousands of work-order / production records
- linked downtime, quality, maintenance, and sensor observations

Change scale with:

```bash
python generate_manufacturing_data.py --output generated_data --seed 42 --days 365
```

## Project mapping

### Project 1 — Manufacturing Operations Intelligence
Use:
- `core/fact_production_with_kpis.csv`
- `core/fact_downtime.csv`
- `core/fact_quality.csv`
- dimensions

Recommended dashboard pages:
- Executive Overview
- OEE / Production
- Downtime Pareto
- Quality / Scrap
- Maintenance reliability

### Project 2 — Data Pipeline & Analytics Engineering
Treat `source_systems/*` as raw extracts.

Build:
- RAW schema
- STAGING schema
- analytics marts
- SQL transformations
- data-quality checks

Use `project2_qa_exercises/` to test your QA rules.

### Project 3 — Multi-Plant Standardization
Use:
- `project3_multiplant_local/P01_*`
- `project3_multiplant_local/P02_*`
- `project3_multiplant_local/P03_*`
- `downtime_reason_mapping.csv`

Your task is to harmonize:
- field names
- date formats
- shift encodings
- downtime units
- local reason codes

into one enterprise model.

## Important portfolio wording

Use wording such as:

> "Built a synthetic manufacturing analytics environment that simulates ERP, MES, QMS, CMMS, and SCADA/IIoT source data and preserves operational relationships among production, downtime, quality, maintenance, and equipment telemetry."

Do **not** say:
> "Worked with Siemens MES/SCADA data."

unless you actually did.
