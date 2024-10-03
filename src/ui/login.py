import pygame
import pygame_gui
from pygame_gui.core import ObjectID
import requests

def display_login_form(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Display the login form for username and password.
    """
    window_surface.blit(background, (0, 0))
    manager.clear_and_reset()

    # Username Label and Input
    username_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100), (200, 50)),
        text='Username:',
        manager=manager
    )
    username_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50), (200, 50)),
        manager=manager
    )

    # Password Label and Input
    password_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (200, 50)),
        text='Password:',
        manager=manager
    )
    password_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50), (200, 50)),
        manager=manager
    )
    password_input.set_text_hidden(True)  # Hide password characters

    # Login Button
    login_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120), (200, 50)),
        text='Login',
        manager=manager,
        object_id=ObjectID(class_id="@menu_buttons", object_id="#login_button")
    )

    return username_input, password_input, login_button


def handle_login_event(event, username_input, password_input):
    """
    Handle login form submission and authenticate using the API.
    """
    if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element.object_id == '#login_button':
        username = username_input.get_text()
        password = password_input.get_text()

        if username and password:
            login_url = 'http://localhost:8000/api/login/'  # Adjust to your correct login endpoint
            credentials = {'username': username, 'password': password}

            session = requests.Session()  # Create a session to persist cookies
            response = session.post(login_url, data=credentials)

            if response.status_code == 200:
                print("Login successful!")
                return session  # Return the session if login succeeds
            else:
                print(f"Login failed. Status: {response.status_code}")
        else:
            print("Please enter both username and password.")
