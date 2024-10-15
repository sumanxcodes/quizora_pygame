import pygame
import pygame_gui
from pygame_gui.core import ObjectID

def show_summary_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data):
    """
    Display a summary view showing the final score, correct and incorrect answer counts.
    """
    manager.clear_and_reset()

    # Calculate the number of correct and incorrect answers
    total_questions = len(state_data['question_data'])
    correct_answers = state_data['game_session']['correct_answers_count']
    incorrect_answers = total_questions - correct_answers
    final_score = state_data['game_session']['score']

    # Display final score, correct and incorrect answer counts
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - 400) // 2, 100), (400, 50)),
        text="Quiz Summary",
        manager=manager,
        object_id=ObjectID(class_id='@title_text')
    )

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - 400) // 2, 180), (400, 40)),
        text=f"Final Score: {final_score}",
        manager=manager,
        object_id=ObjectID(class_id='@summary_text')
    )

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - 400) // 2, 230), (400, 40)),
        text=f"Correct Answers: {correct_answers}",
        manager=manager,
        object_id=ObjectID(class_id='@summary_text')
    )

    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - 400) // 2, 280), (400, 40)),
        text=f"Incorrect Answers: {incorrect_answers}",
        manager=manager,
        object_id=ObjectID(class_id='@summary_text')
    )

    # Add a button to restart or exit the quiz
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 90), (200, 50)),
        text='Main Menu',
        manager=manager
    )

    return [exit_button]


