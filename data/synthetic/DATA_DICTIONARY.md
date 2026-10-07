
# Data Dictionary

## dim_plant
- `plant_id`: enterprise plant key
- `plant_name`: display name
- `region`: broad operating region
- `timezone`: plant timezone
- `planned_shift_hours`: nominal hours per shift

## dim_line
- `line_id`: production-line key
- `plant_id`: parent plant
- `nominal_units_per_hour`: line-level practical capacity
- `commission_year`: commissioning year

## dim_machine
- `machine_id`: equipment key
- `line_id`: parent production line
- `machine_type`: Press / CNC / Assembly / Packaging
- `install_year`: simulated installation year
- `rated_units_per_hour`: rated machine capacity
- `baseline_health_index`: latent synthetic health parameter used by the simulation

## dim_product
- `product_id`: SKU key
- `product_family`: Standard / Premium / Industrial
- `standard_cycle_seconds`: nominal cycle time
- `standard_unit_cost`: synthetic standard cost
- `target_scrap_rate`: nominal target quality-loss rate

## fact_production
Grain: one plant + line + shift + work order.

Key fields:
- `scheduled_minutes`
- `planned_downtime_minutes`
- `unplanned_downtime_minutes`
- `operating_minutes`
- `ideal_rate_units_per_hour`
- `total_units`
- `good_units`
- `scrap_units`
- `actual_run_rate_units_per_hour`

## fact_production_with_kpis
Adds:
- `availability`
- `performance`
- `quality`
- `oee`
- `scrap_rate`

OEE is calculated as:
`Availability × Performance × Quality`

## fact_downtime
Grain: downtime event.

Contains:
- planned/unplanned classification
- reason code
- start/end timestamps
- machine
- duration

## fact_quality
Grain: defect category recorded against a work order.

Defect counts reconcile to the scrap quantity for that work order.

## fact_maintenance
Grain: maintenance work order.

Contains:
- preventive/corrective type
- machine
- opened/closed timestamps
- labor hours
- failure mode
- synthetic parts cost

## fact_sensor_hourly
Grain: machine-hour snapshot.

Contains:
- run state
- load %
- temperature
- vibration
- power

Sensor behavior is conditionally related to machine load, health, and failures.
