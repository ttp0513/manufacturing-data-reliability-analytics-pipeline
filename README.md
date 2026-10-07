# Manufacturing Data Reliability & Analytics Pipeline

This repository is a portfolio implementation for the fictional organization
Northstar Components Manufacturing. It uses synthetic manufacturing data to
demonstrate a production-like data reliability and analytics workflow without
representing a real company, facility, or vendor deployment.

## Current status

The repository structure is established. Snowflake objects, governed data
models, KPI calculations, reporting marts, and Power BI deliverables have not
yet been implemented.

See [PROJECT_STATUS.md](PROJECT_STATUS.md) for the current phase and next tasks,
and [DECISION_LOG.md](DECISION_LOG.md) for approved material decisions.

## Repository layout

- `data/synthetic/`: self-contained synthetic-data generator package and its
  generated datasets.
- `data/synthetic/generated_data/source_systems/`: simulated ERP, MES, QMS,
  CMMS, and SCADA source extracts intended for future pipeline ingestion.
- `data/synthetic/generated_data/core/`: generator-supplied reference outputs;
  these are not evidence that this repository's analytics layer is implemented.
- `data/synthetic/generated_data/project2_qa_exercises/`: controlled bad-data
  fixtures kept separate from the clean production-like data.
- `data/synthetic/generated_data/project3_multiplant_local/`: synthetic local
  plant extracts for a future standardization exercise.
- `docs/`: project documentation as it is approved and implemented.

The synthetic package's own [README](data/synthetic/README.md),
[data dictionary](data/synthetic/DATA_DICTIONARY.md), and
[realism notes](data/synthetic/REALISM_NOTES.md) describe the supplied data and
generator assumptions.

## Intended logical flow

Simulated source systems → Python/SQL ingestion → Snowflake RAW → Snowflake
STAGING → Snowflake ANALYTICS → reporting marts → Power BI Desktop.

Each stage will be added incrementally after the required discovery, decisions,
and validation are complete.
