"""
This file, `leaderboard.py` manages the leaderboard screen.

Main Functions:
- **fetch_leaderboard_data**: Retrieves quiz results from the server.
- **get_user_data**: Fetches specific user details using user id from the Users API.
- **enter_leaderboard**: Displays the leaderboard showing player ranks based on cumulative quiz scores.

The leaderboard is sorted by total score in descending order, with each player’s rank, username, and score displayed.
Back button allows users to return to the previous menu.
"""

import pygame
import pygame_gui
from session_manager import SessionManager
from pygame_gui.core import ObjectID
from collections import defaultdict
from settings import LARGE_LABEL_HEIGHT, LARGE_LABEL_WIDTH
from utils import get_api_endpoint

def fetch_leaderboard_data():
    """
    Fetch data from the server from Quiz Result API.
    """
    session = SessionManager.get_session()
    if session:
        response = session.get(get_api_endpoint("quiz_result"))
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch leaderboard data:", response.status_code)
    else:
        print("User is not logged in.")
    return []

def get_user_data(user_id):
    """
    Get user data from users API endpoints
    """
    session = SessionManager.get_session()
    if session:
        response = session.get(f"{get_api_endpoint("get_user")}{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch leaderboard data:", response.status_code)
    else:
        print("User is not logged in.")
    return []



def enter_leaderboard(manager, window_surface, background, SCREEN_WIDTH, SCREEN_HEIGHT):
    """
    Display leaderboard with player rankings.
    """
    manager.clear_and_reset()
    
    # Fetch leaderboard data
    leaderboard_data = fetch_leaderboard_data()

    # Display leaderboard title
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH )// 2, 20), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
        text="Leaderboard",
        manager=manager,
        object_id=ObjectID(class_id='@title_text')
    )
    
    # Display leaderboard items (Example: rank, username, score)
    y_offset = 80  # Starting vertical offset
    
    #Pytthon dict to store sum of student score of all quizzes 
    score_summary = defaultdict(int)
    for entry in leaderboard_data:
        # combine score
        if(entry['student']):
            user_data = get_user_data(entry['student'])
            student = f"{user_data['first_name']} {user_data['last_name']}" if user_data['first_name'] and user_data['last_name'] else user_data['username']
            score = entry['score']
            score_summary[student] += score

    print(score_summary)
    # python lamda func and sorted func to sort in desc order
    sorted_leaderboard = sorted(score_summary.items(), key=lambda x:x[1], reverse=True)
    
    # displaying the leaderboard entries
    for index, (student, total_score) in enumerate(sorted_leaderboard):
        rank_text = f"{index + 1}. {student} - Score: {total_score}"
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(((SCREEN_WIDTH - LARGE_LABEL_WIDTH) // 2, y_offset), (LARGE_LABEL_WIDTH, LARGE_LABEL_HEIGHT)),
            text=rank_text,
            manager=manager,
            object_id=ObjectID(class_id='@subtitle_text')

        )
        y_offset += 40  # Space between entries
        

    # Back button to return to the post-login menu
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 90), (200, 50)),
        text='Back',
        manager=manager
    )

    return [back_button]
