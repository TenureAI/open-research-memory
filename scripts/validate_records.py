#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD_DIRS = {
    "episodes": "episode",
    "procedures": "procedure",
    "insights": "insight",
}
ALLOWED_STATUS = {
    "draft",
    "reviewed",
    "verified",
    "trusted",
    "deprecated",
    "conflicted",
    "active",
}
REQUIRED_SECTIONS = [
    "Context",
    "Reproduce",
    "Evidence",
    "Failure Boundary",
]


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, None, "missing frontmatter start delimiter"
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, None, "missing frontmatter end delimiter"
    fm = text[4:end]
    body = text[end + 5 :]
    return fm, body, None


def get_value(frontmatter: str, key: str):
    m = re.search(rf"(?m)^{re.escape(key)}\s*:\s*(.+)\s*$", frontmatter)
    if not m:
        return None
    return m.group(1).strip().strip('"').strip("'")


def has_field(frontmatter: str, key: str):
    return re.search(rf"(?m)^{re.escape(key)}\s*:", frontmatter) is not None


def check_sections(body: str):
    missing = []
    for section in REQUIRED_SECTIONS:
        if re.search(rf"(?m)^##\s+{re.escape(section)}\s*$", body) is None:
            missing.append(section)
    return missing


def check_record(path: Path, expected_type: str):
    errors = []
    text = path.read_text(encoding="utf-8")

    frontmatter, body, err = parse_frontmatter(text)
    if err:
        return [f"{path}: {err}"]

    required_fields = [
        "id",
        "type",
        "status",
        "title",
        "tags",
        "created_at",
        "updated_at",
        "confidence",
        "human_verified",
        "source_run_id",
        "schema_version",
    ]
    for field in required_fields:
        if not has_field(frontmatter, field):
            errors.append(f"{path}: missing frontmatter field '{field}'")

    declared_type = get_value(frontmatter, "type")
    if declared_type and declared_type != expected_type:
        errors.append(
            f"{path}: type '{declared_type}' does not match folder type '{expected_type}'"
        )

    status = get_value(frontmatter, "status")
    if status and status not in ALLOWED_STATUS:
        errors.append(f"{path}: invalid status '{status}'")

    schema_version = get_value(frontmatter, "schema_version")
    if schema_version and re.match(r"^[0-9]+\.[0-9]+(\.[0-9]+)?$", schema_version) is None:
        errors.append(f"{path}: invalid schema_version '{schema_version}'")

    confidence = get_value(frontmatter, "confidence")
    if confidence:
        try:
            value = float(confidence)
            if value < 0 or value > 1:
                errors.append(f"{path}: confidence must be in [0,1], got {confidence}")
        except ValueError:
            errors.append(f"{path}: confidence is not numeric: {confidence}")

    human_verified = get_value(frontmatter, "human_verified")
    if human_verified and human_verified not in {"true", "false"}:
        errors.append(
            f"{path}: human_verified must be true/false, got '{human_verified}'"
        )

    tags = get_value(frontmatter, "tags")
    if tags is not None and tags.strip() in {"[]", ""}:
        errors.append(f"{path}: tags must not be empty")

    missing_sections = check_sections(body)
    for section in missing_sections:
        errors.append(f"{path}: missing required section '## {section}'")

    return errors


def main():
    md_files = []
    for folder in RECORD_DIRS.keys():
        root = ROOT / folder
        if not root.exists():
            continue
        md_files.extend(
            p
            for p in root.rglob("*.md")
            if not p.name.startswith(".")
        )

    if not md_files:
        print("No record markdown files found. Validation passed.")
        return 0

    all_errors = []
    for path in sorted(md_files):
        top = path.relative_to(ROOT).parts[0]
        expected_type = RECORD_DIRS[top]
        all_errors.extend(check_record(path, expected_type))

    if all_errors:
        print("Validation failed:")
        for err in all_errors:
            print(f"- {err}")
        return 1

    print(f"Validation passed for {len(md_files)} record file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

