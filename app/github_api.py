# Import requests library (used to call GitHub API)
import requests

# Base GitHub API URL
BASE_URL = "https://api.github.com/users/"


# -------------------------------
# GET USER PROFILE DATA
# -------------------------------
def get_user_profile(username):

    # Create full API URL
    url = BASE_URL + username

    # Send GET request to GitHub API
    response = requests.get(url)

    # If success → return JSON data
    if response.status_code == 200:
        return response.json()

    # If user not found → return None
    return None


# -------------------------------
# GET USER REPOSITORY DATA
# -------------------------------
def get_user_repos(username):

    # API endpoint for repositories
    url = BASE_URL + username + "/repos"

    # Send request
    response = requests.get(url)

    # If success → return repo list JSON
    if response.status_code == 200:
        return response.json()

    # If fail → return empty list
    return []