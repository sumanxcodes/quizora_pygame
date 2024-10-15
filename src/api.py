
"""
This file manages interactions with the backend server for quiz-related data and sessions..

Main Functions:
- **create_update_game_session**: Creates or updates a quiz session, including details like quiz ID, score, 
  and answer count. Returns success status.
- **fetch_quiz_questions**: Retrieves questions for a specified quiz from the server.
- **fetch_quiz_data**: Gets available quizzes and details from the server.
- **fetch_user_info**: Fetches logged-in user's info, including name and ID.
- **submit_quiz_result**: Submits the quiz result, including score and feedback, at the end of the quiz.

Enables server-side communication with CSRF protection.
"""

from session_manager import SessionManager
from utils import get_api_endpoint
from datetime import datetime


def create_update_game_session(game_session, session_id=None):
    """
    ccreates a new quiz session with details like Quiz_id, duration, status, score,
    and correct answer count. returns True if successful, False otherwise.
    """
    print("> inside session update")
    print(session_id)
    session = SessionManager.get_session()
    csrf_token = session.cookies.get('csrftoken')
    headers = {
        'X-CSRFToken': csrf_token  # including the CSRF token in the headers
    }

    if session:
        try:
            if session_id:
                # Update the existing game session
                temp_game_session = game_session.copy()
                temp_game_session.pop('id', None) 
                update_endpoint = f"{get_api_endpoint('gamesessions')}{session_id}/"
                print(update_endpoint)
                response = session.put(update_endpoint, json=temp_game_session, headers=headers)
            else:
                # Create a new game session
                response = session.post(get_api_endpoint('gamesessions'), json=game_session, headers=headers)
            if response.status_code in [200, 201]:
                print("Game session created or updated successfully!")
                game_session['id'] = response.json().get('id')  # Store session ID if created
                return True
            else:
                print("Failed to create/update game session:", response.status_code, response.text)
                return False

        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    else:
        print("User is not logged in.")
        return False


def fetch_quiz_questions(quiz_id):
    """
    Fetch quiz questions from the server from Question API.
    """
    session = SessionManager.get_session()
    if session:
        response = session.get(get_api_endpoint("questions") + str(quiz_id))
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch quiz question:", response.status_code)
    else:
        print("User is not logged in.")
    return []


def fetch_quiz_data():
    """
    Fetch data from the server from Quiz Result API.
    """
    session = SessionManager.get_session()
    if session:
        response = session.get(get_api_endpoint("quizzes"))
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch quiz data:", response.status_code)
    else:
        print("User is not logged in.")
    return []

def fetch_user_info():
    session = SessionManager.get_session()
    if session:
        response = session.get(get_api_endpoint("user_info"))
        if response.status_code == 200:
            user_info = response.json()
            return user_info
        else:
            print("Failed to fetch user info:", response.status_code)
    else:
        print("User is not logged in.")


def submit_quiz_result(state_data):
    """
    submit the quiz result at the end of the quiz to the server via the quiz_result API endpoint.
    """
    session = SessionManager.get_session()
    if not session:
        print("User is not logged in.")
        return False

    # quiz title based on the quiz ID in game_session
    quiz_id = state_data["game_session"]["quiz"]
    quiz_title = next((quiz['title'] for quiz in state_data["quiz_data"] if quiz['id'] == quiz_id), "Unknown Quiz")

    # quiz result data from state_data
    quiz_result_data = {
        "student": state_data["user_info"]["id"],  
        "quiz": state_data["game_session"]["quiz"],      
        "score": state_data["game_session"]["score"],
        "feedback": "Needs improvement" if state_data["game_session"]["score"] < 5 else "Good job!",  # Example feedback
        "completed_at": datetime.utcnow().isoformat()
    }
    print("><><Reuslt")
    print(session.cookies.get('csrftoken'))
    print(quiz_result_data)

    headers = {
        'X-CSRFToken': session.cookies.get('csrftoken')
    }

    try:
        # post the quiz result data
        response = session.post(get_api_endpoint("quiz_result"), json=quiz_result_data, headers=headers)

        if response.status_code in [200, 201]:
            print("Quiz result submitted successfully!")
            return True
        else:
            print("Failed to submit quiz result:", response.status_code, response.text)
            return False

    except Exception as e:
        print(f"An error occurred while submitting quiz result: {e}")
        return False
