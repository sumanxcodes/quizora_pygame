# states/leaderboard.py
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from collections import defaultdict
from settings import LARGE_LABEL_HEIGHT, LARGE_LABEL_WIDTH
from api import create_update_game_session, fetch_quiz_questions, fetch_quiz_data
from ui.questions_type import display_drag_and_drop, display_fill_in_the_blank, display_multiple_choice



def enter_quiz_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data):
    """
    Display quizzes
    """
    manager.clear_and_reset()
    
    # Fetch quiz data
    state_data['quiz_data'] = fetch_quiz_data()

    # Display quizzes title
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH )// 2, 20), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
        text="Quizzes",
        manager=manager,
        object_id=ObjectID(class_id='@title_text')
    )
    
    btn_gap = 600
    quiz_btns = []
    button_width = 400
    button_height = 50
    vertical_spacing = 60

   # Calculate the x positions for left and right columns, centered on screen
    left_column_x = (SCREEN_WIDTH // 2) - button_width - 20
    right_column_x = (SCREEN_WIDTH // 2) + 20

    # Flag to toggle between columns
    place_in_left_column = True

    # Create buttons for each quiz title in the data
    for quiz in state_data['quiz_data']:
        # Set x position based on current column
        x_position = left_column_x if place_in_left_column else right_column_x

        # Create the button for this quiz
        quiz_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x_position, SCREEN_HEIGHT - btn_gap), (button_width, button_height)),
            text=quiz['title'],
            manager=manager
        )
        # Adding quiz id to quiz button
        quiz_button.quiz_id = quiz['id']

        # Add button to our list to keep track of them
        quiz_btns.append(quiz_button)

        # Toggle to the other column for the next button
        place_in_left_column = not place_in_left_column

        # If we've placed a button in both columns, move down to the next row
        if place_in_left_column:
            btn_gap -= vertical_spacing

        
    # Back button to return to the post-login menu
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 90), (200, 50)),
        text='Back',
        manager=manager
    )
    quiz_btns.append(back_button)

    return quiz_btns

def quiz_question_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data):
    """
    Display quiz title and description with stack and back button
    """
    manager.clear_and_reset()

    # Display quizzes title
    if state_data['question_data'] != None:
        active_quiz_index = state_data['active_quiz_index']
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH )// 2, 20), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
            text=state_data['quiz_data'][active_quiz_index]['title'],
            manager=manager,
            object_id=ObjectID(class_id='@title_text')
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH )// 2, 70), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
            text=state_data['quiz_data'][active_quiz_index]['description'],
            manager=manager,
            object_id=ObjectID(class_id='@subtitle_text')
        )
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH )// 2, 150), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
            text=f"There are {len(state_data['question_data'])} questions in the quiz segments..",
            manager=manager,
            object_id=ObjectID(class_id='@subtitle_text')
        )
    else:
          pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH )// 2, 20), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
            text="No Quiz question data",
            manager=manager,
            object_id=ObjectID(class_id='@title_text')
        )

    start_quiz_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 160), (200, 50)),
        text='Start Quiz',
        manager=manager
    )

     # Back button to return to the quiz menu - enter_quiz_view
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 90), (200, 50)),
        text='Back',
        manager=manager
    )

    return [start_quiz_button, back_button]

def game_session_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data):
    """
    Display quiz related questions
    """
    manager.clear_and_reset()
    # Creating a new game session using gamesession API endpoint
    active_quiz = state_data['quiz_data'][state_data['active_quiz_index']]
    state_data['game_session']['quiz'] = active_quiz['id']
    question_buttons = []

    if (create_update_game_session(state_data['game_session'], state_data['game_session']['id'])):
        # Store session in state_data with session ID for future updates
        question_buttons = show_question_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data)

    # Quit button to return to the quiz menu - enter_quiz_view
    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 90), (200, 50)),
        text='Quit quiz',
        manager=manager
    )
    question_buttons.append(quit_button)
    return question_buttons


def show_question_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data):
    """
    Display the current question based on active_question_index
    """
    # Reset the answer selected flag for the new question
    state_data['answer_selected'] = False

    manager.clear_and_reset()

    # Initialize answer_buttons
    answer_buttons = []

    # Fetch the current question
    questions = state_data['question_data']
    current_index = state_data['active_question_index']
    question = questions[current_index]

    # Display question text
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH) // 2, 20), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
        text=question['question_text'],
        manager=manager,
        object_id=ObjectID(class_id='@question_text')
    )

    # Choose which function to call based on question type
    if question['question_type'] == 'multiple_choice':
        answer_buttons = display_multiple_choice(question, manager, SCREEN_WIDTH, SCREEN_HEIGHT)
    elif question['question_type'] == 'fill_in_the_blank':
        answer_buttons = display_fill_in_the_blank(question, manager, SCREEN_WIDTH, SCREEN_HEIGHT)
    elif question['question_type'] == 'drag_and_drop':
        answer_buttons = display_drag_and_drop(question, manager, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Add a "Next" button to move to the next question
    next_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 160), (200, 50)),
        text="Next",
        manager=manager
    )
    answer_buttons.append(next_button)

    return answer_buttons

def handle_quiz_events(event, switch_state, current_buttons, state_data, is_running):
    """
    Handle menu button click events.
    """
    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        for index, btn in enumerate(current_buttons):
            if event.ui_element == btn:
                state_data['active_quiz_index'] = index
                state_data['question_data'] = fetch_quiz_questions(btn.quiz_id)
                switch_state("question")