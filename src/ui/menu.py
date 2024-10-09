import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from settings import BTN_WIDTH, BTN_HEIGHT, LABEL_HEIGHT, LABEL_WIDTH, LARGE_LABEL_HEIGHT,LARGE_LABEL_WIDTH


def enter_menu(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
        Initializes the main menu with Login and Quit buttons.
    """
    manager.clear_and_reset()

    # Welcome Message
    welcome_message_title = f"Welcome to Quizora!"
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH)// 2, SCREEN_HEIGHT // 2 - 300), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
        text=welcome_message_title,
        manager=manager,
        object_id=ObjectID(class_id='@title_text')
    )
    welcome_message_subtitle = f"Let the adventure begins!"
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH)// 2, SCREEN_HEIGHT // 2 - 250), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
        text=welcome_message_subtitle,
        manager=manager,
        object_id=ObjectID(class_id='@subtitle_text')
    )

    login_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - BTN_WIDTH) // 2, SCREEN_HEIGHT // 2 - 40), (BTN_WIDTH, BTN_HEIGHT)),
        text='Login',
        manager=manager
    )
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - BTN_WIDTH) // 2, SCREEN_HEIGHT // 2 + 40), (BTN_WIDTH, BTN_HEIGHT)),
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
