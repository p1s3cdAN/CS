import requests
import json

# API endpoint
endpoint = "https://api.crowdstrike.com/devices/entities/devices/v1"

# API access token
access_token = "your_access_token_here"

# Headers for API request
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Parameters for API request
params = {
    "filter": "status:active",
    "sort": "last_seen:desc"
}

# Make API request
response = requests.get(endpoint, headers=headers, params=params)

# Check for success
if response.status_code == 200:
    # Parse response data
    data = json.loads(response.text)

    # Dictionary to store hostname: device_id mappings
    hostname_map = {}

    # Iterate through the devices
    for device in data["resources"]:
        hostname = device["hostname"]
        device_id = device["id"]
        last_seen = device["last_seen"]

        # Check if hostname is already in the dictionary
        if hostname in hostname_map:
            print(f"Duplicate detected: hostname = {hostname}, device_id = {device_id}, last_seen = {last_seen}")

            # Delete duplicate
            delete_endpoint = f"{endpoint}/{device_id}"
            delete_response = requests.delete(delete_endpoint, headers=headers)

            # Check for success
            if delete_response.status_code == 204:
                print(f"Successfully deleted duplicate: device_id = {device_id}")
            else:
                # Handle error
                print(f"Error deleting duplicate: {delete_response.text}")
        else:
            hostname_map[hostname] = device_id
else:
    # Handle error
    print("Error making API request:", response.text)