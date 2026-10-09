from fastapi import FastAPI
from pydantic import BaseModel
import requests

from graph.workflow import app

api = FastAPI()

WEBHOOK_URL = "http://localhost:5678/webhook/support-escalation"


# ---------- CHAT REQUEST ----------

class Query(BaseModel):

    question: str
    email: str
    name: str


# ---------- EMAIL REQUEST ----------

class EmailRequest(BaseModel):

    question: str
    answer: str
    email: str
    name: str


# ---------- CHAT ENDPOINT ----------

@api.post("/chat")
def chat(query: Query):

    result = app.invoke({

        "question": query.question,
        "email": query.email,
        "name": query.name

    })

    return result


# ---------- SEND EMAIL ENDPOINT ----------

@api.post("/send-email")
def send_email(data: EmailRequest):

    payload = {

        "question": data.question,
        "answer": data.answer,
        "email": data.email,
        "name": data.name

    }

    requests.post(

        WEBHOOK_URL,

        json=payload

    )

    return {

        "status": "email_sent"

    }