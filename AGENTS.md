# AGENTS

## Project

Manufacturing Data Reliability & Analytics Pipeline

This repository is a portfolio project for the fictional organization
Northstar Components Manufacturing.

The project demonstrates how fragmented simulated manufacturing data can be
profiled, ingested, standardized, validated, modeled, governed, and delivered
as analytics-ready data for business intelligence.

The project emphasizes manufacturing analytics, analytics engineering,
data reliability, KPI governance, lineage, documentation, and business
understanding.

## Integrity Rules

This project is a simulation.

Treat all ERP, MES, QMS, CMMS, SCADA, and Industrial IoT data as synthetic
or simulated.

Never imply that:
- Northstar Components Manufacturing is a real company.
- The data came from a real manufacturing facility or employer.
- The schemas reproduce proprietary vendor systems.
- Simulated source systems are real enterprise deployments.
- The author has professional manufacturing experience they do not have.
- Simulated stakeholder activity represents real stakeholder approval.
- A business result or financial impact occurred unless the project actually
  calculates and supports the claim.

Use truthful terms such as:
- simulated manufacturing environment
- synthetic manufacturing data
- simulated ERP/MES/QMS/CMMS/SCADA extracts
- portfolio implementation
- production-like architecture

Never fabricate resume metrics, ROI, cost savings, downtime reductions,
efficiency improvements, or other unsupported business outcomes.

## Project Scope

The intended logical flow is:

Simulated source systems
-> Python / SQL ingestion
-> Snowflake RAW
-> Snowflake STAGING
-> Snowflake ANALYTICS
-> Reporting marts
-> Power BI Desktop

Data profiling, reconciliation, data-quality validation, KPI governance,
lineage, and documentation are cross-cutting concerns.

Core technologies:
- Python
- pandas
- SQL
- Snowflake
- Power BI Desktop
- Git / GitHub
- Mermaid
- pytest where useful

Do not add technologies merely for complexity or resume keywords.

Do not introduce Kafka, Spark, Kubernetes, Airflow, Databricks, dbt,
streaming infrastructure, orchestration platforms, or additional cloud
services unless a documented requirement creates a clear need.

Prefer a small, coherent, working implementation over a large unfinished one.

## Architecture Principles

### RAW

RAW preserves source data as close to its original structure as practical.

RAW should:
- preserve source lineage;
- retain source-system fields;
- minimize transformation;
- avoid governed business calculations.

### STAGING

STAGING standardizes source data.

Appropriate responsibilities include:
- column naming;
- explicit data types;
- timestamp normalization;
- string cleaning;
- documented code normalization;
- justified unit conversions;
- source metadata;
- controlled deduplication where evidence supports it.

Do not silently delete or repair suspicious source records.

### ANALYTICS

ANALYTICS contains reusable business-oriented models and governed logic.

For every fact model, document:
- grain;
- candidate/business key;
- foreign-key relationships;
- source lineage;
- key measures.

Do not create joins or relationships that the source data cannot support.

### Reporting Marts

Create marts only when they serve documented business requirements or
reporting questions.

Do not create marts simply to increase repository size.

Power BI should consume governed analytics rather than reproduce important
transformation or KPI logic independently.

## Discovery Before Design

Treat incoming datasets as unfamiliar enterprise extracts.

Before finalizing:
- table grain;
- candidate or primary keys;
- foreign-key relationships;
- dimensions;
- facts;
- marts;
- KPI support;

profile the relevant source data and document the evidence.

Inspect, where applicable:
- row counts;
- column structure;
- data types;
- nulls;
- duplicates;
- uniqueness;
- date ranges;
- distributions;
- suspicious values;
- cross-file relationships.

Early model names, keys, relationships, and KPI ideas are candidates only
until supported by profiling and an approved decision.

Do not infer data quality merely because a file loads successfully.

## Manufacturing Data Invariants

Preserve intentional relationships in the synthetic manufacturing environment.

Where applicable:

good_units + scrap_units = total_units

Downtime should be reconcilable with operating-time concepts.

Quality, production, maintenance, equipment, work-order, and telemetry
relationships must not be changed casually.

Machine condition, failure behavior, maintenance activity, production,
quality, and sensor behavior may be intentionally related in the synthetic data.

Known corrupted data used for QA must remain separate from clean
production-like data.

Never silently clean intentional QA fixtures before validation runs.

## KPI Governance

Do not invent, silently redefine, or force support for manufacturing KPIs.

KPI definitions must ultimately be documented in the governed KPI
documentation and supported by available source fields.

If an essential input is unavailable, classify or document the KPI as
unsupported or partially supported rather than manufacturing a value.

Important governed business logic should live upstream of Power BI unless
there is an explicit documented reason otherwise.

If a KPI definition changes, identify all affected SQL, marts,
documentation, tests, and BI outputs before implementing the change.

## Data Quality

Data quality is a first-class project requirement.

Validation should test meaningful manufacturing and relational behavior,
not only whether code executes or schemas exist.

Where appropriate, validation results should be reproducible and persisted
or captured as project evidence.

Never hide invalid data by silently dropping records.

Controlled bad-data fixtures exist to demonstrate validation behavior and
must remain clearly identified as test data.

## Source of Truth and Conflict Handling

Project artifacts have different responsibilities.

Use the following precedence when interpreting project state:

1. Actual executed and validated behavior is evidence of what currently works.
2. DECISION_LOG.md records approved material design and business decisions.
3. PROJECT_STATUS.md records the current phase, completed work, blockers,
   and immediate next tasks.
4. Task-specific documentation contains detailed requirements, architecture,
   mappings, KPI definitions, and implementation specifications.
5. AGENTS.md governs persistent integrity, scope, workflow, and engineering
   behavior.

Code existing in the repository proves implementation, not successful execution.

Documentation must not claim functionality that has not been implemented
and validated.

If files contradict each other, do not silently choose one.
Identify the conflict and determine the appropriate correction before making
a material change.

## Evidence and Status Language

Use these terms consistently:

- Planned: intended but not implemented.
- Proposed: designed or suggested but not yet approved.
- Approved: a material decision has been accepted but may not be implemented.
- Implemented: code or an artifact exists.
- Executed: the implementation was actually run.
- Validated: execution results were checked against expected behavior.
- Simulated: intentionally fictional business context, stakeholder activity,
  incident, or test scenario.
- Future Improvement: intentionally outside the current MVP.

Never promote an item to a stronger status without supporting evidence.

Examples:

Writing Snowflake SQL does not mean the Snowflake object was created.

Creating an ingestion script does not mean ingestion succeeded.

Creating a validation test does not mean the test passed.

Writing a Power BI specification does not mean a dashboard exists.

## Working Rules

### Inspect Before Modifying

Before making a material change:
- read this file;
- read PROJECT_STATUS.md;
- inspect relevant repository files;
- identify reusable existing work;
- inspect relevant approved decisions;
- determine the current project phase.

Never assume a file or implementation does not exist without checking.

### Work Incrementally

Work only on the current requested objective.

Do not automatically advance to another project phase.

Do not build downstream components before required upstream discovery,
decisions, or validation are complete.

### Change Only What Is Necessary

Modify only files required for the current task.

Do not:
- refactor unrelated working code;
- rename project-wide objects without justification;
- introduce unrelated dependencies;
- rewrite the synthetic generator without a documented reason;
- alter governed business logic silently;
- modify unrelated documentation merely for formatting.

If a necessary change affects multiple layers, identify the downstream
impact before implementation.

### Explain Material Decisions

For important architecture, modeling, KPI, or data-quality decisions:
1. state the problem;
2. identify reasonable alternatives;
3. explain tradeoffs;
4. recommend an option;
5. obtain or record the decision when appropriate;
6. document the result in DECISION_LOG.md if the decision is material.

Do not silently make major architecture or business-logic decisions.

### Preserve Learning Value

This is a learning and portfolio project.

Prefer:
- readable code;
- descriptive names;
- explicit transformations;
- small understandable functions;
- practical comments;
- documented assumptions;
- reproducible behavior;
- clear validation.

Avoid:
- unnecessary abstraction;
- excessive classes;
- clever one-line code;
- unnecessary design patterns;
- hidden side effects;
- unnecessary dependencies.

Optimize for clarity, realism, traceability, reliability, learning value,
and portfolio credibility.

## Security

Never commit:
- passwords;
- Snowflake credentials;
- private keys;
- API tokens;
- secrets.

Use environment variables or local configuration excluded by Git.

Keep `.env` ignored.

Use `.env.example` or equivalent files with placeholder values only.

Before recommending a commit or release, check for accidental secrets or
sensitive information.

## Documentation

Documentation must describe actual project state.

Do not claim that something exists merely because it is planned.

Detailed project information belongs in the appropriate task-specific files,
such as:
- project charter;
- business requirements;
- source assessment;
- architecture;
- data dictionary;
- source-to-target mapping;
- KPI dictionary;
- data-quality plan;
- incident documentation;
- UAT documentation;
- deployment/runbook documentation.

Keep AGENTS.md focused on persistent rules rather than detailed project history.

## Session Protocol

At the beginning of a project task:

1. Read AGENTS.md.
2. Read PROJECT_STATUS.md.
3. Read DECISION_LOG.md when the task could be affected by an approved decision.
4. Inspect only the repository files relevant to the current objective.
5. Determine the current phase.
6. Identify existing work that should be reused.
7. State material assumptions before implementation.

Before substantial implementation, briefly state:
- the current objective;
- files likely to be affected;
- important assumptions;
- how the work will be validated.

After implementation:
- summarize files created;
- summarize files modified;
- report validation actually performed;
- identify unresolved issues;
- recommend the next step;
- update PROJECT_STATUS.md when project state changed.

Do not automatically begin the next task.

## Default Decision Rule

When multiple reasonable options exist, prefer the option that best improves:

- realism;
- traceability;
- reliability;
- clarity;
- maintainability;
- learning value;
- portfolio credibility;

while remaining achievable within the project scope.

When uncertain, prefer the smaller coherent implementation over the more
complex unfinished implementation.