import pygame


class Pipes():
    def __init__(self, game, x, y, width, gap):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.pipe_gap = gap

        self.pipe_image_bottom = pygame.image.load("image/pipe.png")
        self.pipe_image_top = pygame.transform.flip(self.pipe_image_bottom, False, True)

        self.pipe_image_bottom = pygame.transform.scale(self.pipe_image_bottom, (40,self.game.border_down.top-self.y))
        self.pipe_bottom = self.pipe_image_bottom.get_rect()

        self.pipe_image_top = pygame.transform.scale(self.pipe_image_top, (40, self.game.border_down.top-self.pipe_bottom.height-self.pipe_gap))
        self.pipe_top = self.pipe_image_top.get_rect()

    def draw(self, scrolling_bg_x_index):
        self.pipe_bottom = pygame.rect.Rect(self.x - scrolling_bg_x_index, self.y, self.width, self.game.border_down.top-self.y)
        self.pipe_top = pygame.rect.Rect(self.x - scrolling_bg_x_index, 0, self.width, self.game.border_down.top-self.pipe_bottom.height-self.pipe_gap)

        self.game.window.blit(self.pipe_image_bottom, (self.x - scrolling_bg_x_index, self.y))
        self.game.window.blit(self.pipe_image_top, (self.x - scrolling_bg_x_index, 0))
