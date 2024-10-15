# utils/api_endpoints.py

BASE_URL = "http://localhost:8000/api"

def get_api_endpoint(endpoint_name):
    endpoints = {
        "login": f"{BASE_URL}/login/",
        "logout": f"{BASE_URL}/logout/",
        "user_info": f"{BASE_URL}/user-info/",
        "quizzes": f"{BASE_URL}/quizzes/",
        "questions": f"{BASE_URL}/questions/?quiz_id=",
        "quiz_result": f"{BASE_URL}/quizresults/",
        "gamesessions": f"{BASE_URL}/gamesessions/",
    }

    return endpoints.get(endpoint_name, None)