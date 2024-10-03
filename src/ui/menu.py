# menu.py
import pygame
import pygame_gui
from pygame_gui.core import ObjectID

def main_menu(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Display main menu options with dynamic positioning based on screen size.
    """
    window_surface.blit(background, (0, 0))
    manager.clear_and_reset()

    # Title Label
    title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 4 - 70), (600, 100)),
        text='Welcome to Quizora',
        manager=manager,
        object_id=ObjectID(class_id='@title_text', object_id='#main_page_title')
    )
    
    # Subtitle Label
    sub_title = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 4), (400, 50)),
        text='The Ultimate Quiz Game',
        manager=manager,
        object_id=ObjectID(class_id='@subtitle_text', object_id='#main_page_subtitle')
    )

    # Play Button
    play_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (200, 50)),
        text='Login',
        manager=manager,
        object_id=ObjectID(class_id="@menu_buttons", object_id="#play_button")
    )

    # Quit Button
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80), (200, 50)),
        text='Quit',
        manager=manager,
        object_id=ObjectID(class_id="@menu_buttons", object_id="#quit_button")
    )

    return play_button, quit_button
