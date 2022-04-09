from time import time
from tkinter import *
import pygame
import sys
from agent import Agent
from puzzle import Puzzle
from tree import Tree
from buttons import Button

NUM_ROW = 6
NUM_COL = 7

# size constants
SCREEN_WIDTH = 670
SCREEN_HEIGHT = SCREEN_WIDTH + 50
SIDES_PADDING = 10

WHITE = (255, 255, 255)
BG_COLOR = WHITE
# back ground color constant
BGROUND_IMG = pygame.image.load("new_BG.jpg")


# properties of buttons
# TEXT_COLOR = (150,150,150)
TEXT_COLOR = WHITE
BUTTONS_COLOR = (0,0,0)
BUTTON_WIDTH = SCREEN_WIDTH - (2* SIDES_PADDING)
BUTTON_HEIGHT = 120
FONT_SIZE1 = 50
FONT_SIZE2 = 30



# windows variables
# start_player checks if player or AI
start_players = None
# agent_selected store the selected agent  
pruning_selected = None


# start window contains two buttons play and AI
def start_window():
    global start_players
    game_screen.blit(BGROUND_IMG,(0, 0))
    buttons = []
    player_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR,"            Player VS Player",TEXT_COLOR,FONT_SIZE1)
    player_button.draw(game_screen)
    buttons.append(player_button)
    AI_button = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100 + 50 + BUTTON_HEIGHT + SIDES_PADDING, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR,"              Player VS AI",TEXT_COLOR,FONT_SIZE1)
    AI_button.draw(game_screen)
    buttons.append(AI_button)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            start_players = True
                            return
                        if i == 1:
                            start_players = False
                            return
                
            pygame.display.update()
    pygame.quit()

# AI window contains Two Buttons: Alpha beta pruning and no pruning
def AI_window():
    global pruning_selected
    game_screen.blit(BGROUND_IMG,(0, 0))
    buttons = []
    pruning = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-100, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," Alpha-Beta pruning",TEXT_COLOR,FONT_SIZE1)
    pruning.draw(game_screen)
    buttons.append(pruning)
    no_pruning = Button((SCREEN_WIDTH//2)-(BUTTON_WIDTH//2), (SCREEN_HEIGHT//2)-(BUTTON_HEIGHT//2)-50 + BUTTON_HEIGHT + SIDES_PADDING, BUTTON_WIDTH,BUTTON_HEIGHT,BUTTONS_COLOR," Without Pruning",TEXT_COLOR,FONT_SIZE1)
    no_pruning.draw(game_screen)
    buttons.append(no_pruning)
    start_button = Button(SCREEN_WIDTH//5, SCREEN_HEIGHT - BUTTON_HEIGHT - SIDES_PADDING, BUTTON_WIDTH*3/5,BUTTON_HEIGHT,(0,0,40),"  Player Starts",TEXT_COLOR,FONT_SIZE1)
    start_button.draw(game_screen)
    buttons.append(start_button)
    I_start = True
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_clicked,y_clicked = pygame.mouse.get_pos()
                for i in range(len(buttons)):
                    if buttons[i].check_clicked(x_clicked, y_clicked):
                        if i == 0:
                            pruning_selected = True
                            return I_start
                        if i == 1:
                            pruning_selected = False
                            return I_start
                        if i == 2:
                            I_start = not I_start
                            if I_start:
                                start_button.draw(game_screen,"  Player Starts")
                                break
                            else:
                                start_button.draw(game_screen,"     AI Starts")
                                break
            pygame.display.update()
    pygame.quit()


def tree_window(states):
    if Tree.current_tk:
        Tree.current_tk.destroy()
    tree = Tree(states)
    image_name = tree.png_name +'.'+tree.extension
    tree.display(image_name)



pygame.init()
# starting the pygame screen
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# draw the backgroun
#game_screen.fill(BG_COLOR)
# game_screen.blit(BGROUND_IMG,(0,0))
# set the title
pygame.display.set_caption("Connect 4")
# set the logo
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)



start_window()
if start_players:
    #game_screen.fill(BG_COLOR)
    # playing_circle = Circle(game_screen, puzzle.circles[0].x_pos, puzzle.circles[0].y_pos - puzzle.diameter-10, puzzle.player1_color, puzzle.diameter/2)
    # playing_circle.draw()
    
    puzzle = Puzzle(game_screen, NUM_ROW, NUM_COL, SCREEN_WIDTH, SCREEN_HEIGHT)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if event.type == pygame.MOUSEMOTION:
            #     x_hovered, y_hovered = pygame.mouse.get_pos()
            #     if x_hovered > puzzle.circles[0].x_pos and x_hovered < puzzle.circles[NUM_COL-1].x_pos:
            #         clear_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 140)
            #         #pygame.draw.rect(game_screen, BG_COLOR, clear_rect)
            #         # playing_circle.change_pos(x_hovered, puzzle.circles[0].y_pos - puzzle.diameter-10)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # store the coordinates of the clicked position
                x_clicked, y_clicked = pygame.mouse.get_pos()
                puzzle.play(x_clicked , y_clicked)
                
                pygame.display.update()
                # if puzzle.player_turn == '1': tree_window(copy(puzzle.states))

            pygame.display.update()
else:
    I_start = AI_window()
    puzzle = Puzzle(game_screen, NUM_ROW, NUM_COL, SCREEN_WIDTH, SCREEN_HEIGHT)
    agent = Agent(puzzle)
    if pruning_selected:
        minmax = agent.prune_minmax
    else:
        minmax = agent.minmax
    tree = True
    k = 3
    max = False
    buttons = []
    tree_button = Button(SCREEN_WIDTH*2/5+10, 10,SCREEN_WIDTH*1/5-20,50,(0,0,40),"  Tree = ON",TEXT_COLOR,20)
    tree_button.draw(game_screen)
    buttons.append(tree_button)
    plus_button = Button(SCREEN_WIDTH*2/5+90, 80,35,35,(0,0,40)," +",TEXT_COLOR,25)
    plus_button.draw(game_screen)
    buttons.append(plus_button)
    minus_button = Button(SCREEN_WIDTH*2/5+10, 80,35,35,(0,0,40),"  -",TEXT_COLOR,25)
    minus_button.draw(game_screen)
    buttons.append(minus_button)
    k_button = Button(SCREEN_WIDTH*2/5+50,80,35,35,(0,0,0),str(k),TEXT_COLOR,25)
    k_button.draw(game_screen)
    if not I_start:
        max = True
        ts = time()
        index , _ , _ = minmax(puzzle.current_state,k,max,puzzle.playable)
        print("time taken = ",time()-ts," s")
        print("Number of expanded nodes = " , str(len(agent.parent_map.keys())))
        puzzle.play_piece(index)
        if tree:
            tree_window(agent.parent_map)
    while not puzzle.Complete:
        pygame.display.update()
        played = False
        while not played:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # if event.type == pygame.MOUSEMOTION:
                #     x_hovered, y_hovered = pygame.mouse.get_pos()
                #     if x_hovered > puzzle.circles[0].x_pos and x_hovered < puzzle.circles[NUM_COL-1].x_pos:
                #         clear_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 140)
                #         #pygame.draw.rect(game_screen, BG_COLOR, clear_rect)
                #         # playing_circle.change_pos(x_hovered, puzzle.circles[0].y_pos - puzzle.diameter-10)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # store the coordinates of the clicked position
                    x_clicked, y_clicked = pygame.mouse.get_pos()
                    Clicked = False
                    for i in range(len(buttons)):
                        if buttons[i].check_clicked(x_clicked, y_clicked):
                            Clicked = True
                            if i == 0:
                                tree = not tree
                                if tree:
                                    tree_button.draw(game_screen,"  Tree = ON")
                                else:
                                    tree_button.draw(game_screen,"  Tree = OFF")
                            if i == 1:
                                k += 1
                                k_button.draw(game_screen," "+str(k))
                                if k == 2:
                                    minus_button.draw(game_screen)
                            if i == 2:
                                if k > 1:
                                    k -= 1
                                    k_button.draw(game_screen," "+str(k))
                                    if k == 1:
                                        minus_button.draw(game_screen,color=(170,0,0))
                            pygame.display.update()
                    if not Clicked:
                        if puzzle.play(x_clicked , y_clicked):
                            played = True
        pygame.display.update()
        if puzzle.Complete:
            break
        agent.parent_map = dict()
        ts = time()
        index , _ , _= minmax(puzzle.current_state,k,max,puzzle.playable)
        print("time taken = ",time()-ts," s")
        puzzle.play_piece(index)
        pygame.display.update()
        if tree:
            tree_window(agent.parent_map)
    while True:
        for event in pygame.event.get([pygame.QUIT]):
            pygame.quit()
            sys.exit()