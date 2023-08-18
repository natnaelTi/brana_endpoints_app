import requests

# Base URL of the API
base_url = "https://brana.earaldtradinget.com/api"

# Helper function to print a human-readable response
def print_response(response):
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
    print()

# Scenario 1: Retrieve audiobook details
print("Scenario 1: Retrieve audiobook details")
audiobook_id = "audiobook1"
audiobook_url = f"{base_url}/audiobook/{audiobook_id}"
response = requests.get(audiobook_url)
print_response(response)

# Scenario 2: Retrieve chapter details
print("Scenario 2: Retrieve chapter details")
chapter_id = "chapter1"
chapter_url = f"{base_url}/chapter/{chapter_id}"
response = requests.get(chapter_url)
print_response(response)

# Scenario 3: Update audiobook chapter listening time
print("Scenario 3: Update audiobook chapter listening time")
update_listening_time_url = f"{base_url}/audiobook/{audiobook_id}/chapter/{chapter_id}/listening_time"
data = {
    "listening_time": 10.5
}
response = requests.put(update_listening_time_url, json=data)
print_response(response)

# Scenario 4: Retrieve user listening history
print("Scenario 4: Retrieve user listening history")
user_id = "user1"
listening_history_url = f"{base_url}/user/{user_id}/listening_history"
response = requests.get(listening_history_url)
print_response(response)

# Scenario 5: Upload audiobook file
print("Scenario 5: Upload audiobook file")
upload_file_url = f"{base_url}/upload_file"
data = {
    "file_name": "my_audiobook.mp3"
}
response = requests.post(upload_file_url, json=data)
print_response(response)

# Scenario 6: Invalid API endpoint (404: Not Found)
print("Scenario 6: Invalid API endpoint (404: Not Found)")
invalid_url = f"{base_url}/invalid"
response = requests.get(invalid_url)
print_response(response)