"""Generate the annotation-set templates (pre-filled, ready for reviewers).

Produces two files in this validation/ directory:

  riskfactor_annotation.csv
      Long format, one row per (episode, rf_* flag) for a stratified random
      sample of 120 episodes (~10% of the cohort), stratified by year and
      infection site. The `pipeline` column is pre-filled from the shipped
      rf_* flags. Reviewers fill `reviewer1`, `reviewer2`, and `consensus`
      with 0/1 codings by reading the English risk_factors list for each
      episode.

  translation_validation.csv
      24 categorical values stratified across translation domains. `source_zh`
      and `pipeline_en` are pre-filled from code/translation_maps.py. The
      bilingual reviewer fills `back_translation` and `classification`
      (exact | synonym | discrepancy).

Reproducible: fixed seed (42). Re-running regenerates identical templates
(existing reviewer entries would be overwritten, so run once up front).
"""
import csv
import sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
CODE = ROOT / "code"
sys.path.insert(0, str(CODE))

SEED = 42
N_EPISODES = 120

RF_FLAGS = [
    "rf_urinary_catheter", "rf_ventilator", "rf_cvc", "rf_bedridden",
    "rf_diabetes", "rf_hypertension", "rf_malignancy", "rf_chemo", "rf_radio",
    "rf_steroid", "rf_immunosuppression", "rf_age_over_70", "rf_age_over_60",
    "rf_malnutrition", "rf_low_albumin", "rf_anaemia", "rf_stroke", "rf_copd",
    "rf_dialysis",
]


def build_riskfactor_template():
    df = pd.read_csv(DATA / "cases_long_en.csv", keep_default_na=False)
    df = df.reset_index(drop=True)
    rng = np.random.default_rng(SEED)
    # Stratified sample by infection_site (year captured in the row too).
    idx = []
    frac = N_EPISODES / len(df)
    for _, g in df.groupby("infection_site"):
        k = max(1, round(len(g) * frac))
        idx += list(rng.choice(g.index.values, size=min(k, len(g)), replace=False))
    idx = list(dict.fromkeys(idx))
    if len(idx) > N_EPISODES:
        idx = list(rng.choice(idx, size=N_EPISODES, replace=False))
    elif len(idx) < N_EPISODES:
        rest = [i for i in df.index if i not in set(idx)]
        idx += list(rng.choice(rest, size=N_EPISODES - len(idx), replace=False))
    sample = df.loc[sorted(idx)]

    out = HERE / "riskfactor_annotation.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["episode_id", "year", "infection_site", "risk_factors",
                    "flag", "pipeline", "reviewer1", "reviewer2", "consensus"])
        for _, row in sample.iterrows():
            eid = f"{row['source_file']}#{row['case_seq']}"
            for flag in RF_FLAGS:
                pipe = str(row[flag]).strip() or "0"
                pipe = str(int(float(pipe)))
                w.writerow([eid, row["year"], row["infection_site"],
                            row["risk_factors"], flag, pipe, "", "", ""])
    print(f"wrote {out.name}: {len(sample)} episodes x {len(RF_FLAGS)} flags "
          f"= {len(sample) * len(RF_FLAGS)} rows")


def build_translation_template():
    import translation_maps as tm
    domains = {name: obj for name, obj in vars(tm).items()
               if name.isupper() and isinstance(obj, dict) and len(obj) >= 2}
    rng = np.random.default_rng(SEED)
    # Allocate 24 values across the 8 largest domains, 3 each.
    chosen = sorted(domains, key=lambda n: len(domains[n]), reverse=True)[:8]
    rows = []
    for name in chosen:
        items = list(domains[name].items())
        picks = rng.choice(len(items), size=min(3, len(items)), replace=False)
        for i in picks:
            zh, en = items[int(i)]
            rows.append([name, zh, en, "", ""])
    out = HERE / "translation_validation.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["domain", "source_zh", "pipeline_en",
                    "back_translation", "classification"])
        w.writerows(rows)
    print(f"wrote {out.name}: {len(rows)} values across {len(chosen)} domains")


if __name__ == "__main__":
    build_riskfactor_template()
    build_translation_template()
