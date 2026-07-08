"""All Chinese -> English translation dictionaries used for the English export.

Every distinct value seen in the cleaned files is covered. If a new value
appears later, the build script will raise so it can be added here.
"""

# --------------------------------------------------------------------------
# Departments (clinical wards)
# Used by: admission_dept / infection_dept / current_dept / discharge_dept /
#          reporting_dept / department (in summary files)
# --------------------------------------------------------------------------
DEPT = {
    "中医科病区":               "TCM Ward",
    "中医肛肠科病区":           "TCM Anorectal Surgery Ward",
    "乳腺甲状腺外科病区":       "Breast & Thyroid Surgery Ward",
    "产科病区":                 "Obstetrics Ward",
    "儿科病区":                 "Paediatrics Ward",
    "全科医学科病区":           "General Practice Ward",
    "全院":                     "Hospital-wide",
    "内分泌科病区":             "Endocrinology Ward",
    "呼吸与危重症医学科一病区": "Respiratory & Critical Care Ward 1",
    "呼吸与危重症医学科二病区": "Respiratory & Critical Care Ward 2",
    "呼吸与危重症医学科监护病房": "Respiratory & Critical Care ICU",
    "妇科病区":                 "Gynaecology Ward",
    "康复医学科病区":           "Rehabilitation Medicine Ward",
    "心血管内科一病区":         "Cardiology Ward 1",
    "心血管内科二病区":         "Cardiology Ward 2",
    "感染性疾病科病区":         "Infectious Diseases Ward",
    "新生儿病区":               "Neonatology Ward",
    "普通外科一病区":           "General Surgery Ward 1",
    "泌尿外科病区":             "Urology Ward",
    "消化内科病区":             "Gastroenterology Ward",
    "烧伤整形外科病区":         "Burn & Plastic Surgery Ward",
    "眼科病区":                 "Ophthalmology Ward",
    "神经内科一病区":           "Neurology Ward 1",
    "神经内科二病区":           "Neurology Ward 2",
    "神经外科病区":             "Neurosurgery Ward",
    "老年医学科":               "Geriatrics Ward",
    "老年医学科病区":           "Geriatrics Ward",
    "耳鼻咽喉科病区":           "ENT Ward",
    "肝胆外科病区":             "Hepatobiliary Surgery Ward",
    "肾脏内科":                 "Nephrology Ward",
    "肾脏内科病区":             "Nephrology Ward",
    "肿瘤科一病区":             "Oncology Ward 1",
    "肿瘤科二病区":             "Oncology Ward 2",
    "胸心外科":                 "Cardiothoracic Surgery Ward",
    "胸心外科病区":             "Cardiothoracic Surgery Ward",
    "血液内科":                 "Haematology Ward",
    "血液内科病区":             "Haematology Ward",
    "血液透析室":               "Haemodialysis Unit",
    "重症医学科":               "Intensive Care Unit",
    "重症医学科病区":           "Intensive Care Unit",
    "骨科一病区":               "Orthopaedics Ward 1",
    "骨科二病区":               "Orthopaedics Ward 2",
    "骨科三病区":               "Orthopaedics Ward 3",
    "骨科四病区":               "Orthopaedics Ward 4",
    "骨科创伤病区":             "Orthopaedic Trauma Ward",
    "骨科病区(三)":             "Orthopaedics Ward 3",
    "CCU":                      "Coronary Care Unit",
}


# --------------------------------------------------------------------------
# Infection sites (raw value of the 'infection_site' column in cases_long)
# --------------------------------------------------------------------------
INFECTION_SITE = {
    "上呼吸道感染":           "Upper respiratory tract infection",
    "下呼吸道感染":           "Lower respiratory tract infection",
    "中枢神经系统":           "Central nervous system infection",
    "其它部位感染":           "Other site",
    "口腔真菌感染":           "Oral fungal infection",
    "呼吸机相关肺炎":         "Ventilator-associated pneumonia",
    "器官(或腔隙)感染":       "Organ/space SSI",
    "外阴切口感染":           "Perineal incision infection",
    "导尿管相关尿路感染":     "Catheter-associated UTI",
    "导管相关尿路感染":       "Catheter-associated UTI",
    "导管相关血流感染":       "Catheter-associated BSI",
    "心肌炎或心包炎":         "Myocarditis or pericarditis",
    "感染性腹泻":             "Infectious diarrhoea",
    "抗菌药物相关性腹泻":     "Antibiotic-associated diarrhoea",
    "椎管内感染":             "Spinal canal infection",
    "泌尿道感染":             "Urinary tract infection",
    "深部手术切口感染":       "Deep surgical site infection",
    "烧伤感染":               "Burn-wound infection",
    "男女性生殖道的其它感染": "Other genital tract infection",
    "皮肤感染":               "Skin infection",
    "细菌性脑膜炎、脑室炎":   "Bacterial meningitis/ventriculitis",
    "胃肠道感染":             "Gastrointestinal infection",
    "腹(盆)腔内组织感染":     "Intra-abdominal/pelvic tissue infection",
    "腹水感染":               "Ascites infection",
    "血流感染(与导管无关)":   "Non-catheter bloodstream infection",
    "血流感染（与导管无关）": "Non-catheter bloodstream infection",
    "血管导管相关血流感染":   "Vascular catheter-associated BSI",
    "表浅手术切口感染":       "Superficial surgical site infection",
    "败血症":                 "Septicaemia",
    "软组织感染":             "Soft tissue infection",
    "软组织感染（急诊科清创）": "Soft tissue infection (ED debridement)",
    "阴道穹隆部感染":         "Vaginal cuff infection",
    "颅内脓肿":               "Intracranial abscess",
    "骨髓炎":                 "Osteomyelitis",
}


# --------------------------------------------------------------------------
# Specimen types
# --------------------------------------------------------------------------
SPECIMEN = {
    "中段尿":         "Midstream urine",
    "伤口分泌物":     "Wound discharge",
    "伤口渗出物":     "Wound exudate",
    "关节腔积液":     "Joint fluid",
    "分泌物":         "Discharge",
    "口腔拭子":       "Oral swab",
    "咽拭子":         "Throat swab",
    "大便":           "Stool",
    "导管头":         "Catheter tip",
    "导管尖端":       "Catheter tip",
    "导管血":         "Catheter blood",
    "尿液":           "Urine",
    "引流液":         "Drainage fluid",
    "渗出液":         "Exudate",
    "痰液":           "Sputum",
    "痰液（深部）":   "Sputum (deep)",
    "肺泡灌洗液":     "Bronchoalveolar lavage",
    "胆汁":           "Bile",
    "胸水":           "Pleural fluid",
    "脑脊液":         "Cerebrospinal fluid",
    "脓液":           "Pus",
    "腹水":           "Ascitic fluid",
    "血液":           "Blood",
    "血清":           "Serum",
    "静脉血":         "Venous blood",
}


# --------------------------------------------------------------------------
# Pathogens
# --------------------------------------------------------------------------
PATHOGEN = {
    "中间链球菌":               "Streptococcus intermedius",
    "产吲哚金黄杆菌":           "Chryseobacterium indologenes",
    "产气肠杆菌":               "Klebsiella aerogenes",
    "人葡萄球菌":               "Staphylococcus hominis",
    "假单胞菌属":               "Pseudomonas spp.",
    "停乳链球菌停乳亚种":       "Streptococcus dysgalactiae subsp. dysgalactiae",
    "光滑假丝酵母":             "Candida glabrata",
    "光滑假丝酵母菌":           "Candida glabrata",
    "光滑念珠菌":               "Candida glabrata",
    "克柔假丝酵母":             "Candida krusei",
    "克氏柠檬酸杆菌":           "Citrobacter koseri",
    "卡他莫拉（布兰汉）菌":     "Moraxella catarrhalis",
    "卡它莫拉菌":               "Moraxella catarrhalis",
    "口腔链球菌":               "Streptococcus oralis",
    "咽峡炎链球菌":             "Streptococcus anginosus",
    "嗜水气单胞菌":             "Aeromonas hydrophila",
    "嗜麦芽窄食单胞菌":         "Stenotrophomonas maltophilia",
    "大肠埃希菌":               "Escherichia coli",
    "大肠埃希菌(CRE-Eco)":      "Escherichia coli (CRE)",
    "头状葡萄球菌":             "Staphylococcus capitis",
    "奇异变形杆菌":             "Proteus mirabilis",
    "奇异变形菌":               "Proteus mirabilis",
    "奇异变形菌(CRE)":          "Proteus mirabilis (CRE)",
    "季也蒙假丝酵母":           "Candida guilliermondii",
    "屎肠球菌":                 "Enterococcus faecium",
    "弗氏柠檬酸杆菌":           "Citrobacter freundii",
    "拟平滑念珠菌":             "Candida parapsilosis complex",
    "摩氏摩根菌":               "Morganella morganii",
    "斯氏普罗威登斯菌":         "Providencia stuartii",
    "无乳链球菌":               "Streptococcus agalactiae",
    "无菌生长":                 "No growth",
    "普城沙雷菌":               "Serratia plymuthica",
    "松鼠葡萄球菌":             "Staphylococcus sciuri",
    "洋葱伯克霍尔德菌":         "Burkholderia cepacia",
    "流感嗜血杆菌":             "Haemophilus influenzae",
    "海藻希瓦菌":               "Shewanella algae",
    "溶血葡萄球菌":             "Staphylococcus haemolyticus",
    "热带假丝酵母":             "Candida tropicalis",
    "热带假丝酵母菌":           "Candida tropicalis",
    "热带念珠菌":               "Candida tropicalis",
    "琼氏不动杆菌":             "Acinetobacter junii",
    "白假丝酵母菌":             "Candida albicans",
    "白色假丝酵母":             "Candida albicans",
    "白色念珠菌":               "Candida albicans",
    "皮特不动杆菌":             "Acinetobacter pittii",
    "科氏葡萄球菌":             "Staphylococcus cohnii",
    "粘质沙雷菌":               "Serratia marcescens",
    "粪肠球菌":                 "Enterococcus faecalis",
    "约氏不动杆菌":             "Acinetobacter johnsonii",
    "纹带棒杆菌ATCC BAA-1293":  "Corynebacterium striatum ATCC BAA-1293",
    "纹带棒状杆菌":             "Corynebacterium striatum",
    "缓慢葡萄球菌":             "Staphylococcus lentus",
    "肺炎克雷伯菌":             "Klebsiella pneumoniae",
    "肺炎克雷伯菌(CRKP)":       "Klebsiella pneumoniae (CRKP)",
    "肺炎克雷伯菌肺炎亚种":     "Klebsiella pneumoniae subsp. pneumoniae",
    "肺炎克雷伯菌肺炎亚种(CRKP)": "Klebsiella pneumoniae subsp. pneumoniae (CRKP)",
    "肺炎克雷伯菌臭鼻亚种":     "Klebsiella pneumoniae subsp. ozaenae",
    "肺炎链球菌":               "Streptococcus pneumoniae",
    "脆弱拟杆菌":               "Bacteroides fragilis",
    "脑膜脓毒性伊丽莎白金菌":   "Elizabethkingia meningoseptica",
    "表皮葡萄球菌":             "Staphylococcus epidermidis",
    "解脲棒状杆菌":             "Corynebacterium urealyticum",
    "解鸟氨酸拉乌尔菌":         "Raoultella ornithinolytica",
    "赫氏埃希菌":               "Escherichia hermannii",
    "路邓葡萄球菌":             "Staphylococcus lugdunensis",
    "近平滑假丝酵母":           "Candida parapsilosis",
    "近平滑假丝酵母菌":         "Candida parapsilosis",
    "酵母菌":                   "Yeast (unspeciated)",
    "金黄色葡萄球菌":           "Staphylococcus aureus",
    "金黄色葡萄球菌(MRSA)":     "Staphylococcus aureus (MRSA)",
    "铜绿假单胞菌":             "Pseudomonas aeruginosa",
    "铜绿假单胞菌(CRPA)":       "Pseudomonas aeruginosa (CRPA)",
    "阴沟/阿氏肠杆菌":          "Enterobacter cloacae complex",
    "阴沟/阿氏肠杆菌(CRE)":     "Enterobacter cloacae complex (CRE)",
    "阴沟肠杆菌复合菌":         "Enterobacter cloacae complex",
    "阿氏肠杆菌":               "Enterobacter asburiae",
    "非脱羧勒克菌":             "Leclercia adecarboxylata",
    "革兰阴性杆菌":             "Gram-negative bacilli",
    "鲍曼不动杆菌":             "Acinetobacter baumannii",
    "鲍曼不动杆菌(CRAB)":       "Acinetobacter baumannii (CRAB)",
    "鲍曼不动杆菌复合菌":       "Acinetobacter baumannii complex",
    "鲍曼不动杆菌复合菌(CRAB)": "Acinetobacter baumannii complex (CRAB)",
    "鸟肠球菌":                 "Enterococcus avium",
    "鼠伤寒沙门菌血清型":       "Salmonella enterica serovar Typhimurium",
}


# --------------------------------------------------------------------------
# Risk factors (tokens of the comma-separated list in 易感因素)
# All "其他(...)" variants are collapsed to "Other"
# --------------------------------------------------------------------------
RISK_FACTOR = {
    "中心置管":               "CVC",
    "低蛋白血症":             "Hypoalbuminaemia",
    "免疫功能缺陷":           "Immune deficiency",
    "免疫抑制剂":             "Immunosuppressants",
    "免疫抑制状态(放疗、免疫功能缺陷、激素治疗等)": "Immunosuppressed state",
    "其他":                   "Other",
    "内窥镜":                 "Endoscopy",
    "化疗":                   "Chemotherapy",
    "卧床":                   "Bedridden",
    "呼吸机":                 "Ventilator",
    "器官功能衰竭":           "Organ failure",
    "导尿管":                 "Urinary catheter",
    "年龄<=2":                "Age <= 2 yr",
    "年龄>70岁":              "Age > 70 yr",
    "年龄>=60":               "Age >= 60 yr",
    "年龄>=80岁":             "Age >= 80 yr",
    "恶性肿瘤":               "Malignancy",
    "放疗":                   "Radiotherapy",
    "新生儿":                 "Neonate",
    "既往手术史(无植入物30天内)": "Recent surgery <=30 d (no implant)",
    "既往手术史(植入物1年内)":   "Recent surgery <=1 y (with implant)",
    "激素治疗":               "Corticosteroids",
    "白细胞计数<1.5*10^9/L":  "WBC <1.5x10^9/L",
    "糖尿病":                 "Diabetes",
    "胸腔引流":               "Chest drain",
    "脑室引流":               "Ventricular drain",
    "脑血管意外":             "Stroke",
    "腹腔引流":               "Abdominal drain",
    "腹透":                   "Peritoneal dialysis",
    "营养不良":               "Malnutrition",
    "血小板减少":             "Thrombocytopenia",
    "血液系统疾病":           "Haematologic disease",
    "血透":                   "Haemodialysis",
    "贫血":                   "Anaemia",
    "长期卧床":               "Long-term bedridden",
    "高血压":                 "Hypertension",
}


# --------------------------------------------------------------------------
# Other categorical fields
# --------------------------------------------------------------------------
MICRO_TEST_STATUS = {
    "未送检":       "Not sent",
    "送检未出结果": "Pending",
    "送检阳性":     "Positive",
    "送检阴性":     "Negative",
}

OUTCOME = {
    "好转":   "Improved",
    "恶化":   "Worsened",
    "无变化": "Unchanged",
    "未转归": "Pending",
    "死亡":   "Died",
    "治愈":   "Cured",
}

REPORT_STATUS = {
    "正常": "On time",
    "漏报": "Missed (audit-detected)",
    "迟报": "Late",
}

INCISION_GRADE = {
    "Ⅰ类切口": "Class I (clean)",
    "Ⅱ类切口": "Class II (clean-contaminated)",
    "Ⅲ类切口": "Class III (contaminated)",
    "Ⅳ类切口": "Class IV (dirty)",
    "1":       "Class I (clean)",
    "2":       "Class II (clean-contaminated)",
    "3":       "Class III (contaminated)",
    "4":       "Class IV (dirty)",
}

SURGICAL_INFECTION = {
    "是": "Yes",
    "否": "No",
}

# Period labels in department_period.csv
PERIOD = {
    "上半年": "H1",
    "下半年": "H2",
}
