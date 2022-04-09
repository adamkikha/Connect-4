import pygame


# circles class responsible for drawing game pieces and blanks
class Circle:
    def __init__(self, screen, x_pos, y_pos, color, radius):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.player = None
        self.radius = radius
        self.screen = screen
        
    # draw used to draw the circle
    def draw(self):
        pygame.draw.circle(self.screen, self.color,(self.x_pos, self.y_pos), self.radius)
    
    # update used to update the circle called when a play happens
    def update(self, owner, player_image):
        self.player = owner
        self.screen.blit(player_image, (self.x_pos - self.radius, self.y_pos - self.radius))

    # changes the position of a circle    
    def change_pos(self, new_x_pos, new_y_pos):
        self.x_pos = new_x_pos
        self.y_pos = new_y_pos
        self.draw()

