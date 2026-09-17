import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_list_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 16

def test_create_and_get_employee():
    # 1. Create employee (simulating onboarding chat output)
    new_emp_payload = {
        "name": "Testing Candidate",
        "role": "QA Automation Engineer",
        "department": "Engineering",
        "tenure_months": 12,
        "engagement_score": 2.5,
        "time_since_promotion_months": 12,
        "overtime_hours": 10.0,
        "JobLevel": 1,
        "WorkLifeBalance": 2,
        "skills": ["PyTest", "Selenium", "CI/CD"]
    }
    create_res = client.post("/employees", json=new_emp_payload)
    assert create_res.status_code == 201
    created_emp = create_res.json()
    emp_id = created_emp["id"]
    assert created_emp["name"] == "Testing Candidate"

    # 2. Fetch created employee
    get_res = client.get(f"/employees/{emp_id}")
    assert get_res.status_code == 200
    assert get_res.json()["role"] == "QA Automation Engineer"

    # 3. Update employee
    update_res = client.put(f"/employees/{emp_id}", json={"engagement_score": 3.5})
    assert update_res.status_code == 200
    assert update_res.json()["engagement_score"] == 3.5

    # 4. Clean up test record
    del_res = client.delete(f"/employees/{emp_id}")
    assert del_res.status_code == 204

def test_compute_risk():
    # Fetch first seeded employee
    list_res = client.get("/employees")
    emp_id = list_res.json()[0]["id"]

    risk_res = client.get(f"/risk/{emp_id}")
    assert risk_res.status_code == 200
    risk_data = risk_res.json()
    assert "riskScore" in risk_data
    assert "riskLevel" in risk_data
    assert "reasons" in risk_data
    assert "protectiveFactors" in risk_data

def test_mitigation_placeholder():
    list_res = client.get("/employees")
    emp_id = list_res.json()[0]["id"]

    mit_res = client.post(f"/risk/{emp_id}/mitigation")
    assert mit_res.status_code == 200
    mit_data = mit_res.json()
    assert mit_data["employee_id"] == emp_id
    assert "recommendedAction" in mit_data

def test_team_risk_summary():
    team_res = client.get("/teams/Engineering/risk-summary")
    assert team_res.status_code == 200
    summary_data = team_res.json()
    assert summary_data["department"] == "Engineering"
    assert "total_employees" in summary_data
    assert "common_risk_factors" in summary_data

def test_genai_stubs():
    onboarding_res = client.post("/onboarding/chat", json={"user_message": "Hello"})
    assert onboarding_res.status_code == 501

    policy_res = client.post("/policy/ask", json={"question": "What is vacation policy?"})
    assert policy_res.status_code == 501

    mit_gen_res = client.post("/mitigation/generate", json={"employee_id": "test"})
    assert mit_gen_res.status_code == 501
