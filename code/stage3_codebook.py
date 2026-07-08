"""Stage 3 - Codebook construction.

Regenerates the variable inventory from the structured episode table and
checks it against the shipped data dictionary (data/codebook_en.csv). Every
column in cases_long_en.csv must be documented in the codebook.

Source logic: scripts/build_codebook_en.py (internal).
Portable: all paths resolved relative to this file.
"""
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
CASES = DATA / "cases_long_en.csv"
CODEBOOK = DATA / "codebook_en.csv"


def main():
    import pandas as pd
    for f in (CASES, CODEBOOK):
        if not f.exists():
            print(f"[stage3] ERROR: missing input {f}")
            return 1
    df = pd.read_csv(CASES, keep_default_na=False)
    cb = pd.read_csv(CODEBOOK, keep_default_na=False)
    documented = set(cb.loc[cb["file"] == "cases_long_en.csv", "variable"])
    undocumented = [c for c in df.columns if c not in documented]
    if undocumented:
        print(f"[stage3] ERROR: columns absent from codebook: {undocumented}")
        return 1
    print(f"[stage3] codebook OK: all {df.shape[1]} columns documented")
    return 0


if __name__ == "__main__":
    sys.exit(main())
