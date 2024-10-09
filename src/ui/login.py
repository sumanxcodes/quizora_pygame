import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from session_manager import SessionManager
from settings import BTN_WIDTH, BTN_HEIGHT, TXTFIELD_WIDTH, TXTFIELD_HEIGHT

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
        manager=manager,
        object_id=ObjectID(class_id='@subtitle_text')
    )
    username_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - TXTFIELD_WIDTH) // 2, SCREEN_HEIGHT // 2 - 50), (TXTFIELD_WIDTH, TXTFIELD_HEIGHT)),
        manager=manager,
        object_id=ObjectID(class_id='@subtitle_text')
    )

     # Password Label and Input
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (200, 50)),
        text='Password',
        manager=manager,
        object_id=ObjectID(class_id='@subtitle_text')
    )
    password_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - TXTFIELD_WIDTH) // 2, SCREEN_HEIGHT // 2 + 50), (TXTFIELD_WIDTH, TXTFIELD_HEIGHT)),
        manager=manager,
        object_id=ObjectID(class_id='@subtitle_text')
    )
    password_input.set_text_hidden(True)  # Hide password characters

    login_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - BTN_WIDTH) // 2, SCREEN_HEIGHT // 2 + 150), (BTN_WIDTH, BTN_HEIGHT)),
        text='Login',
        manager=manager
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - BTN_WIDTH) // 2, SCREEN_HEIGHT // 2 + 220), (BTN_WIDTH, BTN_HEIGHT)),
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
            username = current_buttons[1].get_text()
            password = current_buttons[2].get_text() 
            # Login API call for auth using session manager (view session_manager.py)
            if SessionManager.login(username, password):
                switch_state("post_login")  # Go to next state if login successful
            else:
                current_buttons[0].set_text("Login failed. Try again.")
        elif event.ui_element == current_buttons[4]:  # Back button
            switch_state("menu")
