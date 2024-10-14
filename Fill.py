import pygame
import sys

pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Basic Math Fill-in-the-Blanks')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 36)

# box class
class InputBox:
    def __init__(self, x, y, w, h, answer):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = ''
        self.answer = str(answer)  # correct answer as a string for comparison
        self.active = False
        self.correct = None  # True/False for correct/incorrect, None if unanswered

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on the input box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = GRAY if self.active else BLACK

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Check if the answer is correct
                    if self.text == self.answer:
                        self.correct = True
                    else:
                        self.correct = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
       
        txt_surface = font.render(self.text, True, self.color)
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # correct/incorrect
        if self.correct is not None:
            if self.correct:
                feedback = font.render("Correct!", True, GREEN)
            else:
                feedback = font.render("Incorrect. Try again.", True, RED)
            screen.blit(feedback, (self.rect.x, self.rect.y + 40))

class Question:
    def __init__(self, question_text, answer):
        self.question_text = question_text
        self.answer = answer

#  questions
math_questions = [
    Question("Solve: 5 + 3 =", 8),
    Question("Solve: 10 - 6 =", 4),
    Question("Solve: 4 * 3 =", 12),
    Question("Solve: 12 / 4 =", 3),
    Question("Solve: 7 + 2 =", 9),
    Question("Solve: 9 - 3 =", 6),
    Question("Solve: 6 * 2 =", 12),
    Question("Solve: 16 / 2 =", 8),
]

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True

    current_index = 0
    current_question = math_questions[current_index]
    input_box = InputBox(350, 150, 140, 32, current_question.answer)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

          
            input_box.handle_event(event)

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Move to the next question
                    current_index = (current_index + 1) % len(math_questions)
                    current_question = math_questions[current_index]
                    input_box = InputBox(350, 150, 140, 32, current_question.answer)
                elif event.key == pygame.K_LEFT:
                    # Move to the previous question
                    current_index = (current_index - 1) % len(math_questions)
                    current_question = math_questions[current_index]
                    input_box = InputBox(350, 150, 140, 32, current_question.answer)

        screen.fill(WHITE)
        
       
        question_text = font.render(current_question.question_text, True, BLACK)
        instructions_text = font.render("Use LEFT/RIGHT to navigate questions", True, BLACK)
        
        screen.blit(question_text, (50, 150))
        screen.blit(instructions_text, (50, 500))

        
        input_box.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()