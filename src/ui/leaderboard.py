# states/leaderboard.py
import pygame
import pygame_gui
from session_manager import SessionManager
from collections import defaultdict

def fetch_leaderboard_data():
    """
    Fetch data from the server from Quiz Result API.
    """
    session = SessionManager.get_session()
    if session:
        response = session.get('http://localhost:8000/api/quizresults/')
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
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, 20), (200, 50)),
        text="Leaderboard",
        manager=manager
    )
    
    # Display leaderboard items (Example: rank, username, score)
    y_offset = 80  # Starting vertical offset
    
    #Pytthon dict to store sum of student score of all quizzes 
    score_summary = defaultdict(int)
    for entry in leaderboard_data:
        # combine score
        student = entry['student']
        score = entry['score']
        score_summary[student] += score

    print(score_summary)
    # python lamda func and sorted func to sort in desc order
    sorted_leaderboard = sorted(score_summary.items(), key=lambda x:x[1], reverse=True)
    
    # displaying the leaderboard entries
    for index, (student, total_score) in enumerate(sorted_leaderboard):
        rank_text = f"{index + 1}. {student} - Score: {total_score}"
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, y_offset), (300, 30)),
            text=rank_text,
            manager=manager
        )
        y_offset += 40  # Space between entries
        

    # Back button to return to the post-login menu
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70), (200, 50)),
        text='Back',
        manager=manager
    )

    return [back_button]
