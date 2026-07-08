# Healthcare-Associated Infection (HAI) Surveillance Dataset — English

Hospital-level HAI surveillance covering **February 2023 – April 2026** (39 monthly source files; January 2023 was unavailable in the source). All Chinese text in the original registry has been translated to English; the files in this folder contain no CJK characters.

## Files

| File | Grain | Rows × Cols | Use |
|---|---|---:|---|
| `cases_long_en.csv`         | one HAI episode per row             | 1 240 × 57 | patient-level analyses (risk factors, pathogens, sites) |
| `department_monthly_en.csv` | department × month                  | 1 461 × 51 | incidence-rate trends, ward comparison |
| `department_period_en.csv`  | department × quarter / half / year  |   643 × 51 | aggregated benchmarks |
| `codebook_en.csv`           | one variable per row                |   115 × 6  | machine-readable variable dictionary |
| `codebook_en.md`            | variable + full value-translation tables | — | human-readable codebook |

All CSVs are UTF-8.

## What changed vs the bilingual version (`cleaned/`)

1. **Categorical translation** — every Chinese categorical value (departments, infection sites, specimen types, pathogens, microbiology status, outcome, report status, incision grade, surgical-infection flag) was translated using exhaustive dictionaries in `scripts/translation_maps.py`. The build script raises if any value is missing, so the dictionaries are guaranteed to cover every observation.
2. **Risk factors** — the comma-separated `predisposing-factors` list became an English `risk_factors` column. The 19 boolean `rf_*` flags from the bilingual file are preserved unchanged because they were already English. All `Other(...)` ("Other (free-text reason)") variants are collapsed to `Other`.
3. **Source filenames** — replaced with a clean `YYYY-MM` provenance key in `cases_long_en.csv` and `department_monthly_en.csv`, and `YYYY-Qn` / `YYYY-H1` / `YYYY-Y` in `department_period_en.csv`.
4. **Free-text Chinese fields dropped** — `reporter`, `attending_doctor`, `admission_diagnosis`, `bed_no`, and `risk_factors_raw`. These contained personal identifiers (staff names) or unstructured Chinese diagnoses that would require manual ICD recoding to be analytically useful. If you need them in the future, they can be re-added from the bilingual `cases_long.csv` and translated/coded separately.

## Data-quality reconciliation (passes)

For every one of the 39 months, the row count in `cases_long_en.csv` exactly equals `n_infection_episodes` in the hospital-wide row of `department_monthly_en.csv` (Σ = 1 240 in both, zero monthly mismatches).

## Caveats to mention in any manuscript

- **2023-01 missing** — not in the source.
- **`patient_days` denominator NaN for all 2023** — the hospital began capturing patient-days on 2024-01; therefore `incidence_per_1000_pd` is only valid from 2024-01 onwards.
- A site-count column being NaN means the column was absent from that month's source file (no cases of that site that month). Treat NaN as 0 when computing site-specific incidence.
- One patient may appear on multiple rows in `cases_long_en.csv` if infected at >1 site within the same admission (`patient_id` repeats).
- `Missed (audit-detected)` and `Late` reports are still included in the case list and counted in episodes; the hospital-wide audit miss rate is captured by `underreport_pct` in the summary files.

## Reproducing the build

```cmd
python scripts\inventory.py
python scripts\build_cases.py            REM bilingual cases_long.csv
python scripts\build_summary.py          REM bilingual department_*.csv
python scripts\sanity_check.py
python scripts\export_english.py         REM produces *_en.csv in cleaned_en/
python scripts\build_codebook_en.py      REM produces codebook_en.csv + .md
python scripts\verify_no_chinese.py      REM final scan: 0 CJK chars expected
```

## Suggested SCI-quality analyses

- **Time-trend** of monthly hospital-wide `incidence_per_1000_pd` (2024-01 → 2026-04): joinpoint regression or interrupted time series if any infection-control interventions can be aligned to a date.
- **Department-stratified incidence ranking** using `department_monthly_en.csv`, excluding rows with `is_hospital_total = 1`. Highlights persistently high-burden wards (ICU, neurosurgery, oncology, haematology in this dataset).
- **Site distribution** of HAI: lower respiratory tract dominates (~ 41 % of episodes), followed by non-catheter BSI and CAUTI. Use `infection_site` in `cases_long_en.csv`.
- **Risk-factor logistic regression** for specific HAI types (CLABSI, CAUTI, VAP) using `rf_*` boolean flags as predictors and infection-site presence as the outcome.
- **Microbiology yield**: cross-tabulate `micro_tested` × `micro_positive` × `infection_site` × year to describe culture submission rates and pathogen spectra.
- **Antimicrobial-resistance burden** using the `(CRE)`, `(CRKP)`, `(CRPA)`, `(CRAB)`, `(MRSA)` suffixes preserved in the `pathogen` column.
