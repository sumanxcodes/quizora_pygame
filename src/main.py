# main.py
import os
import pygame
import pygame_gui
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.menu import enter_menu, handle_menu_events
from ui.login import enter_login, handle_login_events
from ui.post_login import enter_post_login, handle_post_login_events
from ui.leaderboard import enter_leaderboard
from ui.play import enter_quiz

# Initialize Pygame
pygame.init()

# Set up display
pygame.display.set_caption("Quizora")
window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(pygame.Color('#141414'))

theme_path = 'src/theme.json'

# Check if the theme file exists
if os.path.exists(theme_path):
    print("Loading theme file:", theme_path)
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path)
else:
    print("Theme file not found. Using default theme.")
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT)) 



# Set up UI manager
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path)

# Game clock
clock = pygame.time.Clock()

# States for different screens
MENU_STATE = "menu"
LOGIN_STATE = "login"
POST_LOGIN_STATE = "post_login"
QUIT_STATE = "quit"
LEADERBOARD_STATE = "leaderboard"
PLAY = "play"

# Initial state
current_state = MENU_STATE
current_buttons = []
state_initialized = False  # flag to control state initilization
is_running = [True]


def switch_state(new_state):
    global current_state, state_initialized
    current_state = new_state
    state_initialized = False  # Reset state  

while is_running[0]:
    time_delta = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running[0] = False

        # Handle UI manager events
        manager.process_events(event)

        # Check button clicks and change states
        if current_state == MENU_STATE:   
            if not state_initialized:
                current_buttons = enter_menu(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT)
                state_initialized = True      
            handle_menu_events(event, current_buttons, switch_state, is_running)
        
        elif current_state == LOGIN_STATE:
            if not state_initialized:
                current_buttons = enter_login(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT)
                state_initialized = True
            handle_login_events(event, current_buttons, switch_state)

        elif current_state == POST_LOGIN_STATE:
            if not state_initialized:
                current_buttons = enter_post_login(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT)
                state_initialized = True
            handle_post_login_events(event, switch_state, current_buttons, is_running)
        
        elif current_state == LEADERBOARD_STATE:
            if not state_initialized:
                current_buttons = enter_leaderboard(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT)
                state_initialized = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == current_buttons[0]:
                switch_state(POST_LOGIN_STATE)

        elif current_state == PLAY:
            if not state_initialized:
                current_buttons = enter_quiz(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT)
                state_initialized = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == current_buttons[0]:
                switch_state(POST_LOGIN_STATE)
        

        

    # Update UI elements based on the state
    manager.update(time_delta)

    # Draw UI based on state
    window_surface.blit(background, (0, 0)) 

    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
