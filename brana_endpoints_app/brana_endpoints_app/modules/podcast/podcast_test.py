import requests

# Base URL of the API
base_url = "https://brana.earaldtradinget.com/api"

# Helper function to print a human-readable response
def print_response(response):
    print("Status Code:", response.status_code)
    print("Response Body:", response.json())
    print()

# Scenario 1: Retrieve podcast details
print("Scenario 1: Retrieve podcast details")
podcast_id = "podcast1"
podcast_url = f"{base_url}/podcast/{podcast_id}"
response = requests.get(podcast_url)
print_response(response)

# Scenario 2: Retrieve podcast episode details
print("Scenario 2: Retrieve podcast episode details")
episode_id = "episode1"
episode_url = f"{base_url}/podcast/{podcast_id}/episode/{episode_id}"
response = requests.get(episode_url)
print_response(response)

# Scenario 3: Retrieve sample audio for a podcast
print("Scenario 3: Retrieve sample audio for a podcast")
sample_audio_url = f"{base_url}/podcast/{podcast_id}/sample_audio"
response = requests.get(sample_audio_url)
print_response(response)

# Scenario 4: Retrieve audio file for an episode
print("Scenario 4: Retrieve audio file for an episode")
audio_file_url = f"{base_url}/podcast/{podcast_id}/episode/{episode_id}/audio_file"
response = requests.get(audio_file_url)
print_response(response)

# Scenario 5: Update user listening history
print("Scenario 5: Update user listening history")
user_id = "user1"
update_listening_history_url = f"{base_url}/user/{user_id}/listening_history"
data = {
    "podcast_id": podcast_id,
    "episode_id": episode_id,
    "timestamp": "2023-08-18 10:30:00"
}
response = requests.post(update_listening_history_url, json=data)
print_response(response)

# Scenario 6: Check subscription access
print("Scenario 6: Check subscription access")
subscription_level = 2
check_subscription_access_url = f"{base_url}/podcast/{podcast_id}/episode/{episode_id}/check_subscription_access"
data = {
    "subscription_level": subscription_level
}
response = requests.post(check_subscription_access_url, json=data)
print_response(response)

# Scenario 7: Get user subscription level
print("Scenario 7: Get user subscription level")
get_user_subscription_level_url = f"{base_url}/user/{user_id}/subscription_level"
response = requests.get(get_user_subscription_level_url)
print_response(response)

# Scenario 8: Invalid API endpoint (404: Not Found)
print("Scenario 8: Invalid API endpoint (404: Not Found)")
invalid_url = f"{base_url}/invalid"
response = requests.get(invalid_url)
print_response(response)