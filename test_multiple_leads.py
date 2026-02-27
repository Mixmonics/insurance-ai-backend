import requests

# Your deployed API URL
API_URL = "https://insurance-ai-backend-32uc.onrender.com/lead"

# Sample leads with different messages
leads = [
    {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "+12403748141",
        "message": "I need car insurance as soon as possible."
    },
    {
        "name": "Bob Smith",
        "email": "bob@example.com",
        "phone": "555-987-6543",
        "message": "Looking for health insurance for my family."
    },
    {
        "name": "Carol Lee",
        "email": "carol@example.com",
        "phone": "555-555-0000",
        "message": "Want home insurance quotes, not urgent."
    }
]

for lead in leads:
    response = requests.post(API_URL, json=lead)
    print("Sent lead:", lead["name"])
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)
    print("-" * 50)