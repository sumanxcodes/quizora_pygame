import pygame
import pygame_gui
from pygame_gui.core import ObjectID


def enter_menu(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
        Initializes the main menu with Login and Quit buttons.
    """
    manager.clear_and_reset()

    login_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40), (200, 50)),
        text='Login',
        manager=manager
    )
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40), (200, 50)),
        text='Quit',
        manager=manager
    )
    return [login_button, quit_button]


def handle_menu_events(event, current_buttons, switch_state, is_running):
    """
    Handle menu button click events.
    """
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if event.ui_element == current_buttons[0]:  # Login button
            switch_state("login")
        elif event.ui_element == current_buttons[1]:  # Quit button
            is_running[0] = False 
