# main.py
import os
import pygame
import pygame_gui
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.menu import enter_menu, handle_menu_events
from ui.login import enter_login, handle_login_events
from ui.post_login import enter_post_login, handle_post_login_events
from ui.leaderboard import enter_leaderboard
from ui.play import enter_quiz_view, handle_quiz_events, quiz_question_view, game_session_view
from ui.questions_type import handle_question_events
from ui.summary import show_summary_view


# Initialize Pygame
pygame.init()

# Set up display
pygame.display.set_caption("Quizora")
window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill(pygame.Color('#141414'))

theme_path = 'src/theme.json'

# Check if the theme file exists
if os.path.exists(theme_path):
    print("Loading theme file:", theme_path)
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path)
else:
    print("Theme file not found. Using default theme.")
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT)) 



# Set up UI manager
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), theme_path)

# Game clock
clock = pygame.time.Clock()

# States and state data
state_data = {
   "user_info": None,
   "quiz_data": None,
   "question_data": None,
   "active_quiz_index": None,
   "active_question_index": 0,
   "game_session": {
        'id': None,
        'quiz': None,
        'duration': '00:00:00',
        'status': 'in_progress',
        'score': 0,
        'correct_answers_count': 0
    },
   "game_session_id": None,
   'answer_selected': False
}

# States for different screens
MENU_STATE = "menu"
LOGIN_STATE = "login"
POST_LOGIN_STATE = "post_login"
QUIT_STATE = "quit"
LEADERBOARD_STATE = "leaderboard"
PLAY_STATE = "play"
QUESTION_STATE = "question"
GAME_SESSION_STATE = "game_session"
SUMMARY_STATE = "summary"

# Initial state
current_state = MENU_STATE
current_buttons = []
state_initialized = False  # flag to control state initilization
is_running = [True]

def clear_game_session_data(state_data):
    """
    Clear game session-related data 
    """
    state_data["question_data"] = None
    state_data["active_quiz_index"] = 0
    state_data["active_question_index"] = 0
    state_data["answer_selected"] = False
    state_data["game_session"] =  {
        'id': None,
        'quiz': None,
        'duration': '00:00:00',
        'status': 'in_progress',
        'score': 0,
        'correct_answers_count': 0
    }
    state_data["game_session_id"] = ''


def switch_state(new_state):
    global current_state, state_initialized
    current_state = new_state
    state_initialized = False  # Reset state  

while is_running[0]:
    time_delta = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running[0] = False

        # Handle UI manager events
        manager.process_events(event)

        # Check button clicks and change states
        if current_state == MENU_STATE:   
            if not state_initialized:
                current_buttons = enter_menu(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT)
                state_initialized = True      
            handle_menu_events(event, current_buttons, switch_state, is_running)
        
        elif current_state == LOGIN_STATE:
            if not state_initialized:
                current_buttons = enter_login(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT)
                state_initialized = True
            handle_login_events(event, current_buttons, switch_state)

        elif current_state == POST_LOGIN_STATE:
            if not state_initialized:
                current_buttons = enter_post_login(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data)
                state_initialized = True
            handle_post_login_events(event, switch_state, current_buttons, is_running)
        
        elif current_state == LEADERBOARD_STATE:
            if not state_initialized:
                current_buttons = enter_leaderboard(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT)
                state_initialized = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == current_buttons[0]:
                switch_state(POST_LOGIN_STATE)

        elif current_state == PLAY_STATE:
            if not state_initialized:
                current_buttons = enter_quiz_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data)
                state_initialized = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == current_buttons[-1]: # Last button is back button
                switch_state(POST_LOGIN_STATE)
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element != current_buttons[-1]:
                handle_quiz_events(event, switch_state, current_buttons, state_data, is_running)

        elif current_state == QUESTION_STATE:
            if not state_initialized:
                current_buttons = quiz_question_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data)
                state_initialized = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == current_buttons[1]:
                switch_state(PLAY_STATE)
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == current_buttons[0]:
                switch_state(GAME_SESSION_STATE)

        elif current_state == GAME_SESSION_STATE:
            if not state_initialized:
                current_buttons = game_session_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data)
                state_initialized = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # check back button is clicked
                if event.ui_element == current_buttons[-1]:  # quit button
                    clear_game_session_data(state_data)
                    switch_state(POST_LOGIN_STATE)
                elif event.ui_element == current_buttons[-2]:  # next button
                    switch_state(GAME_SESSION_STATE)
                # any options button  clicked
                else:
                    # check the user selected answers 
                    for btn in current_buttons:
                        if event.ui_element == btn:
                            selected_answer = getattr(btn, 'option_id', None)
                            handle_question_events(event, switch_state, current_buttons, selected_answer, state_data, is_running)
                            break  
        elif current_state == SUMMARY_STATE:
            print("Summary state")
            if not state_initialized:
                current_buttons = show_summary_view(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT, state_data)
                state_initialized = True
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == current_buttons[0]:  # Exit button
                clear_game_session_data(state_data)
                switch_state(POST_LOGIN_STATE)

    # Update UI elements based on the state
    manager.update(time_delta)

    # Draw UI based on state
    window_surface.blit(background, (0, 0)) 

    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
