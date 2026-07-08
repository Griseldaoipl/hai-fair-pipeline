"""Run the full de-identification / structuring pipeline in order.

Portable and idempotent: every path is resolved relative to this file, so the
pipeline runs unchanged on any machine. Executes the six stage scripts in
ascending order; halts on the first non-zero exit and reports the failing
stage.

Usage:
    python run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

STAGES = [
    "stage1_ingestion.py",
    "stage2_structuring.py",
    "stage3_codebook.py",
    "stage4_riskfactor_decomposition.py",
    "stage5_translation.py",
    "stage6_deidentification_qa.py",
]


def main():
    for stage in STAGES:
        print(f"\n>>> {stage}")
        result = subprocess.run([sys.executable, str(HERE / stage)])
        if result.returncode != 0:
            print(f"\nFAILED at {stage} (exit {result.returncode})")
            return 1
    print("\nAll six stages OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
