# main.py
import os
import json
import re
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load .env if exists
if os.path.exists(".env"):
    load_dotenv()

# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set!")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# FastAPI app
app = FastAPI(title="Insurance AI Backend")

# Lead model
class Lead(BaseModel):
    name: str
    email: str
    phone: str
    message: str

@app.get("/")
def root():
    return {"status": "AI backend is live!"}

@app.post("/lead")
def process_lead(lead: Lead):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract structured insurance lead info."},
            {
                "role": "user",
                "content": f"""
Name: {lead.name}
Email: {lead.email}
Phone: {lead.phone}
Message: {lead.message}

Return ONLY valid JSON with:
name, email, phone, type_of_insurance, urgency
"""
            }
        ],
        temperature=0
    )

    raw_output = response.choices[0].message.content

    # Remove markdown formatting if present
    cleaned = re.sub(r"```json|```", "", raw_output).strip()

    return json.loads(cleaned)

# Run directly via python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)