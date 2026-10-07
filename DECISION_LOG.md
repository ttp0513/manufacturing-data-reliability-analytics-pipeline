# DECISION LOG

Use this file only for important project decisions.

## Decision Template

### D-XXX - Decision Title

Date:
Status: Proposed | Approved | Superseded

### Problem

### Alternatives Considered

### Decision

### Rationale

### Impacted Objects

### Validation / Follow-up

## D-001 - Preserve the synthetic data package as a self-contained repository asset

Date: 2026-10-07
Status: Approved

### Problem

The synthetic generator, its documentation, generated source extracts,
reference outputs, controlled QA fixtures, and validation evidence were stored
in a long-named package directory at the repository root. The repository needed
a clear structure without splitting related assets or implying that downstream
pipeline components already existed.

### Alternatives Considered

1. Split the package across root-level `scripts/`, `docs/`, and `data/`
   directories. This would provide stronger categorization but require path and
   documentation changes and weaken the package's self-contained provenance.
2. Keep the package unchanged at the repository root. This would avoid moves
   but leave generated data mixed with project-governance files.
3. Move the complete package under `data/synthetic/` while preserving its
   internal layout.

### Decision

Move the complete synthetic data package under `data/synthetic/` without
deleting, duplicating, regenerating, or rewriting its contents. Treat
`generated_data/source_systems/` as future pipeline input. Preserve `core/` as
generator-supplied reference output and keep the controlled QA fixtures separate
from the clean production-like data.

Create downstream implementation directories only when their project phases
begin.

### Rationale

This keeps source provenance and generator documentation together, clearly
separates synthetic data assets from repository governance, and avoids claiming
that Snowflake, analytics, KPI, or Power BI components have been implemented.

### Impacted Objects

- `data/synthetic/`
- `README.md`
- `.gitignore`
- `PROJECT_STATUS.md`

### Validation / Follow-up

- Validated on 2026-10-07: the relocated package contains 37 files totaling
  25,313,617 bytes, and the former root-level package path is absent.
- All seven simulated source-system extracts were read successfully after the
  move; their byte sizes and row counts match the pre-move inspection.
- A SHA-256 manifest digest was captured during validation:
  `33c5236e6aa9f7c27893ab75846f74ca6b2964990c10f1cb0c23696ac5937430`.
- Add `src/`, `sql/`, `tests/`, or `powerbi/` only when approved work requires
  them.
