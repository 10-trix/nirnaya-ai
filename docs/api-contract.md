# Nirnaya.ai API Contract

This document provides the authoritative API specification for the Nirnaya.ai backend services (Python + FastAPI + PostgreSQL / SQLAlchemy).

---

## 1. Shared Employee JSON Schema

All employee-related endpoints use or return the following standard JSON structure:

```json
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
  "riskScore": 0.81,
  "riskLevel": "High",
  "summary": "High risk of leaving (81% likelihood). Main driver: very low engagement score (1.5/4).",
  "reasons": [
    "Very low engagement score (1.5/4) — signals real disengagement from day-to-day work",
    "No promotion in 26 months — well past the typical growth window",
    "Regularly working overtime — a known early indicator of burnout"
  ],
  "protectiveFactors": [
    "Solid tenure (28 months) — has built roots at the company"
  ],
  "recommendedAction": "Offer expedited promotion evaluation to Tech Lead and enforce 40-hour weekly cap."
}
```

---

## 2. Employee CRUD Endpoints (`/employees`)

### `POST /employees`
Creates a new employee record. The onboarding chat parsed output is submitted here by the GenAI teammate.

- **Request Body**:
```json
{
  "name": "Aarav Sharma",
  "role": "Senior Software Engineer",
  "department": "Engineering",
  "tenure_months": 12,
  "engagement_score": 3.0,
  "time_since_promotion_months": 6,
  "overtime_hours": 5.0,
  "JobLevel": 2,
  "WorkLifeBalance": 3,
  "skills": ["Python", "FastAPI"]
}
```
*Note: `name`, `role`, and `department` are required. All other numeric/skills fields are optional with sensible default values.*

- **Response (`201 Created`)**: Shared Employee Object (with generated `id`).

---

### `GET /employees`
Lists all employees stored in the database.

- **Query Parameters**:
  - `department` (optional): Filter employees by department (e.g., `GET /employees?department=Engineering`).
- **Response (`200 OK`)**: Array of Shared Employee Objects.

---

### `GET /employees/{id}`
Retrieves a single employee by unique ID.

- **Path Parameter**: `id` (string)
- **Response (`200 OK`)**: Shared Employee Object.
- **Error Response (`404 Not Found`)**:
```json
{
  "detail": "Employee with id 'emp-eng-999' not found"
}
```

---

### `PUT /employees/{id}`
Updates existing fields of an employee record.

- **Path Parameter**: `id` (string)
- **Request Body** (Partial object containing fields to update):
```json
{
  "engagement_score": 2.0,
  "overtime_hours": 15.0
}
```
- **Response (`200 OK`)**: Updated Shared Employee Object.

---

### `DELETE /employees/{id}`
Deletes an employee record.

- **Path Parameter**: `id` (string)
- **Response (`204 No Content`)**: Empty response body.

---

## 3. Risk Reasoning & Mitigation Endpoints (`/risk`)

### `GET /risk/{employeeId}`
Fetches employee data, executes XGBoost model prediction + SHAP explainability (`backend/models/risk_model.py`), persists `riskScore`, `riskLevel`, `summary`, `reasons`, and `protectiveFactors` back to the employee row, and returns the updated record.

- **Path Parameter**: `employeeId` (string)
- **Response (`200 OK`)**: Shared Employee Object with updated risk fields.

---

### `POST /risk/{employeeId}/mitigation`
Returns risk mitigation action plan for an employee.

- **Path Parameter**: `employeeId` (string)
- **Request Body** (optional context):
```json
{
  "context": "Employee requested remote work flexibility."
}
```
- **Response (`200 OK`)**:
```json
{
  "employee_id": "emp-eng-001",
  "recommendedAction": "Offer expedited promotion evaluation to Tech Lead and enforce 40-hour weekly cap.",
  "status": "success",
  "note": "Placeholder response. GenAI teammate will connect backend/genai/mitigation.py"
}
```

---

## 4. Team-Level Rollup Analytics (`/teams`)

### `GET /teams/{department}/risk-summary`
Computes department-level aggregate risk analytics, counting total and at-risk members, breakdown by risk severity, and top common risk drivers.

- **Path Parameter**: `department` (string, e.g., `Engineering`, `Sales`, `Product`, `Human Resources`, `Marketing`)
- **Response (`200 OK`)**:
```json
{
  "department": "Engineering",
  "total_employees": 5,
  "at_risk_count": 3,
  "high_risk_count": 2,
  "medium_risk_count": 1,
  "low_risk_count": 2,
  "common_risk_factors": [
    {
      "factor": "Regularly working overtime — a known early indicator of burnout",
      "count": 3
    },
    {
      "factor": "Very low engagement score (1.5/4) — signals real disengagement from day-to-day work",
      "count": 2
    },
    {
      "factor": "No promotion in 26 months — well past the typical growth window",
      "count": 1
    }
  ],
  "summary": "3 out of 5 employees in Engineering are currently at-risk (2 High, 1 Medium). Common factor: Regularly working overtime — a known early indicator of burnout (3 employees affected)."
}
```

---

## 5. GenAI Router Integration Stubs `[Pending - GenAI Teammate]`

The following endpoints are registered in `main.py` and act as stubs (`501 Not Implemented`) for seamless integration by the GenAI teammate.

### `POST /onboarding/chat`
- **Status**: `501 Not Implemented`
- **Owner**: GenAI Teammate (`backend/genai/onboarding.py`)
- **Detail Message**: `"Onboarding GenAI agent logic to be implemented by GenAI teammate in backend/genai/onboarding.py"`

### `POST /policy/ask`
- **Status**: `501 Not Implemented`
- **Owner**: GenAI Teammate (`backend/genai/policy_qa.py`)
- **Detail Message**: `"Policy Q&A GenAI agent logic to be implemented by GenAI teammate in backend/genai/policy_qa.py"`

### `POST /mitigation/generate`
- **Status**: `501 Not Implemented`
- **Owner**: GenAI Teammate (`backend/genai/mitigation.py`)
- **Detail Message**: `"Mitigation Reasoning GenAI logic to be implemented by GenAI teammate in backend/genai/mitigation.py"`
