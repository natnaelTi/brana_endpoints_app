import requests

# Base URL of the API
base_url = "https://brana.earaldtradinget.com/api"

# Helper function to print a human-readable response
def print_response(response):
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
    print()

# Scenario 1: Successful login
print("Scenario 1: Successful login")
login_url = f"{base_url}/login"
data = {
    "identifier": "natnaeltilaye30@gmail.com",
    "password": "8123Naty",
    "captcha_response": "valid_captcha_response"
}
response = requests.post(login_url, json=data)
print_response(response)

# Scenario 2: Invalid identifier or password
print("Scenario 2: Invalid identifier or password")
data["identifier"] = "invalid_user@example.com"
response = requests.post(login_url, json=data)
print_response(response)

# Scenario 3: Exceeded rate limit
print("Scenario 3: Exceeded rate limit")
for _ in range(12):
    response = requests.post(login_url, json=data)
print_response(response)

# Scenario 4: Invalid CAPTCHA response
print("Scenario 4: Invalid CAPTCHA response")
data["identifier"] = "user@example.com"
data["captcha_response"] = "invalid_captcha_response"
response = requests.post(login_url, json=data)
print_response(response)

# Scenario 5: Successful logout
print("Scenario 5: Successful logout")
logout_url = f"{base_url}/logout"
response = requests.get(logout_url)
print_response(response)

# Scenario 6: Logout without a valid session
print("Scenario 6: Logout without a valid session")
response = requests.get(logout_url)
print_response(response)

# Scenario 7: Invalid API endpoint (404: Not Found)
print("Scenario 7: Invalid API endpoint (404: Not Found)")
invalid_url = f"{base_url}/invalid"
response = requests.get(invalid_url)
print_response(response)