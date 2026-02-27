import requests

# Your deployed endpoint
url = "https://insurance-ai-backend-32uc.onrender.com/lead"

# Sample lead data
data = {
    "name": "Test User",
    "email": "testuser@example.com",
    "phone": "555-555-5555",
    "message": "This is a test lead."
}

# Send POST request
response = requests.post(url, json=data)

# Print the response from your backend
print("Status Code:", response.status_code)
print("Response JSON:", response.json())