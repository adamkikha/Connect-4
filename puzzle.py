from copy import copy

from circles import Circle

# screen constants
SIDES_PADDING = 10
UPPER_PADDING = 100
LOWER_PADDING = 20
INBTWN_SPACE = 1

# blocks constants
CIRCLE_COLOR = (155,45,205)
PLAYER1_CIRCLE_COLOR = (12, 90, 55)
PLAYER2_CIRCLE_COLOR = (120, 9, 5)

class Puzzle:

    def __init__(self, screen, num_row, num_col, screen_width, screen_height):
        self.screen = screen

        self.circles = [] # array of obj
        self.playable = [] # array of ints
        self.occupied = [] # array of ints
        
        # self.clickable_ranges = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_row = num_row
        self.num_col = num_col

        self.state = '0' * (self.num_row * self.num_col)
        self.player_turn = '1'
        
        # calculate the block width and height depending on the screen width and height
        self.diameter = (self.screen_width - (2 * SIDES_PADDING) - (
                    self.num_col * INBTWN_SPACE - 1)) / self.num_col
        # self.diameter2 = (self.screen_height - LOWER_PADDING - UPPER_PADDING - (
        #             self.num_row * INBTWN_SPACE - 1)) / self.num_row
        # self.diameter = (self.diameter1 + self.diameter2)//2

        self.create_circles()
        self.generate_playable()

# create_rects creates the blocks of the game
    def create_circles(self):
        # initial cordinates of the first block
        x = SIDES_PADDING + self.diameter/2
        y = UPPER_PADDING + self.diameter/2

        for _ in range(0, self.num_row):
            # self.clickable_ranges.append((x-self.diameter/2, y-self.diameter/2))
            for _ in range(0, self.num_col):
                circle = Circle(x, y, CIRCLE_COLOR, self.diameter/2)
                circle.draw(self.screen)
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


    def throw(self, x_clicked, y_clicked, color, owner):
        col_index = self.get_col_clicked(x_clicked, y_clicked)
        if col_index != None:
            if self.playable[col_index]:
                circle_index = max(self.playable[col_index])
                self.circles[circle_index].update(self.screen, color, owner)
                self.playable[col_index].remove(circle_index)
                self.occupied.append(circle_index)
                self.update_state(circle_index, owner)

    def update_state(self, index, player):
        self.state = list(self.state)
        self.state[index] = player
        self.state = "".join(self.state)

    def get_score(self):
        pass


    def play(self, x_clicked, y_clicked):
        if len(self.occupied) == self.num_col*self.num_row:
            print("calc score")
            self.get_score()
            

        elif self.player_turn == '1':
            self.throw(x_clicked, y_clicked, PLAYER1_CIRCLE_COLOR, self.player_turn)
            self.player_turn = '2'
        elif self.player_turn == '2':
            self.throw(x_clicked, y_clicked, PLAYER2_CIRCLE_COLOR, self.player_turn)
            self.player_turn = '1'
        print(self.state)
        

