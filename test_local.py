# test_local.py
import requests

BASE_URL = "http://127.0.0.1:8000"

# Test root endpoint
try:
    r = requests.get(BASE_URL + "/")
    print("Root endpoint response:", r.json())
except Exception as e:
    print("Error calling root endpoint:", e)

# Test /lead endpoint
sample_lead = {
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "phone": "123-456-7890",
    "message": "Looking for car insurance quotes."
}

try:
    r = requests.post(BASE_URL + "/lead", json=sample_lead)
    print("Lead endpoint response:", r.json())
except Exception as e:
    print("Error calling lead endpoint:", e)