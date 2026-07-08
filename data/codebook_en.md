# Data dictionary (codebook)

English-only data dictionary for the HAI surveillance deposit. The
machine-readable source of truth is `codebook_en.csv`. The complete
Chinese-to-English value crosswalk used during translation is provided
separately in `code/translation_maps.py`.

## `cases_long_en.csv`

| Variable | Type | Unit | Description | Allowed values |
|---|---|---|---|---|
| year | int | year | Calendar year of the source file (provenance) |  |
| month | int | month | Calendar month of the source file (1-12) |  |
| source_file | string |  | Provenance key in YYYY-MM form |  |
| case_seq | int |  | Row number inside the original Excel file |  |
| patient_id | string |  | De-identified hospital case-record number; same patient may appear on multiple rows when infected at multiple sites in one admission |  |
| sex | category |  | Patient sex | M \| F |
| age_years | float | years | Age in years; months/days converted (e.g. 11 mo -> 0.917; 2 d -> 0.005) |  |
| admission_date | date | ISO | Date of admission |  |
| discharge_date | date | ISO | Date of discharge |  |
| infection_date | date | ISO | Onset date used for HAI case definition |  |
| specimen_date | date | ISO | Date of specimen collection for microbiology |  |
| report_date | date | ISO | Date the case was reported in the registry |  |
| length_of_stay_days | int | days | discharge_date - admission_date |  |
| days_to_infection | int | days | infection_date - admission_date |  |
| admission_dept | category |  | Department on admission | see Department table |
| infection_dept | category |  | Department where the infection was attributed | see Department table |
| current_dept | category |  | Department at the time of reporting | see Department table |
| discharge_dept | category |  | Department of discharge | see Department table |
| reporting_dept | category |  | Department that filed the report | see Department table |
| infection_site | category |  | Anatomical site of infection (case definition) | see Infection-site table |
| specimen_type | string |  | Specimen(s) sent for culture; comma-separated when multiple | see Specimen table |
| micro_test_status | category |  | Microbiology testing outcome | Not sent \| Pending \| Positive \| Negative |
| micro_tested | bool | 0/1 | 1 if a culture was sent (Positive \| Negative \| Pending), 0 if Not sent |  |
| micro_positive | bool | 0/1 | 1 if Positive, 0 if Negative, NaN if Pending or Not sent |  |
| pathogen | string |  | Identified organism(s); comma-separated when multiple | see Pathogen table |
| incision_grade | category |  | Surgical wound class (when applicable) | Class I (clean) \| Class II (clean-contaminated) \| Class III (contaminated) \| Class IV (dirty) |
| surgical_infection | category |  | Whether the infection followed a surgical procedure | Yes \| No |
| surgical_infection_bool | bool | 0/1 | 1 if surgical_infection == Yes |  |
| n_surgeries | int | count | Number of surgical procedures during the admission |  |
| surgery_start | datetime | ISO | Surgery start time |  |
| surgery_end | datetime | ISO | Surgery end time |  |
| ventilator_days | int | days | Days on mechanical ventilation |  |
| urinary_catheter_days | int | days | Indwelling urinary-catheter days |  |
| cvc_days | int | days | Central venous catheter days |  |
| outcome | category |  | Clinical outcome | Cured \| Improved \| Unchanged \| Worsened \| Died \| Pending |
| report_status | category |  | Reporting status | On time \| Missed (audit-detected) \| Late |
| n_risk_factors | int | count | Number of comma-separated risk factors recorded |  |
| risk_factors | string |  | English comma-separated risk-factor list (use rf_* boolean flags below for analysis) | see Risk-factor table |
| rf_urinary_catheter | bool | 0/1 | Indwelling urinary catheter |  |
| rf_ventilator | bool | 0/1 | Mechanical ventilation |  |
| rf_cvc | bool | 0/1 | Central venous catheter |  |
| rf_bedridden | bool | 0/1 | Bedridden / long-term immobility |  |
| rf_diabetes | bool | 0/1 | Diabetes mellitus |  |
| rf_hypertension | bool | 0/1 | Hypertension |  |
| rf_malignancy | bool | 0/1 | Malignancy |  |
| rf_chemo | bool | 0/1 | Chemotherapy |  |
| rf_radio | bool | 0/1 | Radiotherapy |  |
| rf_steroid | bool | 0/1 | Corticosteroid therapy |  |
| rf_immunosuppression | bool | 0/1 | Immunosuppression |  |
| rf_age_over_70 | bool | 0/1 | Age > 70 years |  |
| rf_age_over_60 | bool | 0/1 | Age >= 60 years |  |
| rf_malnutrition | bool | 0/1 | Malnutrition |  |
| rf_low_albumin | bool | 0/1 | Hypoalbuminaemia |  |
| rf_anaemia | bool | 0/1 | Anaemia |  |
| rf_stroke | bool | 0/1 | Cerebrovascular accident / stroke |  |
| rf_copd | bool | 0/1 | COPD / chronic airway disease |  |
| rf_dialysis | bool | 0/1 | Haemodialysis |  |

## `department_monthly_en.csv`

| Variable | Type | Unit | Description | Allowed values |
|---|---|---|---|---|
| year | int | year | Calendar year |  |
| period | int | month | Calendar month (1-12) |  |
| year_month | string |  | YYYY-MM convenience key |  |
| source_file | string |  | Source provenance key (YYYY-MM) |  |
| department | category |  | Department / ward; 'Hospital-wide' = aggregate over all wards | see Department table |
| is_hospital_total | bool | 0/1 | 1 for the hospital-wide aggregate row, 0 for individual wards |  |
| n_inpatients | int | count | Concurrent inpatients during the period (denominator for incidence_pct) |  |
| patient_days | int | days | Total patient-days during the period. Available from 2024-01 onwards. |  |
| n_infected_patients | int | count | Number of unique patients with at least one new HAI |  |
| n_infection_episodes | int | count | Number of HAI episodes (one patient infected at 2 sites = 2 episodes) |  |
| incidence_pct | float | % | n_infected_patients / n_inpatients x 100 |  |
| episode_incidence_pct | float | % | n_infection_episodes / n_inpatients x 100 |  |
| incidence_per_1000_pd | float | per 1000 PD | n_infected_patients / patient_days x 1000 (2024-01+ only) |  |
| episode_incidence_per_1000_pd | float | per 1000 PD | n_infection_episodes / patient_days x 1000 (2024-01+ only) |  |
| n_underreported | int | count | Cases identified post hoc by audit |  |
| underreport_pct | float | % | n_underreported / n_infection_episodes x 100 |  |
| site_upper_resp | int | count | Upper respiratory tract infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_lower_resp | int | count | Lower respiratory tract infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_vap | int | count | Ventilator-associated pneumonia. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_myocarditis_pericarditis | int | count | Myocarditis or pericarditis. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_vascular_related | int | count | Vascular-access-related infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_septicaemia | int | count | Septicaemia. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_bsi_non_catheter | int | count | Non-catheter bloodstream infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_clabsi | int | count | Central-line-associated bloodstream infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_clabsi_episodes | int | count | CLABSI episode count when reported separately. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_infectious_diarrhoea | int | count | Infectious diarrhoea. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_gi | int | count | Gastrointestinal infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_aad | int | count | Antibiotic-associated diarrhoea. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_intraabdominal | int | count | Intra-abdominal/pelvic tissue infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_ascites | int | count | Ascites infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_meningitis_ventriculitis | int | count | Bacterial meningitis / ventriculitis. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_cns_other | int | count | Other CNS infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_intracranial_abscess | int | count | Intracranial abscess. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_spinal_canal | int | count | Spinal-canal infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_uti | int | count | Urinary tract infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_cauti | int | count | Catheter-associated urinary tract infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_ssi_superficial | int | count | Superficial surgical-site infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_ssi_deep | int | count | Deep surgical-site infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_ssi_deep_episodes | int | count | Deep SSI episode count when reported separately. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_ssi_organ_space | int | count | Organ/space surgical-site infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_ssi_organ_space_episodes | int | count | Organ/space SSI episode count. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_skin | int | count | Skin infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_soft_tissue | int | count | Soft-tissue infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_burn | int | count | Burn-wound infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_perineal_incision | int | count | Perineal incision infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_genital_other | int | count | Other genital tract infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_vaginal_cuff | int | count | Vaginal cuff infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_oral_fungal | int | count | Oral fungal infection. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_oral_fungal_episodes | int | count | Oral fungal infection episode count. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_osteomyelitis | int | count | Osteomyelitis. NaN means the column was absent from that month's source file (no cases of that site that month). |  |
| site_other | int | count | Other / unclassified site. NaN means the column was absent from that month's source file (no cases of that site that month). |  |

## `department_period_en.csv`

| Variable | Type | Unit | Description | Allowed values |
|---|---|---|---|---|
| year | int | year | Calendar year |  |
| period_type | category |  | Aggregation level | quarter \| halfyear \| year |
| period | string |  | Period label: 1-4 for quarters, H1/H2 for half-years, the year for annual |  |
| source_file | string |  | Provenance key (e.g. 2024-Q3, 2024-H1, 2025-Y) |  |
| department | category |  | Department; 'Hospital-wide' for the aggregate row | see Department table |
| is_hospital_total | bool | 0/1 | 1 if the row is the hospital-wide aggregate |  |
| (all other columns) | - | - | Same definitions as in department_monthly_en.csv (denominators and counts cover the whole period) |  |

