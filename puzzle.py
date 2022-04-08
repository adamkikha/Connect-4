from copy import copy
import pygame
from circles import Circle
from PIL import Image

# screen constants
SIDES_PADDING = 10
UPPER_PADDING = 150
LOWER_PADDING = 10
INBTWN_SPACE = 4

WIN_CONNECTION = 4
# blocks constants
# CIRCLE_COLOR = (200,200,200)
CIRCLE_COLOR = (255,255,255)
RECT_COLOR = (0,0,139)
PLAYER1_COLOR = (12, 90, 55)
PLAYER2_COLOR = (120, 9, 5)
BOARD_IMG = pygame.image.load("3D Board.png")


class Puzzle:
    def __init__(self, screen, num_row, num_col, screen_width, screen_height):
        self.screen = screen
        self.circles = [] # array of obj
        self.playable = [] # array of ints
        self.occupied = [] # array of ints
        self.states = []
        # self.clickable_ranges = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_row = num_row
        self.num_col = num_col
        self.current_state = '0' * (self.num_row * self.num_col)
        self.states.append(self.current_state)

        self.player1 = '1'
        self.player2 = '2'
        self.player1_image = None
        self.player2_image = None
        self.player1_score = 0
        self.player2_score = 0
        self.player_turn = '1'

        self.rect = None
        # calculate the block width and height depending on the screen width and height
        self.diameter = ((self.screen_width - (2 * SIDES_PADDING)) - ((self.num_col-1) * INBTWN_SPACE)) / self.num_col

        self.create_circles()
        self.generate_playable()
        self.adjust_image()



# create_rects creates the blocks of the game
    def create_circles(self):
        # initial cordinates of the first block
        x = SIDES_PADDING + self.diameter/2
        y = UPPER_PADDING + self.diameter/2
        BGROUND_IMG = pygame.image.load("BG.jpg")
        self.screen.blit(BGROUND_IMG,(0, 0))
        #self.screen.blit(BOARD_IMG,(0,0))
        self.rect = pygame.Rect(SIDES_PADDING-5, UPPER_PADDING-20, self.screen_width-(2*SIDES_PADDING)+10, self.screen_height - UPPER_PADDING - LOWER_PADDING)
        pygame.draw.rect(self.screen, RECT_COLOR, self.rect)
        
        for _ in range(0, self.num_row):
            for _ in range(0, self.num_col):
                circle = Circle(self.screen, x, y, CIRCLE_COLOR, self.diameter/2)
                circle.draw()
                self.circles.append(circle)
                x = x + self.diameter + INBTWN_SPACE
            x = SIDES_PADDING + self.diameter/2
            y = y + self.diameter + INBTWN_SPACE


    def generate_playable(self):
        temp = []
        for i in range(self.num_col):
            inc = i 
            for j in range(self.num_row):
                temp.append(inc)
                inc += self.num_col
            self.playable.append(copy(temp))
            temp.clear()


    def adjust_image(self):
        redchip = Image.open("redchip.png")
        smallred = redchip.resize((int(self.diameter), int(self.diameter)))
        smallred.save("new_red.png")
        self.player1_image = pygame.image.load("new_red.png")

        yellochip = Image.open("yellowchip.png")
        smallyellow = yellochip.resize((int(self.diameter), int(self.diameter)))
        smallyellow.save("new_yellow.png")
        self.player2_image = pygame.image.load("new_yellow.png")



    def get_col_clicked(self, x_clicked, y_clicked):
        last_circle_index = (self.num_col * self.num_row) -1
        y_end = self.circles[last_circle_index].y_pos + (self.diameter/2)
        for i in range(self.num_col):
            x_start = self.circles[i].x_pos - (self.diameter/2)
            x_end = self.circles[i].x_pos + (self.diameter/2)
            y_start = self.circles[i].y_pos - (self.diameter/2)
            if( x_clicked >= x_start
            and x_clicked < x_end
            and y_clicked >= y_start
            and y_clicked < y_end):
                return i

    def drop_piece(self, x_clicked, y_clicked, image, owner):
        col_index = self.get_col_clicked(x_clicked, y_clicked)
        if col_index != None:
            if self.playable[col_index]:
                circle_index = max(self.playable[col_index])
                self.circles[circle_index].update(owner, image)
                self.playable[col_index].remove(circle_index)
                self.occupied.append(circle_index)
                self.update_state(circle_index, owner)
                return True
            else:
                return False

    def update_state(self, index, player):
        self.current_state = list(self.current_state)
        self.current_state[index] = player
        self.current_state = "".join(self.current_state)
        self.states.append(self.current_state)

    def get_score(self):
        counter = 0
        i = 0
        while i <= (self.num_col*self.num_row)-1:
            while i <= (self.num_col*self.num_row)-1 and self.current_state[i] == self.player1:
                counter += 1
                i += 1
            # print("1_counter: "+ str(counter))
            self.calc_score(counter, self.player1)
            counter = 0
            while i <= (self.num_col*self.num_row)-1 and self.current_state[i] == self.player2 :
                counter += 1
                i += 1
            # print("2_counter: "+ str(counter))
            self.calc_score(counter, self.player2)
            counter = 0

    def calc_score(self, sequence_len, player):
        if sequence_len >= WIN_CONNECTION:
            score = 1 + (sequence_len- WIN_CONNECTION)
            # print(player,"score ",score)
            if player == '1':
                self.player1_score += score
            elif player == '2':
                self.player2_score += score


    def play(self, x_clicked, y_clicked):

        if self.player_turn == self.player1:
            switch_player = self.drop_piece(x_clicked, y_clicked, self.player1_image, self.player_turn)
            if switch_player: 
                self.player_turn = self.player2
                print(self.current_state)

        elif self.player_turn == self.player2:
            switch_player = self.drop_piece(x_clicked, y_clicked, self.player2_image, self.player_turn)
            if switch_player:
                self.player_turn = self.player1
                print(self.current_state)

        if len(self.occupied) == self.num_col*self.num_row:
            print("calc score")
            self.get_score()
            print("player 1 score: "+ str(self.player1_score)+" \nplayer 2 score: "+ str(self.player2_score))




