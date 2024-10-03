# main.py
import pygame
import pygame_gui
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.menu import main_menu
from ui.play import play_screen
from ui.settings import settings_screen

# Initialize Pygame
pygame.init()

# Set up display
pygame.display.set_caption("Quizora")
window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(pygame.Color('#000000'))

# Set up UI manager
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme.json')

# Game clock
clock = pygame.time.Clock()

# States for different screens
MENU_STATE = "menu"
LOGIN_STATE = "login"
PLAY_STATE = "play"
SETTINGS_STATE = "settings"
QUIT_STATE = "quit"

# Initial state
current_state = MENU_STATE
current_buttons = []


# Main game loop
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Handle UI manager events
        manager.process_events(event)

        # Check button clicks and change states
        if current_state == MENU_STATE:
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == current_buttons[0]:
                    current_state = PLAY_STATE  # Switch to Play screen
                elif event.ui_element == current_buttons[1]:
                    current_state = SETTINGS_STATE  # Switch to Settings screen
                elif event.ui_element == current_buttons[2]:
                    is_running = False  # Quit game
        elif current_state == PLAY_STATE or current_state == SETTINGS_STATE:
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == current_buttons[0]:
                    current_state = MENU_STATE  # Back to menu

    # Update UI elements based on the state
    manager.update(time_delta)

    # Draw UI based on state
    if current_state == MENU_STATE:
        current_buttons = main_menu(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT)
    elif current_state == PLAY_STATE:
        current_buttons = play_screen(manager, window_surface, background)
    elif current_state == SETTINGS_STATE:
        current_buttons = settings_screen(manager, window_surface, background)

    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
