import os
import joblib
import pandas as pd
import shap

# ── Setup: runs once when this file is imported ──────────────────────────

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "risk_model.pkl")

model = joblib.load(MODEL_PATH)
explainer = shap.TreeExplainer(model)

FEATURES = [
    "tenure_months",
    "engagement_score",
    "time_since_promotion_months",
    "overtime_hours",
    "JobLevel",
    "WorkLifeBalance"
]

# ── Helper: risk level bucket from the raw score ──────────────────────────

def get_risk_level(score: float) -> str:
    if score >= 0.7:
        return "High"
    elif score >= 0.4:
        return "Medium"
    return "Low"


# ── Helper: turns a feature + value into a detailed, human sentence ──────
# Each entry has multiple severity tiers so the wording actually reflects
# how bad/good the number is, not just a generic template.

def translate_to_plain_english(feature, actual_value, direction):
    """
    direction: 'risk' (this factor is pushing risk up)
               'protective' (this factor is pushing risk down)
    """

    if feature == "engagement_score":
        if direction == "risk":
            if actual_value <= 1:
                return f"Very low engagement score ({actual_value}/4) — signals real disengagement from day-to-day work"
            return f"Below-average engagement score ({actual_value}/4)"
        return f"Healthy engagement score ({actual_value}/4) — genuinely invested in the role"

    if feature == "time_since_promotion_months":
        if direction == "risk":
            if actual_value >= 24:
                return f"No promotion in {actual_value} months — well past the typical growth window"
            return f"No promotion in {actual_value} months"
        return f"Promoted recently ({actual_value} months ago) — career progression feels active"

    if feature == "overtime_hours":
        if direction == "risk":
            return "Regularly working overtime — a known early indicator of burnout"
        return "Not working excessive overtime — healthy workload balance"

    if feature == "tenure_months":
        if direction == "risk":
            if actual_value <= 12:
                return f"Still very new ({actual_value} months) — early tenure carries naturally higher flight risk"
            return f"Relatively short tenure ({actual_value} months)"
        return f"Solid tenure ({actual_value} months) — has built roots at the company"

    if feature == "JobLevel":
        if direction == "risk":
            return f"Lower job level ({actual_value}) — may feel limited growth headroom"
        return f"Established job level ({actual_value})"

    if feature == "WorkLifeBalance":
        if direction == "risk":
            return f"Poor work-life balance rating ({actual_value}/4)"
        return f"Good work-life balance rating ({actual_value}/4)"

    return f"{feature} = {actual_value}"


# ── Helper: splits SHAP output into risk-increasing vs protective factors ─

def explain_prediction(sample_row, shap_vals, feature_names, top_n=4):
    impact = list(zip(feature_names, shap_vals[0]))
    impact.sort(key=lambda x: abs(x[1]), reverse=True)

    risk_factors = []
    protective_factors = []

    for feature, value in impact[:top_n]:
        actual_value = sample_row[feature].values[0]
        if value > 0:
            risk_factors.append(translate_to_plain_english(feature, actual_value, "risk"))
        else:
            protective_factors.append(translate_to_plain_english(feature, actual_value, "protective"))

    return risk_factors, protective_factors


# ── Helper: builds one natural-language summary sentence ─────────────────

def build_summary(risk_level, score, risk_factors):
    pct = int(score * 100)
    if risk_level == "High":
        opener = f"High risk of leaving ({pct}% likelihood)."
    elif risk_level == "Medium":
        opener = f"Moderate risk of leaving ({pct}% likelihood)."
    else:
        opener = f"Low risk of leaving ({pct}% likelihood)."

    if risk_factors:
        opener += f" Main driver: {risk_factors[0].lower()}."
    return opener


# ── Main function: this is what the backend calls ────────────────────────

def get_risk_prediction(employee_data: dict):
    """
    Takes a dict like:
    {
        "tenure_months": 6,
        "engagement_score": 1,
        "time_since_promotion_months": 24,
        "overtime_hours": 1,
        "JobLevel": 1,
        "WorkLifeBalance": 1
    }

    Returns:
    {
        "riskScore": 0.81,
        "riskLevel": "High",
        "summary": "High risk of leaving (81% likelihood). Main driver: very low engagement score (1/4)...",
        "reasons": ["Very low engagement score (1/4) — signals real disengagement...", ...],
        "protectiveFactors": ["Solid tenure (36 months) — has built roots at the company"]
    }
    """
    df_input = pd.DataFrame([employee_data])

    risk_score = float(model.predict_proba(df_input)[0][1])
    risk_level = get_risk_level(risk_score)

    shap_vals = explainer.shap_values(df_input)
    risk_factors, protective_factors = explain_prediction(df_input, shap_vals, FEATURES)

    summary = build_summary(risk_level, risk_score, risk_factors)

    return {
        "riskScore": round(risk_score, 2),
        "riskLevel": risk_level,
        "summary": summary,
        "reasons": risk_factors,
        "protectiveFactors": protective_factors
    }