# states/post_login.py
import pygame
import pygame_gui

def enter_post_login(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Initializes the post-login menu with Play Quiz, Help, Leaderboard, and Quit buttons.
    """
    manager.clear_and_reset()
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

def handle_post_login_events(event, current_buttons, is_running):
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
        elif event.ui_element == current_buttons[3]:  # Quit button
            is_running[0] = False
