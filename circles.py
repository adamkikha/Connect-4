import pygame

class Circle:
    def __init__(self, x_pos, y_pos, color, radius):
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.player = None
        self.radius = radius
        
    # draw used to draw the block
    def draw(self, screen):
        pygame.draw.circle(screen, self.color,(self.x_pos, self.y_pos), self.radius)
    
    # update used to update the block place called when exchange happens
    def update(self, screen, color, owner):
        self.color = color
        self.player = owner
        self.draw(screen)

