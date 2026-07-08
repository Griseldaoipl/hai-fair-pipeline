"""Stage 1 - Ingestion.

In the full internal pipeline this stage reads the monthly Chinese-language
surveillance worksheets and concatenates them into one long-format episode
table. The raw worksheets contain direct identifiers and are NOT part of the
public de-identified deposit; therefore, in the released package this stage
loads and validates the already-ingested, de-identified episode table
(data/cases_long_en.csv) that the raw ingestion produced.

Source logic: scripts/build_cases.py (internal).
Portable: all paths resolved relative to this file.
"""
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
CASES = DATA / "cases_long_en.csv"


def main():
    import pandas as pd
    if not CASES.exists():
        print(f"[stage1] ERROR: missing input {CASES}")
        return 1
    df = pd.read_csv(CASES, dtype=str, keep_default_na=False)
    if len(df) == 0:
        print("[stage1] ERROR: ingested table is empty")
        return 1
    print(f"[stage1] ingested episode table: {len(df)} rows, {df.shape[1]} columns")
    return 0


if __name__ == "__main__":
    sys.exit(main())
