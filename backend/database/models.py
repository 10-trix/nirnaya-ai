import uuid
from sqlalchemy import Column, String, Integer, Float, JSON
from backend.database.db import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    department = Column(String, nullable=False)
    
    # ML Features
    tenure_months = Column(Integer, default=0)
    engagement_score = Column(Float, default=3.0)
    time_since_promotion_months = Column(Integer, default=0)
    overtime_hours = Column(Float, default=0.0)
    JobLevel = Column(Integer, default=1)
    WorkLifeBalance = Column(Integer, default=3)
    
    # Skills array stored as JSON
    skills = Column(JSON, default=list)
    
    # ML Risk Prediction Output
    riskScore = Column(Float, default=0.0)
    riskLevel = Column(String, default="Low")
    summary = Column(String, default="")
    reasons = Column(JSON, default=list)
    protectiveFactors = Column(JSON, default=list)
    
    # Risk Mitigation Action
    recommendedAction = Column(String, default="")
