# Open Research Memory

Open Research Memory is a shared repository for reusable AI R&D experience records.

The goal is to accumulate evidence-backed memory that other contributors can apply safely across projects.

## Scope

This repository accepts:
- `verified` episodes
- `active` procedures
- `active` insights

This repository does not accept:
- run-local `working` state
- unverified noise logs
- secrets or organization-specific sensitive data

## Repository Structure

```text
episodes/
  environment/
  training/
  evaluation/
  reproduction/
procedures/
  setup/
  debug/
  reproduce/
  experiment/
insights/
  planning/
  debugging/
  evaluation/
templates/
schemas/
scripts/
```

## Record Contract

Each record must be a Markdown file with YAML frontmatter.

Required frontmatter fields:
- `id`
- `type` (`episode|procedure|insight`)
- `status`
- `title`
- `tags`
- `created_at`
- `updated_at`
- `confidence`
- `human_verified`
- `source_run_id`
- `schema_version`

Recommended statuses:
- `draft`
- `reviewed`
- `verified`
- `trusted`
- `deprecated`
- `conflicted`
- `active`

## Minimum Content Requirements

Every shared record must contain these sections:
1. `Context`
2. `Reproduce`
3. `Evidence`
4. `Failure Boundary`

Use templates from [`templates/`](templates).

## Contribution Workflow

1. Export candidate records from your local workspace.
2. Place records in the correct folder (`episodes/`, `procedures/`, `insights/`).
3. Run validation:
   - `python3 scripts/validate_records.py`
4. Open a pull request.
5. Merge only after checks and review pass.

Do not push directly to `main`.

## Validation

Validation script:
- checks frontmatter required fields
- checks status/type consistency
- checks minimum required sections
- checks confidence and schema version format

Run locally:

```bash
python3 scripts/validate_records.py
```

## Review Standard

A record is mergeable only when it is:
- reproducible by another contributor
- evidence-backed (logs, metrics, commits, artifacts)
- explicit about applicability and failure boundary
- free of sensitive data

## Schema

See [`schemas/memory-record.schema.json`](schemas/memory-record.schema.json) for the machine-readable schema.

