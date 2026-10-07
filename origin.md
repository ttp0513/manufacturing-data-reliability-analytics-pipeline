# AGENTS.md

## Project Name

Manufacturing Data Reliability & Analytics Pipeline

## Project Purpose

This repository is a portfolio project that simulates a realistic manufacturing analytics engagement.

The project demonstrates how fragmented manufacturing data from multiple operational systems can be:

- ingested
- standardized
- validated
- modeled
- documented
- transformed into analytics-ready datasets
- consumed by business intelligence tools

The target audience includes:

- hiring managers
- recruiters
- manufacturing analytics leaders
- business intelligence teams
- analytics engineering teams
- technical interviewers

The project is intended to demonstrate practical competence in:

- Python
- SQL
- Snowflake
- ETL / ELT
- data modeling
- dimensional modeling
- manufacturing analytics
- data quality
- KPI governance
- Power BI
- documentation
- stakeholder requirements
- analytics architecture
- Git / GitHub

---

# IMPORTANT REALISM RULE

This project is a simulation.

The fictional organization is:

**Northstar Components Manufacturing**

Northstar Components Manufacturing is NOT a real employer.

The datasets are synthetic.

The simulated source systems must be described using language such as:

- simulated ERP extracts
- simulated MES data
- simulated QMS data
- simulated CMMS data
- simulated SCADA / IIoT telemetry
- synthetic manufacturing environment
- production-like architecture
- portfolio implementation

Never imply that:
- the data came from a real manufacturing facility
- the schemas reproduce proprietary vendor systems
- Northstar Components Manufacturing is a real company
- the author has professional manufacturing experience that they do not actually have
- simulated MES, SCADA, ERP, or CMMS systems are real enterprise deployments

Maintain this distinction in:

- README files
- documentation
- code comments
- generated reports
- diagrams
- resume suggestions
- interview preparation

---

# BUSINESS SCENARIO

Northstar Components Manufacturing operates multiple production lines and manufacturing facilities.

Operational data is generated from several independent source systems.

## ERP

Represents information such as:

- product master
- work orders
- production orders
- product information
- order quantities

## MES

Represents:

- production runs
- shift activity
- production quantities
- lines
- work orders
- downtime events

## QMS

Represents:

- inspections
- defects
- scrap
- quality classifications
- rework

## CMMS

Represents:

- preventive maintenance
- corrective maintenance
- equipment failures
- maintenance work orders
- labor hours
- maintenance costs

## SCADA / Industrial IoT

Represents:

- equipment state
- machine load
- temperature
- vibration
- power
- time-series machine telemetry

These source systems currently produce separate operational extracts.

The simulated business problem is that analysts manually combine these sources for reporting, creating:

- manual reporting effort
- inconsistent KPI definitions
- data-quality risk
- duplicate logic
- poor lineage
- difficult troubleshooting
- inconsistent operational visibility

The project builds a centralized analytics pipeline to address these problems.

---

# BUSINESS OBJECTIVE

The solution should demonstrate how manufacturing data could move through:

Source => Systems => Ingestion => RAW => STAGING => ANALYTICS => Reporting Marts => BI

The pipeline should make data:

- traceable
- standardized
- reusable
- testable
- analytics-ready

The solution should support realistic manufacturing questions without becoming unnecessarily complex.

---

# TARGET ARCHITECTURE

The intended architecture is:

```text
ERP ───────────┐
MES ───────────┤
QMS ───────────┤
CMMS ──────────┼──> Python / SQL ingestion
SCADA / IIoT ──┘
                       ↓
                 Snowflake RAW
                       ↓
                 Snowflake STAGING
                       ↓
                 Snowflake ANALYTICS
                       ↓
                 Reporting marts
                       ↓
                 Power BI Desktop

Data-quality checks should operate throughout the pipeline.
```

---

# CORE TECHNOLOGY STACK

Prioritize:

- Python
- pandas
- SQL
- Snowflake
- Power BI Desktop
- Git
- GitHub
- Mermaid diagrams
- AWS/Cloud/Azure

Use pytest where appropriate.

Do not introduce additional technologies unless there is a clear business or technical reason.

Avoid unnecessary additions such as:

- Kafka
- Spark
- Kubernetes
- Airflow
- Databricks
- Docker
- dbt

These technologies may be discussed as future improvements, but should not be introduced merely to make the project appear more sophisticated.

A coherent working pipeline is more valuable than a complicated technology stack.

---

# PROJECT CONSTRAINTS

Assume approximately:

**7-10 hours per week for four weeks**

Prioritize:

1. business realism
2. working pipeline
3. Snowflake
4. SQL
5. dimensional modeling
6. data quality
7. documentation
8. Power BI
9. GitHub presentation

Avoid scope creep.

Prefer a polished minimum viable product over incomplete advanced features.

---

# WORKING PRINCIPLES FOR CODEX / AI AGENTS

## 1. Inspect Before Changing

Before making significant modifications:
- commit the current state
- inspect the current repository
- identify existing useful work
- reuse existing assets where appropriate
- avoid duplicate files
- avoid rewriting working components without justification

Never assume a file does not exist without checking.

---

## 2. Work Incrementally

Do not attempt to complete the entire project in one task.

Work according to the current project phase.

Typical phases are:

### Phase 1
Business analysis and source discovery

### Phase 2
Snowflake and analytics engineering

### Phase 3
Data quality and reliability

### Phase 4
BI delivery and portfolio release

Do not jump ahead unless specifically instructed.

---

## 3. Explain Major Decisions

For meaningful architecture or modeling decisions:

- explain the issue
- identify reasonable alternatives
- recommend one
- explain why
- document the assumption if necessary

Do not silently make major decisions.

---

## 4. Preserve Learning Value

This is a learning and portfolio project.

When implementing important logic:

- keep code readable with detailed comments
- use practical comments
- avoid excessive abstraction
- explain business meaning
- explain technical meaning
- favor maintainability

Do not hide core project logic inside unnecessary frameworks.

---

## 5. Separate Required Work From Optional Polish

When recommending changes, classify them when useful as:

- Required
- Recommended
- Optional

Do not make optional improvements appear mandatory.

---

# DATA PRINCIPLES

The synthetic manufacturing environment was intentionally designed with realistic relationships.

Do not casually destroy these relationships.

Expected constraints include:

```text
good_units + scrap_units = total_units
```

Downtime should affect operating time.

Machine health should be related to failure behavior.

Failures may create maintenance activity.

Quality outcomes may vary by:

- product
- shift
- plant
- equipment conditions

Sensor behavior may relate to:

- machine load
- machine condition
- equipment failure

Controlled bad-data examples must remain separate from clean analytical data.

Do not silently clean the source data before profiling it.

---

# SOURCE DATA WORKFLOW

Treat incoming datasets as unfamiliar enterprise extracts.

Before transformation:

1. profile them
2. identify grain
3. identify likely keys
4. inspect nulls
5. inspect duplicates
6. inspect date ranges
7. inspect distributions
8. inspect referential relationships
9. identify suspicious records
10. document findings

Do not infer data quality solely from successful file loading.

---

# SNOWFLAKE LAYER RULES

Use three primary logical layers.

---

## RAW

Purpose:

Preserve source data as close to the original structure as practical.

RAW should:

- preserve lineage
- retain source-system fields
- minimize transformations
- avoid business calculations

Potential objects include:

```text
RAW.ERP_PRODUCT_MASTER
RAW.ERP_WORK_ORDERS
RAW.MES_PRODUCTION
RAW.MES_DOWNTIME
RAW.QMS_QUALITY
RAW.CMMS_MAINTENANCE
RAW.SCADA_SENSOR
```

---

## STAGING

Purpose:

Standardize source data.

STAGING may handle:

- standardized column names
- data types
- timestamps
- trimming
- code normalization
- unit conversion
- source metadata
- controlled deduplication
- null normalization

Potential models:

```text
STG_PRODUCT
STG_WORK_ORDER
STG_PRODUCTION
STG_DOWNTIME
STG_QUALITY
STG_MAINTENANCE
STG_SENSOR
```

Do not place visualization-specific logic here unless justified.

---

## ANALYTICS

Purpose:

Provide reusable business-oriented models.

Likely dimensions:

```text
DIM_DATE
DIM_PLANT
DIM_LINE
DIM_MACHINE
DIM_PRODUCT
DIM_SHIFT
```

Likely facts:

```text
FACT_PRODUCTION
FACT_DOWNTIME
FACT_QUALITY
FACT_MAINTENANCE
```

For every fact table, clearly document:

- grain
- primary/candidate key
- foreign keys
- source
- key measures

---

# REPORTING MART RULES

Create marts only when they answer actual business questions.

Potential marts include:

```text
MART_DAILY_PRODUCTION
MART_LINE_PERFORMANCE
MART_DOWNTIME_ANALYSIS
MART_QUALITY_PERFORMANCE
MART_MAINTENANCE_RELIABILITY
MART_DATA_QUALITY
```

Avoid creating marts merely to increase repository size.

---

# KPI GOVERNANCE

Business metrics must not be invented casually.

Maintain a KPI dictionary.

Potential metrics include:

- Availability
- Performance
- Quality
- OEE
- Scrap Rate
- First-Pass Yield
- Production Attainment
- Throughput
- Unplanned Downtime
- MTTR
- MTBF

For each metric document:

- business definition
- formula
- numerator
- denominator
- grain
- source
- exclusions
- limitations

If the available data does not correctly support a metric, document that limitation.

Do not manufacture missing inputs.

---

# OEE RULE

When supported by the dataset:

```text
OEE = Availability × Performance × Quality
```

The agreed simulated Availability definition is:

```text
Planned Production Time =
Scheduled Time - Planned Downtime
```

```text
Availability =
Operating Time / Planned Production Time
```

If this definition changes, update:

- KPI dictionary
- decision log
- affected SQL
- affected marts
- affected documentation

Do not define OEE differently in Power BI than in the governed analytics layer without an explicit reason.

---

# DATA QUALITY PRINCIPLES

Data-quality validation is a major feature of this project.

Checks may include:

- duplicate records
- missing identifiers
- orphaned foreign keys
- unknown products
- unknown plants
- unknown machines
- invalid shifts
- negative downtime
- invalid timestamps
- end time before start time
- scrap greater than total production
- good + scrap not equal to total
- missing work-order relationships
- future-dated records
- unexpected null percentages

Validation results should preferably be persisted.

Recommended schema:

```text
test_name
table_name
records_tested
records_failed
severity
status
run_timestamp
```

Do not rely only on console messages.

---

# BAD-DATA TESTING RULE

Known intentionally corrupted datasets are test fixtures.

They should be used to prove validation behavior.

Do not:

- mix corrupted QA fixtures into the clean production-like dataset
- silently repair them before tests run
- present known QA fixtures as genuine source-system defects

Document their purpose clearly.

---

# INCIDENT SIMULATION

Project incidents should simulate realistic analytics work.

A planned scenario is:

Plant B appears to show an unexpected increase in scrap.

Investigation may evaluate:

- actual operational deterioration
- duplicate records
- rework duplication
- mapping problems
- source-system issue
- transformation error

Incident documentation should contain:

- Summary
- Business Impact
- Detection
- Investigation
- Root Cause
- Resolution
- Validation
- Preventive Action
- Regression Test

Do not force a predetermined root cause if the data does not support it.

---

# BUSINESS REQUIREMENTS

Use IDs such as:

```text
BR-001
BR-002
BR-003
```

Requirements should be traceable to:

- stakeholders
- data models
- transformations
- marts
- BI outputs

Avoid vague requirements such as:

"Create useful dashboard."

Prefer:

"Production reporting must support analysis by plant, line, shift, product, date, and work order."

---

# STAKEHOLDERS

Use these fictional stakeholder personas.

## Plant Manager

Cares about:

- production attainment
- OEE
- throughput
- downtime
- operational visibility

Typical questions:

- Why did a line miss its target?
- Which areas are reducing output?
- Are production losses improving?

---

## Quality Manager

Cares about:

- scrap
- defects
- quality trends
- work-order traceability

Typical questions:

- Which products create the most scrap?
- Are defects concentrated by line or shift?
- Can defects be traced to production records?

---

## Maintenance Manager

Cares about:

- machine failure
- downtime
- recurring breakdowns
- MTTR
- MTBF

Typical questions:

- Which machines account for most unplanned downtime?
- Are failures recurring?
- Which assets require attention?

---

## BI / Data Lead

Cares about:

- trusted data
- repeatability
- definitions
- reusable logic
- pipeline reliability
- documentation

Typical questions:

- Why do different teams report different numbers?
- Where is each KPI calculated?
- Can reporting logic be reused?
- How do we know the data is valid?

---

# DOCUMENTATION RULES

Documentation is part of the final product.

Maintain when applicable:

```text
README.md
DECISION_LOG.md
CHANGELOG.md
PROJECT_RETROSPECTIVE.md

docs/project_charter.md
docs/business_requirements.md
docs/stakeholder_notes.md
docs/source_data_assessment.md
docs/architecture.md
docs/source_to_target_mapping.md
docs/data_dictionary.md
docs/kpi_dictionary.md
docs/data_quality_plan.md
docs/uat_plan.md
docs/deployment_runbook.md
```

Project history may include:

```text
docs/project_history/01_project_request.md
docs/project_history/02_kickoff_notes.md
docs/project_history/03_requirements_workshop.md
docs/project_history/04_source_assessment.md
docs/project_history/05_architecture_review.md
docs/project_history/06_change_request.md
docs/project_history/07_data_quality_incident.md
docs/project_history/08_uat_feedback.md
docs/project_history/09_handoff_notes.md
```

These documents should resemble concise internal project records.

Do not turn them into fictional stories.

---

# DOCUMENTATION QUALITY

Documentation should be:

- concise
- professional
- practical
- internally consistent
- traceable to implemented work

Do not claim that something exists if it has not been implemented.

Use labels such as:

- Planned
- Implemented
- Validated
- Simulated
- Future Improvement

when necessary.

---

# ARCHITECTURE DIAGRAMS

Prefer Mermaid source files for version-controlled diagrams.

Recommended diagrams:

```text
diagrams/source_architecture.mmd
diagrams/logical_data_model.mmd
diagrams/pipeline_flow.mmd
```

Keep diagrams understandable to both technical and non-technical viewers.

Avoid overly dense architecture diagrams.

---

# POWER BI

Power BI Desktop is the BI tool for this project.

Do not assume access to Power BI Service.

The project must remain demonstrable through:

- `.pbix` file
- screenshots
- documentation
- exported visuals where appropriate

Project 2's Power BI product should primarily answer:

> Can we trust the manufacturing analytics pipeline?

Potential dashboard areas:

## Pipeline Health

- latest refresh
- records processed
- records rejected
- source-system status
- validation pass rate

## Data Quality

- failures by rule
- failures by source
- failure trends
- severity

## Manufacturing Validation

Use operational metrics to help verify transformed output:

- production
- scrap
- downtime
- OEE components where appropriate

Do not turn Project 2 into the full manufacturing operations dashboard.

That belongs in a separate project.

---

# TABLEAU

Tableau is not required to complete this project.

Do not duplicate Power BI work in Tableau unless specifically instructed.

Tableau may be used in separate portfolio projects.

---

# SECURITY RULES

Never commit:

- passwords
- Snowflake credentials
- private keys
- tokens
- secrets

Use:

```text
.env
```

or configuration files excluded by Git.

Provide examples such as:

```text
.env.example
```

or:

```text
config.example.yaml
```

with placeholder values only.

Ensure `.gitignore` protects credentials.

---

# GIT PRACTICES

Prefer logical commits.

Examples:

```text
scaffold repository structure

add business requirements and stakeholder documentation

add source data profiler

add raw ingestion scripts

add staging transformations

add dimensional analytics model

add KPI governance documentation

add data quality framework

add simulated incident analysis

add Power BI evidence

finalize portfolio README
```

Do not produce meaningless commit recommendations such as:

```text
update files
fix stuff
changes
```

---

# README RULES

README.md is recruiter-facing.

Do not lead with installation instructions.

Recommended order:

1. Project title
2. One-sentence summary
3. Business problem
4. Solution overview
5. Architecture
6. Source systems
7. Data model
8. Data quality
9. KPI governance
10. Simulated incident
11. BI product
12. Key results
13. Technology stack
14. Repository structure
15. Reproduction instructions
16. Limitations
17. Lessons learned
18. Future improvements

A hiring manager should understand the project before reading code.

---

# CODE QUALITY RULES

Prefer:

- descriptive names
- small understandable functions
- docstrings where useful
- meaningful comments
- explicit transformations
- reproducible behavior
- clear error handling

Avoid:

- deeply nested abstractions
- excessive classes
- unnecessary design patterns
- clever one-line code
- hidden side effects
- unnecessary dependencies

Optimize for:

**clarity + learning + portfolio readability**

rather than maximum engineering sophistication.

---

# TESTING RULES

Tests should validate meaningful behavior.

Examples:

- expected source schema
- valid keys
- reconciliation rules
- transformations
- known corrupted records fail correctly
- foreign-key mapping
- manufacturing business constraints

Do not create tests merely to increase code coverage.

---

# CHANGE MANAGEMENT

When requirements change:

1. document the requested change
2. identify impacted objects
3. update decision log if appropriate
4. modify transformations
5. run validation
6. update documentation
7. verify downstream impact

Do not silently change formulas or business logic.

---

# DECISION LOG

Use `DECISION_LOG.md` for decisions such as:

- KPI definition
- dimensional model choice
- layer responsibilities
- handling duplicates
- unit conversion
- null handling
- source precedence

Recommended structure:

```text
Decision ID:
Date:
Problem:
Alternatives:
Decision:
Rationale:
Impacted Objects:
Status:
```

---

# SOURCE-TO-TARGET LINEAGE

Where practical, maintain mapping from:

```text
source system
→ source file/table
→ raw object
→ staging model
→ analytics model
→ reporting mart
→ BI field
```

This lineage is an important portfolio feature.

Do not treat it as optional busywork.

---

# PORTFOLIO EVIDENCE

For major deliverables, identify what competency they demonstrate.

Examples:

Source profiling

→ unfamiliar data analysis

Business requirements

→ stakeholder translation

RAW/STAGING architecture

→ data engineering discipline

Dimensional modeling

→ scalable analytics

KPI dictionary

→ metric governance

QA framework

→ reporting reliability

Incident investigation

→ root-cause analysis

Power BI

→ analytics delivery

Documentation

→ communication and maintainability

GitHub

→ reproducibility and professional presentation

---

# RESUME INTEGRITY

Never fabricate business impact.

Do not create resume bullets using invented metrics such as:

- saved $2M
- increased efficiency 40%
- reduced downtime 25%

unless the project genuinely calculates and supports those outcomes.

Safe portfolio metrics may include:

- number of source systems simulated
- records processed
- number of validation checks
- number of analytics tables
- pipeline runtime
- detected known QA failures

Clearly identify the work as a project.

---

# INTERVIEW PREPARATION

When a milestone is completed, help explain:

- what was built
- why it was built
- architectural decisions
- tradeoffs
- limitations
- how it would differ in production

Prefer honest answers such as:

> In a production environment I would consider orchestration and automated scheduling, but I intentionally kept those outside the MVP because the goal was to demonstrate reliable transformation and data-quality architecture within the one-month project scope.

That is preferable to unnecessarily adding enterprise technologies.

---

# DEVELOPMENT PHASES

## Week 1

Business analysis and source discovery.

Expected outputs:

- repository scaffold
- project charter
- stakeholder notes
- business requirements
- source profiling
- source assessment
- architecture proposal
- initial data dictionary

---

## Week 2

Snowflake analytics engineering.

Expected outputs:

- RAW
- STAGING
- dimensions
- facts
- marts
- KPI dictionary
- source-to-target mapping
- architecture documentation

---

## Week 3

Reliability and data quality.

Expected outputs:

- validation framework
- persistent validation results
- SQL QA checks
- Python QA checks where appropriate
- simulated incident
- regression test
- decision log updates

---

## Week 4

Product delivery.

Expected outputs:

- final reporting marts
- Power BI model
- dashboard screenshots
- UAT documentation
- handoff documentation
- retrospective
- recruiter-facing README
- final repository cleanup

---

# AGENT SESSION BEHAVIOR

At the beginning of a new task:

1. Read this file.
2. Inspect relevant repository files.
3. Determine the current phase.
4. Identify what already exists.
5. Avoid duplicating prior work.

Before substantial implementation, briefly state:

- current objective
- files likely affected
- major assumption if any

After implementation, summarize:

- files created
- files modified
- validation performed
- unresolved issues
- recommended next step

Do not automatically continue into the next phase.

Stop when the requested task is complete.

---

# DO NOT DO THESE THINGS

Do not:

- build the entire project in one response
- rewrite the synthetic generator without reason
- fabricate business results
- fabricate stakeholder approval
- claim Snowflake code was executed when it was only written
- claim Power BI dashboards exist when only specifications exist
- silently correct source data before profiling
- calculate unsupported KPIs
- over-engineer architecture
- add unrelated tools for résumé keywords
- duplicate documentation unnecessarily
- generate massive amounts of boilerplate
- turn simulated communications into unrealistic corporate fiction
- hide important transformations in Power BI if they belong in governed SQL
- expose credentials
- commit secrets
- invent manufacturing experience

---

# DEFAULT DECISION RULE

When uncertain, choose the option that best improves:

1. realism
2. traceability
3. reliability
4. clarity
5. learning value
6. portfolio value

while staying within the one-month scope.

Always prefer a smaller, coherent, well-documented implementation over a larger unfinished one.