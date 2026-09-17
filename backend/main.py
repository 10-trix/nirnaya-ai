from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.db import engine, Base
from backend.routes.employee_routes import router as employee_router
from backend.routes.risk_routes import router as risk_router
from backend.routes.team_routes import router as team_router
from backend.routes.genai_routes import router as genai_router

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nirnaya.ai API",
    description="AI-driven HR & Workforce Risk Management Platform Backend",
    version="1.0.0"
)

# Enable CORS for frontend application integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Application Routers
app.include_router(employee_router)
app.include_router(risk_router)
app.include_router(team_router)
app.include_router(genai_router)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "app": "Nirnaya.ai Backend API",
        "version": "1.0.0"
    }
