import os
import pandas as pd
import joblib
from xgboost import XGBClassifier

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "hr_data.csv")
MODEL_OUTPUT_PATH = os.path.join(BASE_DIR, "..", "backend", "models", "risk_model.pkl")

# Read dataset
df = pd.read_csv(CSV_PATH)

# Map dataset columns to risk model features
df["tenure_months"] = df["YearsAtCompany"] * 12
df["engagement_score"] = df["JobSatisfaction"]
df["time_since_promotion_months"] = df["YearsSinceLastPromotion"] * 12
df["overtime_hours"] = df["OverTime"].apply(lambda x: 15.0 if x == "Yes" else 0.0)
# JobLevel and WorkLifeBalance map directly

FEATURES = [
    "tenure_months",
    "engagement_score",
    "time_since_promotion_months",
    "overtime_hours",
    "JobLevel",
    "WorkLifeBalance"
]

X = df[FEATURES]
y = df["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)

# Train XGBoost Model
model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    random_state=42,
    eval_metric="logloss"
)
model.fit(X, y)

os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
joblib.dump(model, MODEL_OUTPUT_PATH)
print(f"Successfully trained and saved risk model to {os.path.abspath(MODEL_OUTPUT_PATH)}")
