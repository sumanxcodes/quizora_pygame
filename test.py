import requests

# Define the login URL and credentials
login_url = 'http://localhost:8000/api/login/'  # Adjust to your correct login endpoint
logout_url = 'http://localhost:8000/api/logout/'
credentials = {
    'username': 'quizora',  # Replace with valid credentials
    'password': '0000'
}

# Create a session object to persist cookies (like the session cookie)
session = requests.Session()

# Send a POST request to log in
response = session.post(login_url, data=credentials)

# Check if the login was successful
if response.status_code == 200:
    print("Login successful")

    # Now use the session to access other endpoints
    quizzes_endpoint = 'http://localhost:8000/api/quizzes/'  # Adjust to the desired API endpoint

    # Send a GET request to another endpoint using the same session (with the session cookie)
    response = session.get(quizzes_endpoint)

    if response.status_code == 200:
        # If successful, print the data
        print("Request successful:", response.json())
    else:
        # Print the error if the request failed
        print(f"Failed to access the endpoint. Status code: {response.status_code}")
        print("Response text:", response.text)


    csrf_token = session.cookies.get('csrftoken')
    print(f"CSRF token: {csrf_token}")

    headers = {
        'X-CSRFToken': csrf_token  # Include the CSRF token in the headers
    }
    
    logout_response = session.post(logout_url, headers=headers)

    print(logout_response.json())
    if response.status_code == 200:
        print("Logout successful and session destroyed")
    else:
        print(f"Logout failed with status code: {response.status_code}")
        print("Response:", response.text)
else:
    print(f"Login failed with status code {response.status_code}")
    print("Response text:", response.text)
