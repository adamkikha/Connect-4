import pygame
from circles import Circle
from PIL import Image

# screen constants
SIDES_PADDING = 10
UPPER_PADDING = 150
LOWER_PADDING = 10
INBTWN_SPACE = 4

# blocks constants
CIRCLE_COLOR = (255,255,255)
RECT_COLOR = (0,0,139)
PLAYER1_COLOR = (12, 90, 55)
PLAYER2_COLOR = (120, 9, 5)
BOARD_IMG = pygame.image.load("3D Board.png")
FONT_SIZE = 60

class Puzzle:
    def __init__(self, screen : pygame.Surface, num_row, num_col, screen_width, screen_height):
        self.screen = screen
        self.circles = [] # array of obj
        self.playable = [0,1,2,3,4,5,6] # array of ints
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
        self.Complete = False
        self.player1 = '1'
        self.player2 = '2'
        self.player1_image = None
        self.player2_image = None
        self.player1_score = 0
        self.player2_score = 0
        self.player_turn = '1'

        self.rect = None
        # calculate the block width and height depending on the screen width and height
        self.diameter = min(((self.screen_width - (2 * SIDES_PADDING)) - ((self.num_col-1) * INBTWN_SPACE)) / self.num_col,((self.screen_height - UPPER_PADDING - LOWER_PADDING) - ((self.num_row-1) * INBTWN_SPACE)) / self.num_row)
        pygame.font.init()
        self.font = pygame.font.SysFont("calibri",FONT_SIZE)
        self.adjust_image()
        self.create_circles()
        self.generate_checkable()

    def update_score(self):
        self.get_score()
        pygame.draw.rect(self.screen,(0,0,0),self.score1rect)
        pygame.draw.rect(self.screen,(0,0,0),self.score2rect)
        text = self.font.render("player 1",True,(255,0,0))
        self.screen.blit(text,(self.score1rect.x + FONT_SIZE/2,self.score1rect.y+2))
        text = self.font.render("player 2",True,(255,255,0))
        self.screen.blit(text,(self.score2rect.x + FONT_SIZE/2,self.score2rect.y+2))
        text = self.font.render(str(self.player1_score),True,(255,0,0))
        self.screen.blit(text,(self.score1rect.x + self.score1rect.width/2,self.score1rect.y+self.score1rect.height/2+5))
        text = self.font.render(str(self.player2_score),True,(255,255,0))
        self.screen.blit(text,(self.score2rect.x + self.score2rect.width/2,self.score2rect.y+self.score2rect.height/2+5))
        
# creates the circles of the game
    def create_circles(self):
        # initial cordinates of the first circle
        x = SIDES_PADDING + self.diameter/2
        y = UPPER_PADDING + self.diameter/2
        BGROUND_IMG = pygame.image.load("new_BG.jpg")
        self.screen.blit(BGROUND_IMG,(0, 0))
        
        # game board
        self.rect = pygame.Rect(SIDES_PADDING-2, UPPER_PADDING-2, self.screen_width-(2*SIDES_PADDING)+10, self.screen_height - UPPER_PADDING - LOWER_PADDING)
        
        # score rectangles
        self.score1rect = pygame.Rect(SIDES_PADDING,LOWER_PADDING,self.screen_width*2/5 - SIDES_PADDING,UPPER_PADDING-20)
        self.score2rect = pygame.Rect(self.screen_width*3/5 ,LOWER_PADDING,self.screen_width*2/5 - SIDES_PADDING,UPPER_PADDING-20)
        pygame.draw.rect(self.screen, RECT_COLOR,self.rect)

        # draw blanks
        for _ in range(0, self.num_row):
            for _ in range(0, self.num_col):
                circle = Circle(self.screen, x, y, CIRCLE_COLOR, self.diameter/2)
                circle.draw()
                self.circles.append(circle)
                x = x + self.diameter + INBTWN_SPACE
            x = SIDES_PADDING + self.diameter/2
            y = y + self.diameter + INBTWN_SPACE

    # generates all the board's rows, columns and diagonals indicies
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

    # resizes background and game pieces to fit window
    def adjust_image(self):
        Bg = Image.open("BG.jpg")
        newBg = Bg.resize((self.screen_width,self.screen_height))
        newBg.save("new_Bg.jpg")
        Bg = pygame.image.load("new_Bg.jpg")
        
        redchip = Image.open("redchip.png")
        smallred = redchip.resize((int(self.diameter), int(self.diameter)))
        smallred.save("new_red.png")
        self.player1_image = pygame.image.load("new_red.png")

        yellochip = Image.open("yellowchip.png")
        smallyellow = yellochip.resize((int(self.diameter), int(self.diameter)))
        smallyellow.save("new_yellow.png")
        self.player2_image = pygame.image.load("new_yellow.png")


    # returns which column was clicked
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
                return 6-i

    # plays a piece for the AI
    def play_AI(self,index):
        image = self.player2_image
        if self.player_turn == "1":
            image = self.player1_image
        col_index = index % 7
        circle_index = 41 - index
        self.circles[circle_index].update(self.player_turn,image)
        self.playable[col_index] += 7
        self.occupied.append(index)
        self.update_state(index, self.player_turn)
        if self.player_turn == "1":
            self.player_turn = "2"
        else:
            self.player_turn = "1"
        self.update_score()
        if len(self.occupied) == self.num_col*self.num_row:
            self.Complete = True
    
    # checks if column can be played in and plays if available    
    def drop_piece(self, x_clicked, y_clicked, image, owner):
        col_index = self.get_col_clicked(x_clicked, y_clicked)
        if col_index != None:
            if self.playable[col_index] < 42:
                index = self.playable[col_index]
                circle_index = 41 - index
                self.circles[circle_index].update(owner,image)
                self.playable[col_index] += 7
                self.occupied.append(index)
                self.update_state(index, owner)
                return True
            else:
                return False

    # updates the current state by given play
    def update_state(self, index, player):
        self.current_state = list(self.current_state)
        self.current_state[index] = player
        self.current_state = "".join(self.current_state)
        self.states.append(self.current_state)

    # calculates current score
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
    
    # calculates the number of connected fours for a certain player and 
    # a certian set of indicies            
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


    # plays a piece for player
    def play(self, x_clicked, y_clicked):
        if self.player_turn == self.player1:
            switch_player = self.drop_piece(x_clicked, y_clicked, self.player1_image, self.player_turn)
            if switch_player:
                self.update_score() 
                self.player_turn = self.player2
        else:
            switch_player = self.drop_piece(x_clicked, y_clicked, self.player2_image, self.player_turn)
            if switch_player:
                self.update_score()
                self.player_turn = self.player1
        if len(self.occupied) == self.num_col*self.num_row:
            self.Complete = True
        return switch_player
        



