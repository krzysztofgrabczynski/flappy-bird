import pygame


class Button():
    def __init__(self, game, x, y, name, scale_x, scale_y):
        self.game = game
        self.x = x
        self.y = y
        self.name = name
        self.check_hover = False

        self.button_image = pygame.image.load(f"image/buttons/{name}.png")
        self.button_image = pygame.transform.scale(self.button_image, (scale_x, scale_y))
        self.width = self.button_image.get_width()
        self.height = self.button_image.get_height()

        self.button = pygame.Rect(self.x, self.y, self.width, self.height)

    def click(self):
        mouse_position = pygame.mouse.get_pos()
        if self.button.collidepoint(mouse_position) and pygame.mouse.get_pressed()[0] is True:
            return True

    def draw(self):
        mouse_position = pygame.mouse.get_pos()
        if self.button.collidepoint(mouse_position):
            pygame.draw.rect(self.game.window, (205, 205, 205), self.button, 4)
            if self.check_hover is False:
                self.game.sounds[3].play()
                self.check_hover = True
        if not(self.button.collidepoint(mouse_position)):
            self.check_hover = False
        self.game.window.blit(self.button_image, (self.x, self.y))
