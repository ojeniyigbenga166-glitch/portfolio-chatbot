import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google.genai import types, errors
from app.gemini_client import get_gemini_client
from app.knowledge_loader import build_system_prompt

app = FastAPI(
    title="Portfolio AI Chatbot API",
    description="Backend API for Portfolio AI Chatbot",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
# Origins are supplied as a comma-separated env var so the value can differ
# between local development and production without any code changes.
# Example .env:  ALLOWED_ORIGINS=http://localhost:5173
# Example prod:  ALLOWED_ORIGINS=https://portfolio-8zu9.vercel.app
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
ALLOWED_ORIGINS: list[str] = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,        # No cookies or auth headers needed
    allow_methods=["GET", "POST"],  # Only what the chatbot widget uses
    allow_headers=["Content-Type"], # Only what fetch() sends by default
)


from app.lead_notifier import send_lead_notification


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message prompt")


class ChatResponse(BaseModel):
    reply: str


class LeadRequest(BaseModel):
    name: str = Field(..., description="Client name")
    email: str = Field(..., description="Client contact email")
    message: str | None = Field(default="", description="Project description or notes")
    service: str | None = Field(default="General Inquiry", description="Service interested in")


class LeadResponse(BaseModel):
    status: str
    message: str


@app.get("/")
def root():
    """Root endpoint welcoming visitors and listing available endpoints."""
    return {
        "message": "Portfolio AI Chatbot API is running successfully!",
        "endpoints": {
            "health": "/health",
            "chat": "POST /chat (Requires JSON body: {\"message\": \"your question\"})",
            "lead": "POST /lead (Requires JSON body: {\"name\": \"...\", \"email\": \"...\"})"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint to verify backend service status."""
    return {"status": "ok"}


@app.post("/lead", response_model=LeadResponse)
def submit_lead(request: LeadRequest):
    """
    POST /lead endpoint to capture prospective client contact details.
    """
    name = request.name.strip() if request.name else ""
    email = request.email.strip() if request.email else ""

    if not name or not email or "@" not in email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A valid name and email address are required.",
        )

    send_lead_notification({
        "name": name,
        "email": email,
        "message": request.message.strip() if request.message else "",
        "service": request.service.strip() if request.service else "General Inquiry",
    })

    return LeadResponse(
        status="success",
        message="Thank you! Your information has been received. Olugbenga will get back to you shortly."
    )




@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    POST /chat endpoint to receive user prompts and generate AI responses
    prioritizing Olugbenga Ojeniyi / ARLTECH portfolio knowledge.
    """
    # 1. Validate empty / whitespace-only message
    user_message = request.message.strip() if request.message else ""
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty.",
        )

    # 2. Get Gemini Client
    client = get_gemini_client()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gemini API key is not configured.",
        )

    # 3. Load portfolio system instruction context
    system_prompt = build_system_prompt()
    config = types.GenerateContentConfig(system_instruction=system_prompt)

    # 4. Call Gemini API using available model candidates
    model_candidates = [
        "gemini-3.5-flash-lite",
        "gemini-3.8-flash",
        "gemini-2.5-flash-lite",
        "gemini-flash-latest",
    ]

    last_error = None
    for model_name in model_candidates:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_message,
                config=config,
            )
            if response and response.text:
                return ChatResponse(reply=response.text.strip())
        except (errors.APIError, Exception) as e:
            last_error = e
            continue

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Gemini API Error: {str(last_error) if last_error else 'Failed to generate response'}",
    )
