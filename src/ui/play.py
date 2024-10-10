# states/leaderboard.py
import pygame
import pygame_gui
from session_manager import SessionManager
from pygame_gui.core import ObjectID
from collections import defaultdict
from settings import LARGE_LABEL_HEIGHT, LARGE_LABEL_WIDTH
from utils import get_api_endpoint

def fetch_quiz_data():
    """
    Fetch data from the server from Quiz Result API.
    """
    session = SessionManager.get_session()
    if session:
        response = session.get(get_api_endpoint("quizzes"))
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch quiz data:", response.status_code)
    else:
        print("User is not logged in.")
    return []

def enter_quiz(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Display leaderboard with player rankings.
    """
    manager.clear_and_reset()
    
    # Fetch quiz data
    quiz_data = fetch_quiz_data()

    # Display leaderboard title
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH )// 2, 20), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
        text="Quiz",
        manager=manager,
        object_id=ObjectID(class_id='@title_text')
    )
    print(quiz_data)
    
    btn_gap = 600
    for quiz in quiz_data:
        print(quiz['title'])
        pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - btn_gap), (200, 50)),
        text= quiz['title'],
        manager=manager)
        btn_gap -= 60
        
    # Back button to return to the post-login menu
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 90), (200, 50)),
        text='Back',
        manager=manager
    )

    return [back_button]
