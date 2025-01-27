"""
This file post_login.py, defines the post-login menu..

Main Functions:
- **enter_post_login**: Sets up the post-login menu with a welcome message and buttons for Play Quiz, Help, Leaderboard, 
  and Quit
- **handle_post_login_events**: Manages user interactions on the post-login screen, navigating to the selected section 
  or quitting the application
"""

import pygame
import pygame_gui
from ui.leaderboard import enter_leaderboard
from pygame_gui.core import ObjectID
from settings import BTN_WIDTH, BTN_HEIGHT, LABEL_HEIGHT, LABEL_WIDTH, LARGE_LABEL_HEIGHT, LARGE_LABEL_WIDTH
from api import fetch_user_info



def enter_post_login(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data):
    """
    Initializes the post-login menu with Play Quiz, Help, Leaderboard, and Quit buttons.
    """
    manager.clear_and_reset()
    
    # Fetch user info to get the user's name for the welcome message
    state_data['user_info'] = fetch_user_info()
    if state_data['user_info'].get('first_name', 'User') != "" and state_data['user_info'].get('last_name', 'User') != "" :
        name = f"{state_data['user_info'].get('first_name', 'User')} {state_data['user_info'].get('last_name', 'User')}"
    else:
       name =  state_data['user_info'].get('username', 'User') if state_data['user_info'] else 'User'
    
    # Welcome Message
    welcome_message = f"Welcome to Quizora!"
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH) // 2, SCREEN_HEIGHT // 2 - 300), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
        text=welcome_message,
        manager=manager,
        object_id=ObjectID(class_id='@title_text')

    )
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH) // 2, SCREEN_HEIGHT // 2 - 250), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
        text=f"{name}",
        manager=manager,
        object_id=ObjectID(class_id='@title_text')

    )

    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH  - BTN_WIDTH) // 2, SCREEN_HEIGHT // 2 - 80), (BTN_WIDTH, BTN_HEIGHT)),
        text='Play Quiz',
        manager=manager
    )
    help_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH  - BTN_WIDTH) // 2, SCREEN_HEIGHT // 2 - 10), (BTN_WIDTH, BTN_HEIGHT)),
        text='Help',
        manager=manager
    )
    leaderboard_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH  - BTN_WIDTH )// 2, SCREEN_HEIGHT // 2 + 60), (BTN_WIDTH, BTN_HEIGHT)),
        text='Leaderboard',
        manager=manager
    )
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH  - BTN_WIDTH) // 2, SCREEN_HEIGHT // 2 + 130), (BTN_WIDTH, BTN_HEIGHT)),
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
            switch_state('play')
        elif event.ui_element == current_buttons[1]:  # Help button
            print("Help clicked!")
        elif event.ui_element == current_buttons[2]:  # Leaderboard button
            print("Leaderboard clicked!")
            switch_state('leaderboard')
        elif event.ui_element == current_buttons[3]:  # Quit button
            is_running[0] = False
            
            
