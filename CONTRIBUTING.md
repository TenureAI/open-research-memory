# Contributing

## Branch and PR Policy

1. Create a feature branch from `main`.
2. Keep one logical topic per pull request.
3. Do not push directly to `main`.

## What to Contribute

Contribute only reusable memory records:
- `episode`
- `procedure`
- `insight`

Use the correct folder and template:
- `episodes/*` with `templates/episode.md`
- `procedures/*` with `templates/procedure.md`
- `insights/*` with `templates/insight.md`

## Required Checks

Before opening a PR, run:

```bash
python3 scripts/validate_records.py
```

Your PR should pass:
- schema and frontmatter checks
- required section checks
- content quality review

## Content Quality Rules

Each record must:
- provide reproducible steps
- provide evidence references
- define applicability and failure boundary
- avoid sensitive data

## Schema Changes

If you modify record schema:
1. Update `schemas/memory-record.schema.json`.
2. Explain migration impact in the PR description.
3. Keep backward compatibility when possible.

