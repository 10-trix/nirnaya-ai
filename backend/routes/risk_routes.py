from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.database.models import Employee
from backend.models.risk_model import get_risk_prediction
from backend.schemas import EmployeeResponse, MitigationRequest, MitigationResponse

router = APIRouter(prefix="/risk", tags=["Risk Reasoning"])

@router.get("/{employeeId}", response_model=EmployeeResponse)
def compute_and_get_employee_risk(employeeId: str, db: Session = Depends(get_db)):
    """
    Fetch employee from DB, compute XGBoost risk prediction + SHAP explainability,
    persist risk fields back to DB, and return merged record.
    """
    employee = db.query(Employee).filter(Employee.id == employeeId).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id '{employeeId}' not found"
        )

    # Format input feature dictionary for XGBoost ML model
    feature_data = {
        "tenure_months": int(employee.tenure_months or 0),
        "engagement_score": float(employee.engagement_score if employee.engagement_score is not None else 3.0),
        "time_since_promotion_months": int(employee.time_since_promotion_months or 0),
        "overtime_hours": float(employee.overtime_hours if employee.overtime_hours is not None else 0.0),
        "JobLevel": int(employee.JobLevel or 1),
        "WorkLifeBalance": int(employee.WorkLifeBalance or 3)
    }

    # Call ML prediction model from backend/models/risk_model.py
    prediction = get_risk_prediction(feature_data)

    # Update database record with computed risk metrics
    employee.riskScore = prediction.get("riskScore", 0.0)
    employee.riskLevel = prediction.get("riskLevel", "Low")
    employee.summary = prediction.get("summary", "")
    employee.reasons = prediction.get("reasons", [])
    employee.protectiveFactors = prediction.get("protectiveFactors", [])

    db.commit()
    db.refresh(employee)
    return employee


@router.post("/{employeeId}/mitigation", response_model=MitigationResponse)
def get_risk_mitigation(employeeId: str, body: MitigationRequest = None, db: Session = Depends(get_db)):
    """
    Risk Mitigation Endpoint (Placeholder).
    Currently returns the employee's existing recommendedAction field or a standard action plan.
    """
    employee = db.query(Employee).filter(Employee.id == employeeId).first()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id '{employeeId}' not found"
        )

    # TODO: GenAI teammate will replace this body with a call to backend/genai/mitigation.py
    # Example integration line when ready:
    # recommended_action = generate_mitigation_plan(employee_id=employeeId, context=body.context if body else None)
    
    action = employee.recommendedAction
    if not action:
        if employee.riskLevel == "High":
            action = f"Schedule immediate 1-on-1 with {employee.name}, evaluate career path promotion options, and rebalance overtime workload."
        elif employee.riskLevel == "Medium":
            action = f"Conduct quarterly check-in with {employee.name} to discuss growth milestones and workload balance."
        else:
            action = f"Maintain regular check-ins and support current project initiatives for {employee.name}."

    return MitigationResponse(
        employee_id=employee.id,
        recommendedAction=action,
        status="success",
        note="Placeholder response. GenAI teammate will connect backend/genai/mitigation.py"
    )
