from asyncio import current_task
from gettext import textdomain
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
green = (0, 150, 0)
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
screen.fill((255, 100, 100))
pygame.display.set_caption("Hello")
# canvas = pygame.Surface((X_DIST, Y_DIST))
# canvas.fill((255, 255, 0, 100))
# screen.blit(canvas, (0, 0))

class GameScreen:
    def __init__(self, color=(255, 255, 0, 100), X_DIST=400, Y_DIST=400):
        self.screen=pygame.Surface((X_DIST, Y_DIST))
        self.screen.fill(color)
        self.color=color
        print(color)



    def add_questions(self, question, answerBox, answers,correctIndex):
        question1 = Question(question, self.screen)
        question1.addAnswerBox(answerBox)
        counter=0
        for ans in answers:
            if counter == correctIndex:
                question1.addAnswer(ans,True)
            else:
                question1.addAnswer(ans)
            counter+=1
        self.question = question1

class Game:
    def __init__(self):
        self.screens = []
        self.currentScreenId = 0  # Start from 0 to ensure the first screen is rendered correctly
        self.currentScreen = None
        self.totalMarks=0

    def addScreen(self, question, ansBox,answers,correctIndex, color=(255, 255, 0, 200), X_DIST=400, Y_DIST=400):
        print(color)
        gameScreen= GameScreen( color, X_DIST, Y_DIST)
        self.screens.append(gameScreen)
        gameScreen.add_questions(question, ansBox,answers,correctIndex)
        if len(self.screens) == 1:  # Set the first screen as the current screen
            self.currentScreen = self.screens[0].screen
            self.nextButton = Button(330, 360, "Next", self.screens[len(self.screens) - 1].screen)
            self.backButton = Button(25, 360, "Back", self.screens[len(self.screens) - 1].screen)
            self.color=self.screens[0].color
        return self.screens[len(self.screens)-1].screen

    def toNextScreen(self):
        if self.currentScreenId < len(self.screens)-1:
            self.currentScreenId += 1
            self.currentScreen = self.screens[self.currentScreenId].screen
            self.color=self.screens[self.currentScreenId].color

    def toPrevScreen(self):
        if self.currentScreenId >0:
            self.currentScreenId -= 1
            self.currentScreen = self.screens[self.currentScreenId].screen
            self.color=self.screens[self.currentScreenId].color


    def toScreenById(self, id):
        if id < len(self.screens):
            self.currentScreenId = id
            self.currentScreen = self.screens[self.currentScreenId].screen
            self.color=self.screens[self.currentScreenId].color

    def clearScreen(self):
        if self.currentScreen:
            self.currentScreen.fill(self.color)

    def renderScreen(self, x=0, y=0):
        if self.currentScreen:  # Ensure currentScreen is set
            screen.blit(self.currentScreen, (x, y))
            pygame.display.update()

    def handle_event(self, event):
        for screen in self.screens:
            screen.question.handle_event(event)
        self.nextButton.rectangle.create_rect_with_text(self.currentScreen)
        self.backButton.rectangle.create_rect_with_text(self.currentScreen)
        if (self.nextButton.handle_click(event)):
            self.toNextScreen()
        if (self.backButton.handle_click(event)):
            self.toPrevScreen()
        self.renderScreen()

    def finish_attempt(self):
        for screen in self.screens:
            print(screen)




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
        self.drag =True
        print("moving to",self.initialPosition[0], self.initialPosition[1])
        self._move(self.initialPosition[0], self.initialPosition[1])
        self.drag=False


class Button:
    def __init__(self, x, y, text,canvas, width=30, height=30):
        self.rectangle= Rectangle(x, y, 60, 30, 0, text, light_green, black)
        self.screen= canvas
    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("clicked",event)
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
        self.checkButton = Button(120, 259, "check", self.screen)
        self.resetButton = Button(190, 259, "reset", self.screen)

    def addAnswer(self, answer,isTrue=False):
        answer.create_rect_with_text(self.screen)
        self.answerSet.append(answer)
        if isTrue:
            self.correct_answer_index= len(self.answerSet)-1

    def addAnswerBox(self,answer_box):
        self.answer_box = answer_box


    def handle_event(self,event):
        self.questionRect.create_rect_with_text(self.screen)
        self.answer_box.create_rect_with_text(self.screen)
        self.checkButton.rectangle.create_rect_with_text(self.screen)
        self.resetButton.rectangle.create_rect_with_text(self.screen)
        if (self.checkButton.handle_click(event)):
            self.handle_check_button_submit()
        if(self.resetButton.handle_click(event)):
            self.handle_reset_button_submit()


        for ans in self.answerSet:
            if (not self.answerAdded):
                ans.dragRect(event, [self.answer_box])
            ans.create_rect_with_text(self.screen)


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
            ans.create_rect_with_text(self.screen)

    def showMessage(self, title, message):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo(title, message)
        root.destroy()

def keystroke(game):
    for event in pygame.event.get():
        game.clearScreen()
        game.handle_event(event)
        if event.type == pygame.QUIT:
            game.finish_attempt()
            pygame.quit()
            sys.exit()

#############################################################
#############################################################
#################### SARA ###################################
#############################################################
#############################################################
#############################################################

game1= Game()


question=Rectangle(15, 80, 210, 30, 0, "Drag and fill the space  2, ___ , 6", yellow, blue)
ansBox=Rectangle(180, 80, 30, 30, 1, "", yellow, blue)
answers=[Rectangle(150, 180, 20, 20, 0, "1", magenta, black),
            Rectangle(180, 180, 20, 20, 0, "2", magenta, black),
            Rectangle(210, 180, 20, 20, 0, "3", magenta, black),
            Rectangle(240, 180, 20, 20, 0, "4", magenta, black)]
correctIndex=3
game1.addScreen(question,ansBox, answers, correctIndex, green)


question=Rectangle(15, 15, 180, 30, 0, "Hi Mr. where are You?", yellow, blue)
ansBox=Rectangle(200, 15, 180, 30, 1, "", red, blue)
answers=[Rectangle(10, 180, 75, 30, 1, "Melbourne", blue, red),
            Rectangle(90, 180, 75, 30, 1, "Colombo", blue, red),
            Rectangle(170, 180, 75, 30, 1, "Malabe", blue, red),
            Rectangle(250, 180, 75, 30, 1, "Matara", blue, red)]
correctIndex=0
canvas=game1.addScreen(question,ansBox, answers, correctIndex, blue)


while True:
    keystroke(game1)
    pygame.time.delay(150)
