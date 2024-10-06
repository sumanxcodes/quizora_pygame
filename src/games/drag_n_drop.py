from tkinter import messagebox
import tkinter as tk

import pygame, sys
from pygame.locals import *
import time

pygame.init()
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
light_green = (144, 238, 144)
grey = (128, 128, 128)
black = (0, 0, 0)
purple = (128, 0, 128)
magenta = (255, 0, 255)
gold = (255, 215, 0)
sky_blue = (135, 206, 235)


X_DIST = 400
Y_DIST = 400
font = pygame.font.SysFont("Arial", 16)
screen = pygame.display.set_mode((X_DIST, Y_DIST))
screen.fill((255, 255, 255))
pygame.display.set_caption("Hello")
canvas = pygame.Surface((X_DIST, Y_DIST))
canvas.fill((255, 255, 0, 100))
screen.blit(canvas, (0, 0))


class Rectangle:
    def __init__(self, x, y, width, height, boader, text, r_color, t_color):
        print("initializing")
        self.rect = pygame.Rect(x, y, width, height)
        self.rect_color = r_color
        self.text_color=t_color
        self.x=x
        self.y=y
        self.width=width
        self.height= height
        self.text=text
        self.boarder=boader
        self.drag=False
        self.blockDragging=False
        self.initialPosition=[x,y]

    def addTextToScreen(self, screen):
        self.screen=screen
        text = font.render(self.text, True, self.text_color)
        if (self.width == 0 and self.height == 0):
            screen.blit(self.text, (self.x, self.y))
        else:
            screen.blit(text, ((self.x + (self.width - text.get_width()) // 2), (self.y + (self.height - text.get_height()) // 2)))

    def create_rect_with_text(self,screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.rect_color, self.rect, self.boarder)
        self.addTextToScreen(screen)


    def _move(self, dx, dy):
        if(not(self.blockDragging) and self.drag):
            self.x = dx
            self.y = dy

    def _enable_dragging(self, event, questionRectBoxes=[]):
        questionBoxes=[]
        for Rect in questionRectBoxes:
            questionBoxes.append(Rect.rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.drag= self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            collideIndex = self.rect.collidelist(questionBoxes)
            if collideIndex ==-1:
                self._move(self.initialPosition[0], self.initialPosition[1])
            else:
                self._move(questionBoxes[collideIndex].x, questionBoxes[collideIndex].y)
            self.drag= False

    def dragRect(self, event, answerBoxes):
        self._enable_dragging(event,answerBoxes)
        self._move(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


    def reset_moves(self):
        print("moving to",self.initialPosition[0], self.initialPosition[1])
        self._move(self.initialPosition[0], self.initialPosition[1])


class Button:
    def __init__(self, x, y, text,canvas, width=30, height=30):
        self.rectangle= Rectangle(x, y, 60, 30, 0, text, light_green, black)

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return  self.rectangle.rect.collidepoint(event.pos)
        return False
#
class Question:
    def __init__(self, questionRect, screen):
        self.answerAdded = False
        self.questionRect=questionRect
        self.answerCorrect=False
        self.answerSet=[]
        self.correct_answer_index= 0
        self.screen=screen
        self.checkButton = Button(120, 259, "check", canvas)
        self.resetButton = Button(190, 259, "reset", canvas)


    def addAnswer(self, answer,isTrue=False):
        answer.create_rect_with_text(canvas)
        self.answerSet.append(answer)
        if isTrue:
            self.correct_answer_index= len(self.answerSet)-1


    def addAnswerBox(self,answer_box):
        self.answer_box = answer_box



    def handle_event(self,event):
        self.questionRect.create_rect_with_text(canvas)
        self.answer_box.create_rect_with_text(canvas)
        self.checkButton.rectangle.create_rect_with_text(canvas)
        self.resetButton.rectangle.create_rect_with_text(canvas)
        if (self.checkButton.handle_click(event)):
            self.handle_check_button_submit()
        if(self.resetButton.handle_click(event)):
            self.handle_reset_button_submit()


        for ans in self.answerSet:
            if (not self.answerAdded):
                ans.dragRect(event, [self.answer_box])
            ans.create_rect_with_text(canvas)


    def handle_check_button_submit(self):
        self.answerAdded=True
        if( self.answer_box.rect.colliderect(self.answerSet[self.correct_answer_index])):
            self.showMessage("WOW", "Fantastic Job!")
            self.answerCorrect=True
        else:
            self.showMessage("Try Again", "It is not !")

    def handle_reset_button_submit(self):
        self.answerCorrect = False
        self.answerAdded=False
        print("reset")
        for ans in self.answerSet:
            ans.reset_moves()
            ans.create_rect_with_text(canvas)

    def showMessage(self, title, message):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo(title, message)
        root.destroy()



def keystroke():
    for event in pygame.event.get():
        clear_screen()
        game(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def clear_screen():
    canvas.fill((255, 255, 0, 100))

def render():
    pygame.display.update()


question1 = Question(Rectangle(15, 15, 200, 30, 0, "Hi how are You?", yellow, blue),canvas)
question1.addAnswerBox(Rectangle(180, 15, 200, 30, 1, "", red, blue))
question1.addAnswer(Rectangle(10, 180, 75, 30, 1, "Fine", blue, red))
question1.addAnswer(Rectangle(90, 180, 75, 30, 1, "Bad", blue, red))
question1.addAnswer(Rectangle(170, 180, 75, 30, 1, "Excellent", blue, red), True)
question1.addAnswer(Rectangle(250, 180, 75, 30, 1, "Natural", blue, red))


def game(event):
    question1.handle_event(event)

while True:
    keystroke()
    screen.blit(canvas, (0, 0))
    render()
    pygame.time.delay(100)