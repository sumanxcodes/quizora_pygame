# states/post_login.py
import pygame
import pygame_gui
from session_manager import SessionManager
from ui.leaderboard import enter_leaderboard

def fetch_user_info():
    session = SessionManager.get_session()
    if session:
        response = session.get('http://localhost:8000/api/user-info/')
        if response.status_code == 200:
            user_info = response.json()
            return user_info
        else:
            print("Failed to fetch user info:", response.status_code)
    else:
        print("User is not logged in.")

def enter_post_login(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Initializes the post-login menu with Play Quiz, Help, Leaderboard, and Quit buttons.
    """
    manager.clear_and_reset()
    
    # Fetch user info to get the user's name for the welcome message
    user_info = fetch_user_info()
    if user_info.get('first_name', 'User') != "" and user_info.get('last_name', 'User') != "" :
        name = f"{user_info.get('first_name', 'User')} {user_info.get('last_name', 'User')}"

    else:
       name =  user_info.get('username', 'User') if user_info else 'User'
    
    # Welcome Message
    welcome_message = f"Welcome to Quizora, {name}!"
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 200), (300, 50)),
        text=welcome_message,
        manager=manager
    )

    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 80), (200, 50)),
        text='Play Quiz',
        manager=manager
    )
    help_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 10), (200, 50)),
        text='Help',
        manager=manager
    )
    leaderboard_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60), (200, 50)),
        text='Leaderboard',
        manager=manager
    )
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 130), (200, 50)),
        text='Quit',
        manager=manager
    )
    return [play_button, help_button, leaderboard_button, quit_button]

def handle_post_login_events(event, switch_state, current_buttons, is_running):
    """
    Handles button clicks for the post-login menu.
    """
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == current_buttons[0]:  # Play Quiz button
            print("Play Quiz clicked!")
        elif event.ui_element == current_buttons[1]:  # Help button
            print("Help clicked!")
        elif event.ui_element == current_buttons[2]:  # Leaderboard button
            print("Leaderboard clicked!")
            switch_state('leaderboard')
        elif event.ui_element == current_buttons[3]:  # Quit button
            is_running[0] = False
            
            