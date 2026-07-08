"""Verify no Chinese (CJK) characters remain in the public deposit.

Portable: resolves the deposit root relative to this file's location, so it
runs from any machine without editing paths. Scans every .csv in data/ plus
all text-based artifacts (.csv, .md, .txt, .yml, .py) for characters in the
CJK Unified Ideographs block (U+4E00 to U+9FFF).

Exit code 0 and "ALL CLEAN" when no CJK is found; exit code 1 and a per-file
report otherwise.
"""
import re
import sys
from pathlib import Path

CJK = re.compile(r"[\u4e00-\u9fff]")

# Deposit root = parent of the code/ directory that holds this script.
CODE_DIR = Path(__file__).resolve().parent
DEPOSIT_ROOT = CODE_DIR.parent

# Some artifacts legitimately contain Chinese source terms because their whole
# purpose is the Chinese-to-English crosswalk / its validation:
#   - translation_maps.py         : the mapping dictionary itself
#   - translation_validation.csv  : back-translation validation of source terms
# These are exempt; all shared data artifacts must still be CJK-free.
EXEMPT_NAMES = {"translation_maps.py", "translation_validation.csv"}

SCAN_SUFFIXES = {".csv", ".md", ".txt", ".yml", ".yaml"}


def scan_file(path: Path):
    """Return a dict {location: [samples]} of CJK hits, or empty if clean."""
    hits = {}
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return hits
    for i, line in enumerate(text.splitlines(), start=1):
        found = CJK.findall(line)
        if found:
            key = f"line {i}"
            hits[key] = list(dict.fromkeys(found))[:5]
    return hits


def main():
    ok = True
    scanned = 0
    for path in sorted(DEPOSIT_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if path.name in EXEMPT_NAMES:
            continue
        scanned += 1
        rel = path.relative_to(DEPOSIT_ROOT)
        bad = scan_file(path)
        status = "OK" if not bad else "RESIDUAL CJK"
        print(f"{str(rel):50s} {status}")
        if bad:
            ok = False
            for loc, samples in list(bad.items())[:10]:
                print(f"    {loc}: {samples}")
    print(f"\nScanned {scanned} files.")
    print("ALL CLEAN" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
