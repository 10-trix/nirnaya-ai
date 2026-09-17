import uuid
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.database.db import SessionLocal, engine, Base
from backend.database.models import Employee
from backend.models.risk_model import get_risk_prediction

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing employees for clean seed
    db.query(Employee).delete()
    db.commit()

    demo_employees = [
        # Engineering Department
        {
            "id": "emp-eng-001",
            "name": "Aarav Sharma",
            "role": "Senior Software Engineer",
            "department": "Engineering",
            "tenure_months": 28,
            "engagement_score": 1.5,
            "time_since_promotion_months": 26,
            "overtime_hours": 18.0,
            "JobLevel": 2,
            "WorkLifeBalance": 1,
            "skills": ["Python", "FastAPI", "React", "PostgreSQL", "System Design"],
            "recommendedAction": "Offer expedited promotion evaluation to Tech Lead and enforce 40-hour weekly cap."
        },
        {
            "id": "emp-eng-002",
            "name": "Priya Patel",
            "role": "Full Stack Developer",
            "department": "Engineering",
            "tenure_months": 14,
            "engagement_score": 2.0,
            "time_since_promotion_months": 14,
            "overtime_hours": 12.0,
            "JobLevel": 1,
            "WorkLifeBalance": 2,
            "skills": ["TypeScript", "Node.js", "Docker", "GraphQL"],
            "recommendedAction": "Assign a senior mentor and adjust weekly sprint commitments."
        },
        {
            "id": "emp-eng-003",
            "name": "Rohan Gupta",
            "role": "Lead DevOps Engineer",
            "department": "Engineering",
            "tenure_months": 42,
            "engagement_score": 3.8,
            "time_since_promotion_months": 6,
            "overtime_hours": 4.0,
            "JobLevel": 3,
            "WorkLifeBalance": 3,
            "skills": ["Kubernetes", "AWS", "Terraform", "CI/CD"],
            "recommendedAction": "Maintain current development plan and involve in quarterly architecture reviews."
        },
        {
            "id": "emp-eng-004",
            "name": "Ananya Verma",
            "role": "Backend Engineer",
            "department": "Engineering",
            "tenure_months": 8,
            "engagement_score": 1.0,
            "time_since_promotion_months": 8,
            "overtime_hours": 20.0,
            "JobLevel": 1,
            "WorkLifeBalance": 1,
            "skills": ["Python", "Django", "Redis", "Microservices"],
            "recommendedAction": "Conduct immediate 1-on-1 career check-in and rebalance workload distribution."
        },

        # Sales Department
        {
            "id": "emp-sales-001",
            "name": "Vikram Singh",
            "role": "Enterprise Account Executive",
            "department": "Sales",
            "tenure_months": 36,
            "engagement_score": 1.2,
            "time_since_promotion_months": 30,
            "overtime_hours": 25.0,
            "JobLevel": 2,
            "WorkLifeBalance": 1,
            "skills": ["B2B Sales", "Negotiation", "CRM", "Pipeline Management"],
            "recommendedAction": "Re-evaluate commission tiers and career progression roadmap."
        },
        {
            "id": "emp-sales-002",
            "name": "Neha Kapoor",
            "role": "Sales Development Representative",
            "department": "Sales",
            "tenure_months": 6,
            "engagement_score": 3.5,
            "time_since_promotion_months": 6,
            "overtime_hours": 5.0,
            "JobLevel": 1,
            "WorkLifeBalance": 3,
            "skills": ["Cold Outreach", "Lead Generation", "Salesforce"],
            "recommendedAction": "Provide SDR-to-AE promotion milestone training."
        },
        {
            "id": "emp-sales-003",
            "name": "Karan Malhotra",
            "role": "Regional Sales Director",
            "department": "Sales",
            "tenure_months": 48,
            "engagement_score": 3.9,
            "time_since_promotion_months": 12,
            "overtime_hours": 8.0,
            "JobLevel": 4,
            "WorkLifeBalance": 3,
            "skills": ["Strategic Sales", "Team Leadership", "Key Account Management"],
            "recommendedAction": "Support expansion initiatives into new regional territories."
        },
        {
            "id": "emp-sales-004",
            "name": "Sneha Reddy",
            "role": "Account Manager",
            "department": "Sales",
            "tenure_months": 22,
            "engagement_score": 2.2,
            "time_since_promotion_months": 22,
            "overtime_hours": 15.0,
            "JobLevel": 2,
            "WorkLifeBalance": 2,
            "skills": ["Client Upselling", "Renewals", "Customer Retention"],
            "recommendedAction": "Review workload targets and schedule mid-year compensation review."
        },

        # Product Department
        {
            "id": "emp-prod-001",
            "name": "Siddharth Rao",
            "role": "Senior Product Manager",
            "department": "Product",
            "tenure_months": 30,
            "engagement_score": 1.8,
            "time_since_promotion_months": 28,
            "overtime_hours": 16.0,
            "JobLevel": 3,
            "WorkLifeBalance": 2,
            "skills": ["Product Strategy", "User Research", "Agile", "Roadmapping"],
            "recommendedAction": "Define clear Principal Product Manager path and delegate roadmap execution."
        },
        {
            "id": "emp-prod-002",
            "name": "Meera Joshi",
            "role": "UI/UX Designer",
            "department": "Product",
            "tenure_months": 18,
            "engagement_score": 3.7,
            "time_since_promotion_months": 8,
            "overtime_hours": 3.0,
            "JobLevel": 2,
            "WorkLifeBalance": 4,
            "skills": ["Figma", "User Testing", "Prototyping", "Design Systems"],
            "recommendedAction": "Encourage lead design workshop facilitation."
        },
        {
            "id": "emp-prod-003",
            "name": "Aditya Nair",
            "role": "Product Analyst",
            "department": "Product",
            "tenure_months": 10,
            "engagement_score": 2.1,
            "time_since_promotion_months": 10,
            "overtime_hours": 14.0,
            "JobLevel": 1,
            "WorkLifeBalance": 2,
            "skills": ["Mixpanel", "SQL", "Data Analytics", "A/B Testing"],
            "recommendedAction": "Enroll in advanced product strategy learning program."
        },

        # Human Resources Department
        {
            "id": "emp-hr-001",
            "name": "Kavita Deshmukh",
            "role": "HR Business Partner",
            "department": "Human Resources",
            "tenure_months": 32,
            "engagement_score": 3.6,
            "time_since_promotion_months": 10,
            "overtime_hours": 6.0,
            "JobLevel": 3,
            "WorkLifeBalance": 3,
            "skills": ["Employee Relations", "Talent Management", "Conflict Resolution"],
            "recommendedAction": "Lead upcoming company-wide retention strategy program."
        },
        {
            "id": "emp-hr-002",
            "name": "Tarun Kumar",
            "role": "Talent Acquisition Specialist",
            "department": "Human Resources",
            "tenure_months": 15,
            "engagement_score": 1.4,
            "time_since_promotion_months": 15,
            "overtime_hours": 19.0,
            "JobLevel": 1,
            "WorkLifeBalance": 1,
            "skills": ["Tech Recruiting", "LinkedIn Recruiter", "Sourcing"],
            "recommendedAction": "Outsource high-volume screening tasks to relieve hiring burden."
        },

        # Marketing Department
        {
            "id": "emp-mkt-001",
            "name": "Diya Sen",
            "role": "Growth Marketing Lead",
            "department": "Marketing",
            "tenure_months": 24,
            "engagement_score": 2.0,
            "time_since_promotion_months": 24,
            "overtime_hours": 14.0,
            "JobLevel": 2,
            "WorkLifeBalance": 2,
            "skills": ["SEO", "Performance Marketing", "Google Ads", "Content Strategy"],
            "recommendedAction": "Review growth leadership progression and allocate external agency budget."
        },
        {
            "id": "emp-mkt-002",
            "name": "Varun Mehta",
            "role": "Content Strategist",
            "department": "Marketing",
            "tenure_months": 40,
            "engagement_score": 3.9,
            "time_since_promotion_months": 4,
            "overtime_hours": 2.0,
            "JobLevel": 2,
            "WorkLifeBalance": 4,
            "skills": ["Copywriting", "Brand Strategy", "Social Media", "PR"],
            "recommendedAction": "Continue empowering content creation for international marketing campaigns."
        },
        {
            "id": "emp-eng-005",
            "name": "Ishaan Saxena",
            "role": "Data Engineer",
            "department": "Engineering",
            "tenure_months": 5,
            "engagement_score": 1.1,
            "time_since_promotion_months": 5,
            "overtime_hours": 22.0,
            "JobLevel": 1,
            "WorkLifeBalance": 1,
            "skills": ["PySpark", "Snowflake", "Airflow", "ETL"],
            "recommendedAction": "Conduct immediate 1-on-1 to address onboarding bottlenecks and high overtime."
        }
    ]

    count = 0
    for emp_data in demo_employees:
        # Prepare ML feature dictionary
        feature_dict = {
            "tenure_months": emp_data["tenure_months"],
            "engagement_score": emp_data["engagement_score"],
            "time_since_promotion_months": emp_data["time_since_promotion_months"],
            "overtime_hours": emp_data["overtime_hours"],
            "JobLevel": emp_data["JobLevel"],
            "WorkLifeBalance": emp_data["WorkLifeBalance"]
        }

        # Predict ML risk score & explainability
        prediction = get_risk_prediction(feature_dict)

        emp = Employee(
            id=emp_data["id"],
            name=emp_data["name"],
            role=emp_data["role"],
            department=emp_data["department"],
            tenure_months=emp_data["tenure_months"],
            engagement_score=emp_data["engagement_score"],
            time_since_promotion_months=emp_data["time_since_promotion_months"],
            overtime_hours=emp_data["overtime_hours"],
            JobLevel=emp_data["JobLevel"],
            WorkLifeBalance=emp_data["WorkLifeBalance"],
            skills=emp_data["skills"],
            riskScore=prediction["riskScore"],
            riskLevel=prediction["riskLevel"],
            summary=prediction["summary"],
            reasons=prediction["reasons"],
            protectiveFactors=prediction["protectiveFactors"],
            recommendedAction=emp_data["recommendedAction"]
        )
        db.add(emp)
        count += 1

    db.commit()
    print(f"Successfully seeded database with {count} realistic demo employees.")
    db.close()

if __name__ == "__main__":
    seed_database()
