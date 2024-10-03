# settings.py
import pygame
import pygame_gui

def settings_screen(manager, window_surface, background):
    """
    Settings screen.
    """
    window_surface.blit(background, (0, 0))
    manager.clear_and_reset()

    back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                                               text='Back',
                                               manager=manager)

    title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((300, 100), (200, 50)),
                                        text='Settings',
                                        manager=manager)

    return back_button
