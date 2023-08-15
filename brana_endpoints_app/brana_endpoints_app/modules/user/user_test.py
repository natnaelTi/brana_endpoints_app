import requests

# Base URL of your Frappe app
base_url = "http://brana.earaldtradinget.com"

# API endpoint URLs
login_url = f"{base_url}/api/method/brana_endpoints_app.modules.user.user_api.login"
logout_url = f"{base_url}/api/method/brana_endpoints_app.modules.user.user_api.logout"

# Test login API
def test_login(identifier, password):
    # Make a POST request to the login API
    response = requests.post(login_url, json={"identifier": identifier, "password": password})

    # Verify the response
    if response.status_code == 200:
        # Login successful
        data = response.json()
        print("Login successful!")
        print("User:", data.get("user"))
        print("First Name:", data.get("first_name"))
        print("Last Name:", data.get("last_name"))
        print("Email:", data.get("email"))
        # Add other user details as needed
    else:
        # Login failed
        print("Login failed. Status code:", response.status_code)
        print("Error:", response.text)

# Test logout API
def test_logout():
    # Make a POST request to the logout API
    response = requests.post(logout_url)

    # Verify the response
    if response.status_code == 200:
        # Logout successful
        data = response.json()
        print("Logout successful!")
        print("Message:", data.get("message"))
    else:
        # Logout failed
        print("Logout failed. Status code:", response.status_code)
        print("Error:", response.text)

# Run the tests
test_login("natnaeltilaye", "8123Naty")  # Login using username
test_login("natnaeltilaye30@gmail.com", "8123Naty")  # Login using email
test_login("+251922825445", "8123Naty")  # Login using phone number
test_logout()