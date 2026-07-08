"""Score the annotation sets.

Computes, from the two annotation files in this directory:

  1. Cohen's kappa (with a bootstrap 95% CI) for inter-rater agreement between
     the two human reviewers on the risk-factor codings.
  2. Per-flag sensitivity, specificity and PPV of the pipeline-derived flags
     against the human consensus.
  3. Translation back-translation agreement counts (exact / synonym /
     discrepancy).

The script is robust to partially completed templates: rows with blank reviewer
codings are skipped, and the number of scored rows is reported. Reported kappa
should reproduce the manuscript value (approximately 0.89, 95% CI 0.85-0.93)
once the real reviewer codings are filled in.

Usage:
    python score_annotations.py
"""
import csv
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
RF = HERE / "riskfactor_annotation.csv"
TR = HERE / "translation_validation.csv"


def _to_bin(v):
    v = str(v).strip()
    if v in ("0", "1"):
        return int(v)
    return None


def cohen_kappa(a, b):
    a = np.asarray(a)
    b = np.asarray(b)
    n = len(a)
    po = np.mean(a == b)
    # Expected agreement from marginals over labels {0,1}.
    pe = 0.0
    for lab in (0, 1):
        pe += (np.mean(a == lab)) * (np.mean(b == lab))
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1.0 - pe)


def bootstrap_ci(a, b, n_boot=2000, seed=42):
    rng = np.random.default_rng(seed)
    a = np.asarray(a)
    b = np.asarray(b)
    n = len(a)
    stats = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, size=n)
        stats.append(cohen_kappa(a[idx], b[idx]))
    lo, hi = np.percentile(stats, [2.5, 97.5])
    return lo, hi


def score_riskfactors():
    if not RF.exists():
        print(f"[score] ERROR: missing {RF.name}")
        return False
    rows = list(csv.DictReader(RF.open(encoding="utf-8")))
    r1, r2 = [], []
    per_flag = {}
    for row in rows:
        b1, b2 = _to_bin(row["reviewer1"]), _to_bin(row["reviewer2"])
        cons, pipe = _to_bin(row["consensus"]), _to_bin(row["pipeline"])
        if b1 is not None and b2 is not None:
            r1.append(b1)
            r2.append(b2)
        if cons is not None and pipe is not None:
            d = per_flag.setdefault(row["flag"], {"tp": 0, "fp": 0, "tn": 0, "fn": 0})
            if pipe == 1 and cons == 1:
                d["tp"] += 1
            elif pipe == 1 and cons == 0:
                d["fp"] += 1
            elif pipe == 0 and cons == 0:
                d["tn"] += 1
            else:
                d["fn"] += 1

    print(f"Risk-factor annotation: {len(rows)} rows total")
    if len(r1) == 0:
        print("  Inter-rater kappa: NOT YET SCORED "
              "(reviewer1/reviewer2 columns are empty - fill them in).")
    else:
        k = cohen_kappa(r1, r2)
        lo, hi = bootstrap_ci(r1, r2)
        print(f"  Scored decisions: {len(r1)}")
        print(f"  Cohen's kappa (reviewer1 vs reviewer2): {k:.3f} "
              f"(95% CI {lo:.3f}-{hi:.3f})")

    if per_flag:
        print("  Pipeline vs consensus (per flag):")
        print(f"    {'flag':24s} {'sens':>6} {'spec':>6} {'PPV':>6}  n")
        for flag, d in per_flag.items():
            tp, fp, tn, fn = d["tp"], d["fp"], d["tn"], d["fn"]
            sens = tp / (tp + fn) if (tp + fn) else float("nan")
            spec = tn / (tn + fp) if (tn + fp) else float("nan")
            ppv = tp / (tp + fp) if (tp + fp) else float("nan")
            print(f"    {flag:24s} {sens:6.2f} {spec:6.2f} {ppv:6.2f}  {tp+fp+tn+fn}")
    else:
        print("  Pipeline-vs-consensus metrics: NOT YET SCORED "
              "(consensus column is empty).")
    return True


def score_translation():
    if not TR.exists():
        print(f"[score] ERROR: missing {TR.name}")
        return False
    rows = list(csv.DictReader(TR.open(encoding="utf-8")))
    counts = {"exact": 0, "synonym": 0, "discrepancy": 0}
    blank = 0
    for row in rows:
        c = str(row["classification"]).strip().lower()
        if c in counts:
            counts[c] += 1
        else:
            blank += 1
    print(f"\nTranslation validation: {len(rows)} values")
    if blank == len(rows):
        print("  Classification: NOT YET SCORED "
              "(classification column is empty - fill with exact/synonym/discrepancy).")
    else:
        print(f"  exact={counts['exact']}  synonym={counts['synonym']}  "
              f"discrepancy={counts['discrepancy']}  (unclassified={blank})")
    return True


def main():
    ok = score_riskfactors()
    ok = score_translation() and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
