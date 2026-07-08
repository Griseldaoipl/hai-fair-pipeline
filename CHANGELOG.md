# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Each tagged release is archived to Zenodo with its own version DOI; the concept
DOI always resolves to the latest version. Backward-incompatible changes to the
dataset schema are reserved for major versions and recorded here.

## [1.1.0](https://github.com/Griseldaoipl/hai-fair-pipeline/releases/tag/v1.1.0) — 2026-07-08

Leakage-corrected release accompanying the CSBJ revision.
Zenodo DOI: 10.5281/zenodo.20725167

### Fixed

* Removed total length of stay (an admission-to-discharge variable not available
at the prediction timepoint) from the antimicrobial-resistance benchmark feature
set, eliminating post-outcome information leakage. Corrected discrimination:
logistic regression AUROC 0.80, random forest 0.82, XGBoost 0.74.

### Added

* Completed FAIR Data Maturity Model assessment (`FAIR\_assessment\_checklist.xlsx`)
and an independent automated F-UJI report.
* Per-flag risk-factor validation results and scoring script.
* Model calibration outputs (reliability curves and Brier scores).
* `Dockerfile` and continuous-integration workflow (`.github/workflows/ci.yml`)
for containerised, regression-tested reproduction.
* `environment.yml` (conda) alongside the pinned `requirements.txt`.

### Changed

* Public-release dates coarsened to year-month precision for k-anonymity (k>=5).
* Expanded machine-readable codebook and README.

## [1.0.0](https://github.com/Griseldaoipl/hai-fair-pipeline/releases/tag/v1.0.0) — 2026-07-08

Initial public release of the dataset and pipeline.
Zenodo DOI: 10.5281/zenodo.20301027

### Added

* First public, FAIR-compliant, patient-level HAI surveillance dataset
(1,240 episodes, 57 variables) from a Chinese district-level hospital.
* Reproducible six-stage bilingual data pipeline with the `run\_all.py` driver,
bilingual codebook, translation dictionaries, and de-identification module.

