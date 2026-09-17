from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["GenAI Extensions (Teammate Stubs)"])

class OnboardingChatRequest(BaseModel):
    user_message: str
    session_id: Optional[str] = None

class PolicyAskRequest(BaseModel):
    question: str
    employee_id: Optional[str] = None

class GenAIMitigationRequest(BaseModel):
    employee_id: str
    prompt: Optional[str] = None

@router.post("/onboarding/chat", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def onboarding_chat_stub(body: OnboardingChatRequest):
    """
    Onboarding Chat Agent (GenAI Stub).
    To be implemented by GenAI teammate in backend/genai/onboarding.py
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Onboarding GenAI agent logic to be implemented by GenAI teammate in backend/genai/onboarding.py"
    )

@router.post("/policy/ask", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def policy_ask_stub(body: PolicyAskRequest):
    """
    Policy Q&A Agent (GenAI Stub).
    To be implemented by GenAI teammate in backend/genai/policy_qa.py
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Policy Q&A GenAI agent logic to be implemented by GenAI teammate in backend/genai/policy_qa.py"
    )

@router.post("/mitigation/generate", status_code=status.HTTP_501_NOT_IMPLEMENTED)
def mitigation_generate_stub(body: GenAIMitigationRequest):
    """
    Mitigation Reasoning Engine (GenAI Stub).
    To be implemented by GenAI teammate in backend/genai/mitigation.py
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Mitigation Reasoning GenAI logic to be implemented by GenAI teammate in backend/genai/mitigation.py"
    )
