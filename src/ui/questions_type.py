# states/leaderboard.py
import pygame
import pygame_gui
from pygame_gui.core import ObjectID

def display_multiple_choice(question, manager, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    display multiple-choice options in two columns with larger buttons...
    """
    left_column_x = (SCREEN_WIDTH // 2) - 270  # Left column x-position
    right_column_x = (SCREEN_WIDTH // 2) + 70  # Right column x-position
    button_width = 300
    button_height = 60
    vertical_spacing = 80
    y_offset = 120  #  vertical position
    answer_buttons = []
    place_in_left_column = True  # Toggle between columns

    for key, value in question['options'].items():
        x_position = left_column_x if place_in_left_column else right_column_x

        option_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x_position, y_offset), (button_width, button_height)),
            text=f"{key}: {value}",
            manager=manager
        )
        answer_buttons.append(option_button)

        # Switch to the other column for the next button
        place_in_left_column = not place_in_left_column
        if place_in_left_column:
            y_offset += vertical_spacing  # Move down for the next row

    return answer_buttons



def display_fill_in_the_blank(question, manager, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    display a text entry field for fill-in-the-blank questions.
    """
    answer_buttons = []
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, 120), (300, 50)),
        text="Enter your answer:",
        manager=manager,
        object_id=ObjectID(class_id='@subtitle_text')
    )
    answer_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, 180), (200, 50)),
        manager=manager
    )
    answer_buttons.append(answer_input)
    return answer_buttons


def display_drag_and_drop(question, manager, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    display drag-and-drop elements for drag-and-drop questions.
    """
    answer_buttons = []
    y_offset = 100
    # For demonstration, add draggable items and target locations
    for index, (key, value) in enumerate(question['options'].items()):
        draggable_item = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, y_offset), (200, 50)),
            text=f"{value}",
            manager=manager,
            object_id=ObjectID(class_id='@draggable_item')
        )
        answer_buttons.append(draggable_item)
        y_offset += 60
    return answer_buttons


def handle_question_events(event, switch_state, current_buttons, state_data, is_running):
    pass