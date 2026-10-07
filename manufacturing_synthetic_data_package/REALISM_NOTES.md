
# Realism Assumptions and Guardrails

This generator is intended to produce **plausible operational data**, not to claim universal manufacturing benchmarks.

## Operational structure
- 8-hour shifts
- Three-shift operation
- Some weekend shifts are unscheduled
- Different production lines have different practical throughput
- Products differ in cycle time and quality targets

## Dependency structure
The generator intentionally creates correlations that should exist in real operations:

1. More downtime -> fewer operating minutes -> lower output.
2. Poorer machine health -> higher failure risk.
3. Longer time since PM -> moderately higher failure risk.
4. Failures can trigger corrective maintenance.
5. Higher machine load and poorer health -> higher temperature/vibration.
6. Premium/industrial products can run slower than simpler products.
7. Scrap risk varies by product, plant, shift, machine health, and production pressure.
8. Night shift receives a modest productivity and quality penalty.
9. Plant effects persist across time rather than changing randomly every shift.

## Constraints
The clean core dataset enforces:
- good_units + scrap_units = total_units
- positive downtime duration
- nonnegative operating minutes
- defect counts reconcile to work-order scrap
- foreign keys use valid generated dimensions

## Controlled "dirty data"
Bad records appear only in `project2_qa_exercises/`, so you can demonstrate:
- duplicate detection
- missing key detection
- impossible quantity checks
- negative-duration checks

without contaminating your primary analytics tables.

## What this does NOT simulate
To avoid false realism, this version does not attempt to model:
- proprietary Siemens system schemas
- PLC tag naming standards
- exact vendor-specific MES/ERP data models
- physics-based equipment degradation
- true causal relationships
- real customer demand
- regulatory production records

Those should not be claimed in your portfolio.
