"""Stage 6 - De-identification and quality assurance.

Confirms the released episode table carries no direct-identifier columns
(names, MRN, bed, physician), then runs the Chinese-character verifier over the
whole deposit as the final QA gate.

Source logic: scripts/export_english.py + scripts/verify_no_chinese.py (internal).
Portable: all paths resolved relative to this file.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
CASES = DATA / "cases_long_en.csv"

# Whole-token identifiers (matched against underscore-split column tokens).
FORBIDDEN_TOKENS = {"name", "mrn", "bed", "physician", "doctor", "nurse"}
# Multi-word identifier phrases (matched as substrings).
FORBIDDEN_PHRASES = ["medical_record", "record_number", "attending"]


def is_identifier(col):
    low = col.lower()
    tokens = set(low.split("_"))
    if tokens & FORBIDDEN_TOKENS:
        return True
    return any(p in low for p in FORBIDDEN_PHRASES)


def main():
    import pandas as pd
    if not CASES.exists():
        print(f"[stage6] ERROR: missing input {CASES}")
        return 1
    df = pd.read_csv(CASES, nrows=1)
    leaked = [c for c in df.columns if is_identifier(c)]
    if leaked:
        print(f"[stage6] ERROR: potential direct-identifier columns present: {leaked}")
        return 1
    print("[stage6] no direct-identifier columns detected")
    r = subprocess.run([sys.executable, str(HERE / "verify_no_chinese.py")])
    if r.returncode != 0:
        print("[stage6] ERROR: Chinese-character verification FAILED")
        return 1
    print("[stage6] de-identification QA passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
