# main.py

print("UPDATED VERSION LOADED")
import os
import json
import re
import time
import threading

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from twilio.rest import Client as TwilioClient

# Load .env if exists
if os.path.exists(".env"):
    load_dotenv()

# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set!")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Twilio setup
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

if not all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
    raise ValueError("Twilio environment variables are not set!")

twilio_client = TwilioClient(twilio_account_sid, twilio_auth_token)

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

    print("---- NEW LEAD RECEIVED ----")
    print("Incoming phone:", lead.phone)

    # Normalize phone number to E.164 if missing +1
    phone = lead.phone.strip()
    if not phone.startswith("+"):
        phone = "+1" + re.sub(r"\D", "", phone)

    print("Normalized phone:", phone)

    # Step 1: Extract structured data
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract structured insurance lead info."},
            {
                "role": "user",
                "content": f"""
Name: {lead.name}
Email: {lead.email}
Phone: {phone}
Message: {lead.message}

Return ONLY valid JSON with:
name, email, phone, type_of_insurance, urgency
"""
            }
        ],
        temperature=0
    )

    raw_output = response.choices[0].message.content
    cleaned = re.sub(r"```json|```", "", raw_output).strip()
    structured_data = json.loads(cleaned)

    structured_data["phone"] = phone  # ensure correct phone format

    # Step 2: Generate AI SMS reply
    reply_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an insurance agency assistant. Respond professionally and briefly to new leads."
            },
            {
                "role": "user",
                "content": f"""
Lead Info:
Name: {structured_data['name']}
Type: {structured_data['type_of_insurance']}
Urgency: {structured_data['urgency']}

Write a short SMS confirming we received their request and ask one qualifying question.
Keep under 300 characters.
"""
            }
        ],
        temperature=0.7
    )

    sms_message = reply_response.choices[0].message.content.strip()
    structured_data["ai_reply"] = sms_message

    print("SMS MESSAGE:", sms_message)
    print("Sending FROM:", twilio_phone_number)
    print("Sending TO:", phone)

    # Step 3: Send SMS instantly (with debug)
    try:
        message = twilio_client.messages.create(
            body=sms_message,
            from_=twilio_phone_number,
            to=phone
        )
        print("Twilio message SID:", message.sid)
    except Exception as e:
        print("TWILIO ERROR:", e)

    return structured_data


# Run directly via python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)