
import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from graph.workflow import app

api = FastAPI(title="AI Support Autopilot API")

WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "").strip()
WEBHOOK_TIMEOUT_SECONDS = 10


class Query(BaseModel):
    question: str
    email: EmailStr
    name: str


class EmailRequest(BaseModel):
    question: str
    answer: str
    email: EmailStr
    name: str


@api.get("/health")
def health():
    return {"status": "ok"}


@api.post("/chat")
def chat(query: Query):
    try:
        result = app.invoke({
            "question": query.question,
            "email": str(query.email),
            "name": query.name,
        })
        return result
    except Exception as exc:
        # Keep internal error details in server logs, not API responses.
        print(f"Chat processing failed: {exc}")
        raise HTTPException(
            status_code=500,
            detail="The support request could not be processed.",
        ) from exc


@api.post("/send-email")
def send_email(data: EmailRequest):
    if not WEBHOOK_URL:
        raise HTTPException(
            status_code=503,
            detail="Email integration is not configured.",
        )

    payload = {
        "question": data.question,
        "answer": data.answer,
        "email": str(data.email),
        "name": data.name,
    }

    try:
        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=WEBHOOK_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Email webhook failed: {exc}")
        raise HTTPException(
            status_code=502,
            detail="The email service could not confirm successful delivery.",
        ) from exc

    return {"status": "webhook_accepted"}