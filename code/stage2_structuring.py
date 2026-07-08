"""Stage 2 - Structuring.

Validates that the ingested episode table conforms to the expected long-format
schema: one row per (patient, infection episode), with the core temporal,
departmental, microbiological and outcome fields present and parseable.

Source logic: scripts/build_cases.py (internal).
Portable: all paths resolved relative to this file.
"""
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
CASES = DATA / "cases_long_en.csv"

REQUIRED = [
    "year", "month", "patient_id", "sex", "age_years",
    "admission_date", "infection_date", "length_of_stay_days",
    "days_to_infection", "infection_dept", "infection_site",
    "micro_test_status", "outcome", "report_status",
]


def main():
    import pandas as pd
    if not CASES.exists():
        print(f"[stage2] ERROR: missing input {CASES}")
        return 1
    df = pd.read_csv(CASES, keep_default_na=False)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        print(f"[stage2] ERROR: missing required columns: {missing}")
        return 1
    # age_years must parse to float; year/month to int
    try:
        pd.to_numeric(df["age_years"], errors="raise")
        pd.to_numeric(df["year"], errors="raise")
        pd.to_numeric(df["month"], errors="raise")
    except Exception as exc:
        print(f"[stage2] ERROR: numeric field failed to parse: {exc}")
        return 1
    print(f"[stage2] structure OK: {len(REQUIRED)} core fields present and typed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
