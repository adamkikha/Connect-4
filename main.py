from time import sleep
from tkinter import *
from PIL import ImageTk, Image
import pygame
from puzzle import Puzzle
from tree import Tree

NUM_ROW = 6
NUM_COL = 7

# size constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = SCREEN_WIDTH

# back ground color constant
BGROUND_IMG = pygame.image.load("BG.jpg")

pygame.init()

def message(image_name):
    tree_screen = Tk()
    tree_screen.title("State Tree")
    tree_image = Image.open(image_name)
    tkimage = ImageTk.PhotoImage(tree_image)
    image_height = tkimage.height()
    image_width = tkimage.width()

    tree_screen.geometry(str(image_width) + "x" + str(image_height))
    frame = Frame(tree_screen, width = image_width, height = image_height)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)
    frame.pack()
    img = ImageTk.PhotoImage(tree_image)
    label = Label(frame, image = img)
    label.pack()
    tree_screen.update()
    tree_screen.deiconify()
    tree_screen.mainloop()


    # tree_screen.withdraw()

def tree_window(states):
    states = [["123",["1st_state_child1","1st_state_child2","1st_state_child3","1st_state_child4"]],
            ["456",["2nd_state_child1","2nd_state_child2","2nd_state_child3","2nd_state_child4"]],
            ["789",["3rd_state_child"]]
            ]
    tree = Tree(states)
    image_name = tree.png_name +'.'+tree.extension
    message(image_name)



# starting the pygame screen
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# draw the background 
game_screen.blit(BGROUND_IMG,(0,0))
# set the title
pygame.display.set_caption("Connect 4")
# set the logo
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)




puzzle = Puzzle(game_screen, NUM_ROW, NUM_COL, SCREEN_WIDTH, SCREEN_HEIGHT)

running = True # running condition

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if user clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            # store the coordinates of the clicked position
            x_clicked, y_clicked = pygame.mouse.get_pos()
            
            puzzle.play(x_clicked , y_clicked)
            pygame.display.update()
            tree_window(puzzle.state)

        pygame.display.update()
pygame.quit()
