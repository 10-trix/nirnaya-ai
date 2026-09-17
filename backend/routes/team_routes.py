from collections import Counter
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.db import get_db
from backend.database.models import Employee
from backend.schemas import TeamRiskSummaryResponse, CommonRiskFactor

router = APIRouter(prefix="/teams", tags=["Team Risk Rollup"])

@router.get("/{department}/risk-summary", response_model=TeamRiskSummaryResponse)
def get_team_risk_summary(department: str, db: Session = Depends(get_db)):
    """
    Get aggregated risk summary for a department, including counts of at-risk employees,
    risk level breakdown, and top common risk factors across team members.
    """
    employees = db.query(Employee).filter(Employee.department.ilike(department)).all()
    if not employees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No employees found for department '{department}'"
        )

    total_employees = len(employees)
    high_count = sum(1 for e in employees if e.riskLevel == "High")
    medium_count = sum(1 for e in employees if e.riskLevel == "Medium")
    low_count = sum(1 for e in employees if e.riskLevel == "Low")
    at_risk_employees = [e for e in employees if e.riskLevel in ["High", "Medium"] or (e.riskScore and e.riskScore >= 0.4)]
    at_risk_count = len(at_risk_employees)

    # Collect and count all reasons/risk factors from at-risk employees
    reason_counter = Counter()
    for emp in at_risk_employees:
        if emp.reasons:
            for reason in emp.reasons:
                reason_counter[reason] += 1

    top_factors = [
        CommonRiskFactor(factor=factor, count=count)
        for factor, count in reason_counter.most_common(5)
    ]

    # Build natural language summary statement
    if at_risk_count == 0:
        summary = f"The {department} team is performing well with 0 at-risk employees out of {total_employees} members."
    else:
        main_driver_str = ""
        if top_factors:
            main_driver_str = f" Common factor: {top_factors[0].factor} ({top_factors[0].count} employees affected)."
        summary = (
            f"{at_risk_count} out of {total_employees} employees in {department} are currently at-risk "
            f"({high_count} High, {medium_count} Medium).{main_driver_str}"
        )

    return TeamRiskSummaryResponse(
        department=department,
        total_employees=total_employees,
        at_risk_count=at_risk_count,
        high_risk_count=high_count,
        medium_risk_count=medium_count,
        low_risk_count=low_count,
        common_risk_factors=top_factors,
        summary=summary
    )
