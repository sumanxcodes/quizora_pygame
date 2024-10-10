import pygame
import sys
import random

pygame.init()

# Colors
BLACK = (0, 0, 0)
Yellow = (255, 255, 0)
DARK_Yellow = (200, 200, 0)
WHITE = (255, 255, 255)


screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Start Quiz Button")

font = pygame.font.SysFont(None, 48)

def render_text(text, font, color):
    return font.render(text, True, color)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.clicked = False
        
    
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Change color on hover
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
            if mouse_pressed[0]:
                self.clicked = True
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # text on the button
        text_surf = render_text(self.text, font, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class Particle:
    def __init__(self):
        # position for the particle
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        # speed and direction
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.speed_y = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.radius = random.randint(2, 5)
        self.color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)) # Soft color

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

   
        if self.x < 0: 
            self.x = screen_width
        if self.x > screen_width: 
            self.x = 0
        if self.y < 0: 
            self.y = screen_height
        if self.y > screen_height: 
            self.y = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# Main function
def main():
    clock = pygame.time.Clock()

    # Start Quiz button
    button = Button(x=screen_width//2 - 100, y=screen_height//2 - 50, width=200, height=100, text="Start Quiz", color=Yellow, hover_color=DARK_Yellow)

    # particles for background animation
    particles = [Particle() for _ in range(50)]  

    running = True
    while running:
        screen.fill(BLACK)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

      
        for particle in particles:
            particle.move()
            particle.draw(screen)

    
        button.draw(screen)

       
        if button.clicked:
            print("Quiz Starting...")
            running = False  

        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
