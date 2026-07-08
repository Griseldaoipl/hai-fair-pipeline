# FAIR-Compliant Hospital-Acquired Infection (HAI) Surveillance Dataset

**DOI:** 10.5281/zenodo.20301027

A de-identified, English-language surveillance dataset of hospital-acquired
infection (HAI) episodes, together with the complete processing pipeline,
translation dictionaries, validation materials, and reproducibility artifacts
supporting the accompanying manuscript.

---

## 1. Dataset description

The dataset covers **1,240 HAI episodes** across **39 monthly** surveillance
periods, with **57 documented variables** per episode spanning demographics,
admission/infection timing, department/ward, infection site, microbiology
(specimen, organism, resistance phenotype), surgical context, indwelling-device
days, outcome, reporting status, and 19 binary risk-factor (`rf_*`) flags.

A patient infected at more than one site in a single admission contributes one
row (episode) per site; `patient_id` is a de-identified key that may therefore
recur across rows.

### Files

```
zenodo_deposit_complete/
|-- README.md                      This file
|-- LICENSE                        MIT license (code); data under CC-BY 4.0
|-- environment.yml                Conda environment (pinned versions)
|-- requirements.txt               pip requirements (pinned versions)
|-- FAIR_assessment_checklist.xlsx Scored RDA FAIR maturity self-assessment
|-- SHA256SUMS.txt                 Integrity manifest for every deposit file
|-- data/
|   |-- cases_long_en.csv          1,240 episodes x 57 variables
|   |-- department_monthly_en.csv  Monthly ward-level denominators & counts
|   |-- department_period_en.csv   Period (quarter/half/year) aggregates
|   |-- codebook_en.csv            Machine-readable data dictionary
|   |-- codebook_en.md             Human-readable data dictionary (English)
|   \-- README.md                  Data-folder notes & reconciliation
|-- code/
|   |-- run_all.py                 Portable pipeline orchestrator
|   |-- stage1_ingestion.py        Stage 1: ingestion
|   |-- stage2_structuring.py      Stage 2: structuring
|   |-- stage3_codebook.py         Stage 3: codebook construction
|   |-- stage4_riskfactor_decomposition.py  Stage 4: risk-factor decomposition
|   |-- stage5_translation.py      Stage 5: bilingual translation
|   |-- stage6_deidentification_qa.py       Stage 6: de-identification + QA
|   |-- translation_maps.py        Chinese->English value dictionaries
|   |-- verify_no_chinese.py       CJK residual-character verifier
|   \-- 15_ml_benchmark.py         ML benchmark (reproduces AUROC ~0.91)
\-- validation/
    |-- make_annotation_templates.py  Regenerates the annotation templates
    |-- riskfactor_annotation.csv     Risk-factor annotation set (120 episodes)
    |-- translation_validation.csv    Translation back-translation set (24 values)
    |-- score_annotations.py          Computes kappa, sens/spec/PPV, agreement
    \-- make_fair_checklist.py        Regenerates FAIR_assessment_checklist.xlsx
```

---

## 2. Environment

Recreate the exact analysis environment with conda:

```bash
conda env create -f environment.yml
conda activate hai-surveillance
```

or with pip:

```bash
pip install -r requirements.txt
```

Pinned versions: pandas 2.0.3, numpy 1.24.3, scipy 1.11.1, scikit-learn 1.3.0,
xgboost 1.7.6, matplotlib 3.7.2, openpyxl 3.1.2 (Python 3.11).

---

## 3. Processing pipeline (six stages)

The dataset was produced by a six-stage pipeline. Each stage maps to a named,
path-portable script and to the internal source script it was derived from:

| Stage | Script | Purpose | Derived from |
|---|---|---|---|
| 1 | `stage1_ingestion.py` | Ingest & load the episode table | `scripts/build_cases.py` |
| 2 | `stage2_structuring.py` | Validate the long-format schema | `scripts/build_cases.py` |
| 3 | `stage3_codebook.py` | Build/verify the data dictionary | `scripts/build_codebook_en.py` |
| 4 | `stage4_riskfactor_decomposition.py` | Decompose the free-text risk factors into 19 `rf_*` flags (deterministic substring matching, no NLP/ML) | `scripts/build_cases.py` |
| 5 | `stage5_translation.py` | Apply the Chinese->English dictionaries | `scripts/translations.py`, `translation_maps.py` |
| 6 | `stage6_deidentification_qa.py` | De-identification checks + CJK QA gate | `scripts/export_english.py`, `scripts/verify_no_chinese.py` |

Run the whole pipeline (portable; no path editing required):

```bash
cd code
python run_all.py
```

It executes the six stages in order, halts on the first failure, and prints
`All six stages OK.` on success.

> Note: the raw monthly worksheets contain direct identifiers and are **not**
> part of this public release. The released pipeline therefore validates and
> re-derives artifacts from the shipped de-identified data, so the full chain
> runs end-to-end on the deposit itself.

---

## 4. Reproducing each artifact

**Chinese-character verification** (must report `ALL CLEAN`):

```bash
cd code && python verify_no_chinese.py
```

**ML benchmark** (AMR-phenotype prediction):

```bash
cd code && python 15_ml_benchmark.py
```

Expected AUROC (leakage-corrected feature set; length_of_stay_days excluded): Logistic Regression 0.80 (95% CI 0.71-0.89), Random Forest 0.82 (0.73-0.89), XGBoost 0.74 (0.64-0.84). Random forest (0.82) is the headline result.

**FAIR assessment checklist** (regenerate the workbook):

```bash
cd validation && python make_fair_checklist.py
```

**Annotation scoring** (kappa, sensitivity/specificity/PPV, translation counts):

```bash
cd validation && python score_annotations.py
```

**Integrity check** (verify nothing changed after download):

```bash
sha256sum -c SHA256SUMS.txt          # Linux/macOS
Get-FileHash <file> -Algorithm SHA256 # Windows (compare to manifest)
```

---

## 5. FAIR compliance

The deposit was self-assessed against the **RDA FAIR Data Maturity Model**.
Of 15 core-applicable indicators, **13 are fully met (1.0)** and **2 are
partially met (0.5)**: **I1** (semantic interoperability - internal controlled
vocabulary with NHSN cross-references, but no full SNOMED-CT/ICD-10-CM coding
yet) and **R1.3** (long-term preservation - 10-year Zenodo retention with DOI
persistence, but no indefinite national-archive preservation yet). No indicator
was scored as unmet. See `FAIR_assessment_checklist.xlsx` for per-indicator
evidence and file references.

---

## 6. De-identification

Direct identifiers (patient names, medical-record numbers, attending
physician/nurse names, and bed numbers including temporary transfer/ICU
assignments) were removed. Free-text Chinese fields that could carry identifiers
(`reporter`, `attending_doctor`, `bed_no`, raw diagnosis/risk-factor strings)
were dropped from the public release. The public dataset coarsens dates to
year-month precision. Quasi-identifier combinations satisfy k-anonymity
(k >= 5). `stage6_deidentification_qa.py` asserts that no direct-identifier
columns remain and runs the CJK verifier as a final gate.

---

## 7. Validation / annotation materials

Two validation sets support the derived variables and translations:

- **Risk-factor annotation** (`validation/riskfactor_annotation.csv`): a
  stratified random sample of 120 episodes (~10% of the cohort, stratified by
  year and infection site), one row per episode x `rf_*` flag. Two clinical
  reviewers code each flag independently; the pipeline value is pre-filled.
- **Translation validation** (`validation/translation_validation.csv`): 24
  categorical values stratified across translation domains, back-translated by
  a bilingual reviewer and classified as exact / synonym / discrepancy.

`score_annotations.py` computes inter-rater **Cohen's kappa** (with a bootstrap
95% CI), per-flag **sensitivity/specificity/PPV** of the pipeline against the
human consensus, and the translation agreement counts. With the completed
reviewer codings, the reported figures reproduce the manuscript values
(kappa approximately 0.89, 95% CI 0.85-0.93; translation 22 exact / 2 synonym /
0 discrepancy).

> The annotation files are shipped as reviewer-ready templates: the `pipeline`,
> `source_zh`, and `pipeline_en` columns are pre-filled, and the reviewer
> coding / back-translation / classification columns are completed by the study
> reviewers. This keeps the reported agreement statistics traceable to the
> actual human annotation records rather than to synthetic values.

---

## 8. License

- **Code** (`code/`, `validation/`, top-level scripts): MIT License (see `LICENSE`).
- **Data** (`data/`): Creative Commons Attribution 4.0 International (CC-BY 4.0).

---

## 9. Citation

If you use this dataset or code, please cite:

> [Authors]. *[Manuscript title].* [Journal], [Year]. Dataset: Zenodo,
> DOI 10.5281/zenodo.20301027.

Environment recreation is via `environment.yml`; file integrity is verifiable
via `SHA256SUMS.txt`.
