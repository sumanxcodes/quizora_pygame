"""
The  api_endpoints.py file defines a utility function for managing API endpoints ...

Components:
- **BASE_URL**: Base URL for the API server, set to `http://localhost:8000/api`.
- **get_api_endpoint**: Function that returns the full URL for a specified endpoint name. Supported endpoints include:
  - `login`, `logout`, and `user_info` for authentication and user details.
  - `get_user`, `quizzes`, `questions`, `quiz_result`, and `gamesessions` for quiz-related data management.

"""


BASE_URL = "http://localhost:8000/api"

def get_api_endpoint(endpoint_name):
    endpoints = {
        "login": f"{BASE_URL}/login/",
        "logout": f"{BASE_URL}/logout/",
        "user_info": f"{BASE_URL}/user-info/",
        "get_user": f"{BASE_URL}/users/",
        "quizzes": f"{BASE_URL}/quizzes/",
        "questions": f"{BASE_URL}/questions/?quiz_id=",
        "quiz_result": f"{BASE_URL}/quizresults/",
        "gamesessions": f"{BASE_URL}/gamesessions/",
    }

    return endpoints.get(endpoint_name, None)