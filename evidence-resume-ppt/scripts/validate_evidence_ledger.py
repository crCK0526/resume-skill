#!/usr/bin/env python3
"""Validate an evidence-ledger JSON file for resume production.

Usage:
    python validate_evidence_ledger.py ledger.json

The script is local-only, uses the Python standard library, and never writes to
or modifies the input file. Error output is sanitized and does not print resume
claims or candidate personal data.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = {"category", "claim", "source", "confidence", "status", "note"}
CONFIDENCE_VALUES = {"high", "medium", "low"}
STATUS_VALUES = {"confirmed", "conflict", "missing", "derived", "excluded"}
CATEGORY_VALUES = {"basic_info", "education", "work", "campus", "award", "certificate", "skill", "project"}
BLOCKING_CATEGORIES = {"basic_info", "education", "work"}
FORBIDDEN_SOURCE_MARKERS = {
    "简历知识库",
    "knowledge base",
    "evidence-and-copy-guide.md",
    "a4-resume-spec.txt",
}
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_RECORDS = 1000
MAX_FIELD_CHARS = 5000
MAX_ERRORS = 100


def add_error(errors: list[str], message: str) -> None:
    if len(errors) < MAX_ERRORS:
        errors.append(message)


def validate(records: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(records, list):
        return ["Top-level JSON value must be an array."]
    if len(records) > MAX_RECORDS:
        return [f"Record count exceeds the limit of {MAX_RECORDS}."]

    for index, record in enumerate(records, start=1):
        prefix = f"Record {index}"
        if not isinstance(record, dict):
            add_error(errors, f"{prefix}: must be an object.")
            continue

        missing_fields = sorted(REQUIRED_FIELDS - set(record))
        if missing_fields:
            add_error(errors, f"{prefix}: required field count is incomplete.")
            continue

        for field in REQUIRED_FIELDS:
            value = record[field]
            if not isinstance(value, str):
                add_error(errors, f"{prefix}: field '{field}' must be a string.")
            elif len(value) > MAX_FIELD_CHARS:
                add_error(errors, f"{prefix}: field '{field}' exceeds the length limit.")

        if record.get("confidence") not in CONFIDENCE_VALUES:
            add_error(errors, f"{prefix}: confidence value is invalid.")
        if record.get("status") not in STATUS_VALUES:
            add_error(errors, f"{prefix}: status value is invalid.")
        if record.get("category") not in CATEGORY_VALUES:
            add_error(errors, f"{prefix}: category value is invalid.")
        if not str(record.get("claim", "")).strip():
            add_error(errors, f"{prefix}: claim is empty.")
        source_text = str(record.get("source", "")).strip()
        if record.get("status") in {"confirmed", "derived"} and not source_text:
            add_error(errors, f"{prefix}: confirmed/derived claim requires a source.")
        if any(marker.casefold() in source_text.casefold() for marker in FORBIDDEN_SOURCE_MARKERS):
            add_error(errors, f"{prefix}: knowledge-base or bundled guidance cannot be used as candidate evidence.")
        if record.get("category") in BLOCKING_CATEGORIES and record.get("status") in {"conflict", "missing"}:
            add_error(errors, f"{prefix}: unresolved blocker exists in a required category.")

    if len(errors) == MAX_ERRORS:
        errors.append("Additional errors were omitted after reaching the reporting limit.")
    return errors


def read_records(path: Path) -> object:
    if path.is_symlink() or not path.is_file():
        raise ValueError("input must be a regular, non-symlink file")
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError(f"input exceeds the {MAX_FILE_BYTES}-byte size limit")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a resume evidence ledger.")
    parser.add_argument("ledger", type=Path, help="Path to the ledger JSON file")
    args = parser.parse_args()

    try:
        records = read_records(args.ledger)
    except FileNotFoundError:
        print("ERROR: input file was not found.", file=sys.stderr)
        return 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: input could not be validated ({type(exc).__name__}).", file=sys.stderr)
        return 2

    errors = validate(records)
    if errors:
        print("FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASSED: {len(records)} record(s) validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
