"""
ML Benchmark - CORRECTED VERSION (No Data Leakage)
Removes length_of_stay_days to prevent using future information
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score, RocCurveDisplay
from sklearn.utils import resample
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

# Portable: paths resolved relative to this script's location in the deposit.
HERE = Path(__file__).resolve().parent
DEPOSIT = HERE.parent
IN = DEPOSIT / "data"
OUT = HERE / "out"
OUT.mkdir(parents=True, exist_ok=True)

SEED = 42
TEST_SIZE = 0.2
N_BOOTSTRAP = 200
np.random.seed(SEED)

cases = pd.read_csv(IN / "cases_long_en.csv")

# ===== CORRECTED FEATURE SET (NO length_of_stay_days) =====
rf_cols = [c for c in cases.columns if c.startswith("rf_")]
FEATURE_COLS = ["age_years", "sex", "days_to_infection", "infection_dept"] + rf_cols

def prepare_features(df, feature_cols):
    X = df[feature_cols].copy()
    for col in X.select_dtypes(include=[np.number]).columns:
        X[col] = X[col].fillna(X[col].median())
    X["sex"] = (X["sex"] == "M").astype(int)
    top_depts = X["infection_dept"].value_counts().head(10).index
    X["infection_dept"] = X["infection_dept"].where(X["infection_dept"].isin(top_depts), "Other")
    X = pd.get_dummies(X, columns=["infection_dept"], drop_first=True)
    return X

def bootstrap_metrics(y_true, y_pred, y_prob, n_iter=N_BOOTSTRAP):
    aurocs, f1s, accs = [], [], []
    for _ in range(n_iter):
        idx = resample(np.arange(len(y_true)), random_state=np.random.randint(0, 100000))
        if len(np.unique(y_true[idx])) < 2:
            continue
        accs.append(accuracy_score(y_true[idx], y_pred[idx]))
        f1s.append(f1_score(y_true[idx], y_pred[idx], average="macro"))
        try:
            aurocs.append(roc_auc_score(y_true[idx], y_prob[idx]))
        except ValueError:
            pass

    def ci(arr):
        return np.mean(arr), np.percentile(arr, 2.5), np.percentile(arr, 97.5)
    return ci(aurocs), ci(f1s), ci(accs)

# AMR Prediction
def has_resistance(p):
    if pd.isna(p):
        return np.nan
    return int(any(m in str(p) for m in ["(CRAB)", "(CRKP)", "(CRPA)", "(CRE)", "(MRSA)"]))

cases["any_resistant"] = cases["pathogen"].apply(has_resistance)
df_amr = cases[cases["any_resistant"].notna() & (cases["micro_positive"] == 1)].copy()
df_amr["any_resistant"] = df_amr["any_resistant"].astype(int)

X_amr = prepare_features(df_amr, FEATURE_COLS)
y_amr = df_amr["any_resistant"].values

X_train, X_test, y_train, y_test = train_test_split(
    X_amr, y_amr, test_size=TEST_SIZE, random_state=SEED, stratify=y_amr
)

amr_imbalance = np.bincount(y_train).max() / np.bincount(y_train).min()

models = {
    "Logistic Regression": LogisticRegression(max_iter=5000, random_state=SEED, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=SEED, class_weight="balanced"),
}
if HAS_XGB:
    models["XGBoost"] = XGBClassifier(n_estimators=200, random_state=SEED, verbosity=0)

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    auroc = roc_auc_score(y_test, y_prob)
    f1 = f1_score(y_test, y_pred, average="macro")
    acc = accuracy_score(y_test, y_pred)

    auroc_ci, f1_ci, acc_ci = bootstrap_metrics(y_test, y_pred, y_prob)

    results.append({
        "Model": name,
        "AUROC": f"{auroc:.3f} ({auroc_ci[1]:.3f}-{auroc_ci[2]:.3f})",
        "F1-macro": f"{f1:.3f} ({f1_ci[1]:.3f}-{f1_ci[2]:.3f})",
        "Accuracy": f"{acc:.3f} ({acc_ci[1]:.3f}-{acc_ci[2]:.3f})",
    })
    print(f"{name}: AUROC={auroc:.3f}, F1={f1:.3f}, Acc={acc:.3f}")

df_results = pd.DataFrame(results)
df_results.to_csv(OUT / "ml_benchmark_results_corrected.csv", index=False)

# Generate Figure 4
fig, ax = plt.subplots(1, 1, figsize=(6, 5), dpi=300)
for name, model in models.items():
    model.fit(X_train, y_train)
    RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax, name=name)

ax.plot([0, 1], [0, 1], "k--", lw=1, label="Chance")
ax.set_title("AMR Phenotype Prediction — ROC Curves")
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.legend(loc="lower right")
plt.tight_layout()
fig.savefig(OUT / "figure4_roc_curves_corrected.tif", dpi=300, bbox_inches="tight")
plt.close()

print(f"\n✓ Results saved: {OUT / 'ml_benchmark_results_corrected.csv'}")
print(f"✓ Figure saved: {OUT / 'figure4_roc_curves_corrected.tif'}")
