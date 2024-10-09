import requests
from utils import get_api_endpoint

login_url = get_api_endpoint("login")
logout_url = get_api_endpoint("logout")
user_info_url = get_api_endpoint("user_info")

# Now you can use these URLs in your API requests


class SessionManager:
    _session = None  # private attribute <- store session value

    @classmethod
    def login(cls, username, password):
        """
        Authenticates the user and stores the session if successful.
        """
        login_url = get_api_endpoint("login")  # Login endpoint
        credentials = {'username': username, 'password': password}
        
        try:
            session = requests.Session()
            response = session.post(login_url, data=credentials)
            
            if response.status_code == 200:
                cls._session = session  # Store session if login succeeds
                print("Login successful.")
                return True
            else:
                print(f"Login failed: {response.status_code}")
                return False
        
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return False

    @classmethod
    def get_session(cls):
        """
        Returns the current session if logged in, or None if not.
        """
        return cls._session

    @classmethod
    def logout(cls):
        """
        Logs out by clearing the session.
        """
        if cls._session:
            cls._session.close()  # Properly close the session
            cls._session = None
            print("Logged out successfully.")

    @classmethod
    def is_logged_in(cls):
        """
        Checks if a session is active.
        """
        return cls._session is not None
