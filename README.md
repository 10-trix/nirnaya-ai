# Nirnaya.ai — AI-Driven Workforce Intelligence Platform

**Team:** Curious Coders
**College:** Dayananda Sagar College of Engineering (DSCE)
**Theme:** AI in HR & Workforce Management

---

## 📌 Problem Statement

HR teams manage hiring, onboarding, performance, and attrition using disconnected tools that never talk to each other — an ATS for hiring, a survey tool for engagement, spreadsheets for performance. Nobody connects the dots automatically, so decisions stay reactive: HR finds out someone's a flight risk only after they've resigned. This affects HR managers (manual cross-checking), team leads (blindsided by exits), and employees (issues caught too late).

## 💡 Our Solution

One connected AI system where onboarding, performance, skills, and engagement data all feed into a single reasoning engine. It doesn't just show data — it explains **why** someone's at risk and recommends a specific, policy-compliant **action**. Existing tools display information; Nirnaya.ai reasons over it and tells HR what to actually do next.

## ⭐ Key Features

1. **AI Onboarding Agent** — Conversational intake that auto-fills employee profiles from a chat instead of forms.
2. **Risk Reasoning Panel** *(core differentiator)* — Explainable attrition risk scoring: a score plus the actual plain-English reasons behind it.
3. **Risk Mitigation Engine** — Turns a risk score into a specific recommended action, checked against company policy.
4. **Policy Q&A** — Answers HR policy questions with citations back to the source document.
5. **HR Dashboard** — Employee list → detail view, plus a team-level risk rollup for managers.

## 🔗 How the Modules Connect

```text
Onboarding Agent → feeds clean data into →

Risk Reasoning Panel → finds & explains problems →

Risk Mitigation Engine → decides the action →

Policy Q&A → checks it's compliant →

Dashboard → shows everything, individual + team view
```

## 🏗️ Architecture

```text
Input (onboarding chat, performance/skill/engagement data)

↓

Process (risk model + explainability + policy RAG + mitigation logic)

↓

Output (dashboard with scored, explained, actionable insights)
```

## 🛠️ Tech Stack

| Layer                       | Technology                      |
| --------------------------- | ------------------------------- |
| Frontend                    | React + Tailwind CSS            |
| Backend                     | Python + FastAPI                |
| Database                    | PostgreSQL                      |
| Risk Model                  | XGBoost + SHAP (explainability) |
| GenAI (chat/Q&A/mitigation) | LangChain + LLM API             |
| Policy Document Search      | ChromaDB                        |

## 📁 Folder Structure

```text
nirnaya-ai/

├── frontend/              → Frontend owns this entirely
│
├── backend/
│   ├── main.py            → routers only (shared file — edit briefly, commit fast)
│   ├── schemas.py         → shared data models (see schema below)
│   ├── database/
│   ├── routes/
│   │   ├── employee_routes.py
│   │   ├── risk_routes.py
│   │   └── genai_routes.py
│   ├── models/
│   │   └── risk_model.py  → ML person's final function goes here
│   └── genai/
│       ├── onboarding.py
│       ├── policy_qa.py
│       └── mitigation.py
│
├── ml/                     → ML person owns this entirely
│   ├── train_model.py
│   ├── notebook.ipynb
│   └── policy_docs/
│
├── docs/
│   └── api-contract.md
│
├── .env.example
├── .gitignore
└── README.md
```

**Rule:** everyone works only inside their own folder. `main.py` and `schemas.py` are the only shared files — edit briefly, commit immediately, mention it in the group chat.

## 🧩 Shared Employee Data Schema

```json
{
  "id": "string",
  "name": "string",
  "role": "string",
  "department": "string",
  "tenure_months": 0,
  "engagement_score": 0.0,
  "time_since_promotion_months": 0,
  "overtime_hours": 0.0,
  "skills": ["string"],
  "riskScore": 0.0,
  "reasons": ["string"],
  "recommendedAction": "string"
}
```

## 🔌 API Contract

See `docs/api-contract.md` for full details.

| Endpoint                  | Returns                                   |
| ------------------------- | ----------------------------------------- |
| `GET /employees`          | list of employee objects                  |
| `GET /employees/{id}`     | single employee (full schema)             |
| `GET /risk/{id}`          | `{riskScore, reasons: []}`                |
| `GET /team-risk/{deptId}` | `{department, atRiskCount, commonFactor}` |
| `POST /onboarding/chat`   | `{parsedEmployeeData}`                    |
| `POST /policy/ask`        | `{answer, source}`                        |
| `GET /mitigation/{id}`    | `{recommendedAction, policyReference}`    |

No one changes a response shape without posting it in the group chat first.

## 👥 Team & Roles

| Person           | Owns                                                        |
| ---------------- | ----------------------------------------------------------- |
| Frontend         | `frontend/`                                                 |
| Backend          | `backend/` (main.py, routes, database)                      |
| ML/AI            | `ml/` + `backend/models/risk_model.py`                      |
| GenAI/Generalist | `backend/genai/` (onboarding, policy Q&A, mitigation logic) |

## 🌿 Git Workflow

* Never push directly to `main` — always a branch, always a PR.
* Branch naming: `feature/frontend-dashboard`, `feature/backend-routes`, `feature/ml-risk-model`, `feature/genai-onboarding`.
* Commit small, commit often (every 1–2 hrs). Pull from `main` before starting work each day.
* Build against fake/mock data matching the schema above — don't wait on anyone else.
* 10-min daily sync: what you finished, what you're touching today, any shared file you'll edit.

## ⚙️ Config Conventions

* Frontend: `localhost:3000` · Backend: `localhost:8000`
* API keys go in `.env` (never committed) — see `.env.example` for required keys
* Naming: `snake_case` for Python, `camelCase` for JS/React

## 🗓️ Build Timeline (1 week)

| Day | Focus                                                      |
| --- | ---------------------------------------------------------- |
| 1   | Setup, dataset, schema, policy docs                        |
| 2   | Core risk model (backend), employee list/detail (frontend) |
| 3   | Onboarding agent + Policy Q&A                              |
| 4   | Mitigation engine + team rollup                            |
| 5   | Full frontend-backend integration                          |
| 6   | Feedback loop, polish, demo data seeding                   |
| 7   | Deck, demo recording, rehearsal                            |
