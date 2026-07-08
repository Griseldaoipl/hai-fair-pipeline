"""Stage 4 - Risk-factor decomposition.

The source registry records predisposing factors as a single comma-delimited
free-text field. The pipeline decomposes it into 19 binary rf_* flags using
deterministic substring matching against a closed glossary of recognised terms
(no NLP / no machine learning), ensuring auditable, reproducible output.

This released stage re-derives the 19 flags from the English `risk_factors`
list and checks them against the shipped rf_* columns, reporting per-flag
agreement so the decomposition logic is fully auditable.

Source logic: scripts/build_cases.py (internal decomposition step).
Portable: all paths resolved relative to this file.
"""
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
CASES = DATA / "cases_long_en.csv"

# English keyword -> rf_* flag. Case-insensitive substring match on the
# comma-separated English risk_factors list. This mirrors the closed-glossary
# substring matching used in the source pipeline.
KEYWORD_MAP = {
    "rf_urinary_catheter": ["urinary catheter"],
    "rf_ventilator": ["mechanical ventilation"],
    "rf_cvc": ["central venous catheter"],
    "rf_bedridden": ["bedridden"],
    "rf_diabetes": ["diabetes"],
    "rf_hypertension": ["hypertension"],
    "rf_malignancy": ["malignancy"],
    "rf_chemo": ["chemotherapy"],
    "rf_radio": ["radiotherapy"],
    "rf_steroid": ["corticosteroid"],
    "rf_immunosuppression": ["immunosuppress", "immunocompromised", "immune deficiency"],
    "rf_age_over_70": ["age >70", "age >=80"],
    "rf_age_over_60": ["age >=60"],
    "rf_malnutrition": ["malnutrition"],
    "rf_low_albumin": ["hypoalbumin"],
    "rf_anaemia": ["anaemia", "anemia"],
    "rf_stroke": ["stroke", "cerebrovascular"],
    "rf_copd": ["copd", "chronic airway"],
    "rf_dialysis": ["haemodialysis", "hemodialysis", "dialysis"],
}


def derive(text):
    t = (text or "").lower()
    return {flag: int(any(k in t for k in keys)) for flag, keys in KEYWORD_MAP.items()}


def main():
    import pandas as pd
    if not CASES.exists():
        print(f"[stage4] ERROR: missing input {CASES}")
        return 1
    df = pd.read_csv(CASES, keep_default_na=False)
    if "risk_factors" not in df.columns:
        print("[stage4] ERROR: risk_factors column absent")
        return 1
    worst = 1.0
    for flag in KEYWORD_MAP:
        if flag not in df.columns:
            print(f"[stage4] ERROR: shipped flag {flag} absent")
            return 1
        shipped = df[flag].astype(str).str.strip().replace({"": "0"}).astype(float).astype(int)
        derived = df["risk_factors"].map(lambda x: derive(x)[flag])
        agree = (shipped.values == derived.values).mean()
        worst = min(worst, agree)
        print(f"[stage4] {flag:24s} agreement={agree:6.3f}")
    print(f"[stage4] decomposition checked on {len(df)} episodes; min agreement={worst:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
