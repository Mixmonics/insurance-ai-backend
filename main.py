from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import json

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Lead(BaseModel):
    name: str
    email: str
    phone: str
    message: str

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/lead")
def process_lead(lead: Lead):

    prompt = f"""
You are an AI assistant for an independent insurance agency.

Analyze this inbound lead.

Extract:
- insurance_type (auto, home, commercial, other)
- intent_score (1-5)
- missing_fields (list)
- short_summary
- professional_email_response

Lead message:
{lead.message}

Return strictly valid JSON.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    try:
        parsed = json.loads(response.choices[0].message.content)
    except:
        parsed = {"raw_output": response.choices[0].message.content}

    return parsed