# states/leaderboard.py
import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from api import submit_quiz_result

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
       
        # Set key of the answers in option_id
        option_button.option_id = key 

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
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, 180), (300, 50)),
        manager=manager
    )
    answer_input.option_id = 'user_input'
    answer_buttons.append(answer_input)

    # Submit button
    submit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, 250), (300, 40)),
        text="Submit",
        manager=manager
    )
    submit_button.option_id = 'submit_answer'  # Set an identifier for the submit button
    answer_buttons.append(submit_button)
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


def handle_question_events(event, switch_state, current_buttons, selected_answer, state_data, is_running):
    """
    Handles events for checking the selected answer and updating button colors based on question type.
    """
   # this flag prevent further option button clicks once an answer is selected
    if state_data.get("answer_selected"):
        return  # Block all option button events

    # Get the current question from state data
    current_question_index = state_data['active_question_index']
    current_question = state_data['question_data'][current_question_index]
    
    # Determine question type
    question_type = current_question['question_type']
    correct_answer = current_question['correct_answer']
    correct_option_id = list(correct_answer.keys())[0] if question_type == 'multiple_choice' else None
    
    # Set the selected answer flag once an option is clicked
    state_data['answer_selected'] = True

    # events based on question type
    if question_type == 'multiple_choice':
        handle_multiple_choice(event, current_buttons, selected_answer, correct_option_id, state_data, current_question)
    elif question_type == 'fill_in_the_blank':
        handle_fill_in_the_blank(event, current_buttons, correct_answer, state_data, current_question)
    elif question_type == 'drag_and_drop':
        handle_drag_and_drop(event, selected_answer, correct_answer, state_data, current_question)
    
    print(state_data['game_session'])
    # checkss if there are more questions or end the quiz
    if current_question_index < len(state_data['question_data']) - 1:
        state_data['active_question_index'] += 1  # Move to the next question
    else:
       print("<<<<END OF quiZZ>>>>")
       print(state_data)
       submit_quiz_result(state_data)
       switch_state("summary") # Summry page when quiz ends

def handle_multiple_choice(event, current_buttons, selected_answer, correct_option_id, state_data, current_question):
    """
    Handles multiple-choice question logic, updates button colors based on correct/incorrect answers.
    """
    
    for button in current_buttons[:-2]:  
        # Disable all option buttons except the last two (Next and Quit)
        button.is_interactable = False
        # Highlight correct and incorrect answers
        if getattr(button, 'option_id', None) == correct_option_id:
            button.set_text(f"{button.text} (Correct)")
            button.colours['normal_bg'] = pygame.Color("#008000")  # Green for correct answer
        else:
            button.set_text(f"{button.text} (Incorrect)")
            button.colours['normal_bg'] = pygame.Color("#FF0000")  # Red for incorrect answers
        button.rebuild()

    # Update score if selected answer is correct
    print("???? bahira")
    print(selected_answer)
    print(correct_option_id)
    if selected_answer == correct_option_id:
        print(f"???? Correct ---- {current_question['points']}")
        print(current_question.get('points', 1) )
        state_data['game_session']['correct_answers_count'] += 1
        state_data['game_session']['score'] += current_question.get('points', 1) 
    

def handle_fill_in_the_blank(event, current_buttons, correct_answer, state_data, current_question):
    """
    Checks the answer for fill-in-the-blank questions.
    """
    # Get the text entry field and submit button from the current buttons
    answer_input = next((btn for btn in current_buttons if getattr(btn, 'option_id', None) == 'user_input'), None)
    submit_button = next((btn for btn in current_buttons if getattr(btn, 'option_id', None) == 'submit_answer'), None)

    # Check if the submit button was pressed
    if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == submit_button:
        user_answer = answer_input.get_text().strip().lower()
        correct_answer_text = correct_answer['blank'].strip().lower()
        submit_button.is_interactable = False
        # Check if the answer is correct
        if user_answer == correct_answer_text:
            print("Correct answer!")
            state_data['game_session']['correct_answers_count'] += 1
            state_data['game_session']['score'] += current_question.get('points', 1) 
            submit_button.set_text("Correct")
            submit_button.is_interactable = False
            submit_button.colours['normal_bg'] = pygame.Color("#008000")  # Green for correct
        else:
            print("Incorrect answer.")
            submit_button.set_text("Incorrect")
            submit_button.is_interactable = False
            submit_button.colours['normal_bg'] = pygame.Color("#FF0000") 
            
        submit_button.rebuild()  # Update the button with new text/color

def handle_drag_and_drop(event, selected_answer, correct_answer, state_data, current_question):
    """
    Checks the answer for drag-and-drop questions.
    """
    if selected_answer == correct_answer:
        print("Correct answer!")
        state_data['game_session']['score'] += current_question.get('points', 1) 
    else:
        print("Incorrect answer. Please try again.")