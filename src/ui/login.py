import pygame
import pygame_gui
from pygame_gui.core import ObjectID
import requests

def enter_login(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Initializes the login form with username, password fields, Login, and Back buttons.
    """
    manager.clear_and_reset()

     # Error message label (initially hidden)
    error_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200), (200, 30)),
        text='',
        manager=manager,
        object_id=ObjectID(class_id='@error_message')
    )

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100), (200, 50)),
        text='Username',
        manager=manager
    )
    username_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50), (200, 50)),
        manager=manager
    )

     # Password Label and Input
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (200, 50)),
        text='Password',
        manager=manager
    )
    password_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50), (200, 50)),
        manager=manager
    )
    password_input.set_text_hidden(True)  # Hide password characters

    login_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120), (200, 50)),
        text='Login',
        manager=manager
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 190), (200, 50)),
        text='Back',
        manager=manager
    )
    return [error_label, username_input, password_input, login_button, back_button]


def handle_login_events(event, current_buttons, switch_state):
    """
    Handles button clicks for the login form.
    """
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == current_buttons[3]:  # Login button
            # API call for authentication
            session = login_api_call(current_buttons[1], current_buttons[2], current_buttons[0])
            if session:  
                print("Login successful!")
                switch_state("post_login")
            else:
                print("Login failed. Please try again.")
        elif event.ui_element == current_buttons[4]:  # Back button
            switch_state("menu")

def login_api_call(username_input, password_input, error_label):
    """
    Handle login form submission and authenticate using the API.
    """
    username = username_input.get_text()
    password = password_input.get_text()

    if username and password:
        login_url = 'http://localhost:8000/api/login/'  
        credentials = {'username': username, 'password': password}
        try:
            session = requests.Session()  # Create a session to persist cookies
            response = session.post(login_url, data=credentials)
            if response.status_code == 200:
                return session  # Return the session if login succeeds
            else:
                error_message = f"Login failed. Status: {response.status_code}"
                print(f"Login failed. Status: {response.status_code}")
                error_label.set_text(error_message)
        except requests.RequestException as e:
            error_message = f"An error occurred during login: {e}"
            print(f"An error occurred during login: {e}")
            error_label.set_text(error_message)
    else:
        print("Please enter both username and password.")
    # Return None if login fails
    return None