import pygame


class Player():
    def __init__(self, game):
        self.game = game
        self.player_image = pygame.image.load("image/bird.png")
        self.width = self.player_image.get_width()
        self.height = self.player_image.get_height()
        self.player = self.player_image.get_rect()
        self.player.x = 200
        self.player.y = 500

        self.y_speed = 0
        self.y_acceleration = 0.3
        self.jump_var = -8

    def tick(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and not self.game.click_SPACE_check:
            self.y_speed = self.jump_var
            self.game.click_SPACE_check = True
            self.game.sounds[2].play()

        self.y_speed += self.y_acceleration
        self.player.y += self.y_speed

    def draw(self):
        self.game.window.blit(self.player_image, (self.player.x, self.player.y))
