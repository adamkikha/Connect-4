from copy import copy
import pygame
from circles import Circle


# screen constants
SIDES_PADDING = 10
UPPER_PADDING = 150
LOWER_PADDING = 10
INBTWN_SPACE = 4

WIN_CONNECTION = 4
# blocks constants
CIRCLE_COLOR = (100,100,100)
RECT_COLOR = (0,0,120)
PLAYER1_COLOR = (200, 0, 0)
PLAYER2_COLOR = (200, 200, 0)

class Puzzle:

    def __init__(self, screen, num_row, num_col, screen_width, screen_height):
        self.screen = screen
        self.circles = [] # array of obj
        self.playable = [] # array of ints
        self.occupied = [] # array of ints
        self.states = []
        self.rows = []
        self.columns = []
        self.nw_digs = []
        self.ne_digs = []
        # self.clickable_ranges = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_row = num_row
        self.num_col = num_col
        self.current_state = '0' * (self.num_row * self.num_col)
        self.states.append(self.current_state)
        self.player1 = '1'
        self.player2 = '2'
        self.player1_color = PLAYER1_COLOR
        self.player2_color = PLAYER2_COLOR
        self.player1_score = 0
        self.player2_score = 0
        self.player_turn = '1'
        self.rect = None

        # calculate the block width and height depending on the screen width and height
        self.diameter = ((self.screen_width - (2 * SIDES_PADDING)) - ((self.num_col-1) * INBTWN_SPACE)) / self.num_col

        self.create_circles()
        self.generate_playable()
        self.generate_checkable()

# create_rects creates the blocks of the game
    def create_circles(self):
        # initial cordinates of the first block
        x = SIDES_PADDING + self.diameter/2
        y = UPPER_PADDING + self.diameter/2
        self.rect = pygame.Rect(SIDES_PADDING-5, UPPER_PADDING-5, self.screen_width-(2*SIDES_PADDING)+10, self.screen_height - UPPER_PADDING - LOWER_PADDING)
        pygame.draw.rect(self.screen, RECT_COLOR, self.rect)

        for _ in range(0, self.num_row):
            for _ in range(0, self.num_col):
                circle = Circle(self.screen, x, y, CIRCLE_COLOR, self.diameter/2)
                circle.draw()
                self.circles.append(circle)
                x = x + self.diameter + INBTWN_SPACE
            x = SIDES_PADDING + self.diameter/2
            y = y + self.diameter + INBTWN_SPACE

    def generate_checkable(self):
        row = []
        for r in range(self.num_row):
            for c in range(self.num_col):
                row.append(r*self.num_col+c)
            self.rows.append(row.copy())
            row.clear()

        column = []
        for c in range(self.num_col):
            for r in range(self.num_row):
                column.append(r*self.num_col+c)
            self.columns.append(column.copy())
            column.clear()

        nw = []
        c = 0
        for r in range(self.num_row-4,-1,-1):
            i = r*self.num_col+c
            while i < self.num_col*self.num_row:
                nw.append(i)
                i += self.num_col+1
            self.nw_digs.append(nw.copy())
            nw.clear()
            i = c*self.num_col+r
            while i < self.num_col*self.num_row and i != 0:
                nw.append(i)
                i += self.num_col+1
            
            if(nw):
                self.nw_digs.append(nw.copy())
                nw.clear()
        
        ne = []
        i = 3
        j = 0
        while j < 4:
            nw.append(i+j)
            ne.append(i-j)
            i += 7
            j += 1
        self.nw_digs.append(nw.copy())
        self.ne_digs.append(ne.copy())
        nw.clear()
        ne.clear()
        c = self.num_col - 1
        for r in range(self.num_row-4,-1,-1):
            i = r*self.num_col+c
            j = c
            while i < self.num_col*self.num_row and j > -1:
                ne.append(i)
                i += self.num_col-1
                j -= 1
            self.ne_digs.append(ne.copy())
            ne.clear()
            i = self.num_col - r - 1
            j = i
            while i < self.num_col*self.num_row and j > -1 and i != 6:
                ne.append(i)
                i += self.num_col-1
                j -= 1
            if (ne):
                self.ne_digs.append(ne.copy())
                ne.clear()

    # def generate_checkable(self):
    #     index = []
    #     w = []
    #     nw = []
    #     n = []
    #     ne = []
    #     for r in range(self.num_row):
    #         for c in range(self.num_col):
    #             i = r*self.num_col + c
    #             if c+3 < self.num_col:
    #                 w.extend([i+1,i+2,i+3])
    #                 if c+4 < self.num_col:
    #                     w.append(i+4)
    #             if r+3 < self.num_row:
    #                 n.extend([i+self.num_col,i+self.num_col*2,i+self.num_col*3])
    #                 if r+4 < self.num_row:
    #                     n.append(i+self.num_col*4)
    #             if n:
    #                 if w:
    #                     nw.extend([i+self.num_col+1,i+(self.num_col+1)*2,i+(self.num_col+1)*3])
    #                     if len(w) == 4 and len(n) == 4:
    #                         nw.append(i+(self.num_col+1)*4)
    #                 if c-3 > -1:
    #                     ne.extend([i+self.num_col-1,i+(self.num_col-1)*2,i+(self.num_col-1)*3])
    #                     if c-4 > -1 and len(n) == 4:
    #                         ne.append(i+(self.num_col-1)*4)
    #             index.extend([w.copy(),nw.copy(),n.copy(),ne.copy()])
    #             self.checkable.append(index.copy())
    #             print(index,end="\n\n\n")
    #             w.clear()
    #             nw.clear()
    #             n.clear()
    #             ne.clear()
    #             index.clear()


    
    def generate_playable(self):
        temp = []
        for i in range(self.num_col):
            inc = i 
            for j in range(self.num_row):
                temp.append(inc)
                inc += self.num_col
            self.playable.append(copy(temp))
            temp.clear()


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


    def drop_piece(self, x_clicked, y_clicked, color, owner):
        
        col_index = self.get_col_clicked(x_clicked, y_clicked)
        if col_index != None:
            if self.playable[col_index]:
                circle_index = max(self.playable[col_index])
                self.circles[circle_index].update(color, owner)
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
        self.player1_score = 0
        self.player2_score = 0
        # Horizontal check
        for row in self.rows:
            if self.current_state[row[3]] != "0":
                player = self.current_state[row[3]]
                self.calc_score(self.current_state,row,player)
        
        # Vertical check   
        for col in self.columns:
            if self.current_state[col[3]] != "0":
                if self.current_state[col[2]] == self.current_state[col[3]]:
                    player = self.current_state[col[3]]
                    self.calc_score(self.current_state,col,player)
                
        # main diagonal check
        for dig in self.nw_digs:
            if self.current_state[dig[3]] != "0":
                if self.current_state[dig[2]] == self.current_state[dig[3]]:
                    player = self.current_state[dig[3]]
                    self.calc_score(self.current_state,dig,player)
                
        # secondary diagonal check
        for dig in self.ne_digs:
            if self.current_state[dig[3]] != "0":
                if self.current_state[dig[2]] == self.current_state[dig[3]]:
                    player = self.current_state[dig[3]]
                    self.calc_score(self.current_state,dig,player)
                
    def calc_score(self, state , seq , player):
        i = 0
        c = 0
        score = 0
        while i < len(seq):
            c = 0
            while i < len(seq) and state[seq[i]] != player:
                i += 1
            while i < len(seq) and state[seq[i]] == player:
                c += 1
                i += 1            
            if c > 3:
                score = c - 3
                break
            
        if player == '1':
            self.player1_score += score
        else:
            self.player2_score += score


    def play(self, x_clicked, y_clicked):
        if self.player_turn == self.player1:
            switch_player = self.drop_piece(x_clicked, y_clicked, self.player1_color, self.player_turn)
            if switch_player: 
                self.player_turn = self.player2
        elif self.player_turn == self.player2:
            switch_player = self.drop_piece(x_clicked, y_clicked, self.player2_color, self.player_turn)
            if switch_player:
                self.player_turn = self.player1
        self.get_score()
        print("player 1 score: "+ str(self.player1_score)+" \nplayer 2 score: "+ str(self.player2_score))
        
        if len(self.occupied) == self.num_col*self.num_row:
            print("calc score")
            self.get_score()
            print("player 1 score: "+ str(self.player1_score)+" \nplayer 2 score: "+ str(self.player2_score))


